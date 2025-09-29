import logging
import os

log_level = os.environ.get("LOG_LEVEL", "INFO").upper()
logging.basicConfig(level=getattr(logging, log_level))
logger = logging.getLogger(__name__)


class GameScore:
    def __init__(self, snake_part_repository, environment_repository):
        self.current_points = 0
        self.cumulative_points = 0
        self.snake_part_repository = snake_part_repository
        self.environment_repository = environment_repository

    def calculate(self):
        length = self.snake_part_repository.get_length()
        num_locations = self.environment_repository.get_num_locations()
        percentage = int(length / num_locations * 100)
        self.current_points = length * percentage
        return self.current_points

    def display_stats(self):
        length = self.snake_part_repository.get_length()
        num_locations = self.environment_repository.get_num_locations()
        percentage = int(length / num_locations * 100)
        logging.info("The ophidian had a length of %d", length)
        logging.info("The ophidian took up %d percent of the world", percentage)
        logging.info("Level Score: %d", self.current_points)
        logging.info("Total Score: %d", self.cumulative_points)
        logging.info("-----")

    def reset(self):
        self.current_points = 0

    def level_complete(self):
        """Call this method when a level is successfully completed to add current points to cumulative score"""
        self.cumulative_points += self.current_points
        self.current_points = 0
