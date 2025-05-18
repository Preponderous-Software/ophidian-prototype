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
        self.initializeGameDisplay()
        pygame.display.set_icon(pygame.image.load("src/media/icon.PNG"))
        self.graphik = Graphik(self.gameDisplay)
        self.running = True
        self.snakeParts = []
        self.level = 1
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
        self.locationWidth = x / self.environment.getGrid().getRows()
        self.locationHeight = y / self.environment.getGrid().getColumns()

    # Draws the environment in its entirety.
    def drawEnvironment(self):
        for locationId in self.environment.getGrid().getLocations():
            location = self.environment.getGrid().getLocation(locationId)
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
        length = len(self.snakeParts)
        numLocations = len(self.environment.grid.getLocations())
        percentage = int(length / numLocations * 100)
        self.score = length * percentage

    def displayStatsInConsole(self):
        length = len(self.snakeParts)
        numLocations = len(self.environment.grid.getLocations())
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
            len(self.snakeParts)
            > len(self.environment.grid.getLocations())
            * self.config.levelProgressPercentageRequired
        ):
            self.level += 1
        self.initialize()

    def quitApplication(self):
        self.displayStatsInConsole()
        pygame.quit()
        quit()

    def getLocation(self, entity: Entity):
        locationID = entity.getLocationID()
        grid = self.environment.getGrid()
        return grid.getLocation(locationID)

    def getLocationAndGrid(self, entity: Entity):
        locationID = entity.getLocationID()
        grid = self.environment.getGrid()
        return grid, grid.getLocation(locationID)

    def moveEntity(self, entity: Entity, direction):
        grid, location = self.getLocationAndGrid(entity)

        newLocation = -1
        # get new location
        if direction == 0:
            newLocation = grid.getUp(location)
        elif direction == 1:
            newLocation = grid.getLeft(location)
        elif direction == 2:
            newLocation = grid.getDown(location)
        elif direction == 3:
            newLocation = grid.getRight(location)

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
        location.removeEntity(entity)
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

    def getRandomDirection(self, grid: Grid, location: Location):
        direction = random.randrange(0, 4)
        if direction == 0:
            return grid.getUp(location)
        elif direction == 1:
            return grid.getRight(location)
        elif direction == 2:
            return grid.getDown(location)
        elif direction == 3:
            return grid.getLeft(location)

    def getLocationDirection(self, direction, grid, location):
        if direction == 0:
            return grid.getUp(location)
        elif direction == 1:
            return grid.getLeft(location)
        elif direction == 2:
            return grid.getDown(location)
        elif direction == 3:
            return grid.getRight(location)

    def getLocationOppositeDirection(self, direction, grid, location):
        if direction == 0:
            return grid.getDown(location)
        elif direction == 1:
            return grid.getRight(location)
        elif direction == 2:
            return grid.getUp(location)
        elif direction == 3:
            return grid.getLeft(location)

    def spawnSnakePart(self, snakePart: SnakePart, color):
        newSnakePart = SnakePart(color)
        snakePart.setPrevious(newSnakePart)
        newSnakePart.setNext(snakePart)
        grid, location = self.getLocationAndGrid(snakePart)

        targetLocation = -1
        while True:
            targetLocation = self.getRandomDirection(grid, location)
            if targetLocation != -1 and targetLocation != self.getLocationDirection(
                snakePart.getDirection(), grid, location
            ):
                break

        self.environment.addEntityToLocation(newSnakePart, targetLocation)
        self.snakeParts.append(newSnakePart)

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
            targetLocation = self.environment.getGrid().getRandomLocation()
            if targetLocation.getNumEntities() == 0:
                notFound = False

        self.environment.addEntity(food)

    def initialize(self):
        self.collision = False
        self.score = 0
        self.snakeParts = []
        self.tick = 0
        if self.level == 1:
            self.environment = Environment(
                "Level " + str(self.level), self.config.gridSize
            )
        else:
            self.environment = Environment(
                "Level " + str(self.level), self.config.gridSize + (self.level - 1) * 2
            )
        self.initializeLocationWidthAndHeight()
        pygame.display.set_caption("Ophidian - Level " + str(self.level))
        self.selectedSnakePart = SnakePart(
            (
                random.randrange(50, 200),
                random.randrange(50, 200),
                random.randrange(50, 200),
            )
        )
        self.environment.addEntity(self.selectedSnakePart)
        self.snakeParts.append(self.selectedSnakePart)
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
            percentage = len(self.snakeParts) / len(
                self.environment.grid.getLocations()
            )
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
