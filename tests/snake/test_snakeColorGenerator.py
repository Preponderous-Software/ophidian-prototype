import unittest

from src.snake.snakeColorGenerator import SnakeColorGenerator


class TestSnakeColorGenerator(unittest.TestCase):
    def test_generate_green_shade_returns_tuple(self):
        # Act
        color = SnakeColorGenerator.generate_green_shade()

        # Assert
        self.assertIsInstance(color, tuple)
        self.assertEqual(len(color), 3)

    def test_generate_green_shade_has_correct_ranges(self):
        # Act & Assert - test multiple times to check randomness
        for _ in range(10):
            color = SnakeColorGenerator.generate_green_shade()
            red, green, blue = color

            # Red should be low (0-50)
            self.assertGreaterEqual(red, 0)
            self.assertLessEqual(red, 50)

            # Green should be high (100-255) - this is the dominant color
            self.assertGreaterEqual(green, 100)
            self.assertLessEqual(green, 255)

            # Blue should be low to medium (0-100)
            self.assertGreaterEqual(blue, 0)
            self.assertLessEqual(blue, 100)

    def test_generate_green_shade_produces_green_dominant_colors(self):
        # Act & Assert - test that green is always the dominant component
        for _ in range(10):
            color = SnakeColorGenerator.generate_green_shade()
            red, green, blue = color

            # Green should be greater than or equal to red and blue
            self.assertGreaterEqual(green, red)
            self.assertGreaterEqual(green, blue)


if __name__ == "__main__":
    unittest.main()
