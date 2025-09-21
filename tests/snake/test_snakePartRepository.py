import unittest

from src.snake.snakePartRepository import SnakePartRepository
from src.snake.snakePart import SnakePart


class TestSnakePartRepository(unittest.TestCase):
    def setUp(self):
        self.repository = SnakePartRepository()

    def test_get_length_initial(self):
        # Assert that the initial length of the repository is 0
        self.assertEqual(self.repository.get_length(), 0)

    def test_append_snake_part(self):
        # Arrange
        snake_part = SnakePart("blue")

        # Act
        self.repository.append(snake_part)

        # Assert
        self.assertEqual(self.repository.get_length(), 1)
        self.assertIn(snake_part, self.repository.snake_parts)

    def test_append_multiple_snake_parts(self):
        # Arrange
        snake_part = SnakePart("blue")
        snake_part2 = SnakePart("red")

        # Act
        self.repository.append(snake_part)
        self.repository.append(snake_part2)

        # Assert
        self.assertEqual(self.repository.get_length(), 2)
        self.assertIn(snake_part, self.repository.snake_parts)
        self.assertIn(snake_part2, self.repository.snake_parts)

    def test_clear_snake_parts(self):
        # Arrange
        snake_part = SnakePart("blue")
        snake_part2 = SnakePart("red")
        self.repository.append(snake_part)
        self.repository.append(snake_part2)

        # Act
        self.repository.clear()

        # Assert
        self.assertEqual(self.repository.get_length(), 0)
        self.assertEqual(self.repository.snake_parts, [])


if __name__ == '__main__':
    unittest.main()
