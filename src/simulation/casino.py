from loguru import logger
import random

from src.entities.player import Player
from src.entities.goose import Goose, WetBanditGoose, DriverGoose, KevinGoose
from src.entities.chip import Chip

from src.collections.chip_collection import ChipCollection
from src.collections.casino_balance import CasinoBalance
from src.collections.player_collection import PlayerCollection
from src.collections.goose_collection import GooseCollection

class Casino:
    def __init__(self, players: PlayerCollection | None = None, gooses: GooseCollection | None = None) -> None:
        # Initialize collections
        self.players: PlayerCollection = PlayerCollection()
        self.gooses: GooseCollection = GooseCollection()
        self.balances: CasinoBalance = CasinoBalance()
        self.goose_ledger: CasinoBalance = CasinoBalance()
        self.balance = 0

        # Register players and geese
        if players is not None:
            for player in players:
                self.register_player(player)

        if gooses is not None:
            for goose in gooses:
                self.register_goose(goose)

        # Initialize events
        self.events = [
            self._event_player_bet,
            self._event_wetbanditgoose_rob,
            self._event_drivergoose_horn,
            self._event_goose_steal,
            self._event_goose_flock,
            self._event_player_panic,
            self._event_kevingoose_trap
        ]

        logger.info("Initialized Casino object.")

    def get_balance_total(self, balance: ChipCollection) -> int:
        """
        ChipCollection total value
        """
        return balance.total_value() if balance else 0

    def add_chip_to_balance(self, name: str, amount: int, is_goose: bool = False) -> None:
        """
        Add chip to a ChipCollection
        """
        goose_text = ""
        if is_goose:
            goose_text = " (Goose)"
            balance = self.goose_ledger[name]
        else:
            balance = self.balances[name]
            name = name

        if amount > 0:
            balance.append(Chip(amount))

            logger.info(f"Added Chip({amount}) to balance of {name}{goose_text}")


    def remove_chip_from_balance(self, name: str, amount: int, is_goose: bool = False) -> bool:
        """
        Remove chips from balance.
        Returns True if successful, False if insufficient funds.
        """
        goose_text = ""
        if is_goose:
            goose_text = " (Goose)"
            balance = self.goose_ledger[name]
        else:
            balance = self.balances[name]
            name = name

        amount = int(amount)
        total = self.get_balance_total(balance)
        if total < amount:
            logger.warning(f"Tried to remove chips for ({amount}) from balance of {name}{goose_text}, but its balance total value={total}")
            return False

        # Remove chips until we've removed enough
        remaining = amount
        chips_to_remove = []

        # Collect chips to remove
        for chip in balance:
            if remaining <= 0:
                break
            if chip.amount <= remaining:
                chips_to_remove.append(chip)
                remaining -= chip.amount
            else:
                chip.amount -= remaining
                remaining = 0

        # Remove collected chips
        for chip in chips_to_remove:
            balance.remove(chip)

        new_balance = self.get_balance_total(balance)
        logger.info(f"Removed Chips for amount ({amount}) from balance of {name}{goose_text}. Current balance: {new_balance}")

        return True

    def run_step(self):
        """
        Execute one random event in the simulation.
        """
        event = random.choice(self.events)
        logger.info(f"---Event: {event}---")
        event()

    def register_player(self, player: Player) -> None:
        if player.name not in self.balances:
            self.players.append(player)
            self.balances[player.name] = player.balance
            logger.info(f"Registered player, name={player.name}")

    def register_goose(self, goose: Goose) -> None:
        if goose.name not in self.goose_ledger:
            self.gooses.append(goose)
            self.goose_ledger[goose.name] = goose.balance
            logger.info(f"Registered goose, name={goose.name}")

    def steal_from_player(self, goose: Goose, player_name: str, amount: int) -> None:
        player_balance: ChipCollection = self.balances[player_name]
        if player_name not in self.balances:
            logger.warning(f"Player {player_name} not found. Players: {self.players}")
            return
        if goose.name not in self.goose_ledger:
            logger.warning(f"Goose {goose.name} not found. Gooses: {self.gooses}")
            return

        player_total = self.get_balance_total(player_balance)

        if player_total < amount:
            amount = player_total

        print(f"[ВНИМАНИЕ] Гусь {goose.name} пытается украсть {amount} рублей у игрока {player_name}")
        logger.info(f"Goose {goose.name} trying to steal {amount} from player {player_name}")

        success = bool(random.getrandbits(1))
        if success:
            if amount > 0:
                self.remove_chip_from_balance(player_name, amount)
                self.add_chip_to_balance(goose.name, amount, True)
            else:
                goose_balance = ChipCollection()
                self.goose_ledger[goose.name] = goose_balance
                self.add_chip_to_balance(goose.name, amount, True)
            print(f"[СВОРОВАЛ] Игрок {player_name} загляделся на новогоднюю ёлку с ярко горящими гирляндами и шарами, а гусь {goose.name} - не пальцем деланный, воспользовался этим и успешно своровал у него {amount} рублей.")
            logger.info(f"SUCCESS - Goose {goose.name} stole {amount} from {player_name}.")
        else:
            print(f"[ОТБИЛСЯ] Игрок {player_name} выпил шампанского для смелости и, не побоявшись даже зубов гуся {goose.name}, гордо отбился от него, не проронив ни копейки.")
            logger.info(f"FAILURE - Goose {goose.name} didn't steel anything from {player_name}.")

    def print_balance_update_entity(self, entity: Player | Goose):
        balance = self.get_balance_total(entity.balance)
        print(f"[ОБНОВЛЕНИЕ БАЛАНСА] Баланс {entity.name} -> {balance}")
        logger.info(f"[BALANCE UPD] {type(entity)} {entity.name} -> {balance}")

    def print_balance_update(self, name: str, balance: int):
        print(f"[ОБНОВЛЕНИЕ БАЛАНСА] Баланс {name} -> {balance}")
        logger.info(f"[BALANCE UPD] {name} -> {balance}")

    @staticmethod
    def event_with_probability(probability: float) -> bool:
        """
        Randomly calculate if some event should happen with probability

        :param probability: 0 < probability < 1
        """
        return random.random() < probability

    def bet(self, player_name: str, amount: int):
        player_balance: ChipCollection = self.balances[player_name]
        total_value = self.get_balance_total(player_balance)
        if total_value < amount:
            logger.warning("Attempted to bet when unsufficient funds")
            return

        self.remove_chip_from_balance(player_name, amount)

        win = self.event_with_probability(0.6)
        jackpot = self.event_with_probability(0.3)
        if jackpot:
            win_amount = amount * 100
            self.add_chip_to_balance(player_name, win_amount)
            print(f"[ДЖЕКПОТ!] ИГРОКУ {player_name} НЕВЕРОЯТНО ПОВЕЗЛО, ВСЕ ЗВЁЗДЫ СОШЛИСЬ, И ОН ВЫИГРЫВАЕТ {win_amount} РУБЛЕЙ!")
            logger.info(f"[JACKPOT] Player {player_name} got Jackpot and won {win_amount}")
        elif win:
            coef = 1.2 + random.random()
            win_amount = int(amount * coef)
            self.add_chip_to_balance(player_name, win_amount)
            print(f"[ВЫИГРЫШ] У игрока {player_name} сбылось новогоднее желание, он приумножил свою ставку {amount} рублей в {coef} раза и получил {win_amount} рублей!")
            logger.info(f"[WIN] Player {player_name} won {win_amount}")
        else:
            print(f"[ПРОИГРЫШ] Игрок {player_name} ГЛУПО проиграл свои {amount} рублей, стыд и позор! Ты плохо вёл себя в этом году, не жди подарка от Деда Мороза.")
            self.balance += amount
            logger.info(f"[LOSE] Player {player_name} lost {amount}")
        self.print_balance_update(player_name, self.get_balance_total(player_balance))

    def _event_player_bet(self) -> None:
        """
        Random player makes a bet.
        """
        if not self.players:
            logger.warning("[!WARN!] No players")
            return
        player_name = random.choice(list(self.balances.keys()))
        player_balance = self.balances[player_name]
        player_total = self.get_balance_total(player_balance)
        bet_amount = 0
        if player_total > 10:
            bet_amount = random.randint(10, player_total)
        else:
            bet_amount = player_total

        if bet_amount == 0:
            print(f"[ПОПЫТКА СТАВКИ] {player_name} пытался сделать ставку, но у него нет денег(")
            return

        print(f"[СТАВКА] {player_name} делает ставку в размере {bet_amount}")
        self.bet(player_name, bet_amount)

    def pick_random_goose(self, GooseType: Goose) -> Goose | None:
        gooses = [g for g in self.gooses if isinstance(g, GooseType)]
        if not gooses:
            return

        return random.choice(gooses)
    def goose_attack(self, GooseType: Goose, func_name: str) -> None:
        """
        General method for attacks
        """

        goose = self.pick_random_goose(GooseType)
        player = random.choice(self.players)
        player_name = player.name

        damage = getattr(goose, func_name)(player)
        player_balance = self.balances[player_name]
        player_total = self.get_balance_total(player_balance)

        if player_total >= damage:
            self.remove_chip_from_balance(player_name, damage)
            # Goose gains money from attack
            self.add_chip_to_balance(goose.name, damage, True)
        else:
            # Take all remaining money
            if player_total > 0:
                self.remove_chip_from_balance(player_name, player_total)
                self.add_chip_to_balance(goose.name, player_total, True)

    def _event_kevingoose_trap(self) -> None:
        """
        KevinGoose attacks a random player.
        """
        self.goose_attack(KevinGoose, "trap")

    def _event_wetbanditgoose_rob(self) -> None:
        """
        WetBanditGoose attacks a random player.
        """
        self.goose_attack(WetBanditGoose, "rob")

    def _event_drivergoose_horn(self) -> None:
        """
        DriverGoose uses its special honk ability.
        """
        if not self.gooses:
            return

        # Find DriverGoose instances
        goose: DriverGoose = self.pick_random_goose(DriverGoose)

        honk_damage = goose()
        total_stolen = 0

        for player_name in list(self.balances.keys()):
            player_balance = self.balances[player_name]
            player_total = self.get_balance_total(player_balance)

            if player_total >= honk_damage:
                self.remove_chip_from_balance(player_name, honk_damage)
                total_stolen += honk_damage
            elif player_total > 0:
                self.remove_chip_from_balance(player_name, player_total)
                total_stolen += player_total

        # Goose gains all stolen money
        if total_stolen > 0:
            self.add_chip_to_balance(goose.name, total_stolen, True)
            print(f"[ПОТЕРЯ] От гудка {goose.name} все игроки подпрыгнули и обронили в общем счёте {total_stolen} рублей!")
            logger.info(f"[LOSE] DriverGoose honked and stole {total_stolen} from each player")
            self.print_balance_update_entity(goose)

    def _event_goose_steal(self) -> None:
        """
        Random goose tries to steal from random player.
        """
        if not self.players or not self.gooses:
            return

        goose = random.choice(self.gooses)
        player_name = random.choice(list(self.balances.keys()))
        amount = random.randint(5, 40)
        self.steal_from_player(goose, player_name, amount)

    def _event_goose_flock(self) -> None:
        """
        Two geese form a flock using
        """
        if len(self.gooses) < 2:
            return

        selected = random.sample(self.gooses, 2)
        goose1 = selected[0]
        goose2 = selected[1]

        print("[СТАЯ] Гуси формируют стаю!")
        flock = goose1 + goose2
        self.register_goose(flock)

    def _event_player_panic(self) -> None:
        """
        Random player panics and loses all money.
        """
        if not self.players:
            return

        player = random.choice(self.players)
        player_balance = self.balances[player.name]
        lost_amount = self.get_balance_total(player_balance) // 2

        print(f"[ПАНИКА] {player.name} поверил, что прохожий с бородой - Дед Мороз и отгрохал ему ПОЛОВИНУ своего СОСТОЯНИЯ! ({lost_amount} рублей потеряно)")
        logger.info(f"[PANIC] {player.name} lost half of his money: {lost_amount}")

        self.remove_chip_from_balance(player.name, lost_amount)

    def show_state(self) -> None:
        """
        Show current state of the game: casino's, players' and geese's balances.
        """
        print('\n--- CASINO STATE ---')
        print("Players:")
        for name, balance in self.balances.items():
            total = self.get_balance_total(balance)
            print(f"    {name}: {total} (chips: {len(balance)})")
        print("Goose:")
        for name, balance in self.goose_ledger.items():
            total = self.get_balance_total(balance)
            print(f"    {name}: {total} (chips: {len(balance)})")
        print(f"Casino balance: {self.balance}")
        print('==================\n')
        logger.info("Showed state.")
