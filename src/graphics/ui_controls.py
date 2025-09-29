import pygame


class UIControl:
    """Base class for UI controls"""

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = pygame.Rect(x, y, width, height)
        self.focused = False

    def handle_mouse_click(self, pos):
        """Handle mouse click, return True if click was handled"""
        return self.rect.collidepoint(pos)

    def handle_key_down(self, key):
        """Handle keyboard input, return True if key was handled"""
        return False

    def draw(self, surface, graphik, config):
        """Draw the control"""


class Slider(UIControl):
    """Slider control for numeric values"""

    def __init__(
        self, x, y, width, height, min_value, max_value, initial_value, label=""
    ):
        super().__init__(x, y, width, height)
        self.min_value = min_value
        self.max_value = max_value
        self.value = initial_value
        self.label = label
        self.dragging = False
        self.handle_width = 10

    def get_value(self):
        return self.value

    def set_value(self, value):
        self.value = max(self.min_value, min(self.max_value, value))

    def handle_mouse_click(self, pos):
        if self.rect.collidepoint(pos):
            self.dragging = True
            self._update_value_from_position(pos[0])
            return True
        return False

    def handle_mouse_motion(self, pos):
        if self.dragging:
            self._update_value_from_position(pos[0])

    def handle_mouse_release(self):
        self.dragging = False

    def _update_value_from_position(self, x):
        # Calculate value based on position
        relative_x = max(0, min(self.width, x - self.x))
        ratio = relative_x / self.width
        self.value = self.min_value + ratio * (self.max_value - self.min_value)

    def handle_key_down(self, key):
        if not self.focused:
            return False

        if key == pygame.K_LEFT or key == pygame.K_a:
            self.set_value(self.value - 0.1)
            return True
        elif key == pygame.K_RIGHT or key == pygame.K_d:
            self.set_value(self.value + 0.1)
            return True
        return False

    def draw(self, surface, graphik, config):
        # Draw label
        if self.label:
            graphik.drawText(
                self.label,
                self.x - 10,
                self.y - 20,
                config.text_size // 3,
                config.white,
            )

        # Draw slider track
        track_color = config.white if self.focused else config.gray
        graphik.drawRectangle(
            self.x, self.y + self.height // 2 - 2, self.width, 4, track_color
        )

        # Draw slider handle
        handle_x = (
            self.x
            + int(
                (self.value - self.min_value)
                / (self.max_value - self.min_value)
                * self.width
            )
            - self.handle_width // 2
        )
        handle_color = config.green if self.focused else config.white
        graphik.drawRectangle(
            handle_x, self.y, self.handle_width, self.height, handle_color
        )

        # Draw value text
        value_text = f"{self.value:.1f}"
        graphik.drawText(
            value_text,
            self.x + self.width + 20,
            self.y + self.height // 2,
            config.text_size // 3,
            config.white,
        )


class Toggle(UIControl):
    """Toggle control for boolean values"""

    def __init__(self, x, y, width, height, initial_value, label=""):
        super().__init__(x, y, width, height)
        self.value = initial_value
        self.label = label

    def get_value(self):
        return self.value

    def set_value(self, value):
        self.value = bool(value)

    def handle_mouse_click(self, pos):
        if self.rect.collidepoint(pos):
            self.value = not self.value
            return True
        return False

    def handle_key_down(self, key):
        if not self.focused:
            return False

        if key == pygame.K_SPACE or key == pygame.K_RETURN:
            self.value = not self.value
            return True
        return False

    def draw(self, surface, graphik, config):
        # Draw label
        if self.label:
            graphik.drawText(
                self.label,
                self.x - 10,
                self.y - 20,
                config.text_size // 3,
                config.white,
            )

        # Draw toggle background
        bg_color = config.green if self.value else config.gray
        border_color = config.white if self.focused else config.gray

        # Draw border first
        graphik.drawRectangle(
            self.x - 2, self.y - 2, self.width + 4, self.height + 4, border_color
        )
        graphik.drawRectangle(self.x, self.y, self.width, self.height, bg_color)

        # Draw toggle indicator
        indicator_text = "ON" if self.value else "OFF"
        text_color = config.white if self.value else config.black
        graphik.drawText(
            indicator_text,
            self.x + self.width // 2,
            self.y + self.height // 2,
            config.text_size // 3,
            text_color,
        )


class Dropdown(UIControl):
    """Dropdown control for selecting from multiple options"""

    def __init__(self, x, y, width, height, options, initial_index=0, label=""):
        super().__init__(x, y, width, height)
        self.options = options
        self.selected_index = initial_index
        self.label = label

    def get_value(self):
        return self.options[self.selected_index] if self.options else ""

    def get_selected_index(self):
        return self.selected_index

    def set_selected_index(self, index):
        if 0 <= index < len(self.options):
            self.selected_index = index

    def handle_key_down(self, key):
        if not self.focused:
            return False

        if key == pygame.K_LEFT or key == pygame.K_UP:
            self.selected_index = (self.selected_index - 1) % len(self.options)
            return True
        elif key == pygame.K_RIGHT or key == pygame.K_DOWN:
            self.selected_index = (self.selected_index + 1) % len(self.options)
            return True
        return False

    def draw(self, surface, graphik, config):
        # Draw label
        if self.label:
            graphik.drawText(
                self.label,
                self.x - 10,
                self.y - 20,
                config.text_size // 3,
                config.white,
            )

        # Draw dropdown background
        bg_color = config.black
        border_color = config.white if self.focused else config.gray

        # Draw border
        graphik.drawRectangle(
            self.x - 2, self.y - 2, self.width + 4, self.height + 4, border_color
        )
        graphik.drawRectangle(self.x, self.y, self.width, self.height, bg_color)

        # Draw current selection
        current_text = self.get_value()
        text_color = config.white
        graphik.drawText(
            current_text,
            self.x + self.width // 2,
            self.y + self.height // 2,
            config.text_size // 3,
            text_color,
        )

        # Draw arrows to indicate it's a dropdown
        graphik.drawText(
            "< >",
            self.x + self.width - 20,
            self.y + self.height // 2,
            config.text_size // 4,
            config.gray,
        )


class Button(UIControl):
    """Button control with enhanced visual feedback"""

    def __init__(self, x, y, width, height, text, callback=None):
        super().__init__(x, y, width, height)
        self.text = text
        self.callback = callback
        self.pressed = False
        self.hovered = False
        self.click_time = 0

    def handle_mouse_click(self, pos):
        if self.rect.collidepoint(pos):
            self.pressed = True
            self.click_time = pygame.time.get_ticks()
            if self.callback:
                result = self.callback()
                return result if result is not None else True
            return True
        return False

    def handle_mouse_motion(self, pos):
        """Handle mouse hover for visual feedback"""
        was_hovered = self.hovered
        self.hovered = self.rect.collidepoint(pos)
        return was_hovered != self.hovered

    def handle_key_down(self, key):
        if not self.focused:
            return False

        if key == pygame.K_SPACE or key == pygame.K_RETURN:
            self.pressed = True
            self.click_time = pygame.time.get_ticks()
            if self.callback:
                result = self.callback()
                return result if result is not None else True
            return True
        return False

    def draw(self, surface, graphik, config):
        # Calculate visual state
        current_time = pygame.time.get_ticks()
        if self.pressed and current_time - self.click_time < 150:  # 150ms press effect
            # Pressed state - darker background
            if self.focused:
                bg_color = config.green
                text_color = config.white
            else:
                bg_color = config.gray
                text_color = config.white
        elif self.focused:
            # Focused state - bright background
            bg_color = config.green
            text_color = config.black
        elif self.hovered:
            # Hovered state - light highlight
            bg_color = config.white
            text_color = config.black
        else:
            # Normal state
            bg_color = config.white
            text_color = config.black

        # Draw button with border for better visibility
        border_color = config.green if self.focused else config.gray

        # Draw border
        graphik.drawRectangle(
            self.x - 1, self.y - 1, self.width + 2, self.height + 2, border_color
        )
        # Draw background
        graphik.drawRectangle(self.x, self.y, self.width, self.height, bg_color)

        # Draw button text
        text_size = max(12, min(24, config.text_size // 2))
        graphik.drawText(
            self.text,
            self.x + self.width // 2,
            self.y + self.height // 2,
            text_size,
            text_color,
        )

        # Reset pressed state after animation
        if self.pressed and current_time - self.click_time > 150:
            self.pressed = False
