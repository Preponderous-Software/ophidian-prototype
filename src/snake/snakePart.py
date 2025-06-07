


# @author Daniel McCoy Stephenson
# @since August 6th, 2022


class SnakePart:
    def __init__(self, color, entityId):
        self.entityId = entityId
        self.color = color
        self.direction = 0
        self.nextSnakePart = -1
        self.previousSnakePart = -1
        self.lastPosition = -1

    def getEntityId(self):
        return self.entityId

    def setEntityId(self, entityId):
        self.entityId = entityId

    def getDirection(self):
        return self.direction

    def setDirection(self, direction):
        self.direction = direction

    def setNext(self, snakePart):
        self.nextSnakePart = snakePart

    def setPrevious(self, snakePart):
        self.previousSnakePart = snakePart

    def setLastPosition(self, position):
        self.lastPosition = position

    def hasNext(self):
        return self.nextSnakePart != -1

    def hasPrevious(self):
        return self.previousSnakePart != -1

    def getTail(self):
        if self.previousSnakePart == -1:
            return self
        temp = self.previousSnakePart
        while temp.hasPrevious():
            temp = temp.previousSnakePart
        return temp

    def getColor(self):
        return self.color
