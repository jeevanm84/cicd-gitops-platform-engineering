import copy
import tempfile
import unittest
from pathlib import Path

from delivery.model import DeliveryError, promote, read_json, rollback, validate_release

ROOT = Path(__file__).resolve().parents[1]


class DeliveryTests(unittest.TestCase):
    def setUp(self) -> None:
        self.policy = read_json(ROOT / "policies/release-policy.json")
        self.release_one = read_json(ROOT / "examples/releases/1.0.0.json")
        self.release_two = read_json(ROOT / "examples/releases/1.1.0.json")

    def test_release_policy_rejects_mutable_artifact(self) -> None:
        release = copy.deepcopy(self.release_one)
        release["artifact"]["image"] = "ghcr.io/jeevanm84/delivery-demo:latest"
        with self.assertRaisesRegex(DeliveryError, "pinned by digest"):
            validate_release(release, self.policy)

    def test_staging_cannot_skip_development(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaisesRegex(DeliveryError, "current in development"):
                promote(self.release_one, "staging", Path(directory), self.policy)

    def test_production_requires_approval(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            state = Path(directory)
            promote(self.release_one, "development", state, self.policy)
            promote(self.release_one, "staging", state, self.policy)
            with self.assertRaisesRegex(DeliveryError, "approval"):
                promote(self.release_one, "production", state, self.policy)

    def test_two_releases_and_rollback(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            state = Path(directory)
            for release in (self.release_one, self.release_two):
                promote(release, "development", state, self.policy)
                promote(release, "staging", state, self.policy)
                promote(release, "production", state, self.policy, "change/approved")
            result = rollback("production", state)
            self.assertEqual(result["current"]["release_id"], "delivery-demo-1.0.0")
            self.assertEqual(result["current"]["rollback_from"], "delivery-demo-1.1.0")


if __name__ == "__main__":
    unittest.main()

