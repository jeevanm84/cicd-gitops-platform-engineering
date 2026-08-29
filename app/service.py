"""Minimal application logic kept dependency-free for local delivery labs."""

from dataclasses import dataclass


@dataclass(frozen=True)
class ServiceInfo:
    name: str = "delivery-demo"
    version: str = "1.1.0"


def health() -> dict[str, str]:
    return {"status": "healthy"}


def ready(dependency_available: bool = True) -> tuple[dict[str, str], int]:
    if dependency_available:
        return {"status": "ready"}, 200
    return {"status": "not-ready"}, 503

