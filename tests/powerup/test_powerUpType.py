import unittest

from src.powerup.powerUpType import PowerUpType


class TestPowerUpType(unittest.TestCase):
    def test_powerup_type_enum_has_expected_members(self):
        """Test that PowerUpType enum has all expected members."""
        expected_types = {
            "SPEED_BOOST",
            "SLOW_TIME",
            "INVINCIBILITY",
            "SCORE_MULTIPLIER",
        }

        actual_types = {member.name for member in PowerUpType}
        self.assertEqual(expected_types, actual_types)

    def test_powerup_type_values(self):
        """Test that PowerUpType enum values are correct."""
        self.assertEqual(PowerUpType.SPEED_BOOST.value, "Speed Boost")
        self.assertEqual(PowerUpType.SLOW_TIME.value, "Slow Time")
        self.assertEqual(PowerUpType.INVINCIBILITY.value, "Invincibility")
        self.assertEqual(PowerUpType.SCORE_MULTIPLIER.value, "Score Multiplier")

    def test_powerup_type_string_representation(self):
        """Test that PowerUpType string representation works correctly."""
        self.assertEqual(str(PowerUpType.SPEED_BOOST), "Speed Boost")
        self.assertEqual(str(PowerUpType.SLOW_TIME), "Slow Time")
        self.assertEqual(str(PowerUpType.INVINCIBILITY), "Invincibility")
        self.assertEqual(str(PowerUpType.SCORE_MULTIPLIER), "Score Multiplier")


if __name__ == "__main__":
    unittest.main()
