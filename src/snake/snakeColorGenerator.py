import random


# @author Daniel McCoy Stephenson
# @since August 6th, 2022
class SnakeColorGenerator:
    """Generator for creating varying shades of green for snake parts."""

    @staticmethod
    def generate_green_shade():
        """Generate a random shade of green for snake parts."""
        # Keep red component low (0-50), vary green (100-255), keep blue low (0-100)
        red = random.randint(0, 50)
        green = random.randint(100, 255)
        blue = random.randint(0, 100)
        return (red, green, blue)
