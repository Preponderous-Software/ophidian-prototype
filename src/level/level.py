from lib.pyenvlib.environment import Environment


# @author Daniel McCoy Stephenson
# @since December 27th, 2022
class Level:
    def __init__(self, name, size):
        self.name = name
        self.size = size
        self.environment = Environment(name, size)
