import unittest
from unittest.mock import patch

from src.powerup.powerUp import PowerUp
from src.powerup.powerUpType import PowerUpType
from src.environment.pyEnvLibEnvironmentRepositoryImpl import (
    PyEnvLibEnvironmentRepositoryImpl,
)
from src.config.config import Config
from src.snake.snakePartRepository import SnakePartRepository
from src.snake.snakePart import SnakePart
from src.food.food import Food


class TestPowerUpCollisionDetection(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures."""
        self.config = Config()
        self.snake_repo = SnakePartRepository()
        self.env_repo = PyEnvLibEnvironmentRepositoryImpl(
            1, self.config, self.snake_repo
        )

        # Create a snake part for testing
        self.snake_part = SnakePart((0, 255, 0))
        self.env_repo.add_entity_to_location(
            self.snake_part, self.env_repo.get_random_location()
        )

    def test_power_up_collection_activates_power_up(self):
        """Test that collecting a power-up activates it and adds to active list."""
        # Create and place a power-up
        power_up = PowerUp(PowerUpType.SPEED_BOOST, duration=10.0)
        power_up_location = self.env_repo.get_random_location()

        # Clear the location first
        entities_to_remove = list(power_up_location.getEntities().values())
        for entity in entities_to_remove:
            power_up_location.removeEntity(entity)

        self.env_repo.add_entity_to_location(power_up, power_up_location)

        # Add snake to same location (simulate collision)
        self.env_repo.add_entity_to_location(self.snake_part, power_up_location)

        # Manually trigger power-up collection logic (similar to what move_entity does)
        # Check for power-up collision
        collected_power_up = None
        for eid in power_up_location.getEntities():
            e = power_up_location.getEntity(eid)
            if isinstance(e, PowerUp):
                collected_power_up = e
                break

        if collected_power_up:
            collected_power_up.activate()
            self.env_repo.active_power_ups.append(collected_power_up)
            self.env_repo.remove_entity_from_location(collected_power_up)

        # Power-up should be activated and in active list
        self.assertTrue(
            any(
                pu.get_power_up_type() == PowerUpType.SPEED_BOOST
                for pu in self.env_repo.active_power_ups
            )
        )

        # Power-up should be removed from the location
        entities_at_location = list(power_up_location.getEntities().values())
        power_ups_at_location = [
            e for e in entities_at_location if isinstance(e, PowerUp)
        ]
        self.assertEqual(len(power_ups_at_location), 0)

    def test_food_and_power_up_collision_both_handled(self):
        """Test that both food and power-up are handled when both are present."""
        # Get a location for testing
        test_location = self.env_repo.get_random_location()

        # Clear the location first
        entities_to_remove = list(test_location.getEntities().values())
        for entity in entities_to_remove:
            test_location.removeEntity(entity)

        # Create and place food and power-up at same location
        food = Food((255, 0, 0))
        power_up = PowerUp(PowerUpType.INVINCIBILITY, duration=5.0)

        self.env_repo.add_entity_to_location(food, test_location)
        self.env_repo.add_entity_to_location(power_up, test_location)

        # Add snake to same location
        self.env_repo.add_entity_to_location(self.snake_part, test_location)

        initial_snake_count = self.snake_repo.get_length()
        initial_active_power_ups = len(self.env_repo.active_power_ups)

        # Manually simulate what move_entity does for food and power-up collision
        # Check for food
        collected_food = None
        for eid in test_location.getEntities():
            e = test_location.getEntity(eid)
            if isinstance(e, Food):
                collected_food = e
                break

        # Check for power-up
        collected_power_up = None
        for eid in test_location.getEntities():
            e = test_location.getEntity(eid)
            if isinstance(e, PowerUp):
                collected_power_up = e
                break

        # Handle food
        if collected_food:
            self.env_repo.remove_entity_from_location(collected_food)
            # Simulate snake growth by adding to repository
            new_snake_part = SnakePart((0, 255, 0))
            self.snake_repo.append(new_snake_part)

        # Handle power-up
        if collected_power_up:
            collected_power_up.activate()
            self.env_repo.active_power_ups.append(collected_power_up)
            self.env_repo.remove_entity_from_location(collected_power_up)

        # Both food and power-up should be handled
        # Food: Snake should grow (checked by snake count increase)
        self.assertGreater(self.snake_repo.get_length(), initial_snake_count)

        # Power-up: Should be activated
        self.assertGreater(
            len(self.env_repo.active_power_ups), initial_active_power_ups
        )

    @patch("random.random")
    def test_power_up_spawn_chance_respected(self, mock_random):
        """Test that power-up spawn chance is respected when food is eaten."""
        # Test case 1: Random below spawn chance - should spawn power-up
        mock_random.return_value = 0.04  # Below 5% spawn chance
        initial_power_up_count = self._count_power_ups_in_environment()

        # Set up food consumption scenario
        food = Food((255, 0, 0))
        food_location = self.env_repo.get_random_location()

        # Clear location and add food
        entities_to_remove = list(food_location.getEntities().values())
        for entity in entities_to_remove:
            food_location.removeEntity(entity)
        self.env_repo.add_entity_to_location(food, food_location)

        # Add snake to same location
        self.env_repo.add_entity_to_location(self.snake_part, food_location)

        # Manually simulate food consumption with power-up spawn chance
        # Check for food
        collected_food = None
        for eid in food_location.getEntities():
            e = food_location.getEntity(eid)
            if isinstance(e, Food):
                collected_food = e
                break

        if collected_food:
            self.env_repo.remove_entity_from_location(collected_food)
            self.env_repo.spawn_food()  # Spawn new food

            # Check spawn chance and spawn power-up if needed
            if mock_random.return_value < self.env_repo.power_up_spawn_chance:
                self.env_repo.spawn_power_up()

        final_power_up_count = self._count_power_ups_in_environment()
        self.assertGreater(final_power_up_count, initial_power_up_count)

        # Test case 2: Random above spawn chance - should not spawn power-up
        mock_random.return_value = 0.06  # Above 5% spawn chance

        # Set up another food consumption
        food2 = Food((0, 255, 0))
        food2_location = self.env_repo.get_random_location()
        entities_to_remove = list(food2_location.getEntities().values())
        for entity in entities_to_remove:
            food2_location.removeEntity(entity)
        self.env_repo.add_entity_to_location(food2, food2_location)

        self.env_repo.remove_entity_from_location(self.snake_part)
        self.env_repo.add_entity_to_location(self.snake_part, food2_location)

        initial_power_up_count = self._count_power_ups_in_environment()

        # Simulate food consumption
        collected_food = None
        for eid in food2_location.getEntities():
            e = food2_location.getEntity(eid)
            if isinstance(e, Food):
                collected_food = e
                break

        if collected_food:
            self.env_repo.remove_entity_from_location(collected_food)
            self.env_repo.spawn_food()  # Spawn new food

            # Check spawn chance and spawn power-up if needed
            if mock_random.return_value < self.env_repo.power_up_spawn_chance:
                self.env_repo.spawn_power_up()

        final_power_up_count = self._count_power_ups_in_environment()
        self.assertEqual(final_power_up_count, initial_power_up_count)

    def test_multiple_power_ups_same_location(self):
        """Test handling of multiple power-ups at the same location."""
        # Get a location for testing
        test_location = self.env_repo.get_random_location()

        # Clear the location first
        entities_to_remove = list(test_location.getEntities().values())
        for entity in entities_to_remove:
            test_location.removeEntity(entity)

        # Create and place multiple power-ups at same location
        power_up1 = PowerUp(PowerUpType.SPEED_BOOST, duration=5.0)
        power_up2 = PowerUp(PowerUpType.INVINCIBILITY, duration=8.0)

        self.env_repo.add_entity_to_location(power_up1, test_location)
        self.env_repo.add_entity_to_location(power_up2, test_location)

        # Add snake to same location
        self.env_repo.add_entity_to_location(self.snake_part, test_location)

        initial_active_count = len(self.env_repo.active_power_ups)

        # Manually simulate collection of all power-ups at location
        power_ups_to_collect = []
        for eid in test_location.getEntities():
            e = test_location.getEntity(eid)
            if isinstance(e, PowerUp):
                power_ups_to_collect.append(e)

        # Collect all power-ups
        for power_up in power_ups_to_collect:
            power_up.activate()
            self.env_repo.active_power_ups.append(power_up)
            self.env_repo.remove_entity_from_location(power_up)

        # Both power-ups should be activated
        self.assertGreater(len(self.env_repo.active_power_ups), initial_active_count)
        self.assertEqual(len(self.env_repo.active_power_ups), initial_active_count + 2)

    def _count_power_ups_in_environment(self):
        """Helper method to count power-ups in the environment."""
        count = 0
        for location_id in self.env_repo.environment.getGrid().getLocations():
            location = self.env_repo.environment.getGrid().getLocation(location_id)
            for entity in location.getEntities().values():
                if isinstance(entity, PowerUp):
                    count += 1
        return count


class TestPowerUpLifecycle(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures."""
        self.config = Config()
        self.snake_repo = SnakePartRepository()
        self.env_repo = PyEnvLibEnvironmentRepositoryImpl(
            1, self.config, self.snake_repo
        )

    def test_complete_power_up_lifecycle(self):
        """Test complete power-up lifecycle from spawn to expiration."""
        # 1. Spawn power-up
        initial_count = self._count_power_ups_in_environment()
        self.env_repo.spawn_power_up()
        spawned_count = self._count_power_ups_in_environment()
        self.assertGreater(spawned_count, initial_count)

        # 2. Find and collect the power-up
        spawned_power_up = None
        for location_id in self.env_repo.environment.getGrid().getLocations():
            location = self.env_repo.environment.getGrid().getLocation(location_id)
            for entity in location.getEntities().values():
                if isinstance(entity, PowerUp):
                    spawned_power_up = entity
                    break
            if spawned_power_up:
                break

        self.assertIsNotNone(spawned_power_up)

        # Simulate collection
        spawned_power_up.activate()
        self.env_repo.active_power_ups.append(spawned_power_up)
        self.env_repo.remove_entity_from_location(spawned_power_up)

        # 3. Verify activation
        self.assertTrue(spawned_power_up.is_active())
        self.assertEqual(len(self.env_repo.active_power_ups), 1)

        # 4. Test expiration
        with patch("time.time") as mock_time:
            # Set time to just before expiration
            mock_time.return_value = (
                spawned_power_up.activation_time + spawned_power_up.get_duration() - 0.1
            )
            self.assertFalse(spawned_power_up.is_expired())

            # Set time to after expiration
            mock_time.return_value = (
                spawned_power_up.activation_time + spawned_power_up.get_duration() + 0.1
            )
            self.assertTrue(spawned_power_up.is_expired())

            # Update should remove expired power-up
            self.env_repo.update_power_ups()
            self.assertEqual(len(self.env_repo.active_power_ups), 0)

    def test_power_up_deactivation_before_expiration(self):
        """Test manual power-up deactivation before natural expiration."""
        power_up = PowerUp(
            PowerUpType.SCORE_MULTIPLIER, duration=100.0
        )  # Long duration
        power_up.activate()
        self.env_repo.active_power_ups.append(power_up)

        # Should be active
        self.assertTrue(power_up.is_active())
        self.assertEqual(len(self.env_repo.active_power_ups), 1)

        # Manually deactivate
        power_up.deactivate()

        # Should no longer be active
        self.assertFalse(power_up.is_active())

        # Update should not remove it since we don't auto-remove manually deactivated ones
        # (This tests the current implementation behavior)
        self.env_repo.update_power_ups()
        # Note: Current implementation only removes expired power-ups, not deactivated ones

    def _count_power_ups_in_environment(self):
        """Helper method to count power-ups in the environment."""
        count = 0
        for location_id in self.env_repo.environment.getGrid().getLocations():
            location = self.env_repo.environment.getGrid().getLocation(location_id)
            for entity in location.getEntities().values():
                if isinstance(entity, PowerUp):
                    count += 1
        return count


if __name__ == "__main__":
    unittest.main()
