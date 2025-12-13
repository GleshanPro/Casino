from src.simulation.run_simulation import run_simulation
from loguru import logger
import time
import sys

def setup_logger():
    logger.remove()
    logger.add("out.log")

def hello():
    print("=== Новогодняя казнь.. ой.. простите.. кхм-кхм... ===")
    time.sleep(0.8)
    sys.stdout.write('\x1b[1A')
    sys.stdout.write('\x1b[2K')
    print("=== НОВОГОДНЕЕ КАЗИНО! 🎄 🦢 🎰   ===")

def start():
    hello()

    steps = ""
    while not steps.isdigit():
        steps = input("Сколько тазиков оливье Вы готовы сегодня съесть?: ")
    steps = int(steps)

    seed = ""
    while not seed.isdigit():
        seed = input("Введите рецепт вашего оливье в виде цифры: ").strip()
    seed = int(seed)

    want_modifying = False
    if input("Компания, с которой человек празднует Новый Год - это крайне важно!\n Хотите ли вы изменить сегодняшнюю компанию? (да/нет) ") == "да":
        want_modifying = True

    run_simulation(steps, seed, want_modifying)


def main():
    setup_logger()
    start()


if __name__ == "__main__":
    main()
