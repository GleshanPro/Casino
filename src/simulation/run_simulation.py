import random
from src.simulation.casino import Casino
from loguru import logger
from src.simulation.set_collections import set_players, set_gooses
from src.collections.player_collection import PlayerCollection
from src.collections.goose_collection import GooseCollection

def run_simulation(steps: int = 20, seed: int | None = None, want_modyfing: bool = False) -> None:
    """
    Run the casino simulation for specified number of steps.

    Args:
        steps: Number of simulation steps to execute
        seed: Random seed for reproducible simulation (None for random)

    """
    if seed is not None:
        random.seed(seed)
        logger.info(f"Random seed set to {seed}")

    logger.info(f"Started simulation with parameters: steps={steps}, seed={seed}")

    players: PlayerCollection = set_players(want_modyfing)
    gooses: GooseCollection = set_gooses(want_modyfing)

    casino = Casino(players, gooses)


    print("\n=== ИЗНАЧАЛЬНОЕ СОСТОЯНИЕ ===")
    casino.show_state()

    for i in range(1, steps + 1):
        print(f"---{i}-Я ЛОЖКА ОЛИВЬЕ, АМ-НЯМ-НЯМ...---\n")
        casino.run_step()
        print()

    # Set balances
    for player in players:
        player.balance = casino.balances.get(player.name, player.balance)

    for goose in gooses:
        goose.balance = casino.goose_ledger.get(goose.name, goose.balance)


    print("\n=== ИТОГОВОЕ СОСТОЯНИЕ ===")
    casino.show_state()

    logger.info(f"Simulation completed after {steps} steps")
