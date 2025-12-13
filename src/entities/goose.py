from loguru import logger

from dataclasses import dataclass, field

from src.entities.player import Player
from src.collections.chip_collection import ChipCollection

import random

@dataclass
class Goose:
    name: str
    hp: int
    honk_volume: int = 1
    balance: ChipCollection = field(default_factory=ChipCollection)

    def honk(self) -> None:
        # target - one player, not many
        print(f"{self.name} гогочет " + "УРОВЕНЬ ГОГОТА: ", self.honk_volume)
        logger.info(f"[Goose] {self.name} honks, honk_volume={self.honk_volume}")


    def attack(self, target: Player, damage: int) -> int:
        print(f"Гусь {self.name} атакует игрока {target.name} и наносит {damage} урона")
        logger.info(f"[Goose] {self.name} attacks {target.name} for {damage} damage")
        return damage


    def __add__(self, other: "Goose"):
        if not isinstance(other, Goose):
            logger.error("Tried to make flock out of Goose and some incompatible type")
            return NotImplemented

        name = f"{self.name}-{other.name}"
        hp = self.hp + other.hp
        honk_volume = self.honk_volume + other.honk_volume

        combined_balance = ChipCollection()
        combined_balance.data = self.balance.data + other.balance.data
        print(f"Стая сформирована: {name} (hp={hp}), honk_volume={honk_volume}")
        logger.info(f"[Goose] Flock formed: {name} (hp={hp}), honk_volume={honk_volume}")
        return Goose(name, hp, honk_volume, balance=combined_balance)


    def __repr__(self) -> str:
        return f"Goose(name={self.name!r}, hp={self.hp}, honk_volume={self.honk_volume})"


class WarGoose(Goose):
    def attack(self, target: Player, damage: int | None = None) -> int:
        damage = damage or random.randint(8, 20)
        print(f"[WarGoose] {self.name} свирепо атакует игрока {target.name} и наносит {damage} урона!")
        logger.info(f"[WarGoose] {self.name} attacks {target.name} for {damage} damage")
        return damage




class HonkGoose(Goose):
    def __call__(self, times: int | None = None) -> None:
        times = times or random.randint(1, 4)
        self.honk_volume += times
        print(f"{self.name} готовит мега-гогот x{times}!")
        self.honk()

        logger.info(f"[HonkGoose] {self.name} called")
