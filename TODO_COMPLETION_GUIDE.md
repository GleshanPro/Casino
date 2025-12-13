# Lab Work Completion Guide

This document outlines what has been implemented and what you need to complete.

## ✅ What's Already Done

### Collections
1. **PlayerCollection** - List-like collection with:
   - `__iter__`, `__len__`, `__getitem__` (including slice support)
   - `append()`, `remove()`, `__contains__`, `__repr__`

2. **ChipCollection** - List-like collection for Chip objects (same features as PlayerCollection)

3. **CasinoBalance** - Dict-like collection with:
   - `__setitem__`, `__getitem__`, `__iter__`, `__len__`
   - `add_money()`, `remove_money()`
   - Logging on balance changes

4. **GooseLedger** - Dict-like collection for goose incomes (same features as CasinoBalance)

### Classes
1. **Player** - Has `__repr__` and `__eq__`
2. **Goose** (base class) - Has `__add__` for flock formation, `__repr__`
3. **WarGoose** - Extends Goose, overrides `attack()` method
4. **HonkGoose** - Extends Goose, implements `__call__` magic method
5. **Chip** - Has `__add__`, `__radd__`, `__eq__`

### Casino & Simulation
1. **Casino.run_step()** - Implements random event selection with 8 different events
2. **run_simulation()** - Properly runs simulation with seed support and step iteration

## 🔧 What You Need to Complete

### 1. HonkGoose.__call__() Impact on Balances
**Location:** `src/goose.py`, line ~60

**Current state:** The method increases `honk_volume` but doesn't affect player balances.

**What to do:**
- When a HonkGoose is called, it should affect all player balances
- The impact should be based on `honk_volume`
- Example: Reduce all player balances by `honk_volume * 5`

**Google for:**
- "Python __call__ magic method impact on balance"
- "Python how to affect multiple players with single action"
- "Python accessing parent class attributes from method"

**Implementation hint:**
```python
# In HonkGoose.__call__(), after increasing honk_volume:
# You need access to the Casino instance to modify balances
# Consider passing casino as parameter or storing reference
```

### 2. Casino._event_honkgoose_honk() Logic
**Location:** `src/casino.py`, line ~150

**Current state:** Calls the goose but doesn't update balances.

**What to do:**
- After calling `goose()`, calculate damage based on `honk_volume`
- Apply damage to all players (or random subset)
- Update balances accordingly

**Google for:**
- "Python how to affect multiple players with single action"
- "Python iterate over dict values and modify"

**Implementation hint:**
```python
honk_damage = goose.honk_volume * 5
for player_name in self.players:
    if self.balances[player_name] >= honk_damage:
        self.balances[player_name] -= honk_damage
    else:
        self.balances[player_name] = 0
```

### 3. Using PlayerCollection in Casino (Optional Enhancement)
**Location:** `src/casino.py`, line ~14

**Current state:** Uses `dict[str, Player]` for players.

**What to do:**
- Consider using `PlayerCollection` instead of dict
- This would better demonstrate the list-like collection usage
- You'll need to modify methods that access players by name

**Google for:**
- "Python custom collection class usage"
- "Python find item in list by attribute"
- "Python list comprehension with condition"

**Implementation hint:**
```python
# Instead of: self.players[player_name]
# Use: next(p for p in self.players if p.name == player_name)
```

### 4. Negative Balance Handling
**Location:**
- `src/collections/casino_balance.py`, `remove_money()` method
- `src/collections/goose_ledger.py`, `remove_money()` method

**Current state:** Sets balance to 0 if it would go negative.

**What to do:**
- Decide on the desired behavior:
  - Option 1: Set to 0 (current implementation)
  - Option 2: Raise ValueError
  - Option 3: Only remove what's available
- Implement your chosen approach consistently

**Google for:**
- "Python negative balance prevention logic"
- "Python ValueError exception raising"

## 📚 Key Concepts to Research

### Collections
- **UserList/UserDict**: How Python's UserList and UserDict work
- **Slice support**: How to implement `__getitem__` with slice objects
- **Iterator protocol**: `__iter__` and `__next__` methods

### Magic Methods
- **__add__**: Operator overloading for addition
- **__call__**: Making objects callable
- **__repr__ vs __str__**: Difference between representation methods
- **__contains__**: Implementing `in` operator support
- **__getitem__**: Indexing and slicing support

### Random & Simulation
- **random.seed()**: Reproducible random sequences
- **random.choice()**: Selecting random items from sequences
- **random.randint()**: Generating random integers in range
- **random.sample()**: Selecting multiple random items without replacement

### Python Basics
- **isinstance()**: Type checking for inheritance
- **dict.get()**: Safe dictionary access with defaults
- **List comprehensions**: Filtering and transforming lists
- **Generator expressions**: Efficient iteration with `sum()`

## 🧪 Testing Your Implementation

After completing the TODOs:

1. **Test collections:**
   ```python
   # Test PlayerCollection slicing
   players = PlayerCollection([p1, p2, p3])
   print(players[1:3])  # Should return PlayerCollection

   # Test CasinoBalance logging
   balance = CasinoBalance({"Alice": 100})
   balance["Alice"] = 50  # Should log the change
   ```

2. **Test simulation:**
   ```python
   # Run with same seed twice - should produce identical results
   run_simulation(steps=10, seed=42)
   run_simulation(steps=10, seed=42)
   ```

3. **Test magic methods:**
   ```python
   # Test __add__ for geese
   flock = goose1 + goose2

   # Test __call__ for HonkGoose
   honk_goose(3)  # Should increase honk_volume and affect balances
   ```

## 📝 Notes

- All Google search suggestions are in comments throughout the code
- The simulation should produce different events each step
- Make sure all events properly update the collections
- Logging is important - check that balance changes are logged
- The `seed` parameter should make simulations reproducible

Good luck with your lab work! 🎰🦢
