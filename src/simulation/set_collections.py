from src.collections.player_collection import PlayerCollection
from src.collections.goose_collection import GooseCollection
from src.collections.chip_collection import ChipCollection
from src.entities.player import Player
from src.entities.goose import Goose, KevinGoose, WetBanditGoose, DriverGoose
from src.entities.chip import Chip

def input_players() -> PlayerCollection:
    """
    Get player data from user input.
    """
    players = PlayerCollection()
    print("\n=== Создание игроков ===")

    while True:
        name = input("Введите имя игрока (или 'готово' для завершения): ").strip()
        if name.lower() in ['готово', '']:
            break

        try:
            balance_str = input(f"Начальный баланс для {name} (целое число, кратное 5): ").strip()
            balance_amount = int(balance_str)

            balance = ChipCollection()
            if balance_amount > 0:
                balance.append(Chip(balance_amount - (balance_amount % 5)))

            player = Player(name=name, balance=balance)
            players.append(player)
            print(f"✓ Игрок {name} добавлен с балансом {balance_amount}")
        except ValueError:
            print("✗ Ошибка: введите целое число для баланса")
        except Exception as e:
            print(f"✗ Ошибка: {e}")

    return players

def input_gooses() -> GooseCollection:
    """
    Get goose data from user input.
    """
    gooses = GooseCollection()
    print("\n=== Создание гусей ===")

    while True:
        name = input("Введите имя гуся (или 'готово' для завершения): ").strip()
        if name.lower() in ['готово', 'done', '']:
            break

        try:
            goose_type = input(f"Тип гуся для {name} (war/honk/regular): ").strip().lower()
            hp_str = input(f"HP для {name}: ").strip()
            hp = int(hp_str)
            honk_volume_str = input(f"Громкость крика для {name} (по умолчанию 1): ").strip()
            honk_volume = int(honk_volume_str) if honk_volume_str else 1

            # Create ChipCollection for goose balance
            balance = ChipCollection()
            initial_balance_str = input(f"Начальный баланс для {name} (по умолчанию 0): ").strip()
            if initial_balance_str:
                initial_balance = int(initial_balance_str)
                if initial_balance > 0:
                    balance.append(Chip(initial_balance))

            if goose_type == 'war':
                goose1 = WetBanditGoose(name=name, hp=hp, honk_volume=honk_volume, balance=balance)
                gooses.append(goose1)
            elif goose_type == 'honk':
                goose2 = DriverGoose(name=name, hp=hp, honk_volume=honk_volume, balance=balance)
                gooses.append(goose2)
            else:
                goose3 = Goose(name=name, hp=hp, honk_volume=honk_volume, balance=balance)
                gooses.append(goose3)


            print(f"✓ Гусь {name} добавлен")
        except ValueError:
            print("✗ Ошибка: введите целое число")
        except Exception as e:
            print(f"✗ Ошибка: {e}")

    return gooses

def set_players(want_modifying: bool) -> PlayerCollection:
    """
    Create players collection with user interaction.
    Allows viewing slices and modifying the collection.
    """
    print("\n=== Настройка игроков ===")

    # Create default
    players = PlayerCollection()
    oleg = Player(name="Олег", balance=ChipCollection([Chip(500)]))
    max = Player(name="Макс", balance=ChipCollection([Chip(1000)]))
    kira = Player(name="Кира", balance=ChipCollection([Chip(10000)]))
    players.append(oleg)
    players.append(max)
    players.append(kira)
    print("✓ Созданы игроки по умолчанию: Олег (50), Макс (1000), Кира(10000)")
    print(f"Текущее состояние: {len(players)} игроков")

    while want_modifying:
        print("\n--- Управление коллекцией игроков ---")
        print("1. Показать всех игроков")
        print("2. Показать срез (slice)")
        print("3. Добавить игрока")
        print("4. Удалить игрока")
        print("5. Очистить и создать вручную")
        print("6. Продолжить")

        choice = input("Выберите действие (1-6): ").strip()

        if choice == '1':
            print(f"\nВсего игроков: {len(players)}")
            for i, player in enumerate(players):
                print(f"  {i}: {player.name} ({player.balance})")

        elif choice == '2':
            try:
                slice_str = input("Введите срез (например, 0:2 или :1): ").strip()
                if ':' in slice_str:
                    parts = slice_str.split(':')
                    start = int(parts[0]) if parts[0] else None
                    end = int(parts[1]) if parts[1] else None
                    step = int(parts[2]) if len(parts) > 2 and parts[2] else None
                    slice_obj = slice(start, end, step)
                else:
                    idx = int(slice_str)
                    slice_obj = slice(idx, idx + 1)

                for player in players[slice_obj]:
                    print(f" {player.name} ({player.balance})")
            except (ValueError, IndexError) as e:
                print(f"✗ Ошибка: {e}")

        elif choice == '3':
            try:
                name = input("Имя игрока: ").strip()
                balance_str = input("Баланс: ").strip()
                balance_amount = int(balance_str)
                balance = ChipCollection()
                if balance_amount > 0:
                    balance.append(Chip(balance_amount))
                players.append(Player(name=name, balance=balance))
                print(f"✓ Игрок {name} добавлен")
            except ValueError:
                print("✗ Ошибка: введите целое число")

        elif choice == '4':
            try:
                idx_str = input("Индекс игрока для удаления: ").strip()
                idx = int(idx_str)
                removed = players[idx]
                players.remove(removed)
                print(f"✓ Игрок {removed.name} удален")
            except (ValueError, IndexError) as e:
                print(f"✗ Ошибка: {e}")

        elif choice == '5':
            players.data.clear()
            players = input_players()
            print(f"✓ Создано {len(players)} игроков вручную")

        elif choice == '6':
            break

        else:
            print("✗ Неверный выбор")

    return players

def set_gooses(want_modifying: bool) -> GooseCollection:
    """
    Create gooses collection with user interaction.
    Allows viewing slices and modifying the collection.
    """
    print("\n=== Настройка гусей ===")

    # Сreate default gooses first
    gooses = GooseCollection()
    gus_balance = ChipCollection([Chip(10)])
    boba_balance = ChipCollection([Chip(15)])
    buba_balance = ChipCollection([Chip(0)])
    kevin_balance = ChipCollection([Chip(100)])
    biba = WetBanditGoose(name="Биба", hp=40, honk_volume=2, balance=gus_balance)
    boba = DriverGoose(name="Боба", hp=30, honk_volume=3, balance=boba_balance)
    buba = Goose(name="Буба", hp=100, honk_volume=3, balance=buba_balance)
    kevin = KevinGoose(name="Кевин", hp=200, honk_volume=10, balance=kevin_balance)
    gooses.append(biba)
    gooses.append(boba)
    gooses.append(buba)
    gooses.append(kevin)
    print("✓ Созданы гуси по умолчанию: Биба (WetBanditGoose), Боба (DriverGoose), Кевин (KevinGoose), Буба")
    print(f"Текущее состояние: {len(gooses)} гусей")

    while want_modifying:
        print("\n--- Управление коллекцией гусей ---")
        print("1. Показать всех гусей")
        print("2. Показать срез (slice)")
        print("3. Добавить гуся")
        print("4. Удалить гуся")
        print("5. Очистить и создать вручную")
        print("6. Продолжить")

        choice = input("Выберите действие (1-6): ").strip()

        if choice == '1':
            print(f"\nВсего гусей: {len(gooses)}")
            for i, goose in enumerate(gooses):
                print(f"  {i}: {goose}")

        elif choice == '2':
            try:
                slice_str = input("Введите срез (например, 0:2 или :1): ").strip()
                if ':' in slice_str:
                    parts = slice_str.split(':')
                    start = int(parts[0]) if parts[0] else None
                    end = int(parts[1]) if parts[1] else None
                    step = int(parts[2]) if len(parts) > 2 and parts[2] else None
                    slice_obj = slice(start, end, step)
                else:
                    idx = int(slice_str)
                    slice_obj = slice(idx, idx + 1)

                for goose in gooses[slice_obj]:
                    print(f" {goose.name} ({goose.balance})")
            except (ValueError, IndexError) as e:
                print(f"✗ Ошибка: {e}")

        elif choice == '3':
            try:
                name = input("Имя гуся: ").strip()
                goose_type = input("Тип (war/honk/regular): ").strip().lower()
                hp = int(input("HP: ").strip())
                honk_volume = int(input("Громкость крика: ").strip() or "1")
                balance = ChipCollection()

                if goose_type == 'war':
                    new_goose1 = WetBanditGoose(name=name, hp=hp, honk_volume=honk_volume, balance=balance)
                    gooses.append(new_goose1)
                elif goose_type == 'honk':
                    new_goose2 = DriverGoose(name=name, hp=hp, honk_volume=honk_volume, balance=balance)
                    gooses.append(new_goose2)
                else:
                    new_goose3 = Goose(name=name, hp=hp, honk_volume=honk_volume, balance=balance)
                    gooses.append(new_goose3)


                print(f"✓ Гусь {name} добавлен")
            except ValueError:
                print("✗ Ошибка: введите целое число")

        elif choice == '4':
            try:
                idx_str = input("Индекс гуся для удаления: ").strip()
                idx = int(idx_str)
                removed = gooses[idx]
                gooses.remove(removed)
                print(f"✓ Гусь {removed.name} удален")
            except (ValueError, IndexError) as e:
                print(f"✗ Ошибка: {e}")

        elif choice == '5':
            gooses.data.clear()
            gooses = input_gooses()
            print(f"✓ Создано {len(gooses)} гусей вручную")

        elif choice == '6':
            break

        else:
            print("✗ Неверный выбор")

    return gooses
