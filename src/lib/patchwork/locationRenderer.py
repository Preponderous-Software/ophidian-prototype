import random

from Viron.src.main.python.preponderous.viron.models.location import Location
from lib.graphik.src.graphik import Graphik

from Viron.src.main.python.preponderous.viron.services.entityService import EntityService


class LocationRenderer:
    def __init__(self, graphik: Graphik, host, port):
        self.graphik = graphik
        self.entityService = EntityService(host, port)

    def draw(self, location: Location, width: int, height: int):
        x = location.get_x() * width
        y = location.get_y() * height
        color = (255, 255, 255)  # Default color for the location rectangle
        entities = self.entityService.get_entities_in_location(location.get_location_id())
        if len(entities) > 0:
            color = self.get_random_color()
        self.graphik.drawRectangle(x - 1, y - 1, width * 1.5, height * 1.5, color)
    
    def get_random_color(self):
        red = random.randrange(50, 200)
        green = random.randrange(50, 200)
        blue = random.randrange(50, 200)
        return (red, green, blue)