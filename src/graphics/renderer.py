class Renderer:

    def __init__(self, graphik, collision, config):
        self.graphik = graphik
        self.collision = collision
        self.config = config

    # Draws a location at a specified position.
    def draw_location(self, location, x_pos, y_pos, width, height):
        if self.collision:
            color = self.config.red
        else:
            color = self.get_color_of_location(location)
        self.graphik.drawRectangle(x_pos, y_pos, width, height, color)

    # Returns the color that a location should be displayed as.
    def get_color_of_location(self, location):
        if location == -1:
            color = self.config.white
        else:
            color = self.config.white
            if location.getNumEntities() > 0:
                top_entity_id = list(location.getEntities().keys())[-1]
                top_entity = location.getEntity(top_entity_id)
                return top_entity.getColor()
        return color