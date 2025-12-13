from collections import UserList

class PlayerCollection(UserList):
    def __init__(self):
        self.data = []
        
    def __iter__(self):
        return iter(self.data)
    
    def __len__(self):
        return len(self.data)
    
    def __getitem__(self, index):
        return self.data[index]