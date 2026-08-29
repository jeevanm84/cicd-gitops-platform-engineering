#!/usr/bin/env python3
"""Command-line interface for the local delivery model."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPOSITORY = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPOSITORY))

from delivery.model import (  # noqa: E402
    DeliveryError,
    ENVIRONMENT_ORDER,
    load_state,
    promote,
    read_json,
    rollback,
    validate_release,
)


def parser() -> argparse.ArgumentParser:
    command = argparse.ArgumentParser(description=__doc__)
    subcommands = command.add_subparsers(dest="command", required=True)

    verify = subcommands.add_parser("verify", help="validate immutable release evidence")
    verify.add_argument("--release", type=Path, required=True)

    promote_command = subcommands.add_parser("promote", help="promote a release in order")
    promote_command.add_argument("--release", type=Path, required=True)
    promote_command.add_argument("--environment", choices=ENVIRONMENT_ORDER, required=True)
    promote_command.add_argument("--state-dir", type=Path, default=REPOSITORY / ".local/state")
    promote_command.add_argument("--approval", help="required for production")

    status = subcommands.add_parser("status", help="show environment state")
    status.add_argument("--state-dir", type=Path, default=REPOSITORY / ".local/state")

    rollback_command = subcommands.add_parser("rollback", help="restore the prior immutable release")
    rollback_command.add_argument("--environment", choices=ENVIRONMENT_ORDER, required=True)
    rollback_command.add_argument("--state-dir", type=Path, default=REPOSITORY / ".local/state")
    return command


def main() -> int:
    args = parser().parse_args()
    policy = read_json(REPOSITORY / "policies/release-policy.json")
    try:
        if args.command == "verify":
            release = read_json(args.release)
            validate_release(release, policy)
            print(f"valid release: {release['release_id']}")
        elif args.command == "promote":
            result = promote(
                read_json(args.release), args.environment, args.state_dir, policy, args.approval
            )
            print(json.dumps(result, indent=2))
        elif args.command == "status":
            result = {name: load_state(args.state_dir, name) for name in ENVIRONMENT_ORDER}
            print(json.dumps(result, indent=2))
        elif args.command == "rollback":
            print(json.dumps(rollback(args.environment, args.state_dir), indent=2))
    except (DeliveryError, FileNotFoundError, json.JSONDecodeError) as error:
        print(f"delivery error: {error}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

