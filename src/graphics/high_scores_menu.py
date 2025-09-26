import pygame
from src.lib.graphik.src.graphik import Graphik
from src.state.menu_state import MenuState


class HighScoresMenu:
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
        """Draw the high scores menu"""
        # Clear screen with black background
        self.game_display.fill(self.config.black)
        
        # Draw title
        self.graphik.drawText(
            "HIGH SCORES",
            self.config.display_width // 2,
            self.config.display_height // 2 - 100,
            self.config.text_size,
            self.config.green
        )
        
        # Draw placeholder text
        self.graphik.drawText(
            "High scores coming soon...",
            self.config.display_width // 2,
            self.config.display_height // 2,
            self.config.text_size // 2,
            self.config.white
        )
        
        # Draw instructions
        self.graphik.drawText(
            "Press ESC or ENTER to return to main menu",
            self.config.display_width // 2,
            self.config.display_height // 2 + 100,
            self.config.text_size // 3,
            self.config.yellow
        )