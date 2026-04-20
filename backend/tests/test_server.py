import unittest

from src.server import haversine_km, nearest_helper


class TestServerLogic(unittest.TestCase):
    def test_haversine_non_negative(self):
        self.assertGreaterEqual(haversine_km(23.0, 72.0, 23.1, 72.1), 0)

    def test_nearest_helper_has_required_fields(self):
        helper = nearest_helper(23.02, 72.57)
        self.assertIn("id", helper)
        self.assertIn("name", helper)
        self.assertIn("distance_km", helper)


if __name__ == "__main__":
    unittest.main()
