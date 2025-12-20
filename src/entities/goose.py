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
        print(f"[ГОГОТ] {self.name} гогочет с громкостью: ", self.honk_volume)
        logger.info(f"[HONK] {self.name} honks, honk_volume={self.honk_volume}")


    def attack(self, target: Player, damage: int | None = None) -> int:
        damage = damage or random.randint(3, 50)
        print(f"[АТАКА] Гусь {self.name} атакует игрока {target.name} и получает с него {damage} рублей")
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
        print(f"[СТАЯ] Сформирована стая: {name} (hp={hp}), honk_volume={honk_volume}")
        logger.info(f"[Goose] Flock formed: {name} (hp={hp}), honk_volume={honk_volume}")
        return Goose(name, hp, honk_volume, balance=combined_balance)


    def __repr__(self) -> str:
        return f"Goose(name={self.name!r}, hp={self.hp}, honk_volume={self.honk_volume})"


class WetBanditGoose(Goose):
    def rob(self, target: Player, damage: int | None = None) -> int:
        damage = damage or random.randint(8, 20)
        print(f"[ОГРАБЛЕНИЕ] {self.name} забрался в дом игрока {target.name} и обокрал его на {damage} рублей!")
        logger.info(f"[HEIST] {self.name} attacks {target.name} for {damage} damage")
        return damage

class KevinGoose(Goose):
    def trap(self, target: Player, damage: int | None = None) -> int:
        damage = damage or random.randint(1, 100)
        print(f"[ЛОВУШКА] Игрок {target.name} попался в ловушку гусю {self.name} и потерял {damage} рублей!")
        logger.info(f"[TRAP] {target.name} fell into {self.name}'s trap and lost {damage} money!")
        return damage

    # def prank(self, target: Player, damage: int | None = None) -> None:
    #     damage = damage or random.randint(1, 50)
    #     print(f"[РОЗЫГРЫШ] Гусь {self.name} развёл игрока {target.name} попался в ловушку гусю  и потерял {damage} рублей!")
    #     logger.info(f"[PRANK] {target.name} was pranked by goose {self.name} and lost {damage} money")
    #     return damage

class DriverGoose(Goose):
    def __call__(self, times: int | None = None) -> int:
        logger.info(f"[DriverGoose] {self.name} called")

        times = times or random.randint(1, 4)
        coef = 1 + random.random() * random.randint(1, 2)

        self.honk_volume += times
        return int(self.horn() * coef)

    def horn(self) -> int:
        print(f"[ГУДОК] {self.name} сигналит на своём фургоне с громкостью: ", self.honk_volume)
        logger.info(f"[HORN] {self.name} horns, honk_volume={self.honk_volume}")
        return self.honk_volume
