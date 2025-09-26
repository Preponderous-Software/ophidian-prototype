import unittest
from unittest.mock import Mock, MagicMock
import pygame

from src.graphics.renderer import Renderer
from src.config.config import Config


class TestRendererScaling(unittest.TestCase):
    """Test proportional scaling and centering functionality in the Renderer."""

    def setUp(self):
        """Set up test fixtures"""
        pygame.init()
        pygame.display.set_mode((1, 1))  # Minimal display for testing
        
        self.config = Config()
        self.collision = False
        
        # Mock dependencies
        self.environment_repository = Mock()
        self.environment_repository.get_rows.return_value = 5
        self.environment_repository.get_columns.return_value = 5
        self.environment_repository.get_locations.return_value = []
        
        self.snake_part_repository = Mock()
        self.game_score = Mock()
        
        # Create renderer instance
        self.renderer = Renderer(
            self.collision,
            self.config,
            self.environment_repository,
            self.snake_part_repository,
            self.game_score
        )

    def test_proportional_scaling_square_window(self):
        """Test that scaling works correctly for square windows"""
        # Mock a square window (600x600)
        self.renderer.graphik.gameDisplay = Mock()
        self.renderer.graphik.gameDisplay.get_size.return_value = (600, 600)
        
        # Initialize scaling
        self.renderer.initialize_location_width_and_height()
        
        # Available height = 600 - 70 (UI space) = 530
        # Cell size = 530 / 5 = 106
        expected_cell_size = 106.0
        
        self.assertEqual(self.renderer.location_width, expected_cell_size)
        self.assertEqual(self.renderer.location_height, expected_cell_size)
        
        # Game area should be centered horizontally
        # Game area width = 5 * 106 = 530
        # Offset = (600 - 530) / 2 = 35
        expected_offset_x = 35.0
        self.assertEqual(self.renderer.game_area_offset_x, expected_offset_x)
        self.assertEqual(self.renderer.game_area_offset_y, 0)

    def test_proportional_scaling_wide_window(self):
        """Test that scaling works correctly for wide windows"""
        # Mock a wide window (800x600)
        self.renderer.graphik.gameDisplay = Mock()
        self.renderer.graphik.gameDisplay.get_size.return_value = (800, 600)
        
        # Initialize scaling
        self.renderer.initialize_location_width_and_height()
        
        # Available height = 600 - 70 = 530
        # Cell size = 530 / 5 = 106
        expected_cell_size = 106.0
        
        self.assertEqual(self.renderer.location_width, expected_cell_size)
        self.assertEqual(self.renderer.location_height, expected_cell_size)
        
        # Game area should be centered horizontally
        # Game area width = 5 * 106 = 530
        # Offset = (800 - 530) / 2 = 135
        expected_offset_x = 135.0
        self.assertEqual(self.renderer.game_area_offset_x, expected_offset_x)

    def test_proportional_scaling_different_grid_size(self):
        """Test scaling with different grid dimensions"""
        # Mock grid with different dimensions
        self.environment_repository.get_rows.return_value = 8
        self.environment_repository.get_columns.return_value = 6
        
        # Mock window
        self.renderer.graphik.gameDisplay = Mock()
        self.renderer.graphik.gameDisplay.get_size.return_value = (600, 600)
        
        # Initialize scaling
        self.renderer.initialize_location_width_and_height()
        
        # Available height = 600 - 70 = 530
        # Grid size = max(8, 6) = 8
        # Cell size = 530 / 8 = 66.25
        expected_cell_size = 66.25
        
        self.assertEqual(self.renderer.location_width, expected_cell_size)
        self.assertEqual(self.renderer.location_height, expected_cell_size)
        
        # Game area width = 8 * 66.25 = 530
        # Offset = (600 - 530) / 2 = 35
        expected_offset_x = 35.0
        self.assertEqual(self.renderer.game_area_offset_x, expected_offset_x)

    def test_scaling_maintains_square_cells(self):
        """Test that cells remain square regardless of window aspect ratio"""
        test_cases = [
            (400, 600),  # Tall window
            (800, 400),  # Wide window  
            (500, 500),  # Square window
        ]
        
        for width, height in test_cases:
            with self.subTest(window_size=(width, height)):
                self.renderer.graphik.gameDisplay = Mock()
                self.renderer.graphik.gameDisplay.get_size.return_value = (width, height)
                
                self.renderer.initialize_location_width_and_height()
                
                # Cells should always be square
                self.assertEqual(self.renderer.location_width, self.renderer.location_height)
                
                # Verify cells are properly sized based on available height
                available_height = height - 70
                expected_size = available_height / 5  # 5x5 grid
                self.assertEqual(self.renderer.location_width, expected_size)

    def tearDown(self):
        """Clean up after tests"""
        pygame.quit()


if __name__ == '__main__':
    unittest.main()