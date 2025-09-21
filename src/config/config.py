# @author Daniel McCoy Stephenson
# @since August 6th, 2022

import random

# @author Daniel McCoy Stephenson
# @since August 6th, 2022
class Config:
    def __init__(self):
        # display
        self.display_width = 500
        self.display_height = 500
        self.fullscreen = False
        self.black = (0, 0, 0)
        self.white = (255, 255, 255)
        self.green = (0, 255, 0)
        self.red = (255, 0, 0)
        self.yellow = (255, 255, 0)
        self.text_size = 50

        # grid size
        self.initial_grid_size = 5

        # tick speed
        self.limit_tick_speed = True
        self.tick_speed = 0.1

        # misc
        self.debug = False
        self.restart_upon_collision = True
        self.level_progress_percentage_required = 0.25

    def generate_green_shade(self):
        """Generate a random shade of green for snake parts."""
        # Keep red component low (0-50), vary green (100-255), keep blue low (0-100)
        red = random.randint(0, 50)
        green = random.randint(100, 255)
        blue = random.randint(0, 100)
        return (red, green, blue)
