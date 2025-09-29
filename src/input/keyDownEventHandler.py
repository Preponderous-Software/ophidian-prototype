import pygame


class KeyDownEventHandler:

    def __init__(self, config, game_display, selected_snake_part):
        self.config = config
        self.game_display = game_display
        self.selected_snake_part = selected_snake_part
        self.running = True
        self.changed_direction_this_tick = False

    def handle_key_down_event(self, key):
        # Use configurable key bindings
        if key == self.config.key_bindings.get("quit", pygame.K_q):
            return "quit"
        elif (
            key == self.config.key_bindings.get("move_up", pygame.K_w)
            or key == pygame.K_UP
        ):
            if (
                self.changed_direction_this_tick == False
                and self.selected_snake_part.getDirection() != 2
            ):
                self.selected_snake_part.setDirection(0)
                self.changed_direction_this_tick = True
                return None
            return None
        elif (
            key == self.config.key_bindings.get("move_left", pygame.K_a)
            or key == pygame.K_LEFT
        ):
            if (
                self.changed_direction_this_tick == False
                and self.selected_snake_part.getDirection() != 3
            ):
                self.selected_snake_part.setDirection(1)
                self.changed_direction_this_tick = True
                return None
            return None
        elif (
            key == self.config.key_bindings.get("move_down", pygame.K_s)
            or key == pygame.K_DOWN
        ):
            if (
                self.changed_direction_this_tick == False
                and self.selected_snake_part.getDirection() != 0
            ):
                self.selected_snake_part.setDirection(2)
                self.changed_direction_this_tick = True
                return None
            return None
        elif (
            key == self.config.key_bindings.get("move_right", pygame.K_d)
            or key == pygame.K_RIGHT
        ):
            if (
                self.changed_direction_this_tick == False
                and self.selected_snake_part.getDirection() != 1
            ):
                self.selected_snake_part.setDirection(3)
                self.changed_direction_this_tick = True
                return None
            return None
        elif key == self.config.key_bindings.get("fullscreen", pygame.K_F11):
            if self.config.fullscreen:
                self.config.fullscreen = False
            else:
                self.config.fullscreen = True
            return "initialize game display"
        elif key == pygame.K_l:  # Keep this as backup for tick speed toggle
            if self.config.limit_tick_speed:
                self.config.limit_tick_speed = False
                return None
            else:
                self.config.limit_tick_speed = True
                return None
        elif key == self.config.key_bindings.get("restart", pygame.K_r):
            return "restart"
        else:
            return "unknown"
