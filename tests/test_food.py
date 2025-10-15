"""Unit tests for Food class"""
import pytest
import sys
sys.path.insert(0, '/home/runner/work/ophidian-prototype/ophidian-prototype/src')

from food.food import Food


class TestFood:
    """Test Food entity class"""

    def test_food_initialization(self):
        """Test that Food initializes correctly"""
        color = (255, 0, 0)
        food = Food(color)
        
        assert food.getName() == "Food"
        assert food.getColor() == color

    def test_food_with_different_colors(self):
        """Test Food with various color values"""
        colors = [
            (255, 0, 0),
            (0, 255, 0),
            (0, 0, 255),
            (100, 150, 200)
        ]
        
        for color in colors:
            food = Food(color)
            assert food.getColor() == color

    def test_food_inherits_from_entity(self):
        """Test that Food properly inherits Entity properties"""
        food = Food((255, 255, 0))
        
        # Check Entity methods are available
        assert hasattr(food, 'getID')
        assert hasattr(food, 'getName')
        assert hasattr(food, 'getEnvironmentID')
        assert hasattr(food, 'getGridID')
        assert hasattr(food, 'getLocationID')
        
        # Check ID is generated
        assert food.getID() is not None

    def test_food_entity_ids(self):
        """Test that different Food instances have different IDs"""
        food1 = Food((255, 0, 0))
        food2 = Food((0, 255, 0))
        
        assert food1.getID() != food2.getID()
