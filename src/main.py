from src.goose import WarGoose, HonkGoose
from src.player import Player
from src.casino import Casino, GooseLedger
from loguru import logger
import string
import sys

"""
Задача - сделать свой турнир.
Придумать самому, какие методы и поля есть у Гуся, Игрока, Казино
КРЕАТИВНЫЙ КАЗИК! - ДОП БАЛЛЫ.
Гуси - коллекторское агенство.
- Функция симулятор должна быть

Пользователь может:
- поставить на паузу
- добавить денег
- добавить урон/гусей
"""
def run_simulation(steps: int = 20, seed: int | None = None) -> None:
    logger.info(f"Started simulation with parameters: steps={steps}, seed={seed}")
    
    gus = WarGoose(name="Gus", hp=40, honk_volume=2)
    boba = HonkGoose(name="Boba", hp=30, honk_volume=3)
    jack = Player(name="Jack", balance=128)
    mia = Player(name="Mia", balance=239)

    goose_ledger = GooseLedger()

    casino = Casino(players=[jack, mia], gooses=[gus, boba], ledger=goose_ledger)
    casino.register_goose(gus)
    casino.register_goose(boba)

    casino.show_state()

    # Объединяем гусей в "стак" (демонстрация __add__)
    flock = gus + boba
    casino.register_goose(flock)

    # WarGoose атакует Jack напрямую
    gus.attack(jack)
    casino.balances["Jack"] = jack.balance

    # Boba использует __call__, чтобы усилить HONK
    boba(2)

    # Стая ворует фишки у игроков
    casino.steal_from_player(flock, player_name="Jack", amount=25)
    casino.steal_from_player(flock, player_name="Mia", amount=40)

    casino.show_state()
    
    
def setup_logger():
    logger.remove()
    logger.add("out.log")
    # logger.add(
    #     "out.log",
    #     format="{time:YYYY-MM-DD HH:mm:ss:ms} | {level} | {message}",
    #     level="INFO"
    # )
    # logger.add(
    #     "out.log",
    #     colorize=True,
    #     format="{time:YYYY-MM-DD HH:mm:ss:ms} | ***{level}*** | {message}",
    #     level="ERROR",
    # )
    

if __name__ == "__main__":
    setup_logger()
    
    print("=== Goose & Casino Simulation ===")
    steps = ""
    while not steps.isdigit():
        steps = input("How much steps of simulation do you want?: ")
    steps = int(steps)
        
    seed = ""
    while not seed.isdigit():
        seed = input("Write seed (number): ")
    seed = int(seed)

    run_simulation(steps, seed)
    
    
