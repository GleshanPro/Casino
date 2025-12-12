from dataclasses import dataclass

from src.player import Player

import random

@dataclass  # делает:
            # - конструктор __init__
            # - сравнение __eq__
            # - хэширование __hash__
            # - __repr__ - метод для отладки
class Goose:
    name: str
    hp: int
    honk_volume: int = 1
    
    def honk(self) -> None:
        print(f"{self.name} honks " + "HONK: " + self.honk_volume)
        

    def attack(self, target: Player, damage: int) -> None:
        print(f"{self.name} attacks {target.name} for {damage} damage")
    
    
    def __add__(self, other: "Goose") -> "Goose":
        name = f"{self.name}-{other.name}"
        hp = self.hp + other.hp
        honk_volume = self.honk_volume + other.honk_volume
        print(f"Flock formed: {name} (hp={hp}), honk_volume={honk_volume}")
        
    def __repr__(self) -> str:
        return f"Goose(name={self.name!r}, hp={self.hp}, honk_volume={self.honk_volume})"
    
    
class WarGoose(Goose):
    def attack(self, target: Player, damage: int | None = None) -> None:
        damage = damage or random.randint(8, 20)
        print(f"[WarGoose] {self.name} viciously attacks {target.name} for {damage} damage!")
        

class HonkGoose(Goose):
    def __call__(self, times: int | None = None) -> None:
        time = times or random.randInt(1, 4)
        self.honk_volume += time
        print(f"{self.name} prepares a mega-honk x{times}!")
        self.honk()
        
        