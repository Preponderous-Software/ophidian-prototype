import unittest
from unittest.mock import patch

from src.powerup.powerUp import PowerUp
from src.powerup.powerUpType import PowerUpType


class TestPowerUpEdgeCases(unittest.TestCase):
    def test_power_up_with_zero_duration(self):
        """Test power-up behavior with zero duration."""
        power_up = PowerUp(PowerUpType.SPEED_BOOST, duration=0.0)
        power_up.activate()

        # Should immediately be expired
        self.assertTrue(power_up.is_expired())
        self.assertEqual(power_up.get_remaining_time(), 0.0)

    def test_power_up_with_negative_duration(self):
        """Test power-up behavior with negative duration."""
        power_up = PowerUp(PowerUpType.SLOW_TIME, duration=-5.0)
        power_up.activate()

        # Should be considered expired
        self.assertTrue(power_up.is_expired())
        self.assertEqual(power_up.get_remaining_time(), 0.0)

    def test_power_up_activation_time_consistency(self):
        """Test that activation time is set consistently."""
        power_up = PowerUp(PowerUpType.INVINCIBILITY)

        with patch("time.time") as mock_time:
            test_time = 123.456
            mock_time.return_value = test_time

            power_up.activate()

            self.assertEqual(power_up.activation_time, test_time)
            self.assertTrue(power_up.is_active())

    def test_multiple_activations(self):
        """Test behavior when activating an already active power-up."""
        power_up = PowerUp(PowerUpType.SCORE_MULTIPLIER, duration=10.0)

        with patch("time.time") as mock_time:
            # First activation
            mock_time.return_value = 100.0
            power_up.activate()
            first_activation_time = power_up.activation_time

            # Second activation (should update activation time)
            mock_time.return_value = 105.0
            power_up.activate()
            second_activation_time = power_up.activation_time

            self.assertNotEqual(first_activation_time, second_activation_time)
            self.assertEqual(second_activation_time, 105.0)

    def test_deactivation_resets_activation_time(self):
        """Test that deactivation properly resets activation time."""
        power_up = PowerUp(PowerUpType.SPEED_BOOST)
        power_up.activate()

        # Should have activation time set
        self.assertGreater(power_up.activation_time, 0)

        power_up.deactivate()

        # Should be reset to 0
        self.assertEqual(power_up.activation_time, 0.0)
        self.assertFalse(power_up.is_active())

    def test_power_up_type_immutability(self):
        """Test that power-up type cannot be changed after creation."""
        power_up = PowerUp(PowerUpType.INVINCIBILITY)
        original_type = power_up.get_power_up_type()

        # Power-up type should remain the same
        self.assertEqual(power_up.get_power_up_type(), original_type)
        self.assertEqual(power_up.get_power_up_type(), PowerUpType.INVINCIBILITY)

    def test_power_up_color_modification(self):
        """Test that power-up color can be accessed and remains consistent."""
        original_color = (100, 150, 200)
        power_up = PowerUp(PowerUpType.SLOW_TIME, color=original_color)

        # Color should remain consistent
        self.assertEqual(power_up.getColor(), original_color)

        # Modifying the returned color should not affect the power-up
        returned_color = power_up.getColor()
        if isinstance(returned_color, list):
            returned_color[0] = 255

        # Original should be unchanged (assuming tuple is used)
        self.assertEqual(power_up.getColor(), original_color)

    def test_power_up_duration_precision(self):
        """Test power-up duration with high precision values."""
        precise_duration = 5.123456789
        power_up = PowerUp(PowerUpType.SCORE_MULTIPLIER, duration=precise_duration)

        self.assertEqual(power_up.get_duration(), precise_duration)

        # Test remaining time precision
        power_up.activate()
        with patch("time.time") as mock_time:
            mock_time.return_value = power_up.activation_time + 1.123456789
            expected_remaining = precise_duration - 1.123456789
            self.assertAlmostEqual(
                power_up.get_remaining_time(), expected_remaining, places=6
            )

    def test_expired_power_up_remaining_time_boundary(self):
        """Test remaining time calculation at expiration boundary."""
        power_up = PowerUp(PowerUpType.SPEED_BOOST, duration=5.0)

        with patch("time.time") as mock_time:
            mock_time.return_value = 100.0
            power_up.activate()

            # Exactly at expiration time
            mock_time.return_value = 105.0
            self.assertEqual(power_up.get_remaining_time(), 0.0)
            self.assertTrue(power_up.is_expired())

            # Just before expiration
            mock_time.return_value = 104.999999
            self.assertGreater(power_up.get_remaining_time(), 0.0)
            self.assertFalse(power_up.is_expired())

    def test_power_up_entity_inheritance_methods(self):
        """Test that PowerUp properly implements Entity interface."""
        power_up = PowerUp(PowerUpType.INVINCIBILITY)

        # Test Entity methods are accessible
        self.assertIsNotNone(power_up.getID())
        self.assertTrue(power_up.getName().startswith("PowerUp"))
        self.assertIsNotNone(power_up.getCreationDate())

        # Test setter methods work
        power_up.setEnvironmentID(123)
        self.assertEqual(power_up.getEnvironmentID(), 123)

        power_up.setGridID(456)
        self.assertEqual(power_up.getGridID(), 456)

        power_up.setLocationID(789)
        self.assertEqual(power_up.getLocationID(), 789)

    def test_power_up_name_format_consistency(self):
        """Test that power-up names are formatted consistently."""
        test_cases = [
            (PowerUpType.SPEED_BOOST, "PowerUp(Speed Boost)"),
            (PowerUpType.SLOW_TIME, "PowerUp(Slow Time)"),
            (PowerUpType.INVINCIBILITY, "PowerUp(Invincibility)"),
            (PowerUpType.SCORE_MULTIPLIER, "PowerUp(Score Multiplier)"),
        ]

        for power_type, expected_name in test_cases:
            with self.subTest(power_type=power_type):
                power_up = PowerUp(power_type)
                self.assertEqual(power_up.getName(), expected_name)

    def test_power_up_with_extreme_durations(self):
        """Test power-up behavior with extreme duration values."""
        # Very large duration
        large_duration = 999999.999
        power_up_large = PowerUp(PowerUpType.SPEED_BOOST, duration=large_duration)
        self.assertEqual(power_up_large.get_duration(), large_duration)

        # Very small positive duration
        small_duration = 0.001
        power_up_small = PowerUp(PowerUpType.SLOW_TIME, duration=small_duration)
        self.assertEqual(power_up_small.get_duration(), small_duration)

    def test_concurrent_power_up_operations(self):
        """Test power-up state consistency under concurrent-like operations."""
        power_up = PowerUp(PowerUpType.INVINCIBILITY, duration=10.0)

        # Simulate rapid activate/deactivate cycles
        for i in range(10):
            power_up.activate()
            self.assertTrue(power_up.is_active())

            power_up.deactivate()
            self.assertFalse(power_up.is_active())
            self.assertEqual(power_up.activation_time, 0.0)

    def test_power_up_time_calculations_with_system_clock_changes(self):
        """Test power-up time calculations when system time changes."""
        power_up = PowerUp(PowerUpType.SCORE_MULTIPLIER, duration=10.0)

        with patch("time.time") as mock_time:
            # Initial activation
            mock_time.return_value = 1000.0
            power_up.activate()

            # Simulate system clock going backwards (edge case)
            mock_time.return_value = 500.0

            # Should handle gracefully (not crash)
            remaining_time = power_up.get_remaining_time()
            is_expired = power_up.is_expired()

            # Should return 0 or handle gracefully, not negative values
            self.assertGreaterEqual(remaining_time, 0.0)
            self.assertIsInstance(is_expired, bool)

    def test_power_up_printinfo_method(self):
        """Test that PowerUp can use Entity's printInfo method without crashing."""
        power_up = PowerUp(PowerUpType.SPEED_BOOST)

        # Should not raise an exception
        try:
            # Capture output to avoid cluttering test output
            import io
            import sys

            captured_output = io.StringIO()
            sys.stdout = captured_output

            power_up.printInfo()

            # Restore stdout
            sys.stdout = sys.__stdout__

            # Should have printed something
            output = captured_output.getvalue()
            self.assertIn("PowerUp", output)
            self.assertIn("Speed Boost", output)

        except Exception as e:
            self.fail(f"printInfo() raised {type(e).__name__} unexpectedly!")


if __name__ == "__main__":
    unittest.main()
