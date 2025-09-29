import os
import random
import time
import logging
from typing import Any, Optional

from src.lib.pyenvlib.environment import Environment
from src.lib.pyenvlib.entity import Entity
from src.food.food import Food
from src.snake.snakePart import SnakePart
from src.snake.snakeColorGenerator import SnakeColorGenerator
from src.environment.environmentRepository import EnvironmentRepository
from src.powerup.powerUp import PowerUp
from src.powerup.powerUpType import PowerUpType

from src.config.config import Config
from src.snake.snakePartRepository import SnakePartRepository

from src.lib.pyenvlib.location import Location

log_level = os.environ.get("LOG_LEVEL", "INFO").upper()
logging.basicConfig(level=getattr(logging, log_level))
logger = logging.getLogger(__name__)


class PyEnvLibEnvironmentRepositoryImpl(EnvironmentRepository):
    def __init__(
        self, level: int, config: Config, snake_part_repository: SnakePartRepository
    ) -> None:
        self.level = level
        self.config = config
        self.snake_part_repository = snake_part_repository

        # Adjust game parameters based on difficulty
        base_grid_size = config.initial_grid_size
        if level == 1:
            grid_size = base_grid_size
        else:
            grid_size = base_grid_size + level

        # Apply difficulty modifiers
        if config.difficulty == "Easy":
            # Larger grid = easier game
            grid_size = max(5, int(grid_size * 1.3))
        elif config.difficulty == "Hard":
            # Smaller grid = harder game (but ensure minimum of 4 for Hard)
            grid_size = max(4, int(grid_size * 0.7))
        # Normal difficulty uses default grid size

        logging.info(
            f"Initializing environment repository for level {level} with grid size {grid_size} (difficulty: {config.difficulty})"
        )
        self.environment = Environment("Level " + str(level), grid_size)

        self.collision = False
        self.running = True

        # Power-up system
        self.active_power_ups = []  # List of currently active power-ups
        self.power_up_spawn_chance = (
            0.05  # 5% chance to spawn power-up when food is eaten
        )

    def get_rows(self) -> int:
        return self.environment.getGrid().getRows()

    def get_columns(self) -> int:
        return self.environment.getGrid().getColumns()

    def get_locations(self) -> list:
        return self.environment.getGrid().getLocations()

    def get_location(self, x: int, y: int) -> Any:
        return self.environment.getGrid().getLocation(x, y)

    def get_num_locations(self) -> int:
        return len(self.environment.getGrid().getLocations())

    def get_location_of_entity(self, entity: Entity) -> Optional[Location]:
        location_id = entity.getLocationID()
        if location_id is None:
            return None
        return self.environment.getGrid().getLocation(location_id)

    def get_location_above_entity(self, entity: Entity) -> Optional[Location]:
        current_location = self.get_location_of_entity(entity)
        if current_location is None:
            return None
        grid = self.environment.getGrid()
        return grid.getUp(current_location)

    def get_location_left_of_entity(self, entity: Entity) -> Optional[Location]:
        current_location = self.get_location_of_entity(entity)
        if current_location is None:
            return None
        grid = self.environment.getGrid()
        return grid.getLeft(current_location)

    def get_location_below_entity(self, entity: Entity) -> Optional[Location]:
        current_location = self.get_location_of_entity(entity)
        if current_location is None:
            return None
        grid = self.environment.getGrid()
        return grid.getDown(current_location)

    def get_location_right_of_entity(self, entity: Entity) -> Optional[Location]:
        current_location = self.get_location_of_entity(entity)
        if current_location is None:
            return None
        grid = self.environment.getGrid()
        return grid.getRight(current_location)

    def get_location_in_random_direction(self, location: Location) -> Location:
        directions = ["up", "down", "left", "right"]
        direction = random.choice(directions)
        if direction == "up":
            return self.environment.getGrid().getUp(location)
        elif direction == "down":
            return self.environment.getGrid().getDown(location)
        elif direction == "left":
            return self.environment.getGrid().getLeft(location)
        elif direction == "right":
            return self.environment.getGrid().getRight(location)
        else:
            raise ValueError("Invalid direction")

    def get_location_in_direction_of_entity(
        self, param: int, snake_part: SnakePart
    ) -> Optional[Location]:
        location_of_snake_part = self.get_location_of_entity(snake_part)
        if location_of_snake_part is None:
            return None
        if param == 0:
            return self.environment.getGrid().getUp(location_of_snake_part)
        elif param == 1:
            return self.environment.getGrid().getLeft(location_of_snake_part)
        elif param == 2:
            return self.environment.getGrid().getDown(location_of_snake_part)
        elif param == 3:
            return self.environment.getGrid().getRight(location_of_snake_part)
        else:
            raise ValueError("Invalid direction parameter: " + str(param))

    def get_random_location(self) -> Location:
        rows = self.environment.getGrid().getRows()
        columns = self.environment.getGrid().getColumns()
        x = random.randint(0, rows - 1)
        y = random.randint(0, columns - 1)
        return self.environment.getGrid().getLocationByCoordinates(x, y)

    def add_entity_to_random_location(self, selected_snake_part: SnakePart) -> None:
        random_location = self.get_random_location()
        if random_location is not None:
            self.add_entity_to_location(selected_snake_part, random_location)
        else:
            raise Exception("No valid location found to add entity")

    def add_entity_to_location(self, entity: Entity, location: Any) -> None:
        self.environment.addEntityToLocation(entity, location)

    def remove_entity_from_location(self, entity: Entity) -> None:
        self.environment.removeEntity(entity)

    def get_location_by_id(self, location_id: str) -> Location:
        location = self.environment.getGrid().getLocation(location_id)
        if location is None:
            raise Exception(f"Location with ID {location_id} not found")
        return location

    def spawn_snake_part(self, snake_part: SnakePart, color: tuple) -> None:
        new_snake_part = SnakePart(color)
        snake_part.setPrevious(new_snake_part)
        new_snake_part.setNext(snake_part)

        location = self.get_location_of_entity(snake_part)
        while True:
            target_location = self.get_location_in_random_direction(location)
            location_in_current_direction_of_snake_part = (
                self.get_location_in_direction_of_entity(
                    snake_part.getDirection(), snake_part
                )
            )
            if (
                target_location != -1
                and target_location != location_in_current_direction_of_snake_part
            ):
                break

        self.add_entity_to_location(new_snake_part, target_location)
        self.snake_part_repository.append(new_snake_part)

    def spawn_food(self) -> None:
        food = Food(
            (
                random.randrange(50, 200),
                random.randrange(50, 200),
                random.randrange(50, 200),
            )
        )

        target_location = -1
        not_found = True
        while not_found:
            target_location = self.get_random_location()
            if target_location.getNumEntities() == 0:
                not_found = False

        self.add_entity_to_location(food, target_location)

    def spawn_power_up(self) -> None:
        """Spawn a random power-up at an empty location."""
        # Choose a random power-up type
        power_up_types = list(PowerUpType)
        power_up_type = random.choice(power_up_types)

        # Create power-up with type-specific properties
        if power_up_type == PowerUpType.SPEED_BOOST:
            color = (255, 165, 0)  # Orange
            duration = 8.0
        elif power_up_type == PowerUpType.SLOW_TIME:
            color = (0, 191, 255)  # Blue
            duration = 10.0
        elif power_up_type == PowerUpType.INVINCIBILITY:
            color = (255, 20, 147)  # Pink
            duration = 5.0
        elif power_up_type == PowerUpType.SCORE_MULTIPLIER:
            color = (255, 215, 0)  # Gold
            duration = 12.0
        else:
            color = (255, 255, 0)  # Yellow (default)
            duration = 10.0

        power_up = PowerUp(power_up_type, duration, color)

        # Find an empty location to spawn the power-up
        target_location = -1
        not_found = True
        attempts = 0
        max_attempts = 100  # Prevent infinite loop

        while not_found and attempts < max_attempts:
            target_location = self.get_random_location()
            if target_location.getNumEntities() == 0:
                not_found = False
            attempts += 1

        if not not_found:  # Successfully found a location
            self.add_entity_to_location(power_up, target_location)
            logging.info(f"Spawned power-up: {power_up_type.value} at location")
        else:
            logging.warning("Could not find empty location to spawn power-up")

    def update_power_ups(self) -> None:
        """Update active power-ups and remove expired ones."""
        expired_power_ups = []
        for power_up in self.active_power_ups:
            if power_up.is_expired():
                expired_power_ups.append(power_up)
                power_up.deactivate()

        # Remove expired power-ups
        for power_up in expired_power_ups:
            self.active_power_ups.remove(power_up)
            logging.info(f"Power-up expired: {power_up.get_power_up_type().value}")

    def get_active_power_ups(self) -> list:
        """Get list of currently active power-ups."""
        return self.active_power_ups.copy()

    def move_entity(self, entity: Entity, direction: int) -> bool:
        check_for_level_progress_and_reinitialize = False

        if direction == 0:
            new_location = self.get_location_above_entity(entity)
        elif direction == 1:
            new_location = self.get_location_left_of_entity(entity)
        elif direction == 2:
            new_location = self.get_location_below_entity(entity)
        elif direction == 3:
            new_location = self.get_location_right_of_entity(entity)
        else:
            logging.error("Error: Invalid direction specified for entity movement.")
            raise ValueError("Invalid direction specified for entity movement.")

        if new_location == -1:
            return False

        for eid in new_location.getEntities():
            e = new_location.getEntity(eid)
            if type(e) is SnakePart:
                self.collision = True
                logging.info("The ophidian collides with itself and ceases to be.")
                time.sleep(self.config.tick_speed * 20)
                if self.config.restart_upon_collision:
                    check_for_level_progress_and_reinitialize = True
                else:
                    self.running = False

        location = self.get_location_of_entity(entity)
        self.remove_entity_from_location(entity)
        new_location.addEntity(entity)
        entity.lastPosition = location

        if entity.hasPrevious():
            self.move_previous_snake_part(entity)

        # Check for food collision
        food = -1
        for eid in new_location.getEntities():
            e = new_location.getEntity(eid)
            if type(e) is Food:
                food = e

        # Check for power-up collision
        power_up = -1
        for eid in new_location.getEntities():
            e = new_location.getEntity(eid)
            if type(e) is PowerUp:
                power_up = e

        # Handle food consumption
        if food != -1:
            food.getColor()
            self.remove_entity_from_location(food)
            self.spawn_food()
            self.spawn_snake_part(
                entity.getTail(), SnakeColorGenerator.generate_green_shade()
            )

            # Randomly spawn power-up when food is eaten
            if random.random() < self.power_up_spawn_chance:
                self.spawn_power_up()

        # Handle power-up collection
        if power_up != -1:
            power_up.activate()
            self.active_power_ups.append(power_up)
            self.remove_entity_from_location(power_up)
            logging.info(f"Power-up collected: {power_up.get_power_up_type().value}")

        return check_for_level_progress_and_reinitialize

    def move_previous_snake_part(self, snake_part: SnakePart) -> None:
        previous_snake_part = snake_part.previousSnakePart
        previous_snake_part_location = self.get_location_of_entity(previous_snake_part)

        if previous_snake_part_location == -1:
            logging.error(
                "Error: A previous snake part's location was unexpectantly -1."
            )

        target_location = snake_part.lastPosition

        previous_snake_part_location.removeEntity(previous_snake_part)
        target_location.addEntity(previous_snake_part)
        previous_snake_part.lastPosition = previous_snake_part_location

        if previous_snake_part.hasPrevious():
            self.move_previous_snake_part(previous_snake_part)

    def clear(self) -> None:
        entities_to_remove_from_environment = []
        for locationId in self.environment.getGrid().getLocations():
            location = self.environment.getGrid().getLocation(locationId)
            for entity in location.getEntities().values():
                if (
                    isinstance(entity, SnakePart)
                    or isinstance(entity, Food)
                    or isinstance(entity, PowerUp)
                ):
                    entities_to_remove_from_environment.append(entity)
        for entity in entities_to_remove_from_environment:
            self.environment.removeEntity(entity)
        self.snake_part_repository.clear()

        # Clear active power-ups
        self.active_power_ups.clear()

    def reinitialize(self, level):
        self.level = level

        # Determine grid size based on level
        if self.level == 1:
            grid_size = self.config.initial_grid_size
        else:
            grid_size = self.config.initial_grid_size + self.level

        self.environment = Environment("Level " + str(level), grid_size)

        self.collision = False
        self.running = True
