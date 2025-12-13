from src.collections.chip_collection import ChipCollection
from dataclasses import dataclass, field

@dataclass
class Player:
    name: str
    balance: ChipCollection = field(default_factory=ChipCollection)

    def __repr__(self) -> str:
        # Google: "Python __repr__ vs __str__ difference"
        return f"Player(name={self.name!r}, balance={self.balance})"

    def __eq__(self, other):
        # Google: "Python __eq__ magic method implementation"
        if not isinstance(other, Player):
            return NotImplemented
        return self.name == other.name and self.balance == other.balance
