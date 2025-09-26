import pygame

from src.lib.graphik.src.graphik import Graphik


class Renderer:

    def __init__(self, collision, config, environment_repository, snake_part_repository, game_score, game_display):
        self.collision = collision
        self.config = config
        self.environment_repository = environment_repository
        self.snake_part_repository = snake_part_repository
        self.game_score = game_score
        self.game_display = game_display  # Use the provided game display instead of creating new one
        self.graphik = Graphik(self.game_display)
        self.location_width = 0
        self.location_height = 0
        self.game_area_offset_x = 0
        self.game_area_offset_y = 0



    def draw(self):
        self.graphik.getGameDisplay().fill(self.config.white)
        self.draw_game_area_background()
        self.draw_environment()
        self.draw_progress_bar()
        self.draw_score()

    def initialize_location_width_and_height(self):
        x, y = self.graphik.getGameDisplay().get_size()
        
        # Calculate proportional scaling based on window height
        # Reserve space for progress bar (20 pixels) and score (50 pixels)
        available_height = y - 70
        
        # Use the smaller dimension to maintain square grid cells
        grid_size = max(self.environment_repository.get_rows(), self.environment_repository.get_columns())
        cell_size = available_height / grid_size
        
        # Calculate the actual game area dimensions
        game_area_width = self.environment_repository.get_rows() * cell_size
        game_area_height = self.environment_repository.get_columns() * cell_size
        
        # Center the game area horizontally
        self.game_area_offset_x = (x - game_area_width) / 2
        self.game_area_offset_y = 0  # Align to top, leaving space for UI at bottom
        
        # Set uniform location dimensions for square cells
        self.location_width = cell_size
        self.location_height = cell_size
    
    def draw_game_area_background(self):
        """Draw a distinct background for the game area to make it clearly visible"""
        # Calculate game area dimensions
        game_area_width = self.environment_repository.get_rows() * self.location_width
        game_area_height = self.environment_repository.get_columns() * self.location_height
        
        # Draw a subtle gray background for the game area
        light_gray = (240, 240, 240)
        pygame.draw.rect(
            self.graphik.getGameDisplay(), 
            light_gray, 
            (self.game_area_offset_x, self.game_area_offset_y, game_area_width, game_area_height)
        )
        
        # Draw a border around the game area
        border_color = (200, 200, 200)
        pygame.draw.rect(
            self.graphik.getGameDisplay(), 
            border_color, 
            (self.game_area_offset_x - 2, self.game_area_offset_y - 2, game_area_width + 4, game_area_height + 4), 
            2
        )

    # Draws the environment in its entirety.
    def draw_environment(self):
        for locationId in self.environment_repository.get_locations():
            location = self.environment_repository.get_location_by_id(locationId)
            self.draw_location(
                location,
                self.game_area_offset_x + location.getX() * self.location_width - 1,
                self.game_area_offset_y + location.getY() * self.location_height - 1,
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
            raise ValueError("Location cannot be -1")
        else:
            color = self.config.white
            if location.getNumEntities() > 0:
                top_entity_id = list(location.getEntities().keys())[-1]
                top_entity = location.getEntity(top_entity_id)
                return top_entity.getColor()
        return color

    def draw_progress_bar(self):
        x, y = self.graphik.getGameDisplay().get_size()
        percentage = self.snake_part_repository.get_length() / self.environment_repository.get_num_locations()
        pygame.draw.rect(self.graphik.getGameDisplay(), self.config.black, (0, y - 20, x, 20))
        if percentage < self.config.level_progress_percentage_required / 2:
            pygame.draw.rect(
                self.graphik.getGameDisplay(), self.config.red, (0, y - 20, x * percentage, 20)
            )
        elif percentage < self.config.level_progress_percentage_required:
            pygame.draw.rect(
                self.graphik.getGameDisplay(),
                self.config.yellow,
                (0, y - 20, x * percentage, 20),
            )
        else:
            pygame.draw.rect(
                self.graphik.getGameDisplay(), self.config.green, (0, y - 20, x * percentage, 20)
            )
        pygame.draw.rect(self.graphik.getGameDisplay(), self.config.black, (0, y - 20, x, 20), 1)

    def draw_score(self):
        black = (0, 0, 0)
        score_text = str(self.game_score.current_points) + " | " + str(self.game_score.cumulative_points)
        score_position = (
            self.graphik.getGameDisplay().get_size()[0] / 2,
            self.graphik.getGameDisplay().get_size()[1] - 50,
        )
        score_text_size = int(self.config.text_size / 2)
        self.graphik.drawText(
            score_text,
            score_position[0],
            score_position[1],
            score_text_size,
            black
        )