import pygame
from src.lib.graphik.src.graphik import Graphik
from src.state.menu_state import MenuState


class MenuItem:
    def __init__(self, text, action, width=200, height=50):
        self.text = text
        self.action = action
        self.width = width
        self.height = height
        self.is_highlighted = False

    def set_highlighted(self, highlighted):
        self.is_highlighted = highlighted


class MainMenu:
    def __init__(self, config, game_display):
        self.config = config
        self.game_display = game_display
        self.graphik = Graphik(game_display)
        self.current_state = MenuState.MAIN_MENU
        self.selected_index = 0

        # Menu items
        self.menu_items = [
            MenuItem("Play Game", MenuState.GAME),
            MenuItem("Options", MenuState.OPTIONS),
            MenuItem("High Scores", MenuState.HIGH_SCORES),
            MenuItem("Exit", MenuState.EXIT),
        ]

        # Update selection
        self.update_selection()

    def update_selection(self):
        """Update which menu item is highlighted"""
        for i, item in enumerate(self.menu_items):
            item.set_highlighted(i == self.selected_index)

    def handle_key_down(self, key):
        """Handle keyboard input for menu navigation"""
        if key == pygame.K_UP or key == pygame.K_w:
            self.selected_index = (self.selected_index - 1) % len(self.menu_items)
            self.update_selection()
        elif key == pygame.K_DOWN or key == pygame.K_s:
            self.selected_index = (self.selected_index + 1) % len(self.menu_items)
            self.update_selection()
        elif key == pygame.K_RETURN or key == pygame.K_SPACE:
            return self.menu_items[self.selected_index].action
        elif key == pygame.K_ESCAPE:
            return MenuState.EXIT

        return None

    def handle_mouse_motion(self, pos):
        """Handle mouse movement for menu highlighting"""
        x, y = pos
        try:
            current_width, current_height = self.game_display.get_size()
        except (AttributeError, ValueError):
            # Fallback to config values for testing
            current_width, current_height = (
                self.config.display_width,
                self.config.display_height,
            )

        menu_start_y = current_height // 2 - 50

        for i, item in enumerate(self.menu_items):
            item_y = menu_start_y + i * 80
            if (
                current_width // 2 - item.width // 2
                <= x
                <= current_width // 2 + item.width // 2
                and item_y <= y <= item_y + item.height
            ):
                if self.selected_index != i:
                    self.selected_index = i
                    self.update_selection()
                break

    def handle_mouse_click(self, pos):
        """Handle mouse clicks on menu items"""
        x, y = pos
        try:
            current_width, current_height = self.game_display.get_size()
        except (AttributeError, ValueError):
            # Fallback to config values for testing
            current_width, current_height = (
                self.config.display_width,
                self.config.display_height,
            )

        menu_start_y = current_height // 2 - 50

        for i, item in enumerate(self.menu_items):
            item_y = menu_start_y + i * 80
            if (
                current_width // 2 - item.width // 2
                <= x
                <= current_width // 2 + item.width // 2
                and item_y <= y <= item_y + item.height
            ):
                return item.action

        return None

    def draw(self):
        """Draw the main menu"""
        # Get current window size for dynamic rendering
        try:
            current_width, current_height = self.game_display.get_size()
        except (AttributeError, ValueError):
            # Fallback to config values for testing
            current_width, current_height = (
                self.config.display_width,
                self.config.display_height,
            )

        # Clear screen with black background
        self.game_display.fill(self.config.black)

        # Draw title
        title_y = current_height // 2 - 150
        self.graphik.drawText(
            "OPHIDIAN",
            current_width // 2,
            title_y,
            self.config.text_size + 20,
            self.config.green,
        )

        # Draw subtitle
        subtitle_y = title_y + 80
        self.graphik.drawText(
            "Snake Game",
            current_width // 2,
            subtitle_y,
            self.config.text_size // 2,
            self.config.white,
        )

        # Draw menu items
        menu_start_y = current_height // 2 - 50

        for i, item in enumerate(self.menu_items):
            item_x = current_width // 2 - item.width // 2
            item_y = menu_start_y + i * 80

            # Choose colors based on selection
            if item.is_highlighted:
                bg_color = self.config.green
                text_color = self.config.black
            else:
                bg_color = self.config.black
                text_color = self.config.white

            # Draw background rectangle for highlighted items
            if item.is_highlighted:
                self.graphik.drawRectangle(
                    item_x, item_y, item.width, item.height, bg_color
                )

            # Draw text
            self.graphik.drawText(
                item.text,
                current_width // 2,
                item_y + item.height // 2,
                self.config.text_size // 2,
                text_color,
            )

    def get_current_state(self):
        return self.current_state

    def set_current_state(self, state):
        self.current_state = state
