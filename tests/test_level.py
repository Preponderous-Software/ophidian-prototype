"""Unit tests for Level class"""
import pytest
import sys
sys.path.insert(0, '/home/runner/work/ophidian-prototype/ophidian-prototype/src')

from level.level import Level


class TestLevel:
    """Test Level class"""

    def test_level_initialization(self):
        """Test that Level initializes correctly"""
        name = "Level 1"
        size = 5
        level = Level(name, size)
        
        assert level.name == name
        assert level.size == size
        assert level.environment is not None

    def test_level_environment_properties(self):
        """Test that the level's environment is properly initialized"""
        name = "Test Level"
        size = 7
        level = Level(name, size)
        
        assert level.environment.getName() == name
        assert level.environment.getGrid().getSize() == size * size

    def test_level_with_different_sizes(self):
        """Test levels with different sizes"""
        sizes = [3, 5, 10, 12]
        
        for size in sizes:
            level = Level(f"Level {size}", size)
            assert level.size == size
            assert level.environment.getGrid().getColumns() == size
            assert level.environment.getGrid().getRows() == size

    def test_multiple_levels_have_unique_environments(self):
        """Test that different levels have unique environments"""
        level1 = Level("Level 1", 5)
        level2 = Level("Level 2", 5)
        
        assert level1.environment.getID() != level2.environment.getID()

    def test_level_name_variations(self):
        """Test levels with various names"""
        names = ["Level 1", "Test Level", "Boss Level", "Tutorial"]
        
        for name in names:
            level = Level(name, 5)
            assert level.name == name
            assert level.environment.getName() == name
