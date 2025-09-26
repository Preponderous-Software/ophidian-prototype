import unittest
from unittest.mock import MagicMock, patch
import os
import pygame
from src.graphics.options_menu import OptionsMenu
from src.state.menu_state import MenuState


class TestOptionsMenu(unittest.TestCase):
    """Test the OptionsMenu class"""

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
        self.mock_config.blue = (0, 0, 255)
        self.mock_config.gray = (128, 128, 128)
        self.mock_config.text_size = 50
        
        # Add audio settings
        self.mock_config.master_volume = 0.7
        self.mock_config.music_volume = 0.5
        self.mock_config.sfx_volume = 0.8
        self.mock_config.fullscreen = False
        self.mock_config.limit_tick_speed = True
        self.mock_config.difficulty = "Normal"
        
        # Mock methods
        self.mock_config.get_available_resolutions.return_value = [(500, 500), (800, 600)]
        self.mock_config.get_difficulty_levels.return_value = ["Easy", "Normal", "Hard"]
        self.mock_config.save_settings = MagicMock()
        
        self.mock_display = MagicMock()
        self.mock_display.get_size.return_value = (500, 500)

    def tearDown(self):
        """Clean up after tests"""
        pygame.quit()

    def test_options_menu_initialization(self):
        """Test OptionsMenu initialization"""
        menu = OptionsMenu(self.mock_config, self.mock_display)
        
        self.assertIsNotNone(menu.config)
        self.assertIsNotNone(menu.game_display)
        self.assertIsNotNone(menu.graphik)
        self.assertIsNotNone(menu.controls)
        self.assertTrue(len(menu.controls) > 0)

    def test_handle_key_down_escape(self):
        """Test that escape key returns to main menu"""
        menu = OptionsMenu(self.mock_config, self.mock_display)
        
        result = menu.handle_key_down(pygame.K_ESCAPE)
        self.assertEqual(result, MenuState.MAIN_MENU)

    def test_handle_key_down_tab_navigation(self):
        """Test that tab key navigates between controls"""
        menu = OptionsMenu(self.mock_config, self.mock_display)
        
        initial_index = menu.current_control_index
        result = menu.handle_key_down(pygame.K_TAB)
        self.assertIsNone(result)  # Should not return a state change
        self.assertNotEqual(initial_index, menu.current_control_index)

    def test_handle_key_down_arrow_navigation(self):
        """Test that arrow keys navigate between controls"""
        menu = OptionsMenu(self.mock_config, self.mock_display)
        
        initial_index = menu.current_control_index
        result = menu.handle_key_down(pygame.K_DOWN)
        self.assertIsNone(result)
        self.assertNotEqual(initial_index, menu.current_control_index)

    def test_handle_key_down_escape_returns_to_main_menu(self):
        """Test that ESC key returns to main menu (replaces back button functionality)"""
        menu = OptionsMenu(self.mock_config, self.mock_display)
        
        # Test ESC key returns to main menu
        result = menu.handle_key_down(pygame.K_ESCAPE)
        self.assertEqual(result, MenuState.MAIN_MENU)

    def test_apply_settings(self):
        """Test that apply settings saves configuration"""
        menu = OptionsMenu(self.mock_config, self.mock_display)
        
        # Change some values
        menu.master_volume_slider.set_value(0.5)
        menu.fullscreen_toggle.set_value(True)
        
        # Apply settings
        menu.apply_settings()
        
        # Check that config was updated
        self.assertEqual(self.mock_config.master_volume, 0.5)
        self.assertEqual(self.mock_config.fullscreen, True)
        
        # Check that save was called
        self.mock_config.save_settings.assert_called_once()

    def test_cancel_settings(self):
        """Test that cancel restores original settings"""
        menu = OptionsMenu(self.mock_config, self.mock_display)
        
        # Store original values
        original_volume = menu.master_volume_slider.get_value()
        
        # Change values
        menu.master_volume_slider.set_value(0.1)
        self.assertEqual(menu.master_volume_slider.get_value(), 0.1)
        
        # Cancel changes
        menu.cancel_settings()
        
        # Check that values were restored
        self.assertEqual(menu.master_volume_slider.get_value(), original_volume)

    @patch('src.graphics.options_menu.Graphik')
    def test_draw_method(self, mock_graphik_class):
        """Test that draw method works without errors"""
        mock_graphik = MagicMock()
        mock_graphik_class.return_value = mock_graphik
        
        menu = OptionsMenu(self.mock_config, self.mock_display)
        
        # Should not raise an exception
        try:
            menu.draw()
            self.assertTrue(True)
        except Exception as e:
            self.fail(f"draw() raised {e} unexpectedly!")
        
        # Should call fill on display
        menu.game_display.fill.assert_called()
        
        # Should draw text
        self.assertTrue(mock_graphik.drawText.called)


if __name__ == '__main__':
    unittest.main()