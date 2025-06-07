# @author Daniel McCoy Stephenson
# @since August 6th, 2022
class Food:
    def __init__(self, color, entity_id):
        self.entity_id = entity_id
        self.color = color

    def get_entity_id(self):
        return self.entity_id

    def getColor(self):
        return self.color
