from src.entities.player import Player
from src.collections.chip_collection import ChipCollection
from src.entities.chip import Chip


class TestPlayer:
    """Tests for Player class"""

    def test_player_creation(self):
        """Test Player creation"""
        balance = ChipCollection([Chip(100)])
        player = Player("Alice", balance)
        assert player.name == "Alice"
        assert player.balance == balance

    def test_player_default_balance(self):
        """Test Player with default empty balance"""
        player = Player("Bob")
        assert player.name == "Bob"
        assert isinstance(player.balance, ChipCollection)
        assert len(player.balance) == 0

    def test_player_repr(self):
        """Test Player __repr__"""
        balance = ChipCollection([Chip(100)])
        player = Player("Alice", balance)
        repr_str = repr(player)
        assert "Alice" in repr_str
        assert "Player" in repr_str

    def test_player_eq(self):
        """Test Player equality"""
        balance1 = ChipCollection([Chip(100)])
        balance2 = ChipCollection([Chip(100)])
        player1 = Player("Alice", balance1)
        player2 = Player("Alice", balance2)
        player3 = Player("Bob", balance1)

        assert player1 == player2
        assert player1 != player3

    def test_player_eq_different_type(self):
        """Test Player equality with different type returns False (Python's default behavior)"""
        player = Player("Alice", ChipCollection([Chip(100)]))
        # When __eq__ returns NotImplemented, Python tries reverse comparison
        # Since str.__eq__ doesn't handle Player, Python returns False
        result = player == "not a player"
        assert result is False
