import unittest
from src.state.menu_state import MenuState


class TestMenuState(unittest.TestCase):
    """Test the MenuState enum"""

    def test_menu_state_values(self):
        """Test that MenuState enum has correct values"""
        self.assertEqual(MenuState.MAIN_MENU.value, "main_menu")
        self.assertEqual(MenuState.OPTIONS.value, "options")
        self.assertEqual(MenuState.HIGH_SCORES.value, "high_scores")
        self.assertEqual(MenuState.GAME.value, "game")
        self.assertEqual(MenuState.EXIT.value, "exit")

    def test_menu_state_members(self):
        """Test that all expected MenuState members exist"""
        expected_states = {
            MenuState.MAIN_MENU,
            MenuState.OPTIONS,
            MenuState.HIGH_SCORES,
            MenuState.GAME,
            MenuState.EXIT,
        }
        actual_states = set(MenuState)
        self.assertEqual(actual_states, expected_states)

    def test_menu_state_equality(self):
        """Test MenuState equality comparisons"""
        self.assertEqual(MenuState.MAIN_MENU, MenuState.MAIN_MENU)
        self.assertNotEqual(MenuState.MAIN_MENU, MenuState.GAME)


if __name__ == "__main__":
    unittest.main()
