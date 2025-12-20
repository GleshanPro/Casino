import random
from src.simulation.casino import Casino
from src.entities.player import Player
from src.entities.goose import Goose, WetBanditGoose
from src.entities.chip import Chip
from src.collections.chip_collection import ChipCollection
from src.collections.player_collection import PlayerCollection
from src.collections.goose_collection import GooseCollection


class TestCasino:
    """Tests for Casino class"""

    def test_casino_initialization_empty(self):
        """Test Casino initialization with no players or geese"""
        casino = Casino()
        assert len(casino.players) == 0
        assert len(casino.gooses) == 0
        assert len(casino.balances) == 0
        assert len(casino.goose_ledger) == 0

    def test_casino_initialization_with_players(self):
        """Test Casino initialization with players"""
        players = PlayerCollection([
            Player("Alice", ChipCollection([Chip(100)])),
            Player("Bob", ChipCollection([Chip(200)]))
        ])
        casino = Casino(players=players)
        assert len(casino.players) == 2
        assert len(casino.balances) == 2
        assert "Alice" in casino.balances
        assert "Bob" in casino.balances

    def test_casino_initialization_with_geese(self):
        """Test Casino initialization with geese"""
        gooses = GooseCollection([
            Goose("Gus", 50, 2, ChipCollection([Chip(10)])),
            WetBanditGoose("WarGus", 60, 3, ChipCollection([Chip(15)]))
        ])
        casino = Casino(gooses=gooses)
        assert len(casino.gooses) == 2
        assert len(casino.goose_ledger) == 2

    def test_register_player(self):
        """Test registering a player"""
        casino = Casino()
        player = Player("Alice", ChipCollection([Chip(100)]))
        casino.register_player(player)
        assert len(casino.players) == 1
        assert player in casino.players
        assert "Alice" in casino.balances
        assert casino.balances["Alice"].total_value() == 100

    def test_register_goose(self):
        """Test registering a goose"""
        casino = Casino()
        goose = Goose("Gus", 50, 2, ChipCollection([Chip(10)]))
        casino.register_goose(goose)
        assert len(casino.gooses) == 1
        assert goose in casino.gooses
        assert "Gus" in casino.goose_ledger

    def test_get_balance_total(self):
        """Test getting balance total"""
        casino = Casino()
        balance = ChipCollection([Chip(10), Chip(20), Chip(30)])
        total = casino.get_balance_total(balance)
        assert total == 60

    def test_add_chip_to_balance_player(self):
        """Test adding chip to player balance"""
        casino = Casino()
        player = Player("Alice", ChipCollection([Chip(100)]))
        casino.register_player(player)
        casino.add_chip_to_balance(player, 50)
        assert casino.balances["Alice"].total_value() == 150

    def test_add_chip_to_balance_goose(self):
        """Test adding chip to goose balance"""
        casino = Casino()
        goose = Goose("Gus", 50, 2, ChipCollection([Chip(10)]))
        casino.register_goose(goose)
        casino.add_chip_to_balance(goose, 20)
        assert casino.goose_ledger["Gus"].total_value() == 30

    def test_add_chip_to_balance_by_name(self):
        """Test adding chip to balance by player name"""
        casino = Casino()
        player = Player("Alice", ChipCollection([Chip(100)]))
        casino.register_player(player)
        casino.add_chip_to_balance("Alice", 50)
        assert casino.balances["Alice"].total_value() == 150

    def test_remove_chip_from_balance_success(self):
        """Test removing chips from balance successfully"""
        casino = Casino()
        player = Player("Alice", ChipCollection([Chip(100)]))
        casino.register_player(player)
        result = casino.remove_chip_from_balance(player, 30)
        assert result is True
        assert casino.balances["Alice"].total_value() == 70


    def test_remove_chip_splits_large_chip(self):
        """Test removing chips splits large chip if needed"""
        casino = Casino()
        player = Player("Alice", ChipCollection([Chip(100)]))
        casino.register_player(player)
        result = casino.remove_chip_from_balance(player, 30)
        assert result is True
        # Should have 70 remaining
        assert casino.balances["Alice"].total_value() == 70


    def test_event_WetBanditGoose_attack(self):
        """Test WetBanditGoose attack event"""
        random.seed(42)
        casino = Casino()
        player = Player("Alice", ChipCollection([Chip(100)]))
        WetBanditGoose = WetBanditGoose("WarGus", 60, 3, ChipCollection([Chip(10)]))
        casino.register_player(player)
        casino.register_goose(WetBanditGoose)
        initial_player_balance = casino.balances["Alice"].total_value()
        initial_goose_balance = casino.goose_ledger["WarGus"].total_value()
        casino._event_wetbanditgoose_rob()
        # Player should lose money, goose should gain
        final_player_balance = casino.balances["Alice"].total_value()
        final_goose_balance = casino.goose_ledger["WarGus"].total_value()
        assert final_player_balance < initial_player_balance
        assert final_goose_balance >= initial_goose_balance

    def test_event_goose_steal(self):
        """Test goose steal event"""
        random.seed(42)
        casino = Casino()
        player = Player("Alice", ChipCollection([Chip(100)]))
        goose = Goose("Gus", 50, 2, ChipCollection([Chip(10)]))
        casino.register_player(player)
        casino.register_goose(goose)
        initial_player_balance = casino.balances["Alice"].total_value()
        initial_goose_balance = casino.goose_ledger["Gus"].total_value()
        casino._event_goose_steal()
        # Player should lose money, goose should gain
        final_player_balance = casino.balances["Alice"].total_value()
        final_goose_balance = casino.goose_ledger["Gus"].total_value()
        assert final_player_balance <= initial_player_balance
        assert final_goose_balance >= initial_goose_balance

    def test_event_goose_flock(self):
        """Test goose flock formation event"""
        random.seed(42)
        casino = Casino()
        goose1 = Goose("Gus", 50, 2, ChipCollection([Chip(10)]))
        goose2 = Goose("Boba", 30, 3, ChipCollection([Chip(15)]))
        casino.register_goose(goose1)
        casino.register_goose(goose2)
        initial_goose_count = len(casino.gooses)
        casino._event_goose_flock()
        # Should have original geese + 1 flock
        assert len(casino.gooses) >= initial_goose_count

    def test_event_player_panic(self):
        """Test player panic event"""
        random.seed(42)
        casino = Casino()
        player = Player("Alice", ChipCollection([Chip(100)]))
        casino.register_player(player)
        prev_total = casino.balances["Alice"].total_value()
        casino._event_player_panic()
        # Player should lose all money
        assert casino.balances["Alice"].total_value() <= prev_total // 2


    def test_show_state(self, capsys):
        """Test show_state prints casino state"""
        casino = Casino()
        player = Player("Alice", ChipCollection([Chip(100)]))
        goose = Goose("Gus", 50, 2, ChipCollection([Chip(10)]))
        casino.register_player(player)
        casino.register_goose(goose)
        casino.show_state()
        captured = capsys.readouterr()
        assert "CASINO STATE" in captured.out
        assert "Alice" in captured.out
        assert "Gus" in captured.out
