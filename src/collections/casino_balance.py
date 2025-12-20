from src.entities.chip import Chip
from src.collections.chip_collection import ChipCollection
from loguru import logger

class CasinoBalance():
    """
    Dict-like collection for ChipCollection objects.
    Supports iteration and element manipulation
    """

    def __init__(self):
        self.dictionary = {}

    def __setitem__(self, key: str, value: ChipCollection):
        try:
            self.dictionary[key] = value
        except KeyError as e:
            logger.error(f"[ERROR]: {e}")

    def __getitem__(self, key: str) -> ChipCollection | None:
        try:
            return self.dictionary[key]
        except KeyError as e:
            logger.error(f"[ERROR]: {e}")
        return None

    def __getattribute__(self, key: str):
        if key == "items":
            return self.dictionary.items
        elif key == "keys":
            return self.dictionary.keys
        return object.__getattribute__(self, key)

    def __iter__(self):
        return iter(self.dictionary)

    def __len__(self):
        return len(self.dictionary)

    def add_money(self, key: str, chip: Chip):
        """
        :param key: Name of player whose balance will be updated
        :type key: str
        :param amount: Amount of money to add
        :type amount: int
        """
        self.dictionary[key].append(chip)

    def remove_money(self, key: str, chip: Chip):
        """
        :param key: Name of player whose balance will be updated
        :type key: str
        :param chip: Chip to remove
        :type chip: Chip
        """
        if key not in self.dictionary:
            logger.warning(f"Player {key} not found in casino balances")
            raise KeyError(f"Player {key} not found in casino balances")
        if self.dictionary[key].total_value() - chip < 0:
            self.dictionary[key] = ChipCollection()
            return
        self.dictionary[key].remove(chip)
