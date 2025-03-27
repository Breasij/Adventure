import random

class Player:
    def __init__(self, name):
        self.name = name
        self.hp = 100
        self.inventory = {}
        self.weapon = None
        self.gold = 100

    def attack(self):
        if self.weapon:
            damage = random.randint(*self.weapon["damage_dice"]) + self.weapon["damage_bonus"]
            return damage
        return random.randint(1, 4)  # Default unarmed damage

    def equip_weapon(self, weapon):
        self.weapon = weapon
        print(f"You have equipped {weapon['name']}.")

    def add_item(self, item_name, item_data):
        self.inventory[item_name] = item_data
        print(f"{item_name} added to your inventory.")

    def use_potion(self, potion_name):
        potion = self.inventory.get(potion_name)
        if potion and "healing" in potion:
            self.hp += potion["healing"]
            print(f"You used {potion_name} and restored {potion['healing']} HP!")
            del self.inventory[potion_name]
        else:
            print("You don't have that potion.")
