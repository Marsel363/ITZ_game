import random


class Player:
    def __init__(self, username, health=100, attack=10):
        self.username = username
        self.health = health
        self.max_health = health
        self.attack = attack
        self.level = 1
        self.artifacts = []
        self.boss_defeated = False
        self.current_trial = 0
        self.healing_potions = 2

    def take_damage(self, damage):
        self.health -= damage
        if self.health < 0:
            self.health = 0

    def heal(self, amount):
        self.health += amount
        if self.health > self.max_health:
            self.health = self.max_health

    def use_healing_potion(self):
        if self.healing_potions > 0:
            self.heal(30)
            self.healing_potions -= 1
            return True
        return False

    def add_artifact(self, artifact):
        self.artifacts.append(artifact)
        self.attack += 3
        self.max_health += 15
        self.health = self.max_health
        print(f"Получен артефакт: {artifact}")

    def level_up(self):
        self.level += 1
        self.attack += 2
        self.max_health += 10
        self.health = self.max_health
        print(f"Уровень повышен до {self.level}")

    def show_stats(self):
        print(f"\nИгрок: {self.username}")
        print(f"Уровень: {self.level}")
        print(f"Здоровье: {self.health}/{self.max_health}")
        print(f"Атака: {self.attack}")
        print(f"Зелья: {self.healing_potions}")  # ИСПРАВЛЕНО: было player.healing_potions
        print(f"Артефакты: {len(self.artifacts)}")

    def is_alive(self):
        return self.health > 0

    def save_data(self):
        return {
            'username': self.username,
            'health': self.health,
            'max_health': self.max_health,
            'attack': self.attack,
            'level': self.level,
            'artifacts': self.artifacts,
            'boss_defeated': self.boss_defeated,
            'current_trial': self.current_trial,
            'healing_potions': self.healing_potions
        }


class Boss:
    def __init__(self, name, health, attack):
        self.name = name
        self.health = health
        self.max_health = health
        self.attack = attack

    def take_damage(self, damage):
        self.health -= damage

    def is_alive(self):
        return self.health > 0