import unittest

from app.service import ServiceInfo, health, ready


class ServiceTests(unittest.TestCase):
    def test_health_and_version(self) -> None:
        self.assertEqual(health(), {"status": "healthy"})
        self.assertEqual(ServiceInfo().version, "1.1.0")

    def test_readiness_exposes_dependency_failure(self) -> None:
        self.assertEqual(ready(False), ({"status": "not-ready"}, 503))


if __name__ == "__main__":
    unittest.main()

