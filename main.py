import random
from player import Player
from enemy import Enemy
from combat import combat_sequence
from quest import generate_quest
from npc_system import NPCSystem
from utils import GAME_DATA

class GameManager:
    def __init__(self):
        self.current_location_name = "Marketplace"
        self.current_region = GAME_DATA.regions["Kingdom of Lorum"]
        self.current_location = self.current_region["locations"][self.current_location_name]
        self.npc_system = NPCSystem()
        self.player = None

    def generate_enemy_encounter(self, location):
        enemy_names = location.get("enemies", [])
        if enemy_names and random.random() < 0.5:
            enemy_data = GAME_DATA.enemies.get(random.choice(enemy_names))
            if enemy_data:
                enemy_data = dict(enemy_data)  
                enemy_data.pop("drops", None)
                return Enemy(**enemy_data)
        return None

    def manage_inventory(self):
        while True:
            if not self.player.inventory:
                print("\nYour inventory is empty.")
                break

            if self.player.equipment["weapon"]:
                print(f"\nEquipped Weapon: {self.player.equipment['weapon']['name']}")
            else:
                print("\nEquipped Weapon: None")

            print("\nYour Inventory:")
            for idx, (item, details) in enumerate(self.player.inventory.items(), 1):
                print(f"{idx}. {item}: {details['description']}")

            choice = input("Enter the item number to equip/use or [B]ack: ").lower()
            if choice == 'b':
                break

            if choice.isdigit():
                idx = int(choice) - 1
                if 0 <= idx < len(self.player.inventory):
                    item_name = list(self.player.inventory.keys())[idx]
                    item_data = self.player.inventory[item_name]
                    if "damage_dice" in item_data:
                        self.player.equip_item(item_name)
                    elif "healing" in item_data:
                        self.player.use_potion(item_name)
                    else:
                        print("You can't use this item right now.")
                else:
                    print("Invalid selection.")
            else:
                print("Invalid input.")

    def move_player(self, direction):
        exits = self.current_location.get("exits", {})
        if direction not in exits:
            print("You can't go that way!")
            return

        new_location_name = exits[direction]
        for region in GAME_DATA.regions.values():
            if new_location_name in region["locations"]:
                self.current_region = region
                self.current_location_name = new_location_name
                self.current_location = region["locations"][new_location_name]
                break

        print(f"\nYou arrive at {self.current_location_name}. {self.current_location['description']}")

        # Handle NPCs in location
        npcs_here = [npc for npc in GAME_DATA.npcs.values() 
                     if npc["location"] == self.current_location_name]

        for npc in npcs_here:
            npc["mood"] = float(npc.get("mood", 0))
            greeting = self.npc_system.npc_greeting(npc, self.player.name)
            print(f"\n🤙 {greeting}")

            if npc.get("role", "").lower() == "merchant":
                self.handle_merchant(npc)

        # Handle potential combat
        enemy = self.generate_enemy_encounter(self.current_location)
        if enemy:
            combat_sequence(self.player, enemy)

    def handle_merchant(self, npc):
        conversation_history = []
        while True:
            action = input("Merchant: [B]uy, [S]ell, [T]alk, [L]eave? ").lower()
            
            if action == 'b':
                print(self.npc_system.merchant_interaction(npc, self.player))
                item = input("Item to buy ('back' to cancel): ")
                if item.lower() != 'back':
                    print(self.npc_system.merchant_interaction(npc, self.player, 'buy', item))

            elif action == 's':
                if not self.player.inventory:
                    print("You have no items to sell.")
                    continue

                print("\nYour Inventory:")
                for idx, (item_name, details) in enumerate(self.player.inventory.items(), 1):
                    print(f"{idx}. {item_name} - {details['description']}")

                item_input = input("Item to sell ('back' to cancel): ")
                if item_input.lower() == 'back':
                    continue

                matched_item = next((key for key in self.player.inventory.keys() 
                                   if key.lower() == item_input.lower()), None)

                if not matched_item:
                    print("You don't have that item.")
                    continue

                qty_input = input(f"Quantity of {matched_item}: ")
                if not qty_input.isdigit() or int(qty_input) <= 0:
                    print("Invalid quantity.")
                    continue

                qty = int(qty_input)
                print(self.npc_system.handle_exchange(npc, self.player, matched_item, qty))

            elif action == 't':
                msg = input("Speak to merchant: ")
                reply, conversation_history = self.npc_system.npc_conversation(
                    npc, msg, self.player.name)
                print(f"\n🤙 {npc['name']}: {reply}")

            elif action == 'l':
                break
            else:
                print("Invalid option.")

    def start_game(self):
        # Initialize player
        player_name = input("Enter your adventurer's name: ")
        self.player = Player(player_name)

        # Give starting equipment
        starter_weapon = "Rusty Sword"
        if starter_weapon in GAME_DATA.items["weapons"]:
            self.player.inventory[starter_weapon] = GAME_DATA.items["weapons"][starter_weapon]
            self.player.equip_item(starter_weapon)
            print(f"\nYou begin your journey equipped with a {starter_weapon}.")

        # Show quest introduction
        print(f"\n--- Quest Introduction ---\n{generate_quest(self.player.name)}\n--------------------------")

        # Main game loop
        while self.player.hp > 0:
            print(f"\nYou're at {self.current_location_name}. "
                  f"Exits: {', '.join(self.current_location.get('exits', {}))}")
            
            choice = input("Move direction (north, east...), [I]nventory or [Q]uit: ").lower()
            
            if choice in self.current_location.get("exits", {}):
                self.move_player(choice)
            elif choice == 'i':
                self.manage_inventory()
            elif choice == 'q':
                print("Farewell, adventurer!")
                break
            else:
                print("Invalid choice.")

        if self.player.hp <= 0:
            print("You have fallen in your adventures. Game Over.")

def main():
    game = GameManager()
    game.start_game()

if __name__ == "__main__":
    main()