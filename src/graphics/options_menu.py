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
        
        # Feedback message system
        self.feedback_message = ""
        self.feedback_color = None
        self.feedback_time = 0
        
        self.initialize_controls()
    
    def initialize_controls(self):
        """Initialize all UI controls for the options menu"""
        self.controls = []
        
        # Sound Settings
        self.master_volume_slider = Slider(
            0, 0, 200, 30,  # Position will be set dynamically
            0.0, 1.0, self.config.master_volume, "Master Volume"
        )
        self.controls.append(self.master_volume_slider)
        
        self.music_volume_slider = Slider(
            0, 0, 200, 30,  # Position will be set dynamically
            0.0, 1.0, self.config.music_volume, "Music Volume"
        )
        self.controls.append(self.music_volume_slider)
        
        self.sfx_volume_slider = Slider(
            0, 0, 200, 30,  # Position will be set dynamically
            0.0, 1.0, self.config.sfx_volume, "SFX Volume"
        )
        self.controls.append(self.sfx_volume_slider)
        
        # Display Settings
        self.fullscreen_toggle = Toggle(
            0, 0, 80, 30,  # Position will be set dynamically
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
            0, 0, 200, 30,  # Position will be set dynamically
            res_options, res_index, "Resolution"
        )
        self.controls.append(self.resolution_dropdown)
        
        # Controls Settings
        self.limit_tick_speed_toggle = Toggle(
            0, 0, 80, 30,  # Position will be set dynamically
            self.config.limit_tick_speed, "Limit Tick Speed"
        )
        self.controls.append(self.limit_tick_speed_toggle)
        
        # Difficulty Settings
        difficulties = self.config.get_difficulty_levels()
        diff_index = difficulties.index(self.config.difficulty) if self.config.difficulty in difficulties else 1
        self.difficulty_dropdown = Dropdown(
            0, 0, 200, 30,  # Position will be set dynamically
            difficulties, diff_index, "Difficulty"
        )
        self.controls.append(self.difficulty_dropdown)
        
        # Buttons
        self.apply_button = Button(
            0, 0, 80, 40,  # Position will be set dynamically
            "Apply", self.apply_settings
        )
        self.controls.append(self.apply_button)
        
        self.cancel_button = Button(
            0, 0, 80, 40,  # Position will be set dynamically
            "Cancel", self.cancel_settings
        )
        self.controls.append(self.cancel_button)
        
        # Set initial focus
        if self.controls:
            self.controls[0].focused = True
        
        # Update positions dynamically
        self.update_control_positions()
    
    def update_control_positions(self):
        """Update control positions based on current screen size"""
        # Get current window size
        try:
            current_width, current_height = self.game_display.get_size()
        except (AttributeError, ValueError):
            current_width, current_height = self.config.display_width, self.config.display_height
        
        # Calculate responsive dimensions
        min_width = 600  # Minimum supported width
        max_width = 1600  # Maximum width for optimal layout
        actual_width = max(min_width, min(max_width, current_width))
        
        # Scale control dimensions based on screen size
        base_control_width = 200
        base_control_height = 30
        base_spacing = 60
        
        # Scale factor based on screen size (0.8 to 1.2 range)
        scale_factor = 0.8 + (actual_width - min_width) / (max_width - min_width) * 0.4
        scale_factor = max(0.8, min(1.2, scale_factor))
        
        control_width = int(base_control_width * scale_factor)
        control_height = int(base_control_height * scale_factor)
        control_spacing = int(base_spacing * scale_factor)
        
        # Calculate positions
        start_y = max(160, current_height // 2 - 200)
        
        # Adjust column positions based on screen width
        if current_width < 800:
            # Single column layout for narrow screens
            left_column_x = max(10, current_width // 2 - control_width // 2)
            right_column_x = left_column_x
            # Adjust spacing for single column to fit more content
            reduced_spacing = min(control_spacing, max(35, (current_height - start_y - 150) // 8))  # 8 controls + buttons
            sound_start_y = start_y
            display_start_y = start_y + reduced_spacing * 4  # After sound controls
            controls_start_y = display_start_y + reduced_spacing * 3  # After display controls
        else:
            # Two column layout for wider screens
            column_gap = max(50, current_width // 16)
            left_column_x = max(10, current_width // 2 - control_width - column_gap // 2)
            right_column_x = min(current_width - control_width - 10, current_width // 2 + column_gap // 2)
            sound_start_y = start_y
            display_start_y = start_y
            controls_start_y = start_y + control_spacing * 3
            reduced_spacing = control_spacing  # Use normal spacing for two-column layout
        
        # Update Sound Settings positions (left column)
        spacing_to_use = reduced_spacing if current_width < 800 else control_spacing
        
        self.master_volume_slider.x = left_column_x
        self.master_volume_slider.y = sound_start_y
        self.master_volume_slider.width = control_width
        self.master_volume_slider.height = control_height
        self.master_volume_slider.rect.x = left_column_x
        self.master_volume_slider.rect.y = sound_start_y
        self.master_volume_slider.rect.width = control_width
        self.master_volume_slider.rect.height = control_height
        
        self.music_volume_slider.x = left_column_x
        self.music_volume_slider.y = sound_start_y + spacing_to_use
        self.music_volume_slider.width = control_width
        self.music_volume_slider.height = control_height
        self.music_volume_slider.rect.x = left_column_x
        self.music_volume_slider.rect.y = sound_start_y + spacing_to_use
        self.music_volume_slider.rect.width = control_width
        self.music_volume_slider.rect.height = control_height
        
        self.sfx_volume_slider.x = left_column_x
        self.sfx_volume_slider.y = sound_start_y + spacing_to_use * 2
        self.sfx_volume_slider.width = control_width
        self.sfx_volume_slider.height = control_height
        self.sfx_volume_slider.rect.x = left_column_x
        self.sfx_volume_slider.rect.y = sound_start_y + spacing_to_use * 2
        self.sfx_volume_slider.rect.width = control_width
        self.sfx_volume_slider.rect.height = control_height
        
        # Update Display Settings positions (right column or below for narrow screens)
        toggle_width = int(80 * scale_factor)
        
        self.fullscreen_toggle.x = right_column_x
        self.fullscreen_toggle.y = display_start_y
        self.fullscreen_toggle.width = toggle_width
        self.fullscreen_toggle.height = control_height
        self.fullscreen_toggle.rect.x = right_column_x
        self.fullscreen_toggle.rect.y = display_start_y
        self.fullscreen_toggle.rect.width = toggle_width
        self.fullscreen_toggle.rect.height = control_height
        
        self.resolution_dropdown.x = right_column_x
        self.resolution_dropdown.y = display_start_y + spacing_to_use
        self.resolution_dropdown.width = control_width
        self.resolution_dropdown.height = control_height
        self.resolution_dropdown.rect.x = right_column_x
        self.resolution_dropdown.rect.y = display_start_y + spacing_to_use
        self.resolution_dropdown.rect.width = control_width
        self.resolution_dropdown.rect.height = control_height
        
        self.difficulty_dropdown.x = right_column_x
        self.difficulty_dropdown.y = display_start_y + spacing_to_use * 2
        self.difficulty_dropdown.width = control_width
        self.difficulty_dropdown.height = control_height
        self.difficulty_dropdown.rect.x = right_column_x
        self.difficulty_dropdown.rect.y = display_start_y + spacing_to_use * 2
        self.difficulty_dropdown.rect.width = control_width
        self.difficulty_dropdown.rect.height = control_height
        
        # Update Controls Settings positions (left column)
        if current_width < 800:
            # In single column, put this after display settings
            self.limit_tick_speed_toggle.x = left_column_x
            self.limit_tick_speed_toggle.y = controls_start_y
        else:
            # In two column, put this in left column below sound settings
            self.limit_tick_speed_toggle.x = left_column_x
            self.limit_tick_speed_toggle.y = controls_start_y
        
        # Ensure control doesn't go off the bottom of the screen
        max_y = current_height - control_height - 60  # Leave room for buttons
        if self.limit_tick_speed_toggle.y > max_y:
            self.limit_tick_speed_toggle.y = max_y
        
        self.limit_tick_speed_toggle.width = toggle_width
        self.limit_tick_speed_toggle.height = control_height
        self.limit_tick_speed_toggle.rect.x = self.limit_tick_speed_toggle.x
        self.limit_tick_speed_toggle.rect.y = self.limit_tick_speed_toggle.y
        self.limit_tick_speed_toggle.rect.width = toggle_width
        self.limit_tick_speed_toggle.rect.height = control_height
        
        # Update Buttons positions (centered)
        button_width = int(80 * scale_factor)
        button_height = int(40 * scale_factor)
        button_spacing = int(10 * scale_factor)
        
        if current_width < 800:
            button_y = max(self.limit_tick_speed_toggle.y + control_height + 20, controls_start_y + spacing_to_use * 2)
        else:
            button_y = controls_start_y + control_spacing * 2
        
        # Ensure buttons don't go off screen
        button_y = min(button_y, current_height - button_height - 10)
        
        total_button_width = button_width * 3 + button_spacing * 2
        button_start_x = max(10, current_width // 2 - total_button_width // 2)
        
        # Ensure buttons fit within screen width
        if button_start_x + total_button_width > current_width - 10:
            # Make buttons smaller if they don't fit
            available_width = current_width - 20  # 10px margin on each side
            button_width = min(button_width, (available_width - button_spacing * 2) // 3)
            total_button_width = button_width * 3 + button_spacing * 2
            button_start_x = current_width // 2 - total_button_width // 2
        
        self.apply_button.x = button_start_x
        self.apply_button.y = button_y
        self.apply_button.width = button_width
        self.apply_button.height = button_height
        self.apply_button.rect.x = button_start_x
        self.apply_button.rect.y = button_y
        self.apply_button.rect.width = button_width
        self.apply_button.rect.height = button_height
        
        self.cancel_button.x = button_start_x + button_width + button_spacing
        self.cancel_button.y = button_y
        self.cancel_button.width = button_width
        self.cancel_button.height = button_height
        self.cancel_button.rect.x = button_start_x + button_width + button_spacing
        self.cancel_button.rect.y = button_y
        self.cancel_button.rect.width = button_width
        self.cancel_button.rect.height = button_height
        
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
        old_width, old_height = self.config.display_width, self.config.display_height
        self.config.display_width, self.config.display_height = selected_res
        
        # Save settings to file
        self.config.save_settings()
        
        self.settings_changed = False
        self.store_original_settings()  # Update original settings after apply
        
        # Show feedback that settings were applied
        self.show_feedback_message("Settings Applied!", self.config.green)
        
        # Notify parent to update audio volumes if available
        self._notify_audio_update()
        
        # Notify if resolution changed
        if (old_width, old_height) != selected_res:
            self._notify_resolution_change()
    
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
        
        # Show feedback that changes were cancelled
        self.show_feedback_message("Changes Cancelled", self.config.yellow)
    
    def show_feedback_message(self, message, color):
        """Show a temporary feedback message"""
        self.feedback_message = message
        self.feedback_color = color
        self.feedback_time = pygame.time.get_ticks()

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
            result = control.handle_mouse_click(pos)
            if result:
                # Update focus to clicked control
                if self.controls:
                    self.controls[self.current_control_index].focused = False
                self.current_control_index = i
                control.focused = True
                
                # Handle button return values
                if isinstance(control, Button):
                    # Button's handle_mouse_click already called the callback
                    # and returned the result, so we use that result
                    if result is not True:  # True means clicked but no state change
                        return result
                else:
                    # For other controls, mark settings as changed
                    self.settings_changed = True
                break
        
        return None
    
    def handle_mouse_motion(self, pos):
        """Handle mouse motion for sliders and button hover effects"""
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
        
        # Update control positions based on current screen size
        self.update_control_positions()
        
        # Clear screen with black background
        self.game_display.fill(self.config.black)
        
        # Draw title
        title_size = max(30, min(60, int(self.config.text_size * (current_width / 800))))
        self.graphik.drawText(
            "OPTIONS",
            current_width // 2,
            50,
            title_size,
            self.config.green
        )
        
        # Draw category headers with dynamic positioning
        header_size = max(16, min(32, int(self.config.text_size // 3 * (current_width / 800))))
        header_y = 120
        
        if current_width < 800:
            # Single column layout - center headers above their sections
            # Use smaller header size and better spacing for small screens
            self.graphik.drawText(
                "Sound Settings",
                current_width // 2,
                header_y,
                header_size,
                self.config.yellow
            )
            
            # Calculate dynamic position for second header based on actual control positions
            display_header_y = max(header_y + 200, self.fullscreen_toggle.y - 30)
            self.graphik.drawText(
                "Display & Game Settings", 
                current_width // 2,
                display_header_y,
                header_size,
                self.config.yellow
            )
        else:
            # Two column layout - position headers above columns with better spacing
            # Calculate header positions based on actual control positions
            left_header_x = self.master_volume_slider.x + self.master_volume_slider.width // 2
            right_header_x = self.fullscreen_toggle.x + 100  # Offset for better centering
            
            # Ensure headers don't overlap or go off screen
            min_spacing = 150
            if right_header_x - left_header_x < min_spacing:
                left_header_x = current_width // 2 - min_spacing // 2
                right_header_x = current_width // 2 + min_spacing // 2
            
            self.graphik.drawText(
                "Sound Settings",
                left_header_x,
                header_y,
                header_size,
                self.config.yellow
            )
            
            self.graphik.drawText(
                "Display & Game Settings",
                right_header_x,
                header_y,
                header_size,
                self.config.yellow
            )
        
        # Draw all controls
        for control in self.controls:
            control.draw(self.game_display, self.graphik, self.config)
        
        # Draw navigation instructions with responsive sizing
        instructions_y = current_height - 100
        instruction_size = max(10, min(20, int(self.config.text_size // 4 * (current_width / 800))))
        
        self.graphik.drawText(
            "Use TAB/UP/DOWN to navigate, SPACE/ENTER to interact, ESC to go back",
            current_width // 2,
            instructions_y,
            instruction_size,
            self.config.white
        )
        
        # Draw settings changed indicator
        if self.settings_changed:
            self.graphik.drawText(
                "Settings changed - click Apply to save or Cancel to discard",
                current_width // 2,
                instructions_y + 25,
                instruction_size,
                self.config.yellow
            )
        
        # Draw feedback message if active
        current_time = pygame.time.get_ticks()
        if (self.feedback_message and 
            current_time - self.feedback_time < 2000):  # Show for 2 seconds
            feedback_y = instructions_y + (50 if self.settings_changed else 25)
            self.graphik.drawText(
                self.feedback_message,
                current_width // 2,
                feedback_y,
                instruction_size,
                self.feedback_color
            )
        elif current_time - self.feedback_time >= 2000:
            # Clear feedback message after timeout
            self.feedback_message = ""
    
    def set_audio_update_callback(self, callback):
        """Set callback function to notify when audio settings change"""
        self.audio_update_callback = callback
    
    def set_resolution_change_callback(self, callback):
        """Set callback function to notify when resolution changes"""
        self.resolution_change_callback = callback
    
    def _notify_audio_update(self):
        """Notify parent component about audio setting changes"""
        if hasattr(self, 'audio_update_callback') and self.audio_update_callback:
            self.audio_update_callback()
    
    def _notify_resolution_change(self):
        """Notify parent component about resolution changes"""
        if hasattr(self, 'resolution_change_callback') and self.resolution_change_callback:
            self.resolution_change_callback()