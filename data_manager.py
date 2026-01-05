import json
import os


class DataManager:
    def __init__(self):
        self.users_file = "users.txt"
        self.items_file = "items.txt"
        self.init_files()

    def init_files(self):
        if not os.path.exists(self.users_file):
            with open(self.users_file, 'w') as f:
                json.dump({}, f)

        if not os.path.exists(self.items_file):
            items = ["Меч Луны", "Щит Солнца", "Кольцо Ветров",
                     "Амулет Земли", "Плащ Теней", "Посох Магов"]
            with open(self.items_file, 'w') as f:
                json.dump(items, f)

    def register_user(self, username, password):
        try:
            with open(self.users_file, 'r') as f:
                users = json.load(f)
        except:
            users = {}

        if username in users:
            return False

        users[username] = password

        with open(self.users_file, 'w') as f:
            json.dump(users, f)

        self.create_player_file(username)
        return True

    def create_player_file(self, username):
        player_file = f"save_{username}.txt"
        player_data = {
            'username': username,
            'health': 100,
            'max_health': 100,
            'attack': 10,
            'level': 1,
            'artifacts': [],
            'boss_defeated': False,
            'current_trial': 0,
            'healing_potions': 2
        }

        with open(player_file, 'w') as f:
            json.dump(player_data, f)

    def login_user(self, username, password):
        try:
            with open(self.users_file, 'r') as f:
                users = json.load(f)
        except:
            return None

        if username not in users:
            return None

        if users[username] != password:
            return None

        player_file = f"save_{username}.txt"
        if not os.path.exists(player_file):
            return None

        try:
            with open(player_file, 'r') as f:
                player_data = json.load(f)

                if 'healing_potions' not in player_data:
                    player_data['healing_potions'] = 2
                    self.save_player_data(player_data)

                return player_data
        except:
            return None

    def save_player_data(self, player_data):
        player_file = f"save_{player_data['username']}.txt"
        with open(player_file, 'w') as f:
            json.dump(player_data, f)

    def get_artifact(self):
        try:
            with open(self.items_file, 'r') as f:
                items = json.load(f)
        except:
            items = ["Меч Луны", "Щит Солнца", "Кольцо Ветров",
                     "Амулет Земли", "Плащ Теней", "Посох Магов"]

        if not items:
            items = ["Меч Луны", "Щит Солнца", "Кольцо Ветров",
                     "Амулет Земли", "Плащ Теней", "Посох Магов"]

        item = items.pop(0)

        with open(self.items_file, 'w') as f:
            json.dump(items, f)

        return item

    def return_artifacts(self, artifacts):
        if not artifacts:
            return

        try:
            with open(self.items_file, 'r') as f:
                current = json.load(f)
        except:
            current = []

        current.extend(artifacts)

        with open(self.items_file, 'w') as f:
            json.dump(current, f)