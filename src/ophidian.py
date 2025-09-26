import os
import random
import time
import logging

import pygame

from src.config.config import Config
from src.graphics.renderer import Renderer
from src.input.keyDownEventHandler import KeyDownEventHandler
from src.snake.snakePart import SnakePart
from src.snake.snakePartRepository import SnakePartRepository
from src.snake.snakeColorGenerator import SnakeColorGenerator
from src.environment.pyEnvLibEnvironmentRepositoryImpl import PyEnvLibEnvironmentRepositoryImpl
from src.score.game_score import GameScore
from src.state.game_state_repository import GameStateRepository

log_level = os.environ.get('LOG_LEVEL', 'INFO').upper()
logging.basicConfig(level=getattr(logging, log_level))
logger = logging.getLogger(__name__)

# @author Daniel McCoy Stephenson
# @since August 6th, 2022
class Ophidian:
    def __init__(self):
        pygame.init()
        pygame.display.set_icon(pygame.image.load("src/media/icon.PNG"))

        self.running = True
        self.state_repository = GameStateRepository()

        # Load saved state or use defaults
        saved_state = self.state_repository.load()
        if saved_state:
            self.level = saved_state.level
        else:
            self.level = 1

        self.tick = 0
        self.changed_direction_this_tick = False
        self.collision = False

        self.config = Config()
        self.snake_part_repository = SnakePartRepository()
        self.environment_repository = PyEnvLibEnvironmentRepositoryImpl(
            self.level,
            self.config,
            self.snake_part_repository
        )
        self.game_score = GameScore(self.snake_part_repository, self.environment_repository)
        # Load saved state or use defaults
        if saved_state:
            self.game_score.current_points = saved_state.current_score
            self.game_score.cumulative_points = saved_state.cumulative_score
        else:
            self.game_score.current_points = 0
            self.game_score.cumulative_points = 0
        self.renderer = Renderer(
            self.collision,
            self.config,
            self.environment_repository,
            self.snake_part_repository,
            self.game_score
        )
        self.initialize()

    def save_game_state(self):
        """Save current game state"""
        state = {
            'level': self.level,
            'current_score': self.game_score.current_points,
            'cumulative_score': self.game_score.cumulative_points
        }
        self.state_repository.save(state)

    def check_for_level_progress_and_reinitialize(self):
        logging.info("Checking for level progress...")
        if (
                self.snake_part_repository.get_length()
                > self.environment_repository.get_num_locations()
                * self.config.level_progress_percentage_required
        ):
            logging.info("The ophidian has progressed to the next level.")
            self.game_score.level_complete()
            self.level += 1
        else:
            self.game_score.reset()

        self.save_game_state()

        logging.info("Reinitializing the environment...")
        self.environment_repository.reinitialize(self.level)
        logging.info("Clearing the environment repository")
        self.environment_repository.clear()
        logging.info("Re-initializing the game")
        self.initialize()

    def quit_application(self):
        self.save_game_state()
        self.game_score.display_stats()
        pygame.quit()
        quit()

    def handle_key_down_event(self, key):
        key_down_event_handler = KeyDownEventHandler(
            self.config, self.renderer.graphik.gameDisplay, self.selected_snake_part
        )
        result = key_down_event_handler.handle_key_down_event(key)
        if result == "quit":
            logging.info("Quiting the application...")
            self.quit_application()
            return None
        elif result == "restart":
            logging.info("Restarting the game...")
            # Reset score when manually restarting
            self.game_score.reset()
            self.check_for_level_progress_and_reinitialize()
            return "restart"
        elif result == "initialize game display":
            logging.info("Re-initializing the game display...")
            self.renderer.initialize_game_display()
            return None
        return None

    def initialize(self):
        self.collision = False
        self.tick = 0
        self.renderer.initialize_location_width_and_height()
        pygame.display.set_caption("Ophidian - Level " + str(self.level))
        self.selected_snake_part = SnakePart(
            SnakeColorGenerator.generate_green_shade()
        )
        self.environment_repository.add_entity_to_random_location(self.selected_snake_part)
        self.snake_part_repository.append(self.selected_snake_part)
        logging.info("The ophidian enters the world.")
        self.environment_repository.spawn_food()

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
                    self.renderer.initialize_location_width_and_height()

            check_for_level_progress_and_reinitialize = False
            if self.selected_snake_part.getDirection() == 0:
                check_for_level_progress_and_reinitialize = self.environment_repository.move_entity(self.selected_snake_part, 0)
            elif self.selected_snake_part.getDirection() == 1:
                check_for_level_progress_and_reinitialize = self.environment_repository.move_entity(self.selected_snake_part, 1)
            elif self.selected_snake_part.getDirection() == 2:
                check_for_level_progress_and_reinitialize = self.environment_repository.move_entity(self.selected_snake_part, 2)
            elif self.selected_snake_part.getDirection() == 3:
                check_for_level_progress_and_reinitialize = self.environment_repository.move_entity(self.selected_snake_part, 3)

            if (check_for_level_progress_and_reinitialize):
                self.check_for_level_progress_and_reinitialize()

            self.game_score.calculate()
            self.renderer.draw()

            pygame.display.update()

            if self.config.limit_tick_speed:
                time.sleep(self.config.tick_speed)
                self.tick += 1
                self.changed_direction_this_tick = False

        self.quit_application()


ophidian = Ophidian()
ophidian.run()
