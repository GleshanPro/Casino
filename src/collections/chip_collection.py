from collections import UserList
from src.entities.chip import Chip

class ChipCollection(UserList):
    """
    List-like collection for Chip objects
    Supports indexing, slicing, iteration, and element manipulation
    """
    def __init__(self, initlist=None):
        if initlist is None:
            initlist = []
        super().__init__(initlist)

    def __iter__(self):
        return iter(self.data)

    def __len__(self):
        return len(self.data)

    def __getitem__(self, index):
        if isinstance(index, slice):
            return ChipCollection(self.data[index])
        return self.data[index]

    def append(self, item: Chip):
        if not isinstance(item, Chip):
            raise TypeError(f"Expected Chip, got {type(item)}")
        self.data.append(item)

    def remove(self, item: Chip):
        if item not in self.data:
            raise ValueError(f"{item} not in collection")
        self.data.remove(item)

    def __contains__(self, item: Chip):
        return item in self.data

    def __repr__(self):
        """
        Shows total value of all chips in collection.
        """
        return f"{self.total_value()}"

    def total_value(self) -> int:
        """
        Calculate total value of all chips in collection.
        """
        return sum(chip.amount for chip in self.data)
