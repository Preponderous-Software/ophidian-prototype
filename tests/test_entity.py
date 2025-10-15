"""Unit tests for Entity class"""
import pytest
import sys
sys.path.insert(0, '/home/runner/work/ophidian-prototype/ophidian-prototype/src')

from lib.pyenvlib.entity import Entity
import datetime


class TestEntity:
    """Test Entity base class"""

    def test_entity_initialization(self):
        """Test that Entity initializes correctly"""
        name = "TestEntity"
        entity = Entity(name)
        
        assert entity.getName() == name
        assert entity.getID() is not None
        assert isinstance(entity.getCreationDate(), datetime.datetime)
        assert entity.getEnvironmentID() == -1
        assert entity.getGridID() == -1
        assert entity.getLocationID() == -1

    def test_entity_unique_ids(self):
        """Test that different entities have unique IDs"""
        entity1 = Entity("Entity1")
        entity2 = Entity("Entity2")
        
        assert entity1.getID() != entity2.getID()

    def test_entity_name_methods(self):
        """Test getting and setting entity name"""
        entity = Entity("OriginalName")
        
        assert entity.getName() == "OriginalName"
        
        entity.setName("NewName")
        assert entity.getName() == "NewName"

    def test_entity_id_methods(self):
        """Test getting and setting entity ID"""
        entity = Entity("TestEntity")
        original_id = entity.getID()
        
        new_id = "new-test-id"
        entity.setID(new_id)
        assert entity.getID() == new_id
        assert entity.getID() != original_id

    def test_environment_id_methods(self):
        """Test getting and setting environment ID"""
        entity = Entity("TestEntity")
        
        assert entity.getEnvironmentID() == -1
        
        env_id = "env-123"
        entity.setEnvironmentID(env_id)
        assert entity.getEnvironmentID() == env_id

    def test_grid_id_methods(self):
        """Test getting and setting grid ID"""
        entity = Entity("TestEntity")
        
        assert entity.getGridID() == -1
        
        grid_id = "grid-456"
        entity.setGridID(grid_id)
        assert entity.getGridID() == grid_id

    def test_location_id_methods(self):
        """Test getting and setting location ID"""
        entity = Entity("TestEntity")
        
        assert entity.getLocationID() == -1
        
        location_id = "location-789"
        entity.setLocationID(location_id)
        assert entity.getLocationID() == location_id

    def test_creation_date_methods(self):
        """Test getting and setting creation date"""
        entity = Entity("TestEntity")
        original_date = entity.getCreationDate()
        
        assert isinstance(original_date, datetime.datetime)
        
        new_date = datetime.datetime(2023, 1, 1, 12, 0, 0)
        entity.setCreationDate(new_date)
        assert entity.getCreationDate() == new_date
        assert entity.getCreationDate() != original_date

    def test_entity_print_info(self, capsys):
        """Test that printInfo outputs entity information"""
        entity = Entity("TestEntity")
        entity.printInfo()
        
        captured = capsys.readouterr()
        assert "TestEntity" in captured.out
        assert "ID:" in captured.out
        assert "Creation Date:" in captured.out
