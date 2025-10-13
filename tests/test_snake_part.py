"""Unit tests for SnakePart class"""
import pytest
import sys
sys.path.insert(0, '/home/runner/work/ophidian-prototype/ophidian-prototype/src')

from snake.snakePart import SnakePart


class TestSnakePart:
    """Test SnakePart entity class"""

    def test_snake_part_initialization(self):
        """Test that SnakePart initializes correctly"""
        color = (0, 255, 0)
        snake_part = SnakePart(color)
        
        assert snake_part.getName() == "Snake Part"
        assert snake_part.getColor() == color
        assert snake_part.getDirection() == 0
        assert snake_part.nextSnakePart == -1
        assert snake_part.previousSnakePart == -1
        assert snake_part.lastPosition == -1

    def test_direction_methods(self):
        """Test direction getter and setter"""
        snake_part = SnakePart((255, 0, 0))
        
        # Test initial direction
        assert snake_part.getDirection() == 0
        
        # Test setting direction
        for direction in [0, 1, 2, 3]:
            snake_part.setDirection(direction)
            assert snake_part.getDirection() == direction

    def test_next_and_previous_methods(self):
        """Test next and previous snake part linking"""
        part1 = SnakePart((255, 0, 0))
        part2 = SnakePart((0, 255, 0))
        part3 = SnakePart((0, 0, 255))
        
        # Initially no next or previous
        assert not part1.hasNext()
        assert not part1.hasPrevious()
        
        # Link parts
        part1.setNext(part2)
        part2.setPrevious(part1)
        part2.setNext(part3)
        part3.setPrevious(part2)
        
        # Check linking
        assert part1.hasNext()
        assert not part1.hasPrevious()
        assert part2.hasNext()
        assert part2.hasPrevious()
        assert not part3.hasNext()
        assert part3.hasPrevious()

    def test_last_position_methods(self):
        """Test last position tracking"""
        snake_part = SnakePart((100, 100, 100))
        
        assert snake_part.lastPosition == -1
        
        position = (5, 10)
        snake_part.setLastPosition(position)
        assert snake_part.lastPosition == position

    def test_get_tail(self):
        """Test getting the tail of the snake"""
        part1 = SnakePart((255, 0, 0))
        part2 = SnakePart((0, 255, 0))
        part3 = SnakePart((0, 0, 255))
        
        # Single part snake
        assert part1.getTail() == part1
        
        # Link parts: part1 -> part2 -> part3
        part1.setNext(part2)
        part2.setPrevious(part1)
        part2.setNext(part3)
        part3.setPrevious(part2)
        
        # part1 is head, should return part3 (tail)
        # But getTail traverses backwards from current part
        assert part3.getTail() == part1

    def test_snake_part_inherits_from_entity(self):
        """Test that SnakePart properly inherits Entity properties"""
        snake_part = SnakePart((200, 100, 50))
        
        # Check Entity methods are available
        assert hasattr(snake_part, 'getID')
        assert hasattr(snake_part, 'getName')
        assert hasattr(snake_part, 'getEnvironmentID')
        assert hasattr(snake_part, 'getGridID')
        assert hasattr(snake_part, 'getLocationID')
        
        # Check ID is generated
        assert snake_part.getID() is not None

    def test_multiple_snake_parts_have_unique_ids(self):
        """Test that different SnakePart instances have unique IDs"""
        part1 = SnakePart((255, 0, 0))
        part2 = SnakePart((0, 255, 0))
        part3 = SnakePart((0, 0, 255))
        
        assert part1.getID() != part2.getID()
        assert part2.getID() != part3.getID()
        assert part1.getID() != part3.getID()
