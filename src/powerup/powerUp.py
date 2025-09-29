import time
from src.lib.pyenvlib.entity import Entity
from src.powerup.powerUpType import PowerUpType


# @author Daniel McCoy Stephenson
# @since September 2024
class PowerUp(Entity):
    """Base class for all power-ups in the game."""

    def __init__(self, power_up_type: PowerUpType, duration=10.0, color=(255, 255, 0)):
        """
        Initialize a power-up.

        Args:
            power_up_type: Type of power-up from PowerUpType enum
            duration: How long the power-up effect lasts in seconds
            color: RGB color tuple for visual representation
        """
        Entity.__init__(self, f"PowerUp({power_up_type.value})")
        self.power_up_type = power_up_type
        self.duration = duration
        self.color = color
        self.active = False
        self.activation_time = 0.0

    def activate(self):
        """Activate the power-up."""
        self.active = True
        self.activation_time = time.time()

    def deactivate(self):
        """Deactivate the power-up."""
        self.active = False
        self.activation_time = 0.0

    def is_active(self):
        """Check if the power-up is currently active."""
        return self.active

    def is_expired(self):
        """Check if the power-up effect has expired."""
        if not self.active:
            return False
        return time.time() - self.activation_time >= self.duration

    def get_remaining_time(self):
        """Get remaining time for the power-up effect."""
        if not self.active:
            return 0.0
        elapsed = time.time() - self.activation_time
        return max(0.0, self.duration - elapsed)

    def get_power_up_type(self):
        """Get the type of this power-up."""
        return self.power_up_type

    def get_color(self):
        """Get the color of this power-up."""
        return self.color

    def get_duration(self):
        """Get the duration of this power-up."""
        return self.duration
