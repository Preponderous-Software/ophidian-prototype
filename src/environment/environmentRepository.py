from abc import ABC, abstractmethod
from typing import Optional, Any


class EnvironmentRepository(ABC):
    """Interface defining environment operations for the game"""

    @abstractmethod
    def get_rows(self) -> int:
        """Returns the number of rows in the environment grid"""
        pass

    @abstractmethod
    def get_columns(self) -> int:
        """Returns the number of columns in the environment grid"""
        pass

    @abstractmethod
    def get_locations(self) -> list:
        """Returns all locations in the environment"""
        pass

    @abstractmethod
    def get_location(self, x: int, y: int) -> Any:
        """Returns location at the specified coordinates"""
        pass

    @abstractmethod
    def get_num_locations(self):
        pass

    @abstractmethod
    def get_location_of_entity(self, entity) -> Optional[Any]:
        """Returns the location of the specified entity"""
        pass

    @abstractmethod
    def get_location_above_entity(self, entity):
        pass

    @abstractmethod
    def get_location_left_of_entity(self, entity):
        pass

    @abstractmethod
    def get_location_below_entity(self, entity):
        pass

    @abstractmethod
    def get_location_right_of_entity(self, entity):
        pass

    @abstractmethod
    def get_location_in_random_direction(self, location):
        pass

    @abstractmethod
    def get_location_in_direction_of_entity(self, param, snakePart):
        pass

    @abstractmethod
    def get_random_location(self) -> Any:
        """Returns a random location in the environment"""
        pass

    @abstractmethod
    def add_entity_to_random_location(self, selectedSnakePart):
        pass

    @abstractmethod
    def add_entity_to_location(self, entity, location: Any) -> None:
        """Adds an entity to the specified location"""
        pass

    @abstractmethod
    def remove_entity_from_location(self, entity) -> None:
        """Removes an entity from its current location"""
        pass

    @abstractmethod
    def get_location_by_id(self, locationId):
        pass


    @abstractmethod
    def spawn_snake_part(self, snake_part, color):
        pass

    @abstractmethod
    def spawn_food(self):
        pass

    @abstractmethod
    def move_entity(self, entity, direction):
        pass

    @abstractmethod
    def move_previous_snake_part(self, snake_part):
        pass

    @abstractmethod
    def clear(self):
        pass

    @abstractmethod
    def reinitialize(self, level: int, increase_grid_size: bool) -> None:
        """Reinitializes the environment with the specified parameters"""
        pass