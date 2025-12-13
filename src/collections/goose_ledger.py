from collections import UserDict
class GooseLedger(UserDict):
    def __setitem__(self, key: str, value: int):
        print(f"[GooseLedger] {key} balance -> {value}")
        super().__setitem__(key, value)
        
    def __getitem__(self, key):
        return super().__getitem__(key)
        
    def __iter__(self):
        return iter(self.data)
    
    def __len__(self):
        return len(self.data)
    
    
    def add_money(self, key: str, amount: int):
        """
        :param key: Name of goose whose balance will be updated
        :type key: str
        :param amount: Amount of money to add
        :type amount: int
        """
        self.data[key] += amount
        
    def remove_money(self, key: str, amount: int):
        """
        :param key: Name of goose whose balance will be updated
        :type key: str
        :param amount: Amount of money to remove
        :type amount: int
        """
        if (self.data[key] - amount < 0):
            ...
            return
        self.data[key] -= amount