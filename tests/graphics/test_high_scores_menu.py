import unittest
from unittest.mock import MagicMock
import os
import pygame
from src.graphics.high_scores_menu import HighScoresMenu
from src.state.menu_state import MenuState


class TestHighScoresMenu(unittest.TestCase):
    """Test the HighScoresMenu class"""

    def setUp(self):
        """Set up test fixtures"""
        # Disable audio to avoid ALSA warnings in tests
        os.environ['SDL_AUDIODRIVER'] = 'dummy'
        pygame.init()
        
        # Mock config and display
        self.mock_config = MagicMock()
        self.mock_config.display_width = 500
        self.mock_config.display_height = 500
        self.mock_config.black = (0, 0, 0)
        self.mock_config.white = (255, 255, 255)
        self.mock_config.green = (0, 255, 0)
        self.mock_config.yellow = (255, 255, 0)
        self.mock_config.text_size = 50
        
        self.mock_display = MagicMock()

    def tearDown(self):
        """Clean up after tests"""
        pygame.quit()

    def test_high_scores_menu_initialization(self):
        """Test HighScoresMenu initialization"""
        menu = HighScoresMenu(self.mock_config, self.mock_display)
        
        self.assertIsNotNone(menu.config)
        self.assertIsNotNone(menu.game_display)
        self.assertIsNotNone(menu.graphik)

    def test_handle_key_down_escape(self):
        """Test that escape key returns to main menu"""
        menu = HighScoresMenu(self.mock_config, self.mock_display)
        
        result = menu.handle_key_down(pygame.K_ESCAPE)
        self.assertEqual(result, MenuState.MAIN_MENU)

    def test_handle_key_down_enter(self):
        """Test that enter key returns to main menu"""
        menu = HighScoresMenu(self.mock_config, self.mock_display)
        
        result = menu.handle_key_down(pygame.K_RETURN)
        self.assertEqual(result, MenuState.MAIN_MENU)

    def test_handle_key_down_other_keys(self):
        """Test that other keys return None"""
        menu = HighScoresMenu(self.mock_config, self.mock_display)
        
        result = menu.handle_key_down(pygame.K_a)
        self.assertIsNone(result)
        
        result = menu.handle_key_down(pygame.K_SPACE)
        self.assertIsNone(result)

    def test_handle_mouse_click(self):
        """Test mouse click returns to main menu"""
        menu = HighScoresMenu(self.mock_config, self.mock_display)
        
        result = menu.handle_mouse_click((100, 100))
        self.assertEqual(result, MenuState.MAIN_MENU)

    def test_draw_method(self):
        """Test that draw method makes expected calls"""
        menu = HighScoresMenu(self.mock_config, self.mock_display)
        
        # Mock the graphik methods
        menu.graphik.drawText = MagicMock()
        
        menu.draw()
        
        # Should call fill on display
        menu.game_display.fill.assert_called_with(self.mock_config.black)
        
        # Should draw text
        self.assertTrue(menu.graphik.drawText.called)
        
        # Check that "HIGH SCORES" title is drawn
        title_calls = [call for call in menu.graphik.drawText.call_args_list 
                      if len(call[0]) > 0 and call[0][0] == "HIGH SCORES"]
        self.assertTrue(len(title_calls) > 0)


if __name__ == '__main__':
    unittest.main()