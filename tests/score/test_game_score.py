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
        # Assert that the initial points are set to 0
        self.assertEqual(self.game_score.points, 0)

    def test_calculate_points(self):
        # Arrange
        self.snake_part_repository.get_length.return_value = 10
        self.environment_repository.get_num_locations.return_value = 50

        # Act
        points = self.game_score.calculate()

        # Assert
        self.assertEqual(200, points)
        self.assertEqual(200, self.game_score.points)

    def test_reset(self):
        # Arrange
        self.game_score.points = 100

        # Act
        self.game_score.reset()

        # Assert
        self.assertEqual(self.game_score.points, 0)


if __name__ == "__main__":
    unittest.main()
