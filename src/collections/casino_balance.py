from collections import UserDict
from src.entities.chip import Chip
from src.collections.chip_collection import ChipCollection

class CasinoBalance(UserDict):
    """
    Dict-like collection for ChipCollection objects.
    Supports iteration and element manipulation
    """


    def __setitem__(self, key: str, value: ChipCollection):
        super().__setitem__(key, value)

    def __getitem__(self, key):
        return super().__getitem__(key)

    def __iter__(self):
        return iter(self.data)

    def __len__(self):
        return len(self.data)

    def add_money(self, key: str, chip: Chip):
        """
        :param key: Name of player whose balance will be updated
        :type key: str
        :param amount: Amount of money to add
        :type amount: int
        """
        self.data[key].append(chip)

    def remove_money(self, key: str, chip: int):
        """
        :param key: Name of player whose balance will be updated
        :type key: str
        :param amount: Amount of money to remove
        :type amount: int
        """
        if key not in self.data:
            raise KeyError(f"Player {key} not found in balance")
        if (self.data[key] - chip < 0):
            self.data[key] = 0
            return
        self.data[key].remove(chip)
