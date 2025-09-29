import unittest
from unittest.mock import patch

from src.powerup.powerUp import PowerUp
from src.powerup.powerUpType import PowerUpType
from src.lib.pyenvlib.entity import Entity


class TestPowerUp(unittest.TestCase):
    def test_powerup_inherits_from_entity(self):
        """Test that PowerUp properly inherits from Entity."""
        power_up = PowerUp(PowerUpType.SPEED_BOOST)
        self.assertIsInstance(power_up, Entity)

    def test_powerup_initialization(self):
        """Test PowerUp initialization with default values."""
        power_up = PowerUp(PowerUpType.SPEED_BOOST)

        self.assertEqual(power_up.get_power_up_type(), PowerUpType.SPEED_BOOST)
        self.assertEqual(power_up.get_duration(), 10.0)
        self.assertEqual(power_up.getColor(), (255, 255, 0))
        self.assertFalse(power_up.is_active())
        self.assertEqual(power_up.get_remaining_time(), 0.0)

    def test_powerup_initialization_with_custom_values(self):
        """Test PowerUp initialization with custom values."""
        color = (255, 0, 0)
        duration = 15.0
        power_up = PowerUp(PowerUpType.INVINCIBILITY, duration, color)

        self.assertEqual(power_up.get_power_up_type(), PowerUpType.INVINCIBILITY)
        self.assertEqual(power_up.get_duration(), duration)
        self.assertEqual(power_up.getColor(), color)

    def test_powerup_activation(self):
        """Test PowerUp activation."""
        power_up = PowerUp(PowerUpType.SLOW_TIME)

        self.assertFalse(power_up.is_active())

        power_up.activate()

        self.assertTrue(power_up.is_active())
        self.assertGreater(power_up.activation_time, 0)

    def test_powerup_deactivation(self):
        """Test PowerUp deactivation."""
        power_up = PowerUp(PowerUpType.SLOW_TIME)
        power_up.activate()

        self.assertTrue(power_up.is_active())

        power_up.deactivate()

        self.assertFalse(power_up.is_active())
        self.assertEqual(power_up.activation_time, 0.0)

    @patch("time.time")
    def test_powerup_expiration(self, mock_time):
        """Test PowerUp expiration logic."""
        power_up = PowerUp(PowerUpType.SCORE_MULTIPLIER, duration=5.0)

        # Mock initial activation time
        mock_time.return_value = 100.0
        power_up.activate()

        # Test not expired within duration
        mock_time.return_value = 104.0  # 4 seconds later
        self.assertFalse(power_up.is_expired())

        # Test expired after duration
        mock_time.return_value = 106.0  # 6 seconds later
        self.assertTrue(power_up.is_expired())

    @patch("time.time")
    def test_powerup_remaining_time(self, mock_time):
        """Test PowerUp remaining time calculation."""
        power_up = PowerUp(PowerUpType.SPEED_BOOST, duration=10.0)

        # Test remaining time when inactive
        self.assertEqual(power_up.get_remaining_time(), 0.0)

        # Mock activation
        mock_time.return_value = 100.0
        power_up.activate()

        # Test remaining time after activation
        mock_time.return_value = 103.0  # 3 seconds later
        self.assertEqual(power_up.get_remaining_time(), 7.0)

        # Test remaining time when expired
        mock_time.return_value = 115.0  # 15 seconds later
        self.assertEqual(power_up.get_remaining_time(), 0.0)

    def test_powerup_entity_name(self):
        """Test that PowerUp entity name includes type."""
        power_up = PowerUp(PowerUpType.INVINCIBILITY)
        expected_name = "PowerUp(Invincibility)"
        self.assertEqual(power_up.getName(), expected_name)


if __name__ == "__main__":
    unittest.main()
