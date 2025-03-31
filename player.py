import random

class Player:
    def __init__(self, name):
        self.name = name
        self.hp = 100
        self.base_attack_power = 3
        self.attack_power = self.base_attack_power
        self.gold = 0
        self.inventory = {}  # {'item_name': item_data}

        # Equipment slots
        self.equipment = {
            "weapon": None,
            "armor": None,
            "accessory": None
        }

    def equip_item(self, item_name):
        item = self.inventory.get(item_name)
        if not item:
            print("You don't have that item.")
            return

        # Default to weapon if no slot assigned
        slot = item.get("slot", "weapon")
        if slot not in self.equipment:
            print(f"You can't equip {item_name}.")
            return

        # Equip new item
        previously_equipped = self.equipment[slot]
        self.equipment[slot] = item
        print(f"You equipped {item_name}.")

        # Update stats
        self.update_stats()

        # Optionally handle previous item
        if previously_equipped:
            print(f"You unequipped {previously_equipped['name']}.")

    def unequip_item(self, slot):
        if slot not in self.equipment:
            print(f"No such slot '{slot}'.")
            return

        item = self.equipment[slot]
        if item:
            print(f"You unequipped {item['name']}.")
            self.equipment[slot] = None
            self.update_stats()
        else:
            print("Nothing equipped in that slot.")

    def update_stats(self):
        self.attack_power = self.base_attack_power
        # Add weapon damage bonus
        weapon = self.equipment.get("weapon")
        if weapon:
            self.attack_power += weapon.get("damage_bonus", 0)

        # Future: armor or accessory effects
        armor = self.equipment.get("armor")
        if armor:
            # Armor stat handling goes here
            pass

    def attack(self):
        weapon = self.equipment.get("weapon")
        if weapon:
            damage_dice = weapon["damage_dice"]
            damage_bonus = weapon.get("damage_bonus", 0)
            damage = random.randint(1, damage_dice[1]) + damage_bonus
        else:
            damage = random.randint(1, 4)  # Unarmed damage
        return damage

    def use_potion(self, potion_name):
        potion = self.inventory.get(potion_name)
        if potion and 'healing' in potion:
            heal_amount = potion['healing']
            self.hp += heal_amount
            del self.inventory[potion_name]
            print(f"You healed for {heal_amount} HP! Current HP: {self.hp}")
        else:
            print("You can't use that.")
