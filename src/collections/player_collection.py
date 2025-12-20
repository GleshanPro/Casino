from collections import UserList
from src.entities.player import Player

class PlayerCollection(UserList):
    """
    List-like collection for Player objects
    """

    def __init__(self, initlist: list[Player] | None = None):
        if initlist is None:
            initlist = []
        super().__init__(initlist)

    def __iter__(self):
        return iter(self.data)

    def __len__(self):
        return len(self.data)

    def __getitem__(self, index):
        if isinstance(index, slice):
            return PlayerCollection(self.data[index])
        return self.data[index]

    def append(self, item):
        self.data.append(item)

    def remove(self, item):
        if item not in self.data:
            raise ValueError(f"{item} not in collection")
        self.data.remove(item)

    def __contains__(self, item):
        return item in self.data

    def __repr__(self):
        return f"PlayerCollection({self.data})"
