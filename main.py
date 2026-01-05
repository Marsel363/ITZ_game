from classes import Player
from data_manager import DataManager
from adventure import Adventure


def main():
    data_manager = DataManager()
    adventure = Adventure(data_manager)

    while True:
        print("\nГлавное меню:")
        print("1. Регистрация")
        print("2. Вход")
        print("3. Выход")

        choice = input("Выберите: ")

        if choice == "1":
            register_player(data_manager)
        elif choice == "2":
            player = login_player(data_manager)
            if player:
                adventure.start_game(player)
        elif choice == "3":
            break
        else:
            print("Неверный выбор")


def register_player(data_manager):
    print("\nРегистрация")
    username = input("Логин: ")
    password = input("Пароль: ")

    if data_manager.register_user(username, password):
        print("Регистрация успешна")
    else:
        print("Логин занят")


def login_player(data_manager):
    print("\nВход в игру")
    username = input("Логин: ")
    password = input("Пароль: ")

    player_data = data_manager.login_user(username, password)

    if player_data:
        player = Player(username, player_data['health'], player_data['attack'])
        player.artifacts = player_data['artifacts']
        player.level = player_data['level']
        player.boss_defeated = player_data['boss_defeated']
        player.current_trial = player_data['current_trial']

        if 'healing_potions' in player_data:
            player.healing_potions = player_data['healing_potions']
        else:
            player.healing_potions = 2

        print(f"Добро пожаловать, {username}")
        return player
    else:
        print("Неверный логин или пароль")
        return None


if __name__ == "__main__":
    main()