from lib.pyenvlib.entity import Entity


# @author Daniel McCoy Stephenson
# @since August 6th, 2022
class SnakePart(Entity):
    def __init__(self, color):
        Entity.__init__(self, "Snake Part")
        self.color = color
        self.direction = 0
        self.next_snake_part = -1
        self.previous_snake_part = -1
        self.last_position = -1

    def get_direction(self):
        return self.direction

    def set_direction(self, direction):
        self.direction = direction

    def set_next(self, snake_part):
        self.next_snake_part = snake_part

    def set_previous(self, snake_part):
        self.previous_snake_part = snake_part

    def set_last_position(self, position):
        self.last_position = position

    def has_next(self):
        return self.next_snake_part != -1

    def has_previous(self):
        return self.previous_snake_part != -1

    def get_tail(self):
        if self.previous_snake_part == -1:
            return self
        temp = self.previous_snake_part
        while temp.hasPrevious():
            temp = temp.previousSnakePart
        return temp

    def get_color(self):
        return self.color
