"""Unit tests for Location class"""
import pytest
import sys
sys.path.insert(0, '/home/runner/work/ophidian-prototype/ophidian-prototype/src')

from lib.pyenvlib.location import Location
from lib.pyenvlib.entity import Entity


class TestLocation:
    """Test Location class"""

    def test_location_initialization(self):
        """Test that Location initializes correctly"""
        x, y = 5, 10
        location = Location(x, y)
        
        assert location.getX() == x
        assert location.getY() == y
        assert location.getID() is not None
        assert location.getNumEntities() == 0

    def test_location_unique_ids(self):
        """Test that different locations have unique IDs"""
        location1 = Location(0, 0)
        location2 = Location(1, 1)
        
        assert location1.getID() != location2.getID()

    def test_add_entity_to_location(self):
        """Test adding an entity to a location"""
        location = Location(0, 0)
        entity = Entity("TestEntity")
        
        assert location.getNumEntities() == 0
        
        location.addEntity(entity)
        
        assert location.getNumEntities() == 1
        assert location.isEntityPresent(entity)
        assert entity.getLocationID() == location.getID()

    def test_add_multiple_entities(self):
        """Test adding multiple entities to a location"""
        location = Location(2, 3)
        entity1 = Entity("Entity1")
        entity2 = Entity("Entity2")
        entity3 = Entity("Entity3")
        
        location.addEntity(entity1)
        location.addEntity(entity2)
        location.addEntity(entity3)
        
        assert location.getNumEntities() == 3
        assert location.isEntityPresent(entity1)
        assert location.isEntityPresent(entity2)
        assert location.isEntityPresent(entity3)

    def test_add_duplicate_entity_warning(self, capsys):
        """Test that adding a duplicate entity shows a warning"""
        location = Location(0, 0)
        entity = Entity("TestEntity")
        
        location.addEntity(entity)
        location.addEntity(entity)  # Try to add same entity again
        
        captured = capsys.readouterr()
        assert "Warning" in captured.out
        assert location.getNumEntities() == 1

    def test_remove_entity_from_location(self):
        """Test removing an entity from a location"""
        location = Location(1, 1)
        entity = Entity("TestEntity")
        
        location.addEntity(entity)
        assert location.getNumEntities() == 1
        
        location.removeEntity(entity)
        assert location.getNumEntities() == 0
        assert not location.isEntityPresent(entity)

    def test_remove_non_existent_entity_warning(self, capsys):
        """Test that removing a non-existent entity shows a warning"""
        location = Location(0, 0)
        entity = Entity("TestEntity")
        
        location.removeEntity(entity)  # Try to remove entity that was never added
        
        captured = capsys.readouterr()
        assert "Warning" in captured.out

    def test_get_entity_by_id(self):
        """Test retrieving an entity by its ID"""
        location = Location(0, 0)
        entity = Entity("TestEntity")
        
        location.addEntity(entity)
        
        retrieved_entity = location.getEntity(entity.getID())
        assert retrieved_entity == entity

    def test_get_non_existent_entity_warning(self, capsys):
        """Test that getting a non-existent entity shows a warning"""
        location = Location(0, 0)
        
        result = location.getEntity("non-existent-id")
        
        captured = capsys.readouterr()
        assert "Warning" in captured.out
        assert result is None

    def test_get_entities_dictionary(self):
        """Test getting the entities dictionary"""
        location = Location(0, 0)
        entity1 = Entity("Entity1")
        entity2 = Entity("Entity2")
        
        location.addEntity(entity1)
        location.addEntity(entity2)
        
        entities_dict = location.getEntities()
        assert len(entities_dict) == 2
        assert entity1.getID() in entities_dict
        assert entity2.getID() in entities_dict

    def test_is_entity_present(self):
        """Test checking if an entity is present"""
        location = Location(0, 0)
        entity1 = Entity("Entity1")
        entity2 = Entity("Entity2")
        
        location.addEntity(entity1)
        
        assert location.isEntityPresent(entity1)
        assert not location.isEntityPresent(entity2)
