import os
import sys
import termios
import tty
import select


# @author Daniel McCoy Stephenson
# @since October 15th, 2025
class TextRenderer:
    def __init__(self, config):
        self.config = config
        self.old_settings = None

    def clearScreen(self):
        os.system('clear' if os.name != 'nt' else 'cls')

    def renderGrid(self, environment, snakeParts, collision):
        """Render the game grid as text"""
        self.clearScreen()
        
        grid = environment.getGrid()
        rows = grid.getRows()
        cols = grid.getColumns()
        
        # Create a display grid
        display = []
        for _ in range(cols):
            display.append(['.'] * rows)
        
        # Mark snake parts
        for snakePart in snakeParts:
            locationID = snakePart.getLocationID()
            if locationID is not None:
                location = grid.getLocation(locationID)
                x = location.getX()
                y = location.getY()
                display[y][x] = 'S'
        
        # Mark head of snake
        if len(snakeParts) > 0:
            headLocationID = snakeParts[0].getLocationID()
            if headLocationID is not None:
                headLocation = grid.getLocation(headLocationID)
                hx = headLocation.getX()
                hy = headLocation.getY()
                display[hy][hx] = 'H'
        
        # Mark food
        for locationId in grid.getLocations():
            location = grid.getLocation(locationId)
            for eid in location.getEntities():
                entity = location.getEntity(eid)
                if entity.getName() == "Food":
                    x = location.getX()
                    y = location.getY()
                    display[y][x] = 'F'
        
        # Print border
        print('┌' + '─' * (rows * 2 + 1) + '┐')
        
        # Print grid
        for row in display:
            print('│ ' + ' '.join(row) + ' │')
        
        # Print border
        print('└' + '─' * (rows * 2 + 1) + '┘')
        
        if collision:
            print("\n[!] COLLISION! The ophidian collides with itself!")
        
        print("\nLegend: H=Head, S=Snake, F=Food, .=Empty")

    def renderStats(self, level, snakeLength, score, percentage):
        """Render game statistics"""
        print(f"\nLevel: {level}")
        print(f"Length: {snakeLength}")
        print(f"Score: {score}")
        print(f"Progress: {int(percentage * 100)}%")
        
        # Draw progress bar
        bar_length = 30
        filled = int(bar_length * percentage)
        bar = '█' * filled + '░' * (bar_length - filled)
        print(f"[{bar}]")

    def renderControls(self):
        """Render control instructions"""
        print("\nControls: w/↑=Up, a/←=Left, s/↓=Down, d/→=Right, r=Restart, q=Quit")

    def enableRawMode(self):
        """Enable raw mode for non-blocking keyboard input"""
        if os.name != 'nt':
            self.old_settings = termios.tcgetattr(sys.stdin)
            tty.setcbreak(sys.stdin.fileno())

    def disableRawMode(self):
        """Disable raw mode and restore terminal settings"""
        if os.name != 'nt' and self.old_settings:
            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, self.old_settings)

    def getKeyPress(self, timeout=0):
        """
        Get a key press without blocking (non-blocking input)
        Returns the key pressed or None if no key was pressed
        """
        if os.name != 'nt':
            # Unix/Linux/Mac
            if select.select([sys.stdin], [], [], timeout)[0]:
                return sys.stdin.read(1)
        else:
            # Windows - simpler approach for now
            import msvcrt
            if msvcrt.kbhit():
                return msvcrt.getch().decode('utf-8')
        return None
