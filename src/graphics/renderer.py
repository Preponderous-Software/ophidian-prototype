class Renderer:

    def __init__(self, graphik, collision, config, environment_repository):
        self.graphik = graphik
        self.collision = collision
        self.config = config
        self.environment_repository = environment_repository

    def initialize_location_width_and_height(self):
        x, y = self.graphik.getGameDisplay().get_size()
        self.location_width = x / self.environment_repository.get_rows()
        self.location_height = y / self.environment_repository.get_columns()
    
    # Draws the environment in its entirety.
    def draw_environment(self):
        for locationId in self.environment_repository.get_locations():
            location = self.environment_repository.get_location_by_id(locationId)
            self.draw_location(
                location,
                location.getX() * self.location_width - 1,
                location.getY() * self.location_height - 1,
                self.location_width + 2,
                self.location_height + 2,
            )

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