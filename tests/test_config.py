"""Unit tests for Config class"""
import pytest
import sys
sys.path.insert(0, '/home/runner/work/ophidian-prototype/ophidian-prototype/src')

from config.config import Config


class TestConfig:
    """Test Config class initialization and attributes"""

    def test_config_initialization(self):
        """Test that Config initializes with correct default values"""
        config = Config()
        
        # Display settings
        assert config.displayWidth == 500
        assert config.displayHeight == 500
        assert config.fullscreen == False
        assert config.black == (0, 0, 0)
        assert config.white == (255, 255, 255)
        assert config.green == (0, 255, 0)
        assert config.red == (255, 0, 0)
        assert config.yellow == (255, 255, 0)
        assert config.textSize == 50

    def test_grid_size_settings(self):
        """Test grid size configuration"""
        config = Config()
        
        assert config.gridSize == 5
        assert config.minGridSize == 5
        assert config.maxGridSize == 12

    def test_tick_speed_settings(self):
        """Test tick speed configuration"""
        config = Config()
        
        assert config.limitTickSpeed == True
        assert config.tickSpeed == 0.1

    def test_misc_settings(self):
        """Test miscellaneous configuration"""
        config = Config()
        
        assert config.debug == False
        assert config.restartUponCollision == True
        assert config.levelProgressPercentageRequired == 0.5
