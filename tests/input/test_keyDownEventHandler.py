import unittest
from unittest.mock import MagicMock

import pygame
from src.input.keyDownEventHandler import KeyDownEventHandler


class TestKeyDownEventHandler(unittest.TestCase):
    def setUp(self):
        self.config = MagicMock()
        self.game_display = MagicMock()
        self.selected_snake_part = MagicMock()
        self.handler = KeyDownEventHandler(self.config, self.game_display, self.selected_snake_part)

    def test_handle_key_down_event_quit(self):
        result = self.handler.handle_key_down_event(pygame.K_q)
        self.assertEqual(result, "quit")

    def test_handle_key_down_event_up(self):
        self.selected_snake_part.getDirection.return_value = 1
        self.handler.changed_direction_this_tick = False
        result = self.handler.handle_key_down_event(pygame.K_w)
        self.selected_snake_part.setDirection.assert_called_once_with(0)
        self.assertIsNone(result)

    def test_handle_key_down_event_left(self):
        self.selected_snake_part.getDirection.return_value = 0
        self.handler.changed_direction_this_tick = False
        result = self.handler.handle_key_down_event(pygame.K_a)
        self.selected_snake_part.setDirection.assert_called_once_with(1)
        self.assertIsNone(result)

    def test_handle_key_down_event_down(self):
        self.selected_snake_part.getDirection.return_value = 3
        self.handler.changed_direction_this_tick = False
        result = self.handler.handle_key_down_event(pygame.K_s)
        self.selected_snake_part.setDirection.assert_called_once_with(2)
        self.assertIsNone(result)

    def test_handle_key_down_event_right(self):
        self.selected_snake_part.getDirection.return_value = 2
        self.handler.changed_direction_this_tick = False
        result = self.handler.handle_key_down_event(pygame.K_d)
        self.selected_snake_part.setDirection.assert_called_once_with(3)
        self.assertIsNone(result)

    def test_handle_key_down_event_fullscreen_toggle(self):
        self.config.fullscreen = True
        result = self.handler.handle_key_down_event(pygame.K_F11)
        self.assertFalse(self.config.fullscreen)
        self.assertEqual(result, "initialize game display")

    def test_handle_key_down_event_limit_tick_speed_toggle(self):
        self.config.limit_tick_speed = False
        result = self.handler.handle_key_down_event(pygame.K_l)
        self.assertTrue(self.config.limit_tick_speed)
        self.assertIsNone(result)

    def test_handle_key_down_event_restart(self):
        result = self.handler.handle_key_down_event(pygame.K_r)
        self.assertEqual(result, "restart")

    def test_handle_key_down_event_unknown(self):
        result = self.handler.handle_key_down_event(pygame.K_x)
        self.assertEqual(result, "unknown")


if __name__ == '__main__':
    unittest.main()
