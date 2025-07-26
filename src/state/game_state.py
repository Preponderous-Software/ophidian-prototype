class GameState:
    def __init__(self, level=1, current_score=0, cumulative_score=0):
        self.level = level
        self.current_score = current_score
        self.cumulative_score = cumulative_score

    def to_dict(self):
        return {
            'level': self.level,
            'current_score': self.current_score,
            'cumulative_score': self.cumulative_score,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            level=data.get('level', 1),
            current_score=data.get('current_score', 0),
            cumulative_score=data.get('cumulative_score', 0)
        )
