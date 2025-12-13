import pytest
from src.entities.chip import Chip


class TestChip:
    """Tests for Chip class"""

    def test_chip_creation(self):
        """Test Chip creation with amount"""
        chip = Chip(100)
        assert chip.amount == 100
        assert chip.get_amount() == 100

    def test_chip_add_with_int(self):
        """Test Chip + int"""
        chip1 = Chip(50)
        chip2 = chip1 + 25
        assert chip2.amount == 75
        assert isinstance(chip2, Chip)

    def test_chip_add_with_chip(self):
        """Test Chip + Chip"""
        chip1 = Chip(30)
        chip2 = Chip(20)
        chip3 = chip1 + chip2
        assert chip3.amount == 50
        assert isinstance(chip3, Chip)

    def test_chip_radd_with_int(self):
        """Test int + Chip (right addition)"""
        chip1 = Chip(10)
        chip2 = 5 + chip1
        assert chip2.amount == 15
        assert isinstance(chip2, Chip)

    def test_chip_eq_with_int(self):
        """Test Chip == int"""
        chip = Chip(100)
        assert chip == 100
        assert chip != 50

    def test_chip_eq_with_chip(self):
        """Test Chip == Chip"""
        chip1 = Chip(100)
        chip2 = Chip(100)
        chip3 = Chip(50)
        assert chip1 == chip2
        assert chip1 != chip3

    def test_chip_add_incompatible_type(self):
        """Test Chip + incompatible type raises TypeError"""
        chip = Chip(10)
        # When __add__ returns NotImplemented, Python tries __radd__ on the other type
        # Since str doesn't have __radd__ for Chip, Python raises TypeError
        with pytest.raises(TypeError, match="unsupported operand"):
            chip + "invalid"

    def test_chip_eq_incompatible_type(self):
        """Test Chip == incompatible type returns False (Python's default behavior)"""
        chip = Chip(10)
        # When __eq__ returns NotImplemented, Python tries reverse comparison
        # Since str.__eq__ doesn't handle Chip, Python returns False
        result = chip == "invalid"
        assert result is False
