import math
import random
import time

from lib.pyenvlib.environment import Environment
from lib.pyenvlib.grid import Grid

from lib.pyenvlib.entity import Entity

from food.food import Food
from snake.snakePart import SnakePart


class EnvironmentRepository (object):
    def __init__(self, level, gridSize, snakePartRepository, config):
        self.config = config
        print("Initializing environment repository for level " + str(level) + " with grid size " + str(gridSize))
        if level == 1:
            self.environment = Environment(
                "Level " + str(level), gridSize
            )
        else:
            self.environment = Environment(
                "Level " + str(level), gridSize + (level - 1) * 2
            )

        self.snake_part_repository = snakePartRepository
        self.grid_size = gridSize

    def get_rows(self):
        return self.environment.getGrid().getRows()

    def get_columns(self):
        return self.environment.getGrid().getColumns()

    def get_locations(self):
        return self.environment.getGrid().getLocations()

    def get_location(self, x, y):
        return self.environment.getGrid().getLocation(x, y)

    def get_num_locations(self):
        return len(self.environment.getGrid().getLocations())

    def get_location_of_entity(self, entity):
        location_id = entity.getLocationID()
        if location_id is None:
            return None
        return self.environment.getGrid().getLocation(location_id)

    def get_location_above_entity(self, entity):
        current_location = self.get_location_of_entity(entity)
        if current_location is None:
            return None
        grid = self.environment.getGrid()
        return grid.getUp(current_location)

    def get_location_left_of_entity(self, entity):
        current_location = self.get_location_of_entity(entity)
        if current_location is None:
            return None
        grid = self.environment.getGrid()
        return grid.getLeft(current_location)

    def get_location_below_entity(self, entity):
        current_location = self.get_location_of_entity(entity)
        if current_location is None:
            return None
        grid = self.environment.getGrid()
        return grid.getDown(current_location)

    def get_location_right_of_entity(self, entity):
        current_location = self.get_location_of_entity(entity)
        if current_location is None:
            return None
        grid = self.environment.getGrid()
        return grid.getRight(current_location)

    def add_entity_to_location(self, newSnakePart, targetLocation):
        self.environment.addEntityToLocation(newSnakePart, targetLocation)

    def get_location_in_random_direction(self, location):
        directions = ['up', 'down', 'left', 'right']
        import random
        direction = random.choice(directions)
        if direction == 'up':
            return self.environment.getGrid().getUp(location)
        elif direction == 'down':
            return self.environment.getGrid().getDown(location)
        elif direction == 'left':
            return self.environment.getGrid().getLeft(location)
        elif direction == 'right':
            return self.environment.getGrid().getRight(location)
        else:
            raise ValueError("Invalid direction")

    def get_location_in_direction_of_entity(self, param, snakePart):
        location_of_snake_part = self.get_location_of_entity(snakePart)
        if location_of_snake_part is None:
            return None
        if param == 0:
            return self.environment.getGrid().getUp(location_of_snake_part)
        elif param == 1:
            return self.environment.getGrid().getDown(location_of_snake_part)
        elif param == 2:
            return self.environment.getGrid().getLeft(location_of_snake_part)
        elif param == 3:
            return self.environment.getGrid().getRight(location_of_snake_part)
        else:
            raise ValueError("Invalid direction parameter: " + str(param))

    def get_random_location(self):
        import random
        rows = self.environment.getGrid().getRows()
        columns = self.environment.getGrid().getColumns()
        x = random.randint(0, rows - 1)
        y = random.randint(0, columns - 1)
        return self.environment.getGrid().getLocationByCoordinates(x, y)

    def add_entity_to_random_location(self, selectedSnakePart):
        random_location = self.get_random_location()
        if random_location is not None:
            self.add_entity_to_location(selectedSnakePart, random_location)
        else:
            raise Exception("No valid location found to add entity")

    def remove_entity_from_location(self, entity):
        self.environment.removeEntity(entity)

    def get_location_by_id(self, locationId):
        location = self.environment.getGrid().getLocation(locationId)
        if location is None:
            raise Exception(f"Location with ID {locationId} not found")
        return location

    def removeEntityFromLocation(self, entity: Entity):
        location = self.getLocation(entity)
        if location.isEntityPresent(entity):
            location.removeEntity(entity)

    def spawn_snake_part(self, snake_part: SnakePart, color):
        new_snake_part = SnakePart(color)
        snake_part.setPrevious(new_snake_part)
        new_snake_part.setNext(snake_part)

        location = self.get_location_of_entity(snake_part)
        while True:
            target_location = self.get_location_in_random_direction(location)
            location_in_current_direction_of_snake_part = self.get_location_in_direction_of_entity(snake_part.getDirection(), snake_part)
            if target_location != -1 and target_location != location_in_current_direction_of_snake_part:
                break

        self.add_entity_to_location(new_snake_part, target_location)
        self.snake_part_repository.append(new_snake_part)

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
            target_location = self.get_random_location()
            if target_location.getNumEntities() == 0:
                not_found = False

        self.add_entity_to_location(food, target_location)

    def move_entity(self, entity: Entity, direction):
        check_for_level_progress_and_reinitialize = False

        # get new location
        if direction == 0:
            new_location = self.get_location_above_entity(entity)
        elif direction == 1:
            new_location = self.get_location_left_of_entity(entity)
        elif direction == 2:
            new_location = self.get_location_below_entity(entity)
        elif direction == 3:
            new_location = self.get_location_right_of_entity(entity)
        else:
            print("Error: Invalid direction specified for entity movement.")
            raise ValueError("Invalid direction specified for entity movement.")

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
                time.sleep(self.config.tick_speed * 20)
                if self.config.restart_upon_collision:
                    check_for_level_progress_and_reinitialize = True
                else:
                    self.running = False

        # move entity
        location = self.get_location_of_entity(entity)
        self.remove_entity_from_location(entity)
        new_location.addEntity(entity)
        entity.lastPosition = location

        # move all attached snake parts
        if entity.hasPrevious():
            self.move_previous_snake_part(entity)

        food = -1
        # check for food
        for eid in new_location.getEntities():
            e = new_location.getEntity(eid)
            if type(e) is Food:
                food = e

        if food == -1:
            return check_for_level_progress_and_reinitialize

        food_color = food.getColor()

        self.remove_entity_from_location(food)
        self.spawn_food()
        self.spawn_snake_part(entity.getTail(), food_color)
        return check_for_level_progress_and_reinitialize

    def move_previous_snake_part(self, snake_part):
        previous_snake_part = snake_part.previousSnakePart

        previous_snake_part_location = self.get_location_of_entity(previous_snake_part)

        if previous_snake_part_location == -1:
            print("Error: A previous snake part's location was unexpectantly -1.")

        target_location = snake_part.lastPosition

        # move entity
        previous_snake_part_location.removeEntity(previous_snake_part)
        target_location.addEntity(previous_snake_part)
        previous_snake_part.lastPosition = previous_snake_part_location

        if previous_snake_part.hasPrevious():
            self.move_previous_snake_part(previous_snake_part)

    def clear(self):
        entities_to_remove_from_environment = []
        for locationId in self.environment.getGrid().getLocations():
            location = self.environment.getGrid().getLocation(locationId)
            for entity in location.getEntities().values():
                if isinstance(entity, SnakePart) or isinstance(entity, Food):
                    entities_to_remove_from_environment.append(entity)
        for entity in entities_to_remove_from_environment:
            self.environment.removeEntity(entity)
        self.snake_part_repository.clear()

    def reinitialize(self, level, increase_grid_size):
        self.clear()
        current_grid_size = self.grid_size
        print("Current grid size: " + str(current_grid_size))
        if increase_grid_size:
            # Increase grid size based on level
            new_grid_size = current_grid_size + (level - 1) * 2
        else:
            # Keep the same grid size
            new_grid_size = current_grid_size
        print("Reinitializing environment for level " + str(level) + " with grid size " + str(new_grid_size))
        self.environment = Environment(
            "Level " + str(level), new_grid_size
        )
        self.grid_size = new_grid_size