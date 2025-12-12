import pytest
from src.casino import Chip

def test_deposit_chip():
    chip1: Chip = Chip(200)
    chip2: Chip = Chip(10)
    
    chip3 = 10 + chip1
    print("HI: ", chip1, chip2, chip3)
    assert chip3 == 210
    
    
# def test_chip_add_string():
#     chip1: Chip = Chip(200)
#     chip2: Chip = Chip(10)
    
#     chip3 = chip1 + "abc"