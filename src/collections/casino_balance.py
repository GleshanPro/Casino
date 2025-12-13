from collections import UserDict
from src.log_calls import log_calls

# from dataclasses import dataclass

"""
ПЛОХО - наследовать от базовых типов

class CasinoBalance(dict): 
    ...
"""

class CasinoBalance(UserDict): 
    
    @log_calls
    def __setitem__(self, key: str, value: int):
        # Декоратор сделать
        # logger.info(f"[CasinoBalance] {key} balance -> {value}")
        print(f"[CasinoBalance] {key} balance -> {value}")
        super().__setitem__(key, value)
        
    @log_calls
    def __getitem__(self, key):
        return super().__getitem__(key)
    
    @log_calls
    def __iter__(self):
        return iter(self.data)
    
    @log_calls
    def __len__(self):
        return len(self.data)
    
    @log_calls
    def add_money(self, key: str, amount: int):
        """
        :param key: Name of player whose balance will be updated
        :type key: str
        :param amount: Amount of money to add
        :type amount: int
        """
        self.data[key] += amount
        
    @log_calls
    def remove_money(self, key: str, amount: int):
        """
        :param key: Name of player whose balance will be updated
        :type key: str
        :param amount: Amount of money to remove
        :type amount: int
        """
        if (self.data[key] - amount < 0):
            ...
            return
        self.data[key] -= amount