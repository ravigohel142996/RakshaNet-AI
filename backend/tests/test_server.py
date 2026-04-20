import unittest

from src.server import HELPERS, haversine_km, nearest_helper


class TestServerLogic(unittest.TestCase):
    def test_haversine_non_negative(self):
        self.assertGreaterEqual(haversine_km(23.0, 72.0, 23.1, 72.1), 0)

    def test_nearest_helper_has_required_fields(self):
        helper = nearest_helper(23.02, 72.57)
        self.assertIn("id", helper)
        self.assertIn("name", helper)
        self.assertIn("distance_km", helper)

    def test_nearest_helper_is_closest(self):
        lat, lng = 23.02, 72.57
        helper = nearest_helper(lat, lng)
        expected = min(
            HELPERS,
            key=lambda candidate: haversine_km(lat, lng, candidate["lat"], candidate["lng"]),
        )
        expected_distance = round(haversine_km(lat, lng, expected["lat"], expected["lng"]), 2)
        self.assertEqual(helper["id"], expected["id"])
        self.assertEqual(helper["distance_km"], expected_distance)


if __name__ == "__main__":
    unittest.main()
