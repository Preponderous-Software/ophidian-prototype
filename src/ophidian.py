import random
import time
import pygame
from config.config import Config
from lib.pyenvlib.entity import Entity
from lib.pyenvlib.environment import Environment
from food.food import Food
from lib.graphik.src.graphik import Graphik
from lib.pyenvlib.grid import Grid
from lib.pyenvlib.location import Location
from snake.snakePart import SnakePart


# @author Daniel McCoy Stephenson
# @since August 6th, 2022
class Ophidian:
    def __init__(self):
        pygame.init()
        self.config = Config()
        self.initialize_game_display()
        pygame.display.set_icon(pygame.image.load("src/media/icon.PNG"))
        self.graphik = Graphik(self.game_display)
        self.running = True
        self.snake_parts = []
        self.level = 1
        self.initialize()
        self.tick = 0
        self.score = 0
        self.changed_direction_this_tick = False
        self.collision = False

    def initialize_game_display(self):
        if self.config.fullscreen:
            self.game_display = pygame.display.set_mode(
                (self.config.display_width, self.config.display_height), pygame.FULLSCREEN
            )
        else:
            self.game_display = pygame.display.set_mode(
                (self.config.display_width, self.config.display_height), pygame.RESIZABLE
            )

    def initialize_location_width_and_height(self):
        x, y = self.game_display.get_size()
        self.location_width = x / self.environment.getGrid().getRows()
        self.location_height = y / self.environment.getGrid().getColumns()

    # Draws the environment in its entirety.
    def draw_environment(self):
        for locationId in self.environment.getGrid().getLocations():
            location = self.environment.getGrid().getLocation(locationId)
            self.draw_location(
                location,
                location.getX() * self.location_width - 1,
                location.getY() * self.location_height - 1,
                self.location_width + 2,
                self.location_height + 2,
            )

    # Returns the color that a location should be displayed as.
    def get_color_of_location(self, location):
        if location == -1:
            color = self.config.white
        else:
            color = self.config.white
            if location.getNumEntities() > 0:
                top_entity_id = list(location.getEntities().keys())[-1]
                top_entity = location.getEntity(top_entity_id)
                return top_entity.get_color()
        return color

    # Draws a location at a specified position.
    def draw_location(self, location, x_pos, y_pos, width, height):
        if self.collision == True:
            color = self.config.red
        else:
            color = self.get_color_of_location(location)
        self.graphik.drawRectangle(x_pos, y_pos, width, height, color)

    def calculate_score(self):
        length = len(self.snake_parts)
        num_locations = len(self.environment.grid.getLocations())
        percentage = int(length / num_locations * 100)
        self.score = length * percentage

    def display_stats_in_console(self):
        length = len(self.snake_parts)
        num_locations = len(self.environment.grid.getLocations())
        percentage = int(length / num_locations * 100)
        print(
            "The ophidian had a length of",
            length,
            "and took up",
            percentage,
            "percent of the world.",
        )
        print("Score:", self.score)
        print("-----")

    def check_for_level_progress_and_reinitialize(self):
        if (
            len(self.snake_parts)
            > len(self.environment.grid.getLocations())
            * self.config.level_progress_percentage_required
        ):
            self.level += 1
        self.initialize()

    def quit_application(self):
        self.display_stats_in_console()
        pygame.quit()
        quit()

    def get_location(self, entity: Entity):
        location_id = entity.getLocationID()
        grid = self.environment.getGrid()
        return grid.getLocation(location_id)

    def get_location_and_grid(self, entity: Entity):
        location_id = entity.getLocationID()
        grid = self.environment.getGrid()
        return grid, grid.getLocation(location_id)

    def move_entity(self, entity: Entity, direction):
        grid, location = self.get_location_and_grid(entity)

        new_location = -1
        # get new location
        if direction == 0:
            new_location = grid.getUp(location)
        elif direction == 1:
            new_location = grid.getLeft(location)
        elif direction == 2:
            new_location = grid.getDown(location)
        elif direction == 3:
            new_location = grid.getRight(location)

        if new_location == -1:
            # location doesn't exist, we're at a border
            return

        # if new location has a snake part already
        for eid in new_location.getEntities():
            e = new_location.getEntity(eid)
            if type(e) is SnakePart:
                # we have a collision
                self.collision = True
                print("The ophidian collides with itself and ceases to be.")
                self.draw_environment()
                pygame.display.update()
                time.sleep(self.config.tick_speed * 20)
                if self.config.restart_upon_collision:
                    self.check_for_level_progress_and_reinitialize()
                else:
                    self.running = False
                return

        # move entity
        location.removeEntity(entity)
        new_location.addEntity(entity)
        entity.lastPosition = location

        # move all attached snake parts
        if entity.has_previous():
            self.move_previous_snake_part(entity)

        if self.config.debug:
            print(
                "[EVENT] ",
                entity.getName(),
                "moved to (",
                location.getX(),
                ",",
                location.getY(),
                ")",
            )

        food = -1
        # check for food
        for eid in new_location.getEntities():
            e = new_location.getEntity(eid)
            if type(e) is Food:
                food = e

        if food == -1:
            return

        foodColor = food.get_color()

        self.remove_entity(food)
        self.spawn_food()
        self.spawn_snake_part(entity.get_tail(), foodColor)
        self.calculate_score()

    def move_previous_snake_part(self, snake_part):
        previous_snake_part = snake_part.previous_snake_part

        previous_snake_part_location = self.get_location(previous_snake_part)

        if previous_snake_part_location == -1:
            print("Error: A previous snake part's location was unexpectantly -1.")
            time.sleep(1)
            self.quit_application()

        target_location = snake_part.last_position

        # move entity
        previous_snake_part_location.removeEntity(previous_snake_part)
        target_location.addEntity(previous_snake_part)
        previous_snake_part.last_position = previous_snake_part_location

        if previous_snake_part.has_previous():
            self.move_previous_snake_part(previous_snake_part)

    def remove_entity_from_location(self, entity: Entity):
        location = self.get_location(entity)
        if location.isEntityPresent(entity):
            location.removeEntity(entity)

    def remove_entity(self, entity: Entity):
        self.remove_entity_from_location(entity)

    def handle_key_down_event(self, key):
        if key == pygame.K_q:
            self.running = False
        elif key == pygame.K_w or key == pygame.K_UP:
            if (
                self.changed_direction_this_tick == False
                and self.selected_snake_part.get_direction() != 2
            ):
                self.selected_snake_part.set_direction(0)
                self.changed_direction_this_tick = True
        elif key == pygame.K_a or key == pygame.K_LEFT:
            if (
                self.changed_direction_this_tick == False
                and self.selected_snake_part.get_direction() != 3
            ):
                self.selected_snake_part.set_direction(1)
                self.changed_direction_this_tick = True
        elif key == pygame.K_s or key == pygame.K_DOWN:
            if (
                self.changed_direction_this_tick == False
                and self.selected_snake_part.get_direction() != 0
            ):
                self.selected_snake_part.set_direction(2)
                self.changed_direction_this_tick = True
        elif key == pygame.K_d or key == pygame.K_RIGHT:
            if (
                self.changed_direction_this_tick == False
                and self.selected_snake_part.get_direction() != 1
            ):
                self.selected_snake_part.set_direction(3)
                self.changed_direction_this_tick = True
        elif key == pygame.K_F11:
            if self.config.fullscreen:
                self.config.fullscreen = False
            else:
                self.config.fullscreen = True
            self.initialize_game_display()
        elif key == pygame.K_l:
            if self.config.limit_tick_speed:
                self.config.limit_tick_speed = False
            else:
                self.config.limit_tick_speed = True
        elif key == pygame.K_r:
            self.check_for_level_progress_and_reinitialize()
            return "restart"

    def get_random_direction(self, grid: Grid, location: Location):
        direction = random.randrange(0, 4)
        if direction == 0:
            return grid.getUp(location)
        elif direction == 1:
            return grid.getRight(location)
        elif direction == 2:
            return grid.getDown(location)
        elif direction == 3:
            return grid.getLeft(location)

    def get_location_direction(self, direction, grid, location):
        if direction == 0:
            return grid.getUp(location)
        elif direction == 1:
            return grid.getLeft(location)
        elif direction == 2:
            return grid.getDown(location)
        elif direction == 3:
            return grid.getRight(location)

    def get_location_opposite_direction(self, direction, grid, location):
        if direction == 0:
            return grid.getDown(location)
        elif direction == 1:
            return grid.getRight(location)
        elif direction == 2:
            return grid.getUp(location)
        elif direction == 3:
            return grid.getLeft(location)

    def spawn_snake_part(self, snake_part: SnakePart, color):
        new_snake_part = SnakePart(color)
        snake_part.set_previous(new_snake_part)
        new_snake_part.set_next(snake_part)
        grid, location = self.get_location_and_grid(snake_part)

        target_location = -1
        while True:
            target_location = self.get_random_direction(grid, location)
            if target_location != -1 and target_location != self.get_location_direction(
                snake_part.get_direction(), grid, location
            ):
                break

        self.environment.addEntityToLocation(new_snake_part, target_location)
        self.snake_parts.append(new_snake_part)

    def spawn_food(self):
        food = Food(
            (
                random.randrange(50, 200),
                random.randrange(50, 200),
                random.randrange(50, 200),
            )
        )

        # get target location
        target_location = -1
        not_found = True
        while not_found:
            target_location = self.environment.getGrid().getRandomLocation()
            if target_location.getNumEntities() == 0:
                not_found = False

        self.environment.addEntity(food)

    def initialize(self):
        self.collision = False
        self.score = 0
        self.snake_parts = []
        self.tick = 0
        if self.level == 1:
            self.environment = Environment(
                "Level " + str(self.level), self.config.grid_size
            )
        else:
            self.environment = Environment(
                "Level " + str(self.level), self.config.grid_size + (self.level - 1) * 2
            )
        self.initialize_location_width_and_height()
        pygame.display.set_caption("Ophidian - Level " + str(self.level))
        self.selected_snake_part = SnakePart(
            (
                random.randrange(50, 200),
                random.randrange(50, 200),
                random.randrange(50, 200),
            )
        )
        self.environment.addEntity(self.selected_snake_part)
        self.snake_parts.append(self.selected_snake_part)
        print("The ophidian enters the world.")
        self.spawn_food()

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit_application()
                elif event.type == pygame.KEYDOWN:
                    result = self.handle_key_down_event(event.key)
                    if result == "restart":
                        continue
                elif event.type == pygame.WINDOWRESIZED:
                    self.initialize_location_width_and_height()

            if self.selected_snake_part.get_direction() == 0:
                self.move_entity(self.selected_snake_part, 0)
            elif self.selected_snake_part.get_direction() == 1:
                self.move_entity(self.selected_snake_part, 1)
            elif self.selected_snake_part.get_direction() == 2:
                self.move_entity(self.selected_snake_part, 2)
            elif self.selected_snake_part.get_direction() == 3:
                self.move_entity(self.selected_snake_part, 3)

            self.game_display.fill(self.config.white)
            self.draw_environment()
            x, y = self.game_display.get_size()

            # draw progress bar
            percentage = len(self.snake_parts) / len(
                self.environment.grid.getLocations()
            )
            pygame.draw.rect(self.game_display, self.config.black, (0, y - 20, x, 20))
            if percentage < self.config.level_progress_percentage_required / 2:
                pygame.draw.rect(
                    self.game_display, self.config.red, (0, y - 20, x * percentage, 20)
                )
            elif percentage < self.config.level_progress_percentage_required:
                pygame.draw.rect(
                    self.game_display,
                    self.config.yellow,
                    (0, y - 20, x * percentage, 20),
                )
            else:
                pygame.draw.rect(
                    self.game_display, self.config.green, (0, y - 20, x * percentage, 20)
                )
            pygame.draw.rect(self.game_display, self.config.black, (0, y - 20, x, 20), 1)

            pygame.display.update()

            if self.config.limit_tick_speed:
                time.sleep(self.config.tick_speed)
                self.tick += 1
                self.changed_direction_this_tick = False

        self.quit_application()


ophidian = Ophidian()
ophidian.run()
