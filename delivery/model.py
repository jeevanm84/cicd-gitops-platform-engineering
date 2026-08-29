"""Validate, promote, inspect, and roll back immutable release evidence."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


DIGEST = re.compile(r"^sha256:[0-9a-f]{64}$")
COMMIT = re.compile(r"^[0-9a-f]{40}$")
VERSION = re.compile(r"^[0-9]+\.[0-9]+\.[0-9]+$")
ENVIRONMENT_ORDER = ("development", "staging", "production")


class DeliveryError(ValueError):
    """Raised when release evidence or promotion order violates policy."""


def read_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as stream:
        return json.load(stream)


def write_json(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")
    temporary.replace(path)


def validate_release(release: dict[str, Any], policy: dict[str, Any]) -> None:
    errors: list[str] = []
    required = policy["required_release_fields"]
    for field in required:
        if field not in release:
            errors.append(f"missing release field: {field}")

    if errors:
        raise DeliveryError("; ".join(errors))

    if release["schema_version"] != 1:
        errors.append("schema_version must be 1")
    if not VERSION.fullmatch(release["app_version"]):
        errors.append("app_version must use numeric semantic versioning")
    if not COMMIT.fullmatch(release["source_commit"]):
        errors.append("source_commit must be a full lowercase Git SHA")

    artifact = release["artifact"]
    if not DIGEST.fullmatch(artifact.get("digest", "")):
        errors.append("artifact digest must be sha256 with 64 lowercase hex characters")
    if "@sha256:" not in artifact.get("image", ""):
        errors.append("artifact image must be pinned by digest")
    if artifact.get("signature_verified") is not True:
        errors.append("artifact signature evidence must be verified")
    if not artifact.get("sbom"):
        errors.append("artifact SBOM reference is required")

    evidence = release["evidence"]
    for check in policy["required_evidence"]:
        if evidence.get(check) != "passed":
            errors.append(f"required evidence did not pass: {check}")

    if errors:
        raise DeliveryError("; ".join(errors))


def promote(
    release: dict[str, Any],
    environment: str,
    state_dir: Path,
    policy: dict[str, Any],
    approval: str | None = None,
) -> dict[str, Any]:
    validate_release(release, policy)
    if environment not in ENVIRONMENT_ORDER:
        raise DeliveryError(f"unknown environment: {environment}")

    position = ENVIRONMENT_ORDER.index(environment)
    if position:
        previous = ENVIRONMENT_ORDER[position - 1]
        previous_state = load_state(state_dir, previous)
        if previous_state.get("current", {}).get("release_id") != release["release_id"]:
            raise DeliveryError(f"release must be current in {previous} before {environment}")

    if environment == "production" and not approval:
        raise DeliveryError("production promotion requires a non-empty approval reference")

    state = load_state(state_dir, environment)
    current = state.get("current")
    if current and current["release_id"] == release["release_id"]:
        return state

    event = {
        "release_id": release["release_id"],
        "app_version": release["app_version"],
        "artifact_digest": release["artifact"]["digest"],
        "source_commit": release["source_commit"],
        "deployed_at": datetime.now(timezone.utc).isoformat(),
        "approval": approval,
    }
    history = state.get("history", [])
    if current:
        history.append(current)
    result = {"environment": environment, "current": event, "history": history}
    write_json(state_path(state_dir, environment), result)
    return result


def rollback(environment: str, state_dir: Path) -> dict[str, Any]:
    state = load_state(state_dir, environment)
    history = state.get("history", [])
    if not state.get("current") or not history:
        raise DeliveryError(f"{environment} has no prior release to roll back to")
    restored = history.pop()
    replaced = state["current"]
    restored["rollback_at"] = datetime.now(timezone.utc).isoformat()
    restored["rollback_from"] = replaced["release_id"]
    result = {"environment": environment, "current": restored, "history": history}
    write_json(state_path(state_dir, environment), result)
    return result


def state_path(state_dir: Path, environment: str) -> Path:
    return state_dir / f"{environment}.json"


def load_state(state_dir: Path, environment: str) -> dict[str, Any]:
    path = state_path(state_dir, environment)
    return read_json(path) if path.exists() else {"environment": environment, "history": []}

