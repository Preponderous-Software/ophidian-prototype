class GameScore:
    def __init__(self, snake_part_repository, environment_repository):
        self.points = 0
        self.snake_part_repository = snake_part_repository
        self.environment_repository = environment_repository

    def calculate(self):
        length = self.snake_part_repository.get_length()
        num_locations = self.environment_repository.get_num_locations()
        percentage = int(length / num_locations * 100)
        self.points = length * percentage
        return self.points

    def display_stats(self):
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
        print("Score:", self.points)
        print("-----")

    def reset(self):
        self.points = 0