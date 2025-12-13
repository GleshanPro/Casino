import pytest
from src.collections.chip_collection import ChipCollection
from src.entities.chip import Chip


class TestChipCollection:
    """Tests for ChipCollection class"""

    def test_empty_collection(self):
        """Test empty ChipCollection creation"""
        collection = ChipCollection()
        assert len(collection) == 0
        assert collection.total_value() == 0

    def test_collection_with_chips(self):
        """Test ChipCollection with initial chips"""
        chips = [Chip(10), Chip(20), Chip(30)]
        collection = ChipCollection(chips)
        assert len(collection) == 3
        assert collection.total_value() == 60

    def test_append_chip(self):
        """Test appending chip to collection"""
        collection = ChipCollection()
        chip = Chip(50)
        collection.append(chip)
        assert len(collection) == 1
        assert collection[0] == chip
        assert collection.total_value() == 50

    def test_append_wrong_type(self):
        """Test appending non-Chip raises TypeError"""
        collection = ChipCollection()
        with pytest.raises(TypeError, match="Expected Chip"):
            collection.append("not a chip")

    def test_remove_chip(self):
        """Test removing chip from collection"""
        chip1 = Chip(10)
        chip2 = Chip(20)
        collection = ChipCollection([chip1, chip2])
        collection.remove(chip1)
        assert len(collection) == 1
        assert collection[0] == chip2
        assert collection.total_value() == 20

    def test_remove_nonexistent_chip(self):
        """Test removing non-existent chip raises ValueError"""
        collection = ChipCollection([Chip(10)])
        with pytest.raises(ValueError):
            collection.remove(Chip(999))

    def test_getitem_index(self):
        """Test indexing collection"""
        chip1 = Chip(10)
        chip2 = Chip(20)
        collection = ChipCollection([chip1, chip2])
        assert collection[0] == chip1
        assert collection[1] == chip2

    def test_getitem_slice(self):
        """Test slicing collection returns ChipCollection"""
        chips = [Chip(10), Chip(20), Chip(30), Chip(40)]
        collection = ChipCollection(chips)
        sliced = collection[1:3]
        assert isinstance(sliced, ChipCollection)
        assert len(sliced) == 2
        assert sliced[0] == chips[1]
        assert sliced[1] == chips[2]

    def test_iteration(self):
        """Test iterating over collection"""
        chips = [Chip(10), Chip(20), Chip(30)]
        collection = ChipCollection(chips)
        collected = [chip for chip in collection]
        assert collected == chips

    def test_contains(self):
        """Test __contains__ method"""
        chip1 = Chip(10)
        chip2 = Chip(20)
        collection = ChipCollection([chip1, chip2])
        assert chip1 in collection
        assert chip2 in collection
        assert Chip(999) not in collection

    def test_total_value(self):
        """Test total_value calculation"""
        collection = ChipCollection([Chip(10), Chip(20), Chip(30)])
        assert collection.total_value() == 60

    def test_repr_shows_total(self):
        """Test __repr__ shows total value"""
        collection = ChipCollection([Chip(10), Chip(20)])
        repr_str = repr(collection)
        assert repr_str == "30"  # Should show total value
