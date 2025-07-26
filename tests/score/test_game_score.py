import unittest
from unittest.mock import MagicMock

from src.score.game_score import GameScore


class TestGameScore(unittest.TestCase):
    def setUp(self):
        self.snake_part_repository = MagicMock()
        self.environment_repository = MagicMock()
        self.game_score = GameScore(
            self.snake_part_repository, self.environment_repository
        )

    def test_initial_points(self):
        # Assert that both initial points are set to 0
        self.assertEqual(self.game_score.current_points, 0)
        self.assertEqual(self.game_score.cumulative_points, 0)

    def test_calculate_points(self):
        # Arrange
        self.snake_part_repository.get_length.return_value = 10
        self.environment_repository.get_num_locations.return_value = 50

        # Act
        points = self.game_score.calculate()

        # Assert
        self.assertEqual(200, points)
        self.assertEqual(200, self.game_score.current_points)
        self.assertEqual(0, self.game_score.cumulative_points)  # Cumulative should still be 0

    def test_reset(self):
        # Arrange
        self.game_score.current_points = 100
        self.game_score.cumulative_points = 500

        # Act
        self.game_score.reset()

        # Assert
        self.assertEqual(self.game_score.current_points, 0)
        self.assertEqual(self.game_score.cumulative_points, 500)  # Cumulative should not reset

    def test_level_complete(self):
        # Arrange
        self.game_score.current_points = 100
        self.game_score.cumulative_points = 500

        # Act
        self.game_score.level_complete()

        # Assert
        self.assertEqual(self.game_score.current_points, 0)  # Current points should reset
        self.assertEqual(self.game_score.cumulative_points, 600)  # Should add current to cumulative

    def test_display_stats(self):
        # Arrange
        self.snake_part_repository.get_length.return_value = 10
        self.environment_repository.get_num_locations.return_value = 50
        self.game_score.current_points = 200
        self.game_score.cumulative_points = 500

        # Act & Assert
        # We can't easily test the print output, but we can at least ensure it doesn't raise exceptions
        self.game_score.display_stats()

    def test_complete_game_flow(self):
        # Arrange
        self.snake_part_repository.get_length.return_value = 10
        self.environment_repository.get_num_locations.return_value = 50

        # Act - Simulate playing through multiple levels
        # Level 1
        self.game_score.calculate()  # Score = 200
        self.game_score.level_complete()  # Adds to cumulative

        # Level 2
        self.game_score.calculate()  # Score = 200
        self.game_score.reset()  # Simulates death, should not add to cumulative

        # Level 2 retry
        self.game_score.calculate()  # Score = 200
        self.game_score.level_complete()  # Adds to cumulative

        # Assert
        self.assertEqual(self.game_score.current_points, 0)
        self.assertEqual(self.game_score.cumulative_points, 400)  # Only two successful levels


if __name__ == "__main__":
    unittest.main()
