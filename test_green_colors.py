#!/usr/bin/env python3
"""
Quick test script to verify that snake parts are created with green shades.
"""

from src.config.config import Config
from src.snake.snakePart import SnakePart

def test_green_colors():
    config = Config()
    
    print("Testing green color generation:")
    print("=" * 40)
    
    # Test the color generation function directly
    for i in range(5):
        color = config.generate_green_shade()
        red, green, blue = color
        print(f"Color {i+1}: RGB({red}, {green}, {blue})")
        print(f"  Red: {red} (should be 0-50)")
        print(f"  Green: {green} (should be 100-255)")
        print(f"  Blue: {blue} (should be 0-100)")
        print(f"  Green dominant: {green >= red and green >= blue}")
        print()
    
    # Test snake part creation
    print("Testing snake part creation with green colors:")
    print("=" * 40)
    
    for i in range(3):
        snake_part = SnakePart(config.generate_green_shade())
        color = snake_part.getColor()
        red, green, blue = color
        print(f"Snake Part {i+1}: RGB({red}, {green}, {blue})")
        print(f"  Is green dominant: {green >= red and green >= blue}")
        print()

if __name__ == "__main__":
    test_green_colors()