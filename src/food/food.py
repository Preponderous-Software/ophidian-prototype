from lib.pyenvlib.entity import Entity


# @author Daniel McCoy Stephenson
# @since August 6th, 2022
class Food(Entity):
    def __init__(self, color):
        Entity.__init__(self, "Food")
        self.color = color

    def get_color(self):
        return self.color
