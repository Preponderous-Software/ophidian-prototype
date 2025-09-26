import pygame
from src.lib.graphik.src.graphik import Graphik
from src.state.menu_state import MenuState


class OptionsMenu:
    def __init__(self, config, game_display):
        self.config = config
        self.game_display = game_display
        self.graphik = Graphik(game_display)

    def handle_key_down(self, key):
        """Handle keyboard input - return to main menu on escape or enter"""
        if key == pygame.K_ESCAPE or key == pygame.K_RETURN:
            return MenuState.MAIN_MENU
        return None

    def handle_mouse_click(self, pos):
        """Handle mouse clicks - return to main menu"""
        return MenuState.MAIN_MENU

    def draw(self):
        """Draw the options menu"""
        # Get current window size for dynamic rendering
        try:
            current_width, current_height = self.game_display.get_size()
        except (AttributeError, ValueError):
            # Fallback to config values for testing
            current_width, current_height = self.config.display_width, self.config.display_height
        
        # Clear screen with black background
        self.game_display.fill(self.config.black)
        
        # Draw title
        self.graphik.drawText(
            "OPTIONS",
            current_width // 2,
            current_height // 2 - 100,
            self.config.text_size,
            self.config.green
        )
        
        # Draw placeholder text
        self.graphik.drawText(
            "Options menu coming soon...",
            current_width // 2,
            current_height // 2,
            self.config.text_size // 2,
            self.config.white
        )
        
        # Draw instructions
        self.graphik.drawText(
            "Press ESC or ENTER to return to main menu",
            current_width // 2,
            current_height // 2 + 100,
            self.config.text_size // 3,
            self.config.yellow
        )