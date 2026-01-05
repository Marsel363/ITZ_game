import random


class Adventure:
    def __init__(self, data_manager):
        self.data_manager = data_manager

    def start_game(self, player):
        print("\nНачало игры")

        if player.current_trial > 0:
            print(f"Продолжение с испытания {player.current_trial + 1}")

        challenges = [self.challenge_1, self.challenge_2, self.challenge_3, self.challenge_4]

        for i in range(player.current_trial, len(challenges)):
            player.current_trial = i
            challenges[i](player)
            self.data_manager.save_player_data(player.save_data())

            if not player.is_alive():
                print("\nВы погибли")
                self.data_manager.return_artifacts(player.artifacts)
                return

        if not player.boss_defeated:
            self.final_battle(player)
            self.data_manager.save_player_data(player.save_data())

        if player.boss_defeated:
            self.end_game(player)

    def fight(self, player, enemy_name, enemy_health, enemy_attack):
        print(f"\nБой с {enemy_name}")

        while enemy_health > 0 and player.is_alive():
            print(f"\nВаше здоровье: {player.health}")
            print(f"Здоровье {enemy_name}: {enemy_health}")
            print(f"Зелья: {player.healing_potions}")

            print("\n1. Атаковать")
            print("2. Лечиться (+30 HP)")
            print("3. Сбежать (25% шанс)")

            choice = input("Выбор: ")

            if choice == "1":
                damage = random.randint(player.attack - 1, player.attack + 2)
                if damage < 1:
                    damage = 1
                enemy_health -= damage
                print(f"Вы нанесли {damage} урона")

                if enemy_health <= 0:
                    print(f"Вы победили {enemy_name}!")
                    return True

                enemy_damage = random.randint(enemy_attack - 1, enemy_attack + 3)
                if enemy_damage < 1:
                    enemy_damage = 1
                player.take_damage(enemy_damage)
                print(f"{enemy_name} нанес вам {enemy_damage} урона")

                if not player.is_alive():
                    print(f"{enemy_name} убил вас!")
                    return False

            elif choice == "2":
                if player.use_healing_potion():
                    print(f"Здоровье: {player.health}")

                    enemy_damage = random.randint(enemy_attack, enemy_attack + 2)
                    player.take_damage(enemy_damage)
                    print(f"{enemy_name} нанес вам {enemy_damage} урона")
                else:
                    print("Нет зелий")
                    enemy_damage = random.randint(enemy_attack + 1, enemy_attack + 4)
                    player.take_damage(enemy_damage)
                    print(f"{enemy_name} нанес вам {enemy_damage} урона")

            elif choice == "3":
                if random.random() < 0.25:
                    print("Убежали")
                    return False
                else:
                    print("Не удалось сбежать!")
                    enemy_damage = random.randint(enemy_attack + 2, enemy_attack + 5)
                    player.take_damage(enemy_damage)
                    print(f"{enemy_name} нанес вам {enemy_damage} урона")

            else:
                print("Неверный выбор - пропускаете ход")
                enemy_damage = random.randint(enemy_attack, enemy_attack + 3)
                player.take_damage(enemy_damage)
                print(f"{enemy_name} нанес вам {enemy_damage} урона")

            if not player.is_alive():
                return False

        return False

    def challenge_1(self, player):
        print("\nИспытание 1: Хижина в лесу")
        print("Вы находите старую заброшенную хижину.")
        print("Слышны странные звуки изнутри...")

        print("\n1. Войти внутрь")
        print("2. Обойти хижину")
        print("3. Подождать у входа")

        choice = input("Выбор: ")

        if choice == "1":
            print("\nВнутри на вас нападают гоблины!")
            if self.fight(player, "гоблинов", 40, 10):
                print("Победив гоблинов, вы находите сундук.")
                artifact = self.data_manager.get_artifact()
                player.add_artifact(artifact)
                player.level_up()

        elif choice == "2":
            print("\nОбходя хижину, вы находите тайник.")
            if random.random() < 0.5:
                player.healing_potions += 1
                print("Нашли зелье лечения")
            else:
                print("Тайник оказался пустым")

        elif choice == "3":
            print("\nВы ждете...")
            if random.random() < 0.3:
                print("Из хижины выходит торговец.")
                print("Он продает вам улучшенный меч.")
                player.attack += 3
                print(f"Атака увеличена до {player.attack}")
            else:
                print("Ничего не происходит. Вы теряете время.")
                if random.random() < 0.2:
                    print("На вас напали дикие звери!")
                    damage = random.randint(5, 15)
                    player.take_damage(damage)
                    print(f"Потеряли {damage} здоровья")

    def challenge_2(self, player):
        print("\nИспытание 2: Бурная река")
        print("Быстрая река преграждает путь.")
        print("Вода темная и холодная...")

        print("\n1. Попытаться переплыть")
        print("2. Построить плот из бревен")
        print("3. Искать брод")

        choice = input("Выбор: ")

        if choice == "1":
            print("\nВы прыгаете в холодную воду...")
            chance = random.random()

            if chance < 0.3:
                print("Сильное течение тянет вас на дно!")
                print("Вы не смогли выбраться...")
                player.health = 0
                return

            elif chance < 0.6:
                print("Вас сносит течением! Вы едва выбираетесь.")
                damage = random.randint(20, 35)
                player.take_damage(damage)
                print(f"Потеряли {damage} здоровья")

                if player.is_alive():
                    print("Но вы все же достигли другого берега!")
                    if random.random() < 0.5:
                        artifact = self.data_manager.get_artifact()
                        player.add_artifact(artifact)

            else:
                print("Вы успешно переплываете реку!")
                artifact = self.data_manager.get_artifact()
                player.add_artifact(artifact)

        elif choice == "2":
            print("\nВы пытаетесь построить плот...")
            if random.random() < 0.4:
                print("Плот разваливается! Вы падаете в воду.")
                damage = random.randint(10, 20)
                player.take_damage(damage)
                print(f"Потеряли {damage} здоровья")

                if player.is_alive():
                    print("Но вам удается выбраться на берег.")
                    player.level_up()
            else:
                print("Плот держится! Вы переправляетесь.")
                player.level_up()

        elif choice == "3":
            print("\nВы ищете брод...")
            if random.random() < 0.3:
                print("На вас нападают речные твари!")
                if self.fight(player, "речных тварей", 30, 8):
                    print("Победив их, вы находите брод.")
                    player.healing_potions += 1
                    print("Нашли зелье")
            else:
                print("Находите безопасный брод.")
                player.healing_potions += 2
                print("На пути нашли 2 зелья лечения")

    def challenge_3(self, player):
        print("\nИспытание 3: Древний храм")
        print("Древний каменный храм стоит перед вами.")
        print("Он охраняется магическими големами.")

        print("\n1. Атаковать стражей")
        print("2. Попробовать прокрасться")
        print("3. Найти потайной вход")

        choice = input("Выбор: ")

        if choice == "1":
            print("\nВы атакуете големов!")
            if self.fight(player, "каменных големов", 60, 14):
                print("Вы проникаете в храм.")
                artifact = self.data_manager.get_artifact()
                player.add_artifact(artifact)
                player.level_up()

        elif choice == "2":
            print("\nВы пытаетесь прокрасться...")
            if random.random() < 0.4:
                print("Успех! Вы незаметно проникаете в храм.")
                artifact = self.data_manager.get_artifact()
                player.add_artifact(artifact)
            else:
                print("Вас заметили! Приходится сражаться!")
                if self.fight(player, "стражей храма", 45, 11):
                    print("Вы пробиваетесь внутрь!")
                    if random.random() < 0.5:
                        player.heal(20)

        elif choice == "3":
            print("\nВы ищете потайной вход...")
            if random.random() < 0.6:
                print("Находите скрытую дверь.")
                print("Внутри находите полезные предметы.")
                player.heal(30)
                player.attack += 2
                print(f"Здоровье: {player.health}, Атака: {player.attack}")
            else:
                print("Не находите вход. Теряете время.")
                if random.random() < 0.4:
                    print("На вас нападают големы!")
                    if not self.fight(player, "големов", 40, 10):
                        return

    def challenge_4(self, player):
        print("\nИспытание 4: Пещера сокровищ")
        print("Темная пещера, полная золота и драгоценностей.")
        print("У входа спит огромный тролль...")

        print("\n1. Сразиться с троллем")
        print("2. Подождать до ночи")
        print("3. Отвлечь тролля")

        choice = input("Выбор: ")

        if choice == "1":
            print("\nВы нападаете на тролля!")
            if self.fight(player, "пещерного тролля", 75, 18):
                print("Вы побеждаете тролля!")
                artifact = self.data_manager.get_artifact()
                player.add_artifact(artifact)
                player.level_up()
                player.healing_potions += 1
                print("Также нашли зелье")

        elif choice == "2":
            print("\nВы ждете до ночи...")
            if random.random() < 0.7:
                print("Ночью тролль крепко спит.")
                print("Вы пробираетесь в пещеру.")
                artifact = self.data_manager.get_artifact()
                player.add_artifact(artifact)
                player.heal(40)
                print("Нашли артефакт и немного отдохнули")
            else:
                print("Тролль проснулся! Он вас заметил!")
                if not self.fight(player, "разбуженного тролля", 60, 16):
                    return

        elif choice == "3":
            print("\nВы пытаетесь отвлечь тролля...")
            if random.random() < 0.6:
                print("Тролль отвлекается! Вы забираете сокровища!")
                artifact = self.data_manager.get_artifact()
                player.add_artifact(artifact)
            else:
                print("Тролль не поддается на уловку! Он в ярости!")
                if self.fight(player, "разъяренного тролля", 65, 20):
                    print("Вы побеждаете, но это было тяжело!")
                    player.level_up()

    def final_battle(self, player):
        print("\nФИНАЛЬНЫЙ БОСС")
        print("ТЕНЕВОЙ ВОЛК")
        print("Огромное существо из тьмы перед вами.")
        print("Его глаза горят красным светом...")

        boss_health = 100 + (player.level * 5)
        boss_attack = 18 + (player.level * 1)

        print(f"\nЗдоровье волка: {boss_health}")
        print("Это будет самый трудный бой!")
        player.show_stats()

        input("\nНажмите Enter чтобы начать...")

        round_num = 1
        while boss_health > 0 and player.is_alive():
            print(f"\nРаунд {round_num}")
            print(f"Ваше здоровье: {player.health}")
            print(f"Здоровье волка: {boss_health}")
            print(f"Зелья: {player.healing_potions}")

            print("\n1. Атаковать")
            print("2. Лечиться (враг тоже атакует)")
            print("3. Мощный удар (нужен артефакт)")

            choice = input("Выбор: ")

            if choice == "1":
                damage = random.randint(player.attack - 2, player.attack + 3)
                boss_health -= damage
                print(f"Нанесли {damage} урона")

                if boss_health <= 0:
                    break

                boss_damage = random.randint(boss_attack - 2, boss_attack + 4)
                player.take_damage(boss_damage)
                print(f"Волк нанес {boss_damage} урона")

            elif choice == "2":
                if player.use_healing_potion():
                    print(f"Здоровье: {player.health}")
                    boss_damage = random.randint(boss_attack, boss_attack + 3)
                    player.take_damage(boss_damage)
                    print(f"Волк нанес {boss_damage} урона")
                else:
                    print("Нет зелий! Пропускаете ход.")
                    boss_damage = random.randint(boss_attack + 2, boss_attack + 6)
                    player.take_damage(boss_damage)
                    print(f"Волк нанес {boss_damage} урона")

            elif choice == "3":
                if len(player.artifacts) >= 1:
                    print("Используете силу артефактов!")
                    damage = player.attack * 2
                    boss_health -= damage
                    print(f"Критический удар! {damage} урона")

                    if boss_health > 0:
                        boss_damage = random.randint(boss_attack + 2, boss_attack + 8)
                        player.take_damage(boss_damage)
                        print(f"Волк нанес {boss_damage} урона")
                else:
                    print("Нужен хотя бы 1 артефакт!")
                    boss_damage = random.randint(boss_attack + 1, boss_attack + 5)
                    player.take_damage(boss_damage)
                    print(f"Волк нанес {boss_damage} урона")

            else:
                print("Неверный выбор!")
                boss_damage = random.randint(boss_attack, boss_attack + 4)
                player.take_damage(boss_damage)
                print(f"Волк нанес {boss_damage} урона")

            round_num += 1

        if boss_health <= 0:
            print("\nВы победили Теневого Волка!")
            print("Это была невероятно трудная битва!")
            player.boss_defeated = True
            player.level_up()
            player.level_up()

            player.artifacts.append("Корона Героя")
            player.attack += 15
            player.max_health += 50
            player.health = player.max_health

            print("\nТьма отступает. Вы спасли лес!")

        else:
            print("\nТеневой Волк победил вас...")
            print("Тьма поглощает лес...")

    def end_game(self, player):
        print("\nИгра пройдена!")
        print("Поздравляем с победой!")
        player.show_stats()
        input("\nНажмите Enter чтобы выйти")