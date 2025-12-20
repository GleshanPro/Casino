import pytest
from src.collections.goose_collection import GooseCollection
from src.entities.goose import Goose, WetBanditGoose, DriverGoose
from src.collections.chip_collection import ChipCollection
from src.entities.chip import Chip


class TestGooseCollection:
    """Tests for GooseCollection class"""

    def test_empty_collection(self):
        """Test empty GooseCollection creation"""
        collection = GooseCollection()
        assert len(collection) == 0

    def test_collection_with_geese(self):
        """Test GooseCollection with initial geese"""
        goose1 = Goose("Gus", 50, 2, ChipCollection([Chip(10)]))
        goose2 = WetBanditGoose("WarGus", 60, 3, ChipCollection([Chip(15)]))
        collection = GooseCollection([goose1, goose2])
        assert len(collection) == 2

    def test_append_goose(self):
        """Test appending goose to collection"""
        collection = GooseCollection()
        goose = Goose("Gus", 50, 2, ChipCollection([Chip(10)]))
        collection.append(goose)
        assert len(collection) == 1
        assert collection[0] == goose

    def test_remove_goose(self):
        """Test removing goose from collection"""
        goose1 = Goose("Gus", 50, 2, ChipCollection([Chip(10)]))
        goose2 = WetBanditGoose("WarGus", 60, 3, ChipCollection([Chip(15)]))
        collection = GooseCollection([goose1, goose2])
        collection.remove(goose1)
        assert len(collection) == 1
        assert collection[0] == goose2

    def test_remove_nonexistent_goose(self):
        """Test removing non-existent goose raises ValueError"""
        goose = Goose("Gus", 50, 2, ChipCollection([Chip(10)]))
        collection = GooseCollection([goose])
        other_goose = Goose("Boba", 30, 3, ChipCollection([Chip(15)]))
        with pytest.raises(ValueError):
            collection.remove(other_goose)

    def test_getitem_index(self):
        """Test indexing collection"""
        goose1 = Goose("Gus", 50, 2, ChipCollection([Chip(10)]))
        goose2 = WetBanditGoose("WarGus", 60, 3, ChipCollection([Chip(15)]))
        collection = GooseCollection([goose1, goose2])
        assert collection[0] == goose1
        assert collection[1] == goose2

    def test_getitem_slice(self):
        """Test slicing collection returns GooseCollection"""
        geese = [
            Goose("Gus", 50, 2, ChipCollection([Chip(10)])),
            WetBanditGoose("WarGus", 60, 3, ChipCollection([Chip(15)])),
            DriverGoose("HonkGus", 40, 4, ChipCollection([Chip(20)]))
        ]
        collection = GooseCollection(geese)
        sliced = collection[1:3]
        assert isinstance(sliced, GooseCollection)
        assert len(sliced) == 2
        assert sliced[0] == geese[1]
        assert sliced[1] == geese[2]

    def test_iteration(self):
        """Test iterating over collection"""
        goose1 = Goose("Gus", 50, 2, ChipCollection([Chip(10)]))
        goose2 = WetBanditGoose("WarGus", 60, 3, ChipCollection([Chip(15)]))
        collection = GooseCollection([goose1, goose2])
        collected = [g for g in collection]
        assert collected == [goose1, goose2]

    def test_contains(self):
        """Test __contains__ method"""
        goose1 = Goose("Gus", 50, 2, ChipCollection([Chip(10)]))
        goose2 = WetBanditGoose("WarGus", 60, 3, ChipCollection([Chip(15)]))
        collection = GooseCollection([goose1, goose2])
        assert goose1 in collection
        assert goose2 in collection
        other_goose = Goose("Boba", 30, 3, ChipCollection([Chip(20)]))
        assert other_goose not in collection
