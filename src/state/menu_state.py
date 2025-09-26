from enum import Enum


class MenuState(Enum):
    MAIN_MENU = "main_menu"
    OPTIONS = "options"
    HIGH_SCORES = "high_scores"
    GAME = "game"
    EXIT = "exit"