import pygame

from src.lib.graphik.src.graphik import Graphik


class Renderer:

    def __init__(self, collision, config, environment_repository, snake_part_repository, game_score):
        self.collision = collision
        self.config = config
        self.environment_repository = environment_repository
        self.snake_part_repository = snake_part_repository
        self.game_score = game_score
        self.initialize_game_display()
        self.graphik = Graphik(self.game_display)
        self.location_width = 0
        self.location_height = 0


    def initialize_game_display(self):
        if self.config.fullscreen:
            self.game_display = pygame.display.set_mode(
                (self.config.display_width, self.config.display_height), pygame.FULLSCREEN
            )
        else:
            self.game_display = pygame.display.set_mode(
                (self.config.display_width, self.config.display_height), pygame.RESIZABLE
            )

    def draw(self):
        self.graphik.getGameDisplay().fill(self.config.white)
        self.draw_environment()
        self.draw_progress_bar()
        self.draw_score();

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
        # Draw the score
        font = pygame.font.Font(None, 36)
        black = (0, 0, 0)
        level_score = font.render(f"Level Score: {self.game_score.current_points}", True, black)
        total_score = font.render(f"Total Score: {self.game_score.cumulative_points}", True, black)

        # Position the score in the top-left corner with padding
        padding = 10
        self.graphik.gameDisplay.blit(level_score, (padding, padding))
        self.graphik.gameDisplay.blit(total_score, (padding, padding + 40))  # 40 pixels below the level score