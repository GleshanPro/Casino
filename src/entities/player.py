from src.collections.chip_collection import ChipCollection
from dataclasses import dataclass, field

@dataclass
class Player:
    name: str
    balance: ChipCollection = field(default_factory=ChipCollection)

    def __repr__(self) -> str:
        return f"Player(name={self.name!r}, balance={self.balance})"

    def __eq__(self, other):
        if not isinstance(other, Player):
            return NotImplemented
        return self.name == other.name and self.balance == other.balance
