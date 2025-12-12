from src.player import Player
from src.goose import Goose
from loguru import logger

from collections import UserDict
# from dataclasses import dataclass

"""
ПЛОХО - наследовать от базовых типов

class CasinoBalance(dict): 
    ...
"""

# class ...(UserList)

# UserDict - определена нужная база (см. исходный код)
class CasinoBalance(UserDict):
    def __setitem__(self, key: str, value: int):
        logger.info(f"[CasinoBalance] {key} balance -> {value}")
        print(f"[CasinoBalance] {key} balance -> {value}")
        super().__setitem__(key, value)
        
        
    def __iter__(self):
        return iter(self.data)
        
        
        
class GooseLedger(UserDict):
    def __setitem__(self, key: str, value: int):
        print(f"[GooseLedger] {key} balance -> {value}")
        super().__setitem__(key, value)
    

class Casino:
    def __init__(self, players: list[Player], gooses: list[Goose], ledger: GooseLedger | None) -> None:
        self.players: dict[str, Player] = {player.name: player for player in players}
        self.gooses: dict[str, Goose] = {goose.name: goose for goose in gooses}
        self.balances: CasinoBalance = CasinoBalance({player.name: player.balance for player in players})
        self.goose_ledger = ledger
        
    def run_step(self):
        ...    
    
    def register_player(self, player: Player) -> None:
        if player.name not in self.players:
            self.players[player.name] = 0
            
    def register_goose(self, goose: Goose) -> None:
        if goose.name not in self.goose_ledger:
            self.goose_ledger[goose.name] = 0
            
    def steal_from_player(self, goose: Goose, player_name: str, amount: int) -> None:
        player = self.players[player_name]
        print(f"{goose.name} tries to steal {amount} from {player.name}")
        self.balances[player.name] -= amount
        self.goose_ledger[goose.name] = self.goose_ledger.get(goose.name, 0) + amount
        print(f"{goose.name} successfully stole {amount} from {player.name}.")
        
    def show_state(self) -> None:
        print('\n--- CASINO STATE ---')
        print("Players:")
        for name, bal in self.balances.items():
            print(f"    {name}: {bal}")
        print("Goose:")
        for name, bal in self.goose_ledger.items():
            print(f"    {name}: {bal}")
        print('==================\n')
        

class Chip[T]:
    def __init__(self, amount: int):
        self.amount = amount
    
    def __add__(self, other: T) -> T:
        if not isinstance(other, Chip | int):
            logger.error("Tried to add Chip to incompatible type")
            return NotImplemented
        
        amount = self.amount
        if isinstance(other, int):
            amount += other
        else:
            amount += other.amount
        
        return Chip(amount)
    
    # Chip в качестве правого операнда
    def __radd__(self, other: T) -> T:
        return self.__add__(other)
        
    def __eq__(self, other: T | int) -> bool:
        if not isinstance(other, Chip | int):
            logger.error("Tried to compare Chip to incompatible type")
            return NotImplemented
        
        if isinstance(other, int):
            return self.amount == other
        else:
            return self.amount == other.amount
        
    
    def get_amount(self):
        return self.amount
        
        