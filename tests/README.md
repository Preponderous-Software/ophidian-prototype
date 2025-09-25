# Ophidian Menu System Tests

This directory contains unit tests for the Ophidian game's menu system implementation.

## Test Structure

### State Tests
- `state/test_menu_state.py` - Tests for the MenuState enum

### Graphics Tests
- `graphics/test_main_menu.py` - Tests for MainMenu class and MenuItem class
- `graphics/test_options_menu.py` - Tests for OptionsMenu class
- `graphics/test_high_scores_menu.py` - Tests for HighScoresMenu class

### Integration Tests
- `test_ophidian_menu_integration.py` - Integration tests for menu system with main Ophidian class

## Running Tests

### Prerequisites
```bash
pip install pygame
sudo apt-get install xvfb  # For headless testing on Linux
```

### Run All Menu Tests
```bash
# Using the test runner script
python run_tests.py

# Or manually with unittest
DISPLAY=:99 xvfb-run -a python -m unittest tests.state.test_menu_state tests.graphics.test_main_menu tests.graphics.test_options_menu tests.graphics.test_high_scores_menu tests.test_ophidian_menu_integration -v
```

### Run Individual Test Modules
```bash
# Menu state tests
python -m unittest tests.state.test_menu_state -v

# Main menu tests (requires display)
DISPLAY=:99 xvfb-run -a python -m unittest tests.graphics.test_main_menu -v

# Integration tests (requires display)
DISPLAY=:99 xvfb-run -a python -m unittest tests.test_ophidian_menu_integration -v
```

## Test Coverage

The tests cover:
- ✅ MenuState enum functionality
- ✅ MenuItem class creation and highlighting
- ✅ MainMenu keyboard navigation (up/down, WASD)
- ✅ MainMenu selection (Enter, Space, Escape)
- ✅ MainMenu mouse interaction (motion and clicking)
- ✅ MainMenu drawing and UI rendering
- ✅ OptionsMenu and HighScoresMenu basic functionality
- ✅ Ophidian class initialization with menu system
- ✅ State transitions between different menu states
- ✅ Integration with game state repository
- ✅ Error handling for icon loading

## CI/CD

The tests are automatically run by GitHub Actions on push and pull requests. See `.github/workflows/test.yml` for the CI configuration.

## Environment Variables

For headless testing:
- `SDL_AUDIODRIVER=dummy` - Disables audio to avoid ALSA warnings
- `DISPLAY=:99` - Uses virtual display for graphical operations