import random
import time

import pygame
from config.config import Config
from lib.pyenvlib.entity import Entity
from food.food import Food
from lib.graphik.src.graphik import Graphik
from snake.snakePart import SnakePart
from snake.snakePartRepository import SnakePartRepository
from environment.environmentRepository import EnvironmentRepository


# @author Daniel McCoy Stephenson
# @since August 6th, 2022
class Ophidian:
    def __init__(self):
        pygame.init()
        self.config = Config()
        self.initializeGameDisplay()
        pygame.display.set_icon(pygame.image.load("src/media/icon.PNG"))
        self.graphik = Graphik(self.gameDisplay)
        self.running = True
        self.snakePartRepository = SnakePartRepository()
        self.level = 1
        self.environment_repository = EnvironmentRepository(self.level, self.config.gridSize)
        self.initialize()
        self.tick = 0
        self.score = 0
        self.changedDirectionThisTick = False
        self.collision = False

    def initializeGameDisplay(self):
        if self.config.fullscreen:
            self.gameDisplay = pygame.display.set_mode(
                (self.config.displayWidth, self.config.displayHeight), pygame.FULLSCREEN
            )
        else:
            self.gameDisplay = pygame.display.set_mode(
                (self.config.displayWidth, self.config.displayHeight), pygame.RESIZABLE
            )

    def initializeLocationWidthAndHeight(self):
        x, y = self.gameDisplay.get_size()
        self.locationWidth = x / self.environment_repository.get_rows()
        self.locationHeight = y / self.environment_repository.get_columns()

    # Draws the environment in its entirety.
    def drawEnvironment(self):
        for locationId in self.environment_repository.get_locations():
            location = self.environment_repository.get_location_by_id(locationId)
            self.drawLocation(
                location,
                location.getX() * self.locationWidth - 1,
                location.getY() * self.locationHeight - 1,
                self.locationWidth + 2,
                self.locationHeight + 2,
            )

    # Returns the color that a location should be displayed as.
    def getColorOfLocation(self, location):
        if location == -1:
            color = self.config.white
        else:
            color = self.config.white
            if location.getNumEntities() > 0:
                topEntityId = list(location.getEntities().keys())[-1]
                topEntity = location.getEntity(topEntityId)
                return topEntity.getColor()
        return color

    # Draws a location at a specified position.
    def drawLocation(self, location, xPos, yPos, width, height):
        if self.collision == True:
            color = self.config.red
        else:
            color = self.getColorOfLocation(location)
        self.graphik.drawRectangle(xPos, yPos, width, height, color)

    def calculateScore(self):
        length = self.snakePartRepository.get_length()
        numLocations = self.environment_repository.get_num_locations()
        percentage = int(length / numLocations * 100)
        self.score = length * percentage

    def displayStatsInConsole(self):
        length = self.snakePartRepository.get_length()
        numLocations = self.environment_repository.get_num_locations()
        percentage = int(length / numLocations * 100)
        print(
            "The ophidian had a length of",
            length,
            "and took up",
            percentage,
            "percent of the world.",
        )
        print("Score:", self.score)
        print("-----")

    def checkForLevelProgressAndReinitialize(self):
        if (
            self.snakePartRepository.get_length()
            > self.environment_repository.get_num_locations()
            * self.config.levelProgressPercentageRequired
        ):
            self.level += 1
        self.environment_repository = EnvironmentRepository(self.level, self.config.gridSize)
        self.snakePartRepository.clear()
        self.initialize()

    def quitApplication(self):
        self.displayStatsInConsole()
        pygame.quit()
        quit()

    def getLocation(self, entity: Entity):
        return self.environment_repository.get_location_of_entity(entity)

    def moveEntity(self, entity: Entity, direction):
        # get new location
        if direction == 0:
            newLocation = self.environment_repository.get_location_above_entity(entity)
        elif direction == 1:
            newLocation = self.environment_repository.get_location_left_of_entity(entity)
        elif direction == 2:
            newLocation = self.environment_repository.get_location_below_entity(entity)
        elif direction == 3:
            newLocation = self.environment_repository.get_location_right_of_entity(entity)
        else:
            print("Error: Invalid direction specified for entity movement.")
            return

        if newLocation == -1:
            # location doesn't exist, we're at a border
            return

        # if new location has a snake part already
        for eid in newLocation.getEntities():
            e = newLocation.getEntity(eid)
            if type(e) is SnakePart:
                # we have a collision
                self.collision = True
                print("The ophidian collides with itself and ceases to be.")
                self.drawEnvironment()
                pygame.display.update()
                time.sleep(self.config.tickSpeed * 20)
                if self.config.restartUponCollision:
                    self.checkForLevelProgressAndReinitialize()
                else:
                    self.running = False
                return

        # move entity
        location = self.getLocation(entity)
        self.environment_repository.remove_entity_from_location(entity)
        newLocation.addEntity(entity)
        entity.lastPosition = location

        # move all attached snake parts
        if entity.hasPrevious():
            self.movePreviousSnakePart(entity)

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
        for eid in newLocation.getEntities():
            e = newLocation.getEntity(eid)
            if type(e) is Food:
                food = e

        if food == -1:
            return

        foodColor = food.getColor()

        self.removeEntity(food)
        self.spawnFood()
        self.spawnSnakePart(entity.getTail(), foodColor)
        self.calculateScore()

    def movePreviousSnakePart(self, snakePart):
        previousSnakePart = snakePart.previousSnakePart

        previousSnakePartLocation = self.getLocation(previousSnakePart)

        if previousSnakePartLocation == -1:
            print("Error: A previous snake part's location was unexpectantly -1.")
            time.sleep(1)
            self.quitApplication()

        targetLocation = snakePart.lastPosition

        # move entity
        previousSnakePartLocation.removeEntity(previousSnakePart)
        targetLocation.addEntity(previousSnakePart)
        previousSnakePart.lastPosition = previousSnakePartLocation

        if previousSnakePart.hasPrevious():
            self.movePreviousSnakePart(previousSnakePart)

    def removeEntityFromLocation(self, entity: Entity):
        location = self.getLocation(entity)
        if location.isEntityPresent(entity):
            location.removeEntity(entity)

    def removeEntity(self, entity: Entity):
        self.removeEntityFromLocation(entity)

    def handleKeyDownEvent(self, key):
        if key == pygame.K_q:
            self.running = False
        elif key == pygame.K_w or key == pygame.K_UP:
            if (
                self.changedDirectionThisTick == False
                and self.selectedSnakePart.getDirection() != 2
            ):
                self.selectedSnakePart.setDirection(0)
                self.changedDirectionThisTick = True
        elif key == pygame.K_a or key == pygame.K_LEFT:
            if (
                self.changedDirectionThisTick == False
                and self.selectedSnakePart.getDirection() != 3
            ):
                self.selectedSnakePart.setDirection(1)
                self.changedDirectionThisTick = True
        elif key == pygame.K_s or key == pygame.K_DOWN:
            if (
                self.changedDirectionThisTick == False
                and self.selectedSnakePart.getDirection() != 0
            ):
                self.selectedSnakePart.setDirection(2)
                self.changedDirectionThisTick = True
        elif key == pygame.K_d or key == pygame.K_RIGHT:
            if (
                self.changedDirectionThisTick == False
                and self.selectedSnakePart.getDirection() != 1
            ):
                self.selectedSnakePart.setDirection(3)
                self.changedDirectionThisTick = True
        elif key == pygame.K_F11:
            if self.config.fullscreen:
                self.config.fullscreen = False
            else:
                self.config.fullscreen = True
            self.initializeGameDisplay()
        elif key == pygame.K_l:
            if self.config.limitTickSpeed:
                self.config.limitTickSpeed = False
            else:
                self.config.limitTickSpeed = True
        elif key == pygame.K_r:
            self.checkForLevelProgressAndReinitialize()
            return "restart"

    def spawnSnakePart(self, snakePart: SnakePart, color):
        newSnakePart = SnakePart(color)
        snakePart.setPrevious(newSnakePart)
        newSnakePart.setNext(snakePart)

        location = self.environment_repository.get_location_of_entity(snakePart)
        while True:
            targetLocation = self.environment_repository.get_location_in_random_direction(location)
            location_in_current_direction_of_snake_part = self.environment_repository.get_location_in_direction_of_entity(snakePart.getDirection(), snakePart)
            if targetLocation != -1 and targetLocation != location_in_current_direction_of_snake_part:
                break

        self.environment_repository.add_entity_to_location(newSnakePart, targetLocation)
        self.snakePartRepository.append(newSnakePart)

    def spawnFood(self):
        food = Food(
            (
                random.randrange(50, 200),
                random.randrange(50, 200),
                random.randrange(50, 200),
            )
        )

        # get target location
        targetLocation = -1
        notFound = True
        while notFound:
            targetLocation = self.environment_repository.get_random_location()
            if targetLocation.getNumEntities() == 0:
                notFound = False

        self.environment_repository.add_entity_to_location(food, targetLocation)

    def initialize(self):
        self.collision = False
        self.score = 0
        self.tick = 0
        self.initializeLocationWidthAndHeight()
        pygame.display.set_caption("Ophidian - Level " + str(self.level))
        self.selectedSnakePart = SnakePart(
            (
                random.randrange(50, 200),
                random.randrange(50, 200),
                random.randrange(50, 200),
            )
        )
        self.environment_repository.add_entity_to_random_location(self.selectedSnakePart)
        self.snakePartRepository.append(self.selectedSnakePart)
        print("The ophidian enters the world.")
        self.spawnFood()

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quitApplication()
                elif event.type == pygame.KEYDOWN:
                    result = self.handleKeyDownEvent(event.key)
                    if result == "restart":
                        continue
                elif event.type == pygame.WINDOWRESIZED:
                    self.initializeLocationWidthAndHeight()

            if self.selectedSnakePart.getDirection() == 0:
                self.moveEntity(self.selectedSnakePart, 0)
            elif self.selectedSnakePart.getDirection() == 1:
                self.moveEntity(self.selectedSnakePart, 1)
            elif self.selectedSnakePart.getDirection() == 2:
                self.moveEntity(self.selectedSnakePart, 2)
            elif self.selectedSnakePart.getDirection() == 3:
                self.moveEntity(self.selectedSnakePart, 3)

            self.gameDisplay.fill(self.config.white)
            self.drawEnvironment()
            x, y = self.gameDisplay.get_size()

            # draw progress bar
            percentage = self.snakePartRepository.get_length() / self.environment_repository.get_num_locations()
            pygame.draw.rect(self.gameDisplay, self.config.black, (0, y - 20, x, 20))
            if percentage < self.config.levelProgressPercentageRequired / 2:
                pygame.draw.rect(
                    self.gameDisplay, self.config.red, (0, y - 20, x * percentage, 20)
                )
            elif percentage < self.config.levelProgressPercentageRequired:
                pygame.draw.rect(
                    self.gameDisplay,
                    self.config.yellow,
                    (0, y - 20, x * percentage, 20),
                )
            else:
                pygame.draw.rect(
                    self.gameDisplay, self.config.green, (0, y - 20, x * percentage, 20)
                )
            pygame.draw.rect(self.gameDisplay, self.config.black, (0, y - 20, x, 20), 1)

            pygame.display.update()

            if self.config.limitTickSpeed:
                time.sleep(self.config.tickSpeed)
                self.tick += 1
                self.changedDirectionThisTick = False

        self.quitApplication()


ophidian = Ophidian()
ophidian.run()
