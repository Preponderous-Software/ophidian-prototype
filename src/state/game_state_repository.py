import json
from pathlib import Path

from .game_state import GameState


class GameStateRepository:
    def __init__(self, file_path='game_state.json'):
        self.file_path = Path(file_path)

    def save(self, game_state):
        """Save game state to JSON file"""
        try:
            with open(self.file_path, 'w') as f:
                json.dump(game_state, f)
        except IOError as e:
            print(f"Could not save game state: {e}")

    def load(self):
        """Load game state from JSON file"""
        try:
            if self.file_path.exists():
                with open(self.file_path, 'r') as f:
                    data = json.load(f)
                    return GameState.from_dict(data)
            return GameState()  # Return default state if file doesn't exist
        except IOError as e:
            print(f"Could not load game state: {e}")
            return GameState()  # Return default state on error