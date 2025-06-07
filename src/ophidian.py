import random
import time

import pygame

from config.config import Config
from environment.environmentRepository import EnvironmentRepository
from input.keyDownEventHandler import KeyDownEventHandler
from lib.graphik.src.graphik import Graphik
from snake.snakePart import SnakePart
from snake.snakePartRepository import SnakePartRepository
from graphics.renderer import Renderer


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
        self.snake_part_repository = SnakePartRepository()
        self.level = 1
        self.environment_repository = EnvironmentRepository(self.level, self.config.grid_size, self.snake_part_repository, self.config)
        self.tick = 0
        self.score = 0
        self.changed_direction_this_tick = False
        self.collision = False
        self.renderer = Renderer(self.graphik, self.collision, self.config, self.environment_repository,self.snake_part_repository)
        self.initialize()

    def initialize_game_display(self):
        if self.config.fullscreen:
            self.game_display = pygame.display.set_mode(
                (self.config.display_width, self.config.display_height), pygame.FULLSCREEN
            )
        else:
            self.game_display = pygame.display.set_mode(
                (self.config.display_width, self.config.display_height), pygame.RESIZABLE
            )

    def calculate_score(self):
        length = self.snake_part_repository.get_length()
        num_locations = self.environment_repository.get_num_locations()
        percentage = int(length / num_locations * 100)
        self.score = length * percentage

    def display_stats_in_console(self):
        length = self.snake_part_repository.get_length()
        num_locations = self.environment_repository.get_num_locations()
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
            self.snake_part_repository.get_length()
            > self.environment_repository.get_num_locations()
            * self.config.level_progress_percentage_required
        ):
            self.level += 1
        self.environment_repository = EnvironmentRepository(self.level, self.config.grid_size, self.snake_part_repository, self.config)
        self.snake_part_repository.clear()
        self.initialize()

    def quit_application(self):
        self.display_stats_in_console()
        pygame.quit()
        quit()

    def handle_key_down_event(self, key):
        key_down_event_handler = KeyDownEventHandler(
            self.config, self.game_display, self.selected_snake_part
        )
        result = key_down_event_handler.handle_key_down_event(key)
        if result == "quit":
            self.quit_application()
            return None
        elif result == "restart":
            self.check_for_level_progress_and_reinitialize()
            return "restart"
        elif result == "initialize game display":
            self.initialize_game_display()
            return None
        return None

    def initialize(self):
        self.collision = False
        self.score = 0
        self.tick = 0
        self.renderer.initialize_location_width_and_height()
        pygame.display.set_caption("Ophidian - Level " + str(self.level))
        self.selected_snake_part = SnakePart(
            (
                random.randrange(50, 200),
                random.randrange(50, 200),
                random.randrange(50, 200),
            )
        )
        self.environment_repository.add_entity_to_random_location(self.selected_snake_part)
        self.snake_part_repository.append(self.selected_snake_part)
        print("The ophidian enters the world.")
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

            if self.selected_snake_part.getDirection() == 0:
                self.environment_repository.move_entity(self.selected_snake_part, 0, self.check_for_level_progress_and_reinitialize)
            elif self.selected_snake_part.getDirection() == 1:
                self.environment_repository.move_entity(self.selected_snake_part, 1, self.check_for_level_progress_and_reinitialize)
            elif self.selected_snake_part.getDirection() == 2:
                self.environment_repository.move_entity(self.selected_snake_part, 2, self.check_for_level_progress_and_reinitialize)
            elif self.selected_snake_part.getDirection() == 3:
                self.environment_repository.move_entity(self.selected_snake_part, 3, self.check_for_level_progress_and_reinitialize)

            self.calculate_score()
            self.renderer.draw()

            pygame.display.update()

            if self.config.limit_tick_speed:
                time.sleep(self.config.tick_speed)
                self.tick += 1
                self.changed_direction_this_tick = False

        self.quit_application()


ophidian = Ophidian()
ophidian.run()
