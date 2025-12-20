import pytest
from src.entities.goose import Goose, WetBanditGoose, DriverGoose
from src.entities.player import Player
from src.collections.chip_collection import ChipCollection
from src.entities.chip import Chip


class TestGoose:
    """Tests for Goose class"""

    def test_goose_creation(self):
        """Test Goose creation"""
        balance = ChipCollection([Chip(10)])
        goose = Goose("Gus", 50, 2, balance)
        assert goose.name == "Gus"
        assert goose.hp == 50
        assert goose.honk_volume == 2
        assert goose.balance == balance

    def test_goose_default_balance(self):
        """Test Goose with default empty balance"""
        goose = Goose("Gus", 50)
        assert goose.name == "Gus"
        assert isinstance(goose.balance, ChipCollection)
        assert len(goose.balance) == 0

    def test_goose_attack(self):
        """Test Goose attack method"""
        goose = Goose("Gus", 50, 2)
        player = Player("Alice", ChipCollection([Chip(100)]))
        damage = goose.attack(player, 15)
        assert damage == 15

    def test_goose_add(self):
        """Test Goose __add__ for flock formation"""
        balance1 = ChipCollection([Chip(10)])
        balance2 = ChipCollection([Chip(20)])
        goose1 = Goose("Gus", 50, 2, balance1)
        goose2 = Goose("Boba", 30, 3, balance2)

        flock = goose1 + goose2
        assert isinstance(flock, Goose)
        assert flock.hp == 80  # 50 + 30
        assert flock.honk_volume == 5  # 2 + 3
        assert flock.name == "Gus-Boba"
        assert flock.balance.total_value() == 30  # 10 + 20

    def test_goose_add_incompatible_type(self):
        """Test Goose __add__ with incompatible type raises TypeError"""
        goose = Goose("Gus", 50, 2)
        # When __add__ returns NotImplemented, Python tries __radd__ on the other type
        # Since str doesn't have __radd__ for Goose, Python raises TypeError
        with pytest.raises(TypeError, match="unsupported operand"):
            goose + "not a goose"

    def test_goose_repr(self):
        """Test Goose __repr__"""
        goose = Goose("Gus", 50, 2)
        repr_str = repr(goose)
        assert "Gus" in repr_str
        assert "Goose" in repr_str
        assert "50" in repr_str


class TestWetBanditGoose:
    """Tests for WetBanditGoose class"""

    def test_WetBanditGoose_creation(self):
        """Test WetBanditGoose creation"""
        balance = ChipCollection([Chip(10)])
        wetBanditGoose = WetBanditGoose("WarGus", 60, 3, balance)
        assert wetBanditGoose.name == "WarGus"
        assert wetBanditGoose.hp == 60
        assert isinstance(wetBanditGoose, Goose)

    def test_WetBanditGoose_attack_with_damage(self):
        """Test WetBanditGoose attack with specified damage"""
        wetBanditGoose = WetBanditGoose("WarGus", 60, 3)
        player = Player("Alice", ChipCollection([Chip(100)]))
        damage = wetBanditGoose.attack(player, 18)
        assert damage == 18

    def test_wet_bandit_goose_rob_random_damage(self):
        """Test WetBanditGoose attack with random damage (8-20)"""
        wetBanditGoose = WetBanditGoose("WarGus", 60, 3)
        player = Player("Alice", ChipCollection([Chip(100)]))
        damage = wetBanditGoose.rob(player)
        assert 8 <= damage <= 20


class TestDriverGoose:
    """Tests for DriverGoose class"""

    def test_DriverGoose_creation(self):
        """Test DriverGoose creation"""
        balance = ChipCollection([Chip(15)])
        driverGoose = DriverGoose("HonkGus", 40, 4, balance)
        assert driverGoose.name == "HonkGus"
        assert driverGoose.hp == 40
        assert isinstance(driverGoose, Goose)

    def test_DriverGoose_call_with_times(self):
        """Test DriverGoose __call__ with specified times"""
        driverGoose = DriverGoose("HonkGus", 40, 4)
        initial_volume = driverGoose.honk_volume
        driverGoose(3)
        assert driverGoose.honk_volume == initial_volume + 3

    def test_DriverGoose_call_random_times(self):
        """Test DriverGoose __call__ with random times (1-4)"""
        driverGoose = DriverGoose("HonkGus", 40, 4)
        initial_volume = driverGoose.honk_volume
        driverGoose()
        assert driverGoose.honk_volume >= initial_volume + 1
        assert driverGoose.honk_volume <= initial_volume + 4
