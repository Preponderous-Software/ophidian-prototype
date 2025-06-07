import random
import time
import pygame
from Viron.src.main.python.preponderous.viron.models.entity import Entity
from Viron.src.main.python.preponderous.viron.models.environment import Environment
from Viron.src.main.python.preponderous.viron.models.grid import Grid
from Viron.src.main.python.preponderous.viron.models.location import Location
from config.config import Config
from food.food import Food
from lib.graphik.src.graphik import Graphik
from snake.snakePart import SnakePart

from Viron.src.main.python.preponderous.viron.services.entityService import EntityService
from Viron.src.main.python.preponderous.viron.services.environmentService import EnvironmentService
from Viron.src.main.python.preponderous.viron.services.gridService import GridService
from Viron.src.main.python.preponderous.viron.services.locationService import LocationService

from lib.patchwork.environmentRenderer import EnvironmentRenderer
from lib.patchwork.gridRenderer import GridRenderer
from lib.patchwork.locationRenderer import LocationRenderer

import logging

# @author Daniel McCoy Stephenson
# @since August 6th, 2022
class Ophidian:
    def __init__(self):
        logging.basicConfig(filename='example.log', encoding='utf-8', level=logging.DEBUG)
        self.logger = logging.getLogger(__name__)
        print("Initializing Ophidian")
        pygame.init()
        self.config = Config()
        self.initializeGameDisplay()
        pygame.display.set_icon(pygame.image.load("src/media/icon.PNG"))
        self.graphik = Graphik(self.gameDisplay)
        self.running = True
        self.snakeParts = []
        self.level = 1
        
        self.tick = 0
        self.score = 0
        self.changedDirectionThisTick = False
        self.collision = False
        
        self.url = "http://localhost"
        self.port = 9999
        
        self.entityService = EntityService(self.url, self.port)
        self.environmentService = EnvironmentService(self.url, self.port)
        self.gridService = GridService(self.url, self.port)
        self.locationService = LocationService(self.url, self.port)
        
        self.initialize()
        
        self.environmentRenderer = EnvironmentRenderer(self.graphik, self.url, self.port)


    def initializeGameDisplay(self):
        print("Initializing game display")
        if self.config.fullscreen:
            self.gameDisplay = pygame.display.set_mode(
                (self.config.displayWidth, self.config.displayHeight), pygame.FULLSCREEN
            )
        else:
            self.gameDisplay = pygame.display.set_mode(
                (self.config.displayWidth, self.config.displayHeight), pygame.RESIZABLE
            )

    def initializeLocationWidthAndHeight(self, gridSize):
        print("Initializing location width and height")
        x, y = self.gameDisplay.get_size()
        self.locationWidth = x / gridSize
        self.locationHeight = y / gridSize

    # Draws the environment in its entirety.
    def drawEnvironment(self):
        print("Drawing environment")
        self.environmentRenderer.draw(self.environment)

    # Returns the color that a location should be displayed as.
    def getColorOfLocation(self, location):
        print("Getting color for location")
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
        print("Drawing location")
        if self.collision == True:
            color = self.config.red
        else:
            color = self.getColorOfLocation(location)
        self.graphik.drawRectangle(xPos, yPos, width, height, color)

    def calculateScore(self):
        print("Calculating score")
        length = len(self.snakeParts)
        numLocations = len(self.environment.grid.getLocations())
        percentage = int(length / numLocations * 100)
        self.score = length * percentage

    def displayStatsInConsole(self):
        logging.debug("Displaying stats in console")
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
        logging.debug("Checking for level progress")
        if (
            len(self.snakeParts)
            > len(self.environment.grid.getLocations())
            * self.config.levelProgressPercentageRequired
        ):
            self.level += 1
        self.initialize()

    def quitApplication(self):
        logging.debug("Quitting application")
        self.displayStatsInConsole()
        pygame.quit()
        quit()

    def getLocation(self, entity: Entity):
        logging.debug("Getting location")
        locationId = self.locationService.getLocationId(entity.getEntityId())
        grid = self.environment.getGrid()
        return grid.getLocation(locationId)

    def getLocationAndGrid(self, snakePart: SnakePart):
        logging.debug("Getting location and grid")
        location = self.locationService.get_location_of_entity(snakePart.getEntityId())
        grid = self.gridService.get_grid_of_entity(snakePart.getEntityId())
        return grid, location

    def moveEntity(self, snakePart: SnakePart, direction):
        logging.debug("Moving entity")
        grid, location = self.getLocationAndGrid(snakePart)

        newLocation = -1
        # get new location
        if direction == 0:
            newLocation = self.getUp(location, grid)
        elif direction == 1:
            newLocation = self.getLeft(location, grid)
        elif direction == 2:
            newLocation = self.getDown(location, grid)
        elif direction == 3:
            newLocation = self.getRight(location, grid)

        if newLocation == -1:
            # location doesn't exist, we're at a border
            return

        # if new location has a snake part already
        entities_in_new_location = self.entityService.get_entities_in_location(newLocation.get_location_id())
        if len(entities_in_new_location) > 0:
            for entity in entities_in_new_location:
                if isinstance(entity, SnakePart):
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
        self.locationService.remove_entity_from_location(snakePart.getEntityId(), location.get_location_id())
        self.locationService.add_entity_to_location(snakePart.getEntityId(), newLocation.get_location_id())
        snakePart.lastPosition = location

        # move all attached snake parts
        if snakePart.hasPrevious():
            self.movePreviousSnakePart(snakePart)

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
        entities_in_new_location = self.entityService.get_entities_in_location(newLocation.get_location_id())
        if len(entities_in_new_location) == 0:
            # no food in new location
            return

        # check if food is in new location
        for entity in entities_in_new_location:
            if isinstance(entity, Food):
                food = entity
                break

        if food == -1:
            # no food in new location
            return

        foodColor = food.getColor()

        self.removeEntity(food)
        self.spawnFood()
        self.spawnSnakePart(entity.getTail(), foodColor)
        self.calculateScore()

    def getUp(self, location, grid):
        logging.debug("Getting up location")
        y = location.get_y()
        x = location.get_x()
        if y - 1 < 0:
            return -1
        locations = self.locationService.get_locations_in_grid(grid.get_grid_id())
        for loc in locations:
            if loc.get_x() == x and loc.get_y() == y - 1:
                return loc
        return -1


    def getLeft(self, location, grid):
        logging.debug("Getting left location")
        y = location.get_y()
        x = location.get_x()
        if x - 1 < 0:
            return -1
        locations = self.locationService.get_locations_in_grid(grid.get_grid_id())
        for loc in locations:
            if loc.get_x() == x - 1 and loc.get_y() == y:
                return loc
        return -1

    def getDown(self, location, grid):
        logging.debug("Getting down location")
        y = location.get_y()
        x = location.get_x()
        if y + 1 >= self.config.gridSize:
            return -1
        locations = self.locationService.get_locations_in_grid(grid.get_grid_id())
        for loc in locations:
            if loc.get_x() == x and loc.get_y() == y + 1:
                return loc
        return -1

    def getRight(self, location, grid):
        logging.debug("Getting right location")
        y = location.get_y()
        x = location.get_x()
        if x + 1 >= self.config.gridSize:
            return -1
        locations = self.locationService.get_locations_in_grid(grid.get_grid_id())
        for loc in locations:
            if loc.get_x() == x + 1 and loc.get_y() == y:
                return loc
        return -1

    def movePreviousSnakePart(self, snakePart):
        logging.debug("Moving previous snake part")
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
        logging.debug("Removing entity from location")
        location = self.getLocation(entity)
        if location.isEntityPresent(entity):
            location.removeEntity(entity)

    def removeEntity(self, entity: Entity):
        logging.debug("Removing entity")
        self.removeEntityFromLocation(entity)

    def handleKeyDownEvent(self, key):
        logging.debug("Key down event")
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
        logging.debug("Getting random direction")
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
        logging.debug("Getting location direction")
        if direction == 0:
            return grid.getUp(location)
        elif direction == 1:
            return grid.getLeft(location)
        elif direction == 2:
            return grid.getDown(location)
        elif direction == 3:
            return grid.getRight(location)

    def getLocationOppositeDirection(self, direction, grid, location):
        logging.debug("Getting location opposite direction")
        if direction == 0:
            return grid.getDown(location)
        elif direction == 1:
            return grid.getRight(location)
        elif direction == 2:
            return grid.getUp(location)
        elif direction == 3:
            return grid.getLeft(location)

    def spawnSnakePart(self, snakePart: SnakePart, color):
        logging.debug("Spawning snake part")
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
        print("Spawning food")
        foodEntity = self.entityService.create_entity("Food")
        food = Food(
            (
                random.randrange(50, 200),
                random.randrange(50, 200),
                random.randrange(50, 200),
            ),
            foodEntity.getEntityId()
        )
        print("Food entity created with entityId", foodEntity.getEntityId())

        notFound = True
        while notFound:
            print("Getting grids in environment")
            grid = self.gridService.get_grids_in_environment(self.environment.getEnvironmentId())[0]
            print("Getting random location")
            targetLocation = self.get_random_location(grid)
            print("Getting number of entities")
            entities_in_target_location = len(self.entityService.get_entities_in_location(targetLocation.get_location_id()))
            if entities_in_target_location == 0:
                notFound = False

        self.locationService.add_entity_to_location(food.get_entity_id(), targetLocation.get_location_id())

    def initialize(self):
        self.collision = False
        self.score = 0
        self.snakeParts = []
        self.tick = 0
        
        if self.level == 1:
            self.environment = self.environmentService.create_environment("Level " + str(self.level), 1, self.config.gridSize)
        else:
            self.environment = self.environmentService.create_environment("Level " + str(self.level), 1, self.config.gridSize + (self.level - 1) * 2)
        
        self.initializeLocationWidthAndHeight(self.config.gridSize)
        pygame.display.set_caption("Ophidian - Level " + str(self.level))
        newEntity = self.entityService.create_entity("Snake Part")
        self.selectedSnakePart = SnakePart(
            (
                random.randrange(50, 200),
                random.randrange(50, 200),
                random.randrange(50, 200),
            ),
            newEntity.getEntityId()
        )
        first_location = self.locationService.get_all_locations()[0]
        location_id = first_location.get_location_id()
        self.locationService.add_entity_to_location(newEntity.getEntityId(), location_id)
        self.snakeParts.append(self.selectedSnakePart)
        print("The ophidian enters the world.")
        self.spawnFood()
        print("Done initializing")

    def run(self):
        print("Starting game")
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
            locations = self.locationService.get_locations_in_environment(self.environment.getEnvironmentId())
            percentage = len(self.snakeParts) / len(
                locations
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

    def get_random_location(self, grid):
        locations = self.locationService.get_locations_in_grid(grid.get_grid_id())
        if not locations:
            print("bad response from service")
            return -1
        random_index = random.randint(0, len(locations) - 1)
        return locations[random_index]


ophidian = Ophidian()
ophidian.run()
