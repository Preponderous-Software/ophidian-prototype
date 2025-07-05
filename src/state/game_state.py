class GameState:
    def __init__(self, level=1, current_score=0, high_score=0, cumulative_score=0, games_played=0):
        self.level = level
        self.current_score = current_score
        self.high_score = high_score
        self.cumulative_score = cumulative_score
        self.games_played = games_played

    def to_dict(self):
        return {
            'level': self.level,
            'current_score': self.current_score,
            'high_score': self.high_score,
            'cumulative_score': self.cumulative_score,
            'games_played': self.games_played
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            level=data.get('level', 1),
            current_score=data.get('current_score', 0),
            high_score=data.get('high_score', 0),
            cumulative_score=data.get('cumulative_score', 0),
            games_played=data.get('games_played', 0)
        )
