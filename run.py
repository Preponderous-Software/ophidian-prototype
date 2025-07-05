import sys
import os

# Add the project root directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.ophidian import Ophidian

if __name__ == "__main__":
    ophidian = Ophidian()
    ophidian.run()
