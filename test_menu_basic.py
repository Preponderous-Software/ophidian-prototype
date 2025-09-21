#!/usr/bin/env python3
"""
Simple test to verify menu functionality without pygame initialization
"""
import os
import sys

# Add the project root directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.state.menu_state import MenuState
from src.graphics.main_menu import MenuItem

def test_menu_state_enum():
    """Test that MenuState enum works correctly"""
    assert MenuState.MAIN_MENU.value == "main_menu"
    assert MenuState.OPTIONS.value == "options"
    assert MenuState.HIGH_SCORES.value == "high_scores"
    assert MenuState.GAME.value == "game"
    assert MenuState.EXIT.value == "exit"
    print("✓ MenuState enum test passed")

def test_menu_item():
    """Test MenuItem class functionality"""
    item = MenuItem("Test Item", MenuState.GAME)
    assert item.text == "Test Item"
    assert item.action == MenuState.GAME
    assert item.width == 200
    assert item.height == 50
    assert item.is_highlighted == False
    
    item.set_highlighted(True)
    assert item.is_highlighted == True
    print("✓ MenuItem test passed")

if __name__ == "__main__":
    test_menu_state_enum()
    test_menu_item()
    print("All basic tests passed!")