import unittest
from unittest.mock import MagicMock, patch
import os
import pygame
from src.graphics.main_menu import MainMenu, MenuItem
from src.state.menu_state import MenuState


class TestMenuItem(unittest.TestCase):
    """Test the MenuItem class"""

    def setUp(self):
        """Set up test fixtures"""
        # Disable audio to avoid ALSA warnings in tests
        os.environ["SDL_AUDIODRIVER"] = "dummy"

    def test_menu_item_creation(self):
        """Test MenuItem initialization"""
        item = MenuItem("Test Item", MenuState.GAME)
        self.assertEqual(item.text, "Test Item")
        self.assertEqual(item.action, MenuState.GAME)
        self.assertEqual(item.width, 200)
        self.assertEqual(item.height, 50)
        self.assertFalse(item.is_highlighted)

    def test_menu_item_custom_size(self):
        """Test MenuItem with custom width and height"""
        item = MenuItem("Custom Item", MenuState.OPTIONS, width=300, height=60)
        self.assertEqual(item.width, 300)
        self.assertEqual(item.height, 60)

    def test_menu_item_highlighting(self):
        """Test MenuItem highlighting functionality"""
        item = MenuItem("Test Item", MenuState.GAME)
        self.assertFalse(item.is_highlighted)

        item.set_highlighted(True)
        self.assertTrue(item.is_highlighted)

        item.set_highlighted(False)
        self.assertFalse(item.is_highlighted)


class TestMainMenu(unittest.TestCase):
    """Test the MainMenu class"""

    def setUp(self):
        """Set up test fixtures"""
        # Disable audio to avoid ALSA warnings in tests
        os.environ["SDL_AUDIODRIVER"] = "dummy"
        pygame.init()

        # Mock config and display
        self.mock_config = MagicMock()
        self.mock_config.display_width = 500
        self.mock_config.display_height = 500
        self.mock_config.black = (0, 0, 0)
        self.mock_config.white = (255, 255, 255)
        self.mock_config.green = (0, 255, 0)
        self.mock_config.text_size = 50

        self.mock_display = MagicMock()

    def tearDown(self):
        """Clean up after tests"""
        pygame.quit()

    def test_main_menu_initialization(self):
        """Test MainMenu initialization"""
        menu = MainMenu(self.mock_config, self.mock_display)

        self.assertEqual(menu.current_state, MenuState.MAIN_MENU)
        self.assertEqual(menu.selected_index, 0)
        self.assertEqual(len(menu.menu_items), 4)

        # Check menu items
        expected_items = [
            ("Play Game", MenuState.GAME),
            ("Options", MenuState.OPTIONS),
            ("High Scores", MenuState.HIGH_SCORES),
            ("Exit", MenuState.EXIT),
        ]

        for i, (text, action) in enumerate(expected_items):
            self.assertEqual(menu.menu_items[i].text, text)
            self.assertEqual(menu.menu_items[i].action, action)

    def test_initial_selection(self):
        """Test that first item is initially selected"""
        menu = MainMenu(self.mock_config, self.mock_display)

        # First item should be highlighted
        self.assertTrue(menu.menu_items[0].is_highlighted)
        for i in range(1, len(menu.menu_items)):
            self.assertFalse(menu.menu_items[i].is_highlighted)

    def test_keyboard_navigation_down(self):
        """Test keyboard navigation down"""
        menu = MainMenu(self.mock_config, self.mock_display)

        # Initially on first item (index 0)
        self.assertEqual(menu.selected_index, 0)

        # Press down key
        result = menu.handle_key_down(pygame.K_DOWN)
        self.assertIsNone(result)  # Should not return action, just navigate
        self.assertEqual(menu.selected_index, 1)

        # Test with 's' key
        result = menu.handle_key_down(pygame.K_s)
        self.assertIsNone(result)
        self.assertEqual(menu.selected_index, 2)

    def test_keyboard_navigation_up(self):
        """Test keyboard navigation up"""
        menu = MainMenu(self.mock_config, self.mock_display)

        # Start at first item, go up should wrap to last item
        result = menu.handle_key_down(pygame.K_UP)
        self.assertIsNone(result)
        self.assertEqual(menu.selected_index, 3)  # Should wrap to last item

        # Test with 'w' key
        result = menu.handle_key_down(pygame.K_w)
        self.assertIsNone(result)
        self.assertEqual(menu.selected_index, 2)

    def test_keyboard_navigation_wrapping(self):
        """Test that navigation wraps around correctly"""
        menu = MainMenu(self.mock_config, self.mock_display)

        # Go to last item
        menu.selected_index = 3
        menu.update_selection()

        # Press down should wrap to first item
        menu.handle_key_down(pygame.K_DOWN)
        self.assertEqual(menu.selected_index, 0)

    def test_keyboard_selection_enter(self):
        """Test selecting items with Enter key"""
        menu = MainMenu(self.mock_config, self.mock_display)

        # Select first item (Play Game)
        result = menu.handle_key_down(pygame.K_RETURN)
        self.assertEqual(result, MenuState.GAME)

        # Move to second item and select
        menu.handle_key_down(pygame.K_DOWN)
        result = menu.handle_key_down(pygame.K_RETURN)
        self.assertEqual(result, MenuState.OPTIONS)

    def test_keyboard_selection_space(self):
        """Test selecting items with Space key"""
        menu = MainMenu(self.mock_config, self.mock_display)

        # Select first item with space
        result = menu.handle_key_down(pygame.K_SPACE)
        self.assertEqual(result, MenuState.GAME)

    def test_keyboard_escape(self):
        """Test Escape key returns EXIT"""
        menu = MainMenu(self.mock_config, self.mock_display)

        result = menu.handle_key_down(pygame.K_ESCAPE)
        self.assertEqual(result, MenuState.EXIT)

    def test_update_selection(self):
        """Test that update_selection correctly highlights items"""
        menu = MainMenu(self.mock_config, self.mock_display)

        # Set selection to item 2
        menu.selected_index = 2
        menu.update_selection()

        # Only item 2 should be highlighted
        for i, item in enumerate(menu.menu_items):
            if i == 2:
                self.assertTrue(item.is_highlighted)
            else:
                self.assertFalse(item.is_highlighted)

    def test_mouse_motion_detection(self):
        """Test mouse motion detection over menu items"""
        menu = MainMenu(self.mock_config, self.mock_display)

        # Calculate position over second menu item (Options)
        # Menu starts at display_height // 2 - 50 = 200
        # Second item is at y = 200 + 1 * 80 = 280
        # Item width is 200, centered at display_width // 2 = 250
        # So item spans from x=150 to x=350
        x = 250  # Center of item
        y = 285  # Within item bounds

        menu.handle_mouse_motion((x, y))
        self.assertEqual(menu.selected_index, 1)  # Should select second item

    def test_mouse_click_selection(self):
        """Test mouse click selection"""
        menu = MainMenu(self.mock_config, self.mock_display)

        # Click on third menu item (High Scores)
        # Third item is at y = 200 + 2 * 80 = 360
        x = 250  # Center of item
        y = 365  # Within item bounds

        result = menu.handle_mouse_click((x, y))
        self.assertEqual(result, MenuState.HIGH_SCORES)

    def test_mouse_click_outside(self):
        """Test mouse click outside menu items returns None"""
        menu = MainMenu(self.mock_config, self.mock_display)

        # Click outside menu area
        result = menu.handle_mouse_click((50, 50))
        self.assertIsNone(result)

    @patch("pygame.display.update")
    def test_draw_method_calls(self, mock_update):
        """Test that draw method makes expected calls"""
        menu = MainMenu(self.mock_config, self.mock_display)

        # Mock the graphik methods
        menu.graphik.drawText = MagicMock()
        menu.graphik.drawRectangle = MagicMock()

        menu.draw()

        # Should call fill on display
        menu.game_display.fill.assert_called_with(self.mock_config.black)

        # Should draw title and subtitle
        self.assertTrue(menu.graphik.drawText.called)

        # Check that title is drawn
        title_calls = [
            call
            for call in menu.graphik.drawText.call_args_list
            if len(call[0]) > 0 and call[0][0] == "OPHIDIAN"
        ]
        self.assertTrue(len(title_calls) > 0)


if __name__ == "__main__":
    unittest.main()
