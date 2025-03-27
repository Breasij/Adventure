import random
import json

class Enemy:
    def __init__(self, name, hp, ac, attack_bonus, damage_dice, damage_bonus, description, resistances, weaknesses):
        self.name = name
        self.hp = hp
        self.ac = ac
        self.attack_bonus = attack_bonus
        self.damage_dice = damage_dice
        self.damage_bonus = damage_bonus
        self.description = description
        self.resistances = resistances
        self.weaknesses = weaknesses

    def attack(self):
        damage = random.randint(self.damage_dice[0], self.damage_dice[1]) + self.damage_bonus
        return damage

    def __str__(self):
        return f"{self.name} ({self.description}) - HP: {self.hp}, AC: {self.ac}, Attack Bonus: {self.attack_bonus}, Resistances: {', '.join(self.resistances)}, Weaknesses: {', '.join(self.weaknesses)}"

# Singleton class to hold the enemy data
class EnemyData:
    _data = None
    
    @classmethod
    def load_data(cls):
        if cls._data is None:
            try:
                with open('enemies.json', 'r') as file:
                    cls._data = json.load(file)['enemies']
            except FileNotFoundError:
                print("Error: enemies.json not found!")
                cls._data = {}
        return cls._data

    @classmethod
    def get_random_enemy(cls):
        """Randomly select an enemy from the loaded data."""
        enemy_data = cls.load_data()
        if not enemy_data:
            print("No enemy data available.")
            return None

        # Randomly select an enemy
        enemy_name = random.choice(list(enemy_data.keys()))
        enemy_info = enemy_data[enemy_name]

        # Create an Enemy instance with the selected data
        enemy = Enemy(
            name=enemy_info["name"],
            hp=enemy_info["hp"],
            ac=enemy_info["ac"],
            attack_bonus=enemy_info["attack_bonus"],
            damage_dice=enemy_info["damage_dice"],
            damage_bonus=enemy_info["damage_bonus"],
            description=enemy_info["description"],
            resistances=enemy_info["resistances"],
            weaknesses=enemy_info["weaknesses"]
        )
        return enemy
