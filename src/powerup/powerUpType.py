from enum import Enum


# @author Daniel McCoy Stephenson
# @since September 2024
class PowerUpType(Enum):
    """Enumeration of available power-up types in the game."""

    SPEED_BOOST = "Speed Boost"
    SLOW_TIME = "Slow Time"
    INVINCIBILITY = "Invincibility"
    SCORE_MULTIPLIER = "Score Multiplier"

    def __str__(self):
        return self.value
