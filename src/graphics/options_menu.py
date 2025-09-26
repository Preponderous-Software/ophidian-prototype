import pygame
from src.lib.graphik.src.graphik import Graphik
from src.state.menu_state import MenuState
from src.graphics.ui_controls import Slider, Toggle, Dropdown, Button


class OptionsMenu:
    def __init__(self, config, game_display):
        self.config = config
        self.game_display = game_display
        self.graphik = Graphik(game_display)
        
        # Track original config values for cancel functionality
        self.original_settings = {}
        
        # UI controls
        self.controls = []
        self.current_control_index = 0
        
        # Flags
        self.settings_changed = False
        
        self.initialize_controls()
    
    def initialize_controls(self):
        """Initialize all UI controls for the options menu"""
        self.controls = []
        
        # Get current window size
        try:
            current_width, current_height = self.game_display.get_size()
        except (AttributeError, ValueError):
            current_width, current_height = self.config.display_width, self.config.display_height
        
        control_width = 200
        control_height = 30
        start_y = current_height // 2 - 150
        control_spacing = 60
        left_column_x = current_width // 2 - 250
        right_column_x = current_width // 2 + 50
        
        # Sound Settings
        self.master_volume_slider = Slider(
            left_column_x, start_y, control_width, control_height,
            0.0, 1.0, self.config.master_volume, "Master Volume"
        )
        self.controls.append(self.master_volume_slider)
        
        self.music_volume_slider = Slider(
            left_column_x, start_y + control_spacing, control_width, control_height,
            0.0, 1.0, self.config.music_volume, "Music Volume"
        )
        self.controls.append(self.music_volume_slider)
        
        self.sfx_volume_slider = Slider(
            left_column_x, start_y + control_spacing * 2, control_width, control_height,
            0.0, 1.0, self.config.sfx_volume, "SFX Volume"
        )
        self.controls.append(self.sfx_volume_slider)
        
        # Display Settings
        self.fullscreen_toggle = Toggle(
            right_column_x, start_y, 80, control_height,
            self.config.fullscreen, "Fullscreen"
        )
        self.controls.append(self.fullscreen_toggle)
        
        resolutions = self.config.get_available_resolutions()
        current_res = (self.config.display_width, self.config.display_height)
        try:
            res_index = resolutions.index(current_res)
        except ValueError:
            res_index = 0
        
        res_options = [f"{w}x{h}" for w, h in resolutions]
        self.resolution_dropdown = Dropdown(
            right_column_x, start_y + control_spacing, control_width, control_height,
            res_options, res_index, "Resolution"
        )
        self.controls.append(self.resolution_dropdown)
        
        # Controls Settings
        self.limit_tick_speed_toggle = Toggle(
            left_column_x, start_y + control_spacing * 3, 80, control_height,
            self.config.limit_tick_speed, "Limit Tick Speed"
        )
        self.controls.append(self.limit_tick_speed_toggle)
        
        # Difficulty Settings
        difficulties = self.config.get_difficulty_levels()
        diff_index = difficulties.index(self.config.difficulty) if self.config.difficulty in difficulties else 1
        self.difficulty_dropdown = Dropdown(
            right_column_x, start_y + control_spacing * 2, control_width, control_height,
            difficulties, diff_index, "Difficulty"
        )
        self.controls.append(self.difficulty_dropdown)
        
        # Buttons
        button_y = start_y + control_spacing * 5
        self.apply_button = Button(
            current_width // 2 - 100, button_y, 80, 40,
            "Apply", self.apply_settings
        )
        self.controls.append(self.apply_button)
        
        self.cancel_button = Button(
            current_width // 2 - 10, button_y, 80, 40,
            "Cancel", self.cancel_settings
        )
        self.controls.append(self.cancel_button)
        
        self.back_button = Button(
            current_width // 2 + 80, button_y, 80, 40,
            "Back", self.go_back
        )
        self.controls.append(self.back_button)
        
        # Set initial focus
        if self.controls:
            self.controls[0].focused = True
        
        # Store original settings for cancel functionality
        self.store_original_settings()
    
    def store_original_settings(self):
        """Store original settings to allow canceling changes"""
        self.original_settings = {
            'master_volume': self.config.master_volume,
            'music_volume': self.config.music_volume,
            'sfx_volume': self.config.sfx_volume,
            'fullscreen': self.config.fullscreen,
            'display_width': self.config.display_width,
            'display_height': self.config.display_height,
            'limit_tick_speed': self.config.limit_tick_speed,
            'difficulty': self.config.difficulty
        }
    
    def apply_settings(self):
        """Apply current settings to config and save"""
        self.config.master_volume = self.master_volume_slider.get_value()
        self.config.music_volume = self.music_volume_slider.get_value()
        self.config.sfx_volume = self.sfx_volume_slider.get_value()
        self.config.fullscreen = self.fullscreen_toggle.get_value()
        self.config.limit_tick_speed = self.limit_tick_speed_toggle.get_value()
        self.config.difficulty = self.difficulty_dropdown.get_value()
        
        # Handle resolution change
        resolutions = self.config.get_available_resolutions()
        selected_res = resolutions[self.resolution_dropdown.get_selected_index()]
        self.config.display_width, self.config.display_height = selected_res
        
        # Save settings to file
        self.config.save_settings()
        
        self.settings_changed = False
        self.store_original_settings()  # Update original settings after apply
    
    def cancel_settings(self):
        """Cancel changes and restore original settings"""
        # Restore original settings
        for key, value in self.original_settings.items():
            setattr(self.config, key, value)
        
        # Update UI controls to reflect restored settings
        self.master_volume_slider.set_value(self.config.master_volume)
        self.music_volume_slider.set_value(self.config.music_volume)
        self.sfx_volume_slider.set_value(self.config.sfx_volume)
        self.fullscreen_toggle.set_value(self.config.fullscreen)
        self.limit_tick_speed_toggle.set_value(self.config.limit_tick_speed)
        
        # Update dropdown selections
        difficulties = self.config.get_difficulty_levels()
        diff_index = difficulties.index(self.config.difficulty) if self.config.difficulty in difficulties else 1
        self.difficulty_dropdown.set_selected_index(diff_index)
        
        resolutions = self.config.get_available_resolutions()
        current_res = (self.config.display_width, self.config.display_height)
        try:
            res_index = resolutions.index(current_res)
        except ValueError:
            res_index = 0
        self.resolution_dropdown.set_selected_index(res_index)
        
        self.settings_changed = False
    
    def go_back(self):
        """Go back to main menu"""
        return MenuState.MAIN_MENU

    def handle_key_down(self, key):
        """Handle keyboard input for options menu navigation"""
        if key == pygame.K_ESCAPE:
            return MenuState.MAIN_MENU
        elif key == pygame.K_TAB:
            # Move to next control
            if self.controls:
                self.controls[self.current_control_index].focused = False
                self.current_control_index = (self.current_control_index + 1) % len(self.controls)
                self.controls[self.current_control_index].focused = True
        elif key == pygame.K_UP:
            # Move to previous control
            if self.controls:
                self.controls[self.current_control_index].focused = False
                self.current_control_index = (self.current_control_index - 1) % len(self.controls)
                self.controls[self.current_control_index].focused = True
        elif key == pygame.K_DOWN:
            # Move to next control
            if self.controls:
                self.controls[self.current_control_index].focused = False
                self.current_control_index = (self.current_control_index + 1) % len(self.controls)
                self.controls[self.current_control_index].focused = True
        else:
            # Let the focused control handle the key
            if self.controls and self.current_control_index < len(self.controls):
                handled = self.controls[self.current_control_index].handle_key_down(key)
                if handled:
                    self.settings_changed = True
        
        return None

    def handle_mouse_click(self, pos):
        """Handle mouse clicks on controls"""
        for i, control in enumerate(self.controls):
            if control.handle_mouse_click(pos):
                # Update focus to clicked control
                if self.controls:
                    self.controls[self.current_control_index].focused = False
                self.current_control_index = i
                control.focused = True
                self.settings_changed = True
                
                # Handle button clicks that return a state
                if control == self.back_button:
                    return MenuState.MAIN_MENU
                break
        
        return None
    
    def handle_mouse_motion(self, pos):
        """Handle mouse motion for sliders"""
        for control in self.controls:
            if hasattr(control, 'handle_mouse_motion'):
                control.handle_mouse_motion(pos)
    
    def handle_mouse_release(self):
        """Handle mouse release for sliders"""
        for control in self.controls:
            if hasattr(control, 'handle_mouse_release'):
                control.handle_mouse_release()

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
            50,
            self.config.text_size,
            self.config.green
        )
        
        # Draw category headers
        header_y = 120
        self.graphik.drawText(
            "Sound Settings",
            current_width // 2 - 250,
            header_y,
            self.config.text_size // 2,
            self.config.yellow
        )
        
        self.graphik.drawText(
            "Display & Game Settings",
            current_width // 2 + 50,
            header_y,
            self.config.text_size // 2,
            self.config.yellow
        )
        
        # Draw all controls
        for control in self.controls:
            control.draw(self.game_display, self.graphik, self.config)
        
        # Draw navigation instructions
        instructions_y = current_height - 100
        self.graphik.drawText(
            "Use TAB/UP/DOWN to navigate, SPACE/ENTER to interact, ESC to go back",
            current_width // 2,
            instructions_y,
            self.config.text_size // 4,
            self.config.white
        )
        
        # Draw settings changed indicator
        if self.settings_changed:
            self.graphik.drawText(
                "Settings changed - click Apply to save or Cancel to discard",
                current_width // 2,
                instructions_y + 25,
                self.config.text_size // 4,
                self.config.yellow
            )