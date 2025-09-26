import unittest
from unittest.mock import MagicMock, patch
import os
import pygame
from src.ophidian import Ophidian
from src.state.menu_state import MenuState


class TestOphidianMenuIntegration(unittest.TestCase):
    """Integration tests for Ophidian class with menu system"""

    def setUp(self):
        """Set up test fixtures"""
        # Disable audio to avoid ALSA warnings in tests
        os.environ['SDL_AUDIODRIVER'] = 'dummy'

    def tearDown(self):
        """Clean up after tests"""
        if hasattr(self, 'game') and self.game:
            self.game.running = False
        pygame.quit()

    @patch('pygame.display.set_icon')
    @patch('pygame.image.load')
    def test_ophidian_initialization(self, mock_image_load, mock_set_icon):
        """Test Ophidian class initialization with menu system"""
        # Mock icon loading to avoid file dependencies
        mock_image_load.return_value = MagicMock()
        
        self.game = Ophidian()
        
        # Should start in main menu state
        self.assertEqual(self.game.current_state, MenuState.MAIN_MENU)
        self.assertTrue(self.game.running)
        
        # Menu objects should be initialized
        self.assertIsNotNone(self.game.main_menu)
        self.assertIsNotNone(self.game.options_menu)
        self.assertIsNotNone(self.game.high_scores_menu)
        
        # Game-specific objects should be None initially
        self.assertIsNone(self.game.snake_part_repository)
        self.assertIsNone(self.game.environment_repository)
        self.assertIsNone(self.game.game_score)
        self.assertIsNone(self.game.renderer)

    @patch('pygame.display.set_icon')
    @patch('pygame.image.load')
    def test_state_transitions(self, mock_image_load, mock_set_icon):
        """Test state transitions in Ophidian"""
        mock_image_load.return_value = MagicMock()
        
        self.game = Ophidian()
        
        # Test transition to options
        self.game.change_state(MenuState.OPTIONS)
        self.assertEqual(self.game.current_state, MenuState.OPTIONS)
        
        # Test transition to high scores
        self.game.change_state(MenuState.HIGH_SCORES)
        self.assertEqual(self.game.current_state, MenuState.HIGH_SCORES)
        
        # Test transition back to main menu
        self.game.change_state(MenuState.MAIN_MENU)
        self.assertEqual(self.game.current_state, MenuState.MAIN_MENU)

    @patch('pygame.display.set_icon')
    @patch('pygame.image.load')
    def test_menu_key_handling(self, mock_image_load, mock_set_icon):
        """Test keyboard event handling in menu states"""
        mock_image_load.return_value = MagicMock()
        
        self.game = Ophidian()
        
        # Test main menu key handling
        self.assertEqual(self.game.current_state, MenuState.MAIN_MENU)
        
        # Simulate down arrow key
        self.game.handle_key_down_event_based_on_state(pygame.K_DOWN)
        # Menu selection should change but state should remain MAIN_MENU
        self.assertEqual(self.game.current_state, MenuState.MAIN_MENU)
        self.assertEqual(self.game.main_menu.selected_index, 1)

    @patch('pygame.display.set_icon')
    @patch('pygame.image.load')
    def test_mouse_handling(self, mock_image_load, mock_set_icon):
        """Test mouse event handling in menu states"""
        mock_image_load.return_value = MagicMock()
        
        self.game = Ophidian()
        
        # Test mouse motion in main menu
        self.assertEqual(self.game.current_state, MenuState.MAIN_MENU)
        
        # Simulate mouse motion
        self.game.handle_mouse_motion_based_on_state((250, 285))
        # This should be handled by the main menu (exact behavior depends on menu layout)

    @patch('pygame.display.set_icon')
    @patch('pygame.image.load')
    def test_display_initialization(self, mock_image_load, mock_set_icon):
        """Test display initialization"""
        mock_image_load.return_value = MagicMock()
        
        self.game = Ophidian()
        
        # Display should be initialized
        self.assertIsNotNone(self.game.game_display)
        
        # Config should be loaded
        self.assertIsNotNone(self.game.config)
        self.assertEqual(self.game.config.display_width, 500)
        self.assertEqual(self.game.config.display_height, 500)

    @patch('pygame.display.set_icon')
    @patch('pygame.image.load')
    def test_icon_loading_error_handling(self, mock_image_load, mock_set_icon):
        """Test that icon loading errors are handled gracefully"""
        # Make icon loading fail
        mock_image_load.side_effect = pygame.error("Could not load icon")
        
        # Should not raise an exception
        try:
            self.game = Ophidian()
            self.assertTrue(True)  # Success if no exception raised
        except Exception as e:
            self.fail(f"Icon loading error should be handled gracefully, but got: {e}")

    @patch('pygame.display.set_icon')
    @patch('pygame.image.load')
    def test_game_state_repository_integration(self, mock_image_load, mock_set_icon):
        """Test game state repository integration"""
        mock_image_load.return_value = MagicMock()
        
        self.game = Ophidian()
        
        # State repository should be initialized
        self.assertIsNotNone(self.game.state_repository)
        
        # Should be able to save/load state (even if None)
        try:
            self.game.save_game_state()
            # Should not raise exception even with None game_score
        except Exception as e:
            self.fail(f"save_game_state should handle None game_score gracefully: {e}")


if __name__ == '__main__':
    unittest.main()