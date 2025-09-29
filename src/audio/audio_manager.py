import pygame
import logging

logger = logging.getLogger(__name__)


class AudioManager:
    """Manages audio playback and volume controls"""

    def __init__(self, config):
        self.config = config
        self.initialized = False

        try:
            # Initialize pygame mixer for audio
            pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
            self.initialized = True
            logger.info("Audio system initialized successfully")
        except pygame.error as e:
            logger.warning(f"Failed to initialize audio system: {e}")
            self.initialized = False

    def play_sound_effect(self, sound_name: str = "default"):
        """Play a sound effect with SFX volume"""
        if not self.initialized:
            return

        try:
            # Create a simple beep sound programmatically since we don't have audio files
            # This is a placeholder that demonstrates volume control
            effective_volume = self.config.master_volume * self.config.sfx_volume

            if effective_volume > 0:
                # Generate a simple tone for demonstration
                duration = 0.1  # seconds
                sample_rate = 22050
                frames = int(duration * sample_rate)

                # Create a simple sine wave (beep)
                import numpy as np

                frequency = 440  # A note
                arr = np.sin(2 * np.pi * frequency * np.linspace(0, duration, frames))
                arr = (arr * 32767 * effective_volume).astype(np.int16)

                # Convert to stereo
                stereo_arr = np.zeros((frames, 2), np.int16)
                stereo_arr[:, 0] = arr
                stereo_arr[:, 1] = arr

                sound = pygame.sndarray.make_sound(stereo_arr)
                sound.play()
                logger.debug(
                    f"Played sound effect '{sound_name}' at volume {effective_volume:.2f}"
                )
        except Exception as e:
            logger.debug(f"Could not play sound effect: {e}")

    def play_music(self, music_name: str = "background"):
        """Play background music with music volume"""
        if not self.initialized:
            return

        try:
            # Set music volume
            effective_volume = self.config.master_volume * self.config.music_volume
            pygame.mixer.music.set_volume(effective_volume)
            logger.debug(f"Set music volume to {effective_volume:.2f}")

            # In a real implementation, you would load and play music files here
            # pygame.mixer.music.load("path/to/music/file.ogg")
            # pygame.mixer.music.play(-1)  # Loop indefinitely

        except Exception as e:
            logger.debug(f"Could not play music: {e}")

    def stop_music(self):
        """Stop background music"""
        if not self.initialized:
            return

        try:
            pygame.mixer.music.stop()
        except Exception as e:
            logger.debug(f"Could not stop music: {e}")

    def update_volumes(self):
        """Update all audio volumes based on current config"""
        if not self.initialized:
            return

        # Update music volume if music is playing
        try:
            effective_volume = self.config.master_volume * self.config.music_volume
            pygame.mixer.music.set_volume(effective_volume)
            logger.debug(f"Updated music volume to {effective_volume:.2f}")
        except Exception as e:
            logger.debug(f"Could not update music volume: {e}")

    def cleanup(self):
        """Clean up audio resources"""
        if self.initialized:
            try:
                pygame.mixer.quit()
                logger.info("Audio system cleaned up")
            except Exception as e:
                logger.warning(f"Error during audio cleanup: {e}")
