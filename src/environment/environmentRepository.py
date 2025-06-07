from lib.pyenvlib.environment import Environment
from lib.pyenvlib.grid import Grid

from lib.pyenvlib.entity import Entity


class EnvironmentRepository (object):
    def __init__(self, level, gridSize):
        if level == 1:
            self.environment = Environment(
                "Level " + str(level), gridSize
            )
        else:
            self.environment = Environment(
                "Level " + str(level), gridSize + (level - 1) * 2
            )

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