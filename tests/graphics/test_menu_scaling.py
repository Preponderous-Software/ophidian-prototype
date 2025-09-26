import unittest
from unittest.mock import Mock, MagicMock
import pygame

from src.graphics.main_menu import MainMenu
from src.graphics.options_menu import OptionsMenu  
from src.graphics.high_scores_menu import HighScoresMenu
from src.config.config import Config


class TestMenuScaling(unittest.TestCase):
    """Test dynamic scaling functionality for all menus."""

    def setUp(self):
        """Set up test fixtures"""
        pygame.init()
        pygame.display.set_mode((1, 1))  # Minimal display for testing
        
        self.config = Config()
        
        # Mock game display that can return different sizes
        self.game_display = Mock()
        
    def test_main_menu_dynamic_scaling(self):
        """Test that main menu adapts to different window sizes"""
        menu = MainMenu(self.config, self.game_display)
        
        # Test with different window sizes
        test_sizes = [(600, 400), (800, 600), (1200, 800)]
        
        for width, height in test_sizes:
            with self.subTest(window_size=(width, height)):
                self.game_display.get_size.return_value = (width, height)
                
                # Mock the fill method to capture drawing calls
                self.game_display.fill = Mock()
                
                # Mock the graphik object methods
                menu.graphik.drawText = Mock()
                menu.graphik.drawRectangle = Mock()
                
                # Call draw method
                menu.draw()
                
                # Verify that graphik methods were called with scaled positions
                # Title should be centered horizontally
                calls = menu.graphik.drawText.call_args_list
                title_call = calls[0]  # First call is the title
                
                # Title x position should be center of current width
                self.assertEqual(title_call[0][1], width // 2)
                # Title y position should be based on current height
                self.assertEqual(title_call[0][2], height // 2 - 150)

    def test_options_menu_dynamic_scaling(self):
        """Test that options menu adapts to different window sizes"""
        menu = OptionsMenu(self.config, self.game_display)
        
        # Test with different window sizes
        test_sizes = [(600, 400), (800, 600), (1200, 800)]
        
        for width, height in test_sizes:
            with self.subTest(window_size=(width, height)):
                self.game_display.get_size.return_value = (width, height)
                self.game_display.fill = Mock()
                menu.graphik.drawText = Mock()
                
                menu.draw()
                
                # Verify title is centered
                calls = menu.graphik.drawText.call_args_list
                title_call = calls[0]
                self.assertEqual(title_call[0][1], width // 2)
                self.assertEqual(title_call[0][2], height // 2 - 100)

    def test_high_scores_menu_dynamic_scaling(self):
        """Test that high scores menu adapts to different window sizes"""
        menu = HighScoresMenu(self.config, self.game_display)
        
        # Test with different window sizes  
        test_sizes = [(600, 400), (800, 600), (1200, 800)]
        
        for width, height in test_sizes:
            with self.subTest(window_size=(width, height)):
                self.game_display.get_size.return_value = (width, height)
                self.game_display.fill = Mock()
                menu.graphik.drawText = Mock()
                
                menu.draw()
                
                # Verify title is centered
                calls = menu.graphik.drawText.call_args_list
                title_call = calls[0]
                self.assertEqual(title_call[0][1], width // 2)
                self.assertEqual(title_call[0][2], height // 2 - 100)

    def test_main_menu_mouse_interaction_scales(self):
        """Test that main menu mouse interactions scale with window size"""
        menu = MainMenu(self.config, self.game_display)
        
        # Test with a wide window
        self.game_display.get_size.return_value = (1200, 800)
        
        # Click in center of first menu item (should be Play Game)
        center_x = 1200 // 2
        menu_start_y = 800 // 2 - 50
        first_item_y = menu_start_y + 25  # Middle of first item
        
        result = menu.handle_mouse_click((center_x, first_item_y))
        
        # Should return the action for the first menu item (Play Game)
        from src.state.menu_state import MenuState
        self.assertEqual(result, MenuState.GAME)

    def test_fallback_to_config_values(self):
        """Test that menus fall back to config values when get_size() fails"""
        menu = MainMenu(self.config, self.game_display)
        
        # Mock get_size to raise an exception
        self.game_display.get_size.side_effect = ValueError("Mock error")
        self.game_display.fill = Mock()
        menu.graphik.drawText = Mock()
        menu.graphik.drawRectangle = Mock()
        
        # Should not raise an exception and use config values
        menu.draw()
        
        # Verify title uses config dimensions
        calls = menu.graphik.drawText.call_args_list
        title_call = calls[0]
        self.assertEqual(title_call[0][1], self.config.display_width // 2)
        self.assertEqual(title_call[0][2], self.config.display_height // 2 - 150)

    def tearDown(self):
        """Clean up after tests"""
        pygame.quit()


if __name__ == '__main__':
    unittest.main()