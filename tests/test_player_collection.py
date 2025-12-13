import pytest
from src.collections.player_collection import PlayerCollection
from src.entities.player import Player
from src.collections.chip_collection import ChipCollection
from src.entities.chip import Chip


class TestPlayerCollection:
    """Tests for PlayerCollection class"""

    def test_empty_collection(self):
        """Test empty PlayerCollection creation"""
        collection = PlayerCollection()
        assert len(collection) == 0

    def test_collection_with_players(self):
        """Test PlayerCollection with initial players"""
        player1 = Player("Alice", ChipCollection([Chip(100)]))
        player2 = Player("Bob", ChipCollection([Chip(200)]))
        collection = PlayerCollection([player1, player2])
        assert len(collection) == 2

    def test_append_player(self):
        """Test appending player to collection"""
        collection = PlayerCollection()
        player = Player("Charlie", ChipCollection([Chip(50)]))
        collection.append(player)
        assert len(collection) == 1
        assert collection[0] == player

    def test_remove_player(self):
        """Test removing player from collection"""
        player1 = Player("Alice", ChipCollection([Chip(100)]))
        player2 = Player("Bob", ChipCollection([Chip(200)]))
        collection = PlayerCollection([player1, player2])
        collection.remove(player1)
        assert len(collection) == 1
        assert collection[0] == player2

    def test_remove_nonexistent_player(self):
        """Test removing non-existent player raises ValueError"""
        player = Player("Alice", ChipCollection([Chip(100)]))
        collection = PlayerCollection([player])
        other_player = Player("Bob", ChipCollection([Chip(200)]))
        with pytest.raises(ValueError):
            collection.remove(other_player)

    def test_getitem_index(self):
        """Test indexing collection"""
        player1 = Player("Alice", ChipCollection([Chip(100)]))
        player2 = Player("Bob", ChipCollection([Chip(200)]))
        collection = PlayerCollection([player1, player2])
        assert collection[0] == player1
        assert collection[1] == player2

    def test_getitem_slice(self):
        """Test slicing collection returns PlayerCollection"""
        players = [
            Player("Alice", ChipCollection([Chip(100)])),
            Player("Bob", ChipCollection([Chip(200)])),
            Player("Charlie", ChipCollection([Chip(300)]))
        ]
        collection = PlayerCollection(players)
        sliced = collection[1:3]
        assert isinstance(sliced, PlayerCollection)
        assert len(sliced) == 2
        assert sliced[0] == players[1]
        assert sliced[1] == players[2]

    def test_iteration(self):
        """Test iterating over collection"""
        player1 = Player("Alice", ChipCollection([Chip(100)]))
        player2 = Player("Bob", ChipCollection([Chip(200)]))
        collection = PlayerCollection([player1, player2])
        collected = [p for p in collection]
        assert collected == [player1, player2]

    def test_contains(self):
        """Test __contains__ method"""
        player1 = Player("Alice", ChipCollection([Chip(100)]))
        player2 = Player("Bob", ChipCollection([Chip(200)]))
        collection = PlayerCollection([player1, player2])
        assert player1 in collection
        assert player2 in collection
        other_player = Player("Charlie", ChipCollection([Chip(300)]))
        assert other_player not in collection
