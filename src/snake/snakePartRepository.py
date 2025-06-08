class SnakePartRepository:
    def __init__(self):
        self.snake_parts = []

    def get_length(self):
        return len(self.snake_parts)

    def append(self, snake_part):
        self.snake_parts.append(snake_part)

    def clear(self):
        self.snake_parts.clear()