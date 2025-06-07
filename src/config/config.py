# @author Daniel McCoy Stephenson
# @since August 6th, 2022


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
        self.grid_size = 5
        self.min_grid_size = 5
        self.max_grid_size = 12

        # tick speed
        self.limit_tick_speed = True
        self.tick_speed = 0.1

        # misc
        self.debug = False
        self.restart_upon_collision = True
        self.level_progress_percentage_required = 0.5
