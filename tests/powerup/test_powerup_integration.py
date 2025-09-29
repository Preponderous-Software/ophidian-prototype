import unittest
from unittest.mock import Mock, patch
import pygame

from src.powerup.powerUp import PowerUp
from src.powerup.powerUpType import PowerUpType
from src.environment.pyEnvLibEnvironmentRepositoryImpl import (
    PyEnvLibEnvironmentRepositoryImpl,
)
from src.config.config import Config
from src.snake.snakePartRepository import SnakePartRepository
from src.graphics.renderer import Renderer
from src.score.game_score import GameScore


class TestPowerUpIntegration(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures."""
        self.config = Config()
        self.snake_repo = SnakePartRepository()
        self.env_repo = PyEnvLibEnvironmentRepositoryImpl(
            1, self.config, self.snake_repo
        )

        # Mock pygame for renderer tests
        pygame.init()
        self.mock_display = pygame.Surface((800, 600))

    def test_environment_repository_initialization(self):
        """Test that environment repository initializes power-up system correctly."""
        self.assertIsInstance(self.env_repo.active_power_ups, list)
        self.assertEqual(len(self.env_repo.active_power_ups), 0)
        self.assertEqual(self.env_repo.power_up_spawn_chance, 0.05)

    @patch("random.choice")
    def test_power_up_spawning_creates_correct_types(self, mock_choice):
        """Test that power-up spawning creates correct power-up types with proper attributes."""
        # Test each power-up type
        test_cases = [
            (PowerUpType.SPEED_BOOST, (255, 165, 0), 8.0),
            (PowerUpType.SLOW_TIME, (0, 191, 255), 10.0),
            (PowerUpType.INVINCIBILITY, (255, 20, 147), 5.0),
            (PowerUpType.SCORE_MULTIPLIER, (255, 215, 0), 12.0),
        ]

        for power_type, expected_color, expected_duration in test_cases:
            with self.subTest(power_type=power_type):
                mock_choice.return_value = power_type

                # Clear environment first
                self.env_repo.clear()

                # Spawn power-up
                self.env_repo.spawn_power_up()

                # Find the spawned power-up in the environment
                spawned_power_up = None
                for location_id in self.env_repo.environment.getGrid().getLocations():
                    location = self.env_repo.environment.getGrid().getLocation(
                        location_id
                    )
                    for entity in location.getEntities().values():
                        if isinstance(entity, PowerUp):
                            spawned_power_up = entity
                            break
                    if spawned_power_up:
                        break

                self.assertIsNotNone(
                    spawned_power_up, f"No power-up found for type {power_type}"
                )
                self.assertEqual(spawned_power_up.get_power_up_type(), power_type)
                self.assertEqual(spawned_power_up.getColor(), expected_color)
                self.assertEqual(spawned_power_up.get_duration(), expected_duration)

    def test_power_up_update_removes_expired(self):
        """Test that update_power_ups removes expired power-ups."""
        # Create and activate a power-up
        power_up = PowerUp(PowerUpType.SPEED_BOOST, duration=1.0)
        power_up.activate()
        self.env_repo.active_power_ups.append(power_up)

        # Initially should not be expired
        self.assertFalse(power_up.is_expired())
        self.assertEqual(len(self.env_repo.active_power_ups), 1)

        # Mock time to make it expired
        with patch("time.time") as mock_time:
            mock_time.return_value = power_up.activation_time + 2.0  # 2 seconds later

            self.env_repo.update_power_ups()

            # Should be removed from active list
            self.assertEqual(len(self.env_repo.active_power_ups), 0)

    def test_get_active_power_ups_returns_copy(self):
        """Test that get_active_power_ups returns a copy of the list."""
        power_up = PowerUp(PowerUpType.INVINCIBILITY)
        power_up.activate()
        self.env_repo.active_power_ups.append(power_up)

        active_list = self.env_repo.get_active_power_ups()

        # Modify the returned list
        active_list.clear()

        # Original list should be unchanged
        self.assertEqual(len(self.env_repo.active_power_ups), 1)

    def test_clear_removes_power_ups_from_environment(self):
        """Test that clear() removes power-ups from environment and active list."""
        # Spawn a power-up
        self.env_repo.spawn_power_up()

        # Add to active list as well
        power_up = PowerUp(PowerUpType.SCORE_MULTIPLIER)
        power_up.activate()
        self.env_repo.active_power_ups.append(power_up)

        # Clear the environment
        self.env_repo.clear()

        # Check that active power-ups list is cleared
        self.assertEqual(len(self.env_repo.active_power_ups), 0)

        # Check that no power-ups remain in environment
        power_up_count = 0
        for location_id in self.env_repo.environment.getGrid().getLocations():
            location = self.env_repo.environment.getGrid().getLocation(location_id)
            for entity in location.getEntities().values():
                if isinstance(entity, PowerUp):
                    power_up_count += 1

        self.assertEqual(power_up_count, 0)


class TestPowerUpEdgeCases(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures."""
        self.config = Config()
        self.snake_repo = SnakePartRepository()
        self.env_repo = PyEnvLibEnvironmentRepositoryImpl(
            1, self.config, self.snake_repo
        )

    def test_spawn_power_up_when_grid_full(self):
        """Test power-up spawning when grid is full (edge case)."""
        # Fill all locations with mock entities to simulate full grid
        mock_entity = Mock()
        mock_entity.getName.return_value = "MockEntity"

        for location_id in self.env_repo.environment.getGrid().getLocations():
            location = self.env_repo.environment.getGrid().getLocation(location_id)
            location.addEntity(mock_entity)

        # Attempt to spawn power-up
        initial_power_up_count = 0
        for location_id in self.env_repo.environment.getGrid().getLocations():
            location = self.env_repo.environment.getGrid().getLocation(location_id)
            for entity in location.getEntities().values():
                if isinstance(entity, PowerUp):
                    initial_power_up_count += 1

        self.env_repo.spawn_power_up()

        # Count power-ups after spawn attempt
        final_power_up_count = 0
        for location_id in self.env_repo.environment.getGrid().getLocations():
            location = self.env_repo.environment.getGrid().getLocation(location_id)
            for entity in location.getEntities().values():
                if isinstance(entity, PowerUp):
                    final_power_up_count += 1

        # Should not have spawned a power-up due to full grid
        self.assertEqual(initial_power_up_count, final_power_up_count)

    def test_power_up_expiration_when_not_active(self):
        """Test that inactive power-ups are never considered expired."""
        power_up = PowerUp(PowerUpType.SPEED_BOOST, duration=1.0)

        # Should not be expired even after duration would pass
        with patch("time.time") as mock_time:
            mock_time.return_value = 1000.0
            self.assertFalse(power_up.is_expired())

    def test_multiple_power_ups_same_type(self):
        """Test handling multiple active power-ups of the same type."""
        power_up1 = PowerUp(PowerUpType.SPEED_BOOST, duration=5.0)
        power_up2 = PowerUp(PowerUpType.SPEED_BOOST, duration=10.0)

        power_up1.activate()
        power_up2.activate()

        self.env_repo.active_power_ups.extend([power_up1, power_up2])

        self.assertEqual(len(self.env_repo.active_power_ups), 2)

        # Both should be of the same type but be different instances
        self.assertEqual(power_up1.get_power_up_type(), power_up2.get_power_up_type())
        self.assertNotEqual(power_up1, power_up2)


class TestRendererPowerUpIntegration(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures with pygame mocking."""
        pygame.init()
        self.config = Config()
        self.snake_repo = SnakePartRepository()
        self.env_repo = PyEnvLibEnvironmentRepositoryImpl(
            1, self.config, self.snake_repo
        )
        self.game_score = GameScore(self.snake_repo, self.env_repo)
        self.game_display = pygame.display.set_mode((800, 600))
        self.renderer = Renderer(
            False,
            self.config,
            self.env_repo,
            self.snake_repo,
            self.game_score,
            self.game_display,
        )

    def tearDown(self):
        """Clean up pygame."""
        pygame.quit()

    def test_draw_active_power_ups_no_power_ups(self):
        """Test that draw_active_power_ups handles empty power-up list."""
        # Should not raise any exceptions
        try:
            self.renderer.draw_active_power_ups()
        except Exception as e:
            self.fail(f"draw_active_power_ups raised {type(e).__name__} unexpectedly!")

    def test_draw_active_power_ups_with_power_ups(self):
        """Test that draw_active_power_ups handles active power-ups."""
        # Create and activate power-ups
        power_up1 = PowerUp(PowerUpType.SPEED_BOOST, duration=10.0)
        power_up2 = PowerUp(PowerUpType.INVINCIBILITY, duration=5.0)

        power_up1.activate()
        power_up2.activate()

        self.env_repo.active_power_ups.extend([power_up1, power_up2])

        # Should not raise any exceptions
        try:
            self.renderer.draw_active_power_ups()
        except Exception as e:
            self.fail(f"draw_active_power_ups raised {type(e).__name__} unexpectedly!")

    @patch("pygame.draw.rect")
    def test_power_up_visual_indicators_drawn(self, mock_draw_rect):
        """Test that power-up visual indicators are actually drawn."""
        power_up = PowerUp(PowerUpType.SLOW_TIME, duration=8.0, color=(0, 191, 255))
        power_up.activate()
        self.env_repo.active_power_ups.append(power_up)

        self.renderer.draw_active_power_ups()

        # Should have called pygame.draw.rect for the indicator
        mock_draw_rect.assert_called()

        # Check that the color was used correctly
        call_args = mock_draw_rect.call_args
        self.assertEqual(
            call_args[0][1], (0, 191, 255)
        )  # Color should match power-up color


if __name__ == "__main__":
    unittest.main()
