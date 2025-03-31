import json, random
from player import Player
from enemy import Enemy
from combat import combat_sequence
from quest import generate_quest
from llm_api import query_llm
from npc_system import npc_greeting, npc_conversation, merchant_interaction, handle_exchange
from items import get_item

# Load data from JSON files
with open("enemies.json", "r") as f:
    ENEMIES = json.load(f)["enemies"]

with open("locations.json", "r") as f:
    REGIONS = json.load(f)["regions"]

with open("npc.json", "r") as f:
    NPCS = json.load(f)

with open("items.json", "r") as f:
    ITEMS = json.load(f)

current_location_name = "Marketplace"
current_region = REGIONS["Kingdom of Lorum"]
current_location = current_region["locations"][current_location_name]

def generate_enemy_encounter(location):
    enemy_names = location.get("enemies", [])
    if enemy_names and random.random() < 0.5:
        enemy_data = ENEMIES.get(random.choice(enemy_names))
        if enemy_data:
            enemy_data = dict(enemy_data)  # make a copy to avoid mutating global
            enemy_data.pop("drops", None)
            return Enemy(**enemy_data)
    return None

def manage_inventory(player):
    while True:
        if not player.inventory:
            print("\nYour inventory is empty.")
            break

        if player.equipment["weapon"]:
            print(f"\nEquipped Weapon: {player.equipment['weapon']['name']}")
        else:
            print("\nEquipped Weapon: None")

        print("\nYour Inventory:")
        for idx, (item, details) in enumerate(player.inventory.items(), 1):
            print(f"{idx}. {item}: {details['description']}")

        choice = input("Enter the item number to equip/use or [B]ack: ").lower()
        if choice == 'b':
            break

        if choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(player.inventory):
                item_name = list(player.inventory.keys())[idx]
                item_data = player.inventory[item_name]
                if "damage_dice" in item_data:
                    player.equip_item(item_name)
                elif "healing" in item_data:
                    player.use_potion(item_name)
                else:
                    print("You can't use this item right now.")
            else:
                print("Invalid selection.")
        else:
            print("Invalid input.")

def move_player(direction):
    global current_location, current_location_name, current_region
    exits = current_location.get("exits", {})
    if direction not in exits:
        print("You can't go that way!")
        return

    new_location_name = exits[direction]
    for region in REGIONS.values():
        if new_location_name in region["locations"]:
            current_region = region
            current_location_name = new_location_name
            current_location = region["locations"][new_location_name]
            break

    print(f"\nYou arrive at {current_location_name}. {current_location['description']}")

    npcs_here = [npc for npc in NPCS.values() if npc["location"] == current_location_name]

    for npc in npcs_here:
        npc["mood"] = float(npc.get("mood", 0))
        greeting = npc_greeting(npc, player.name)
        print(f"\n🤙 {greeting}")

        conversation_history = [greeting]

        if npc.get("role", "").lower() == "merchant":
            while True:
                action = input("Merchant: [B]uy, [S]ell, [T]alk, [L]eave? ").lower()
                if action == 'b':
                    print(merchant_interaction(npc, player))
                    item = input("Item to buy ('back' to cancel): ")
                    if item.lower() == 'back':
                        continue
                    print(merchant_interaction(npc, player, 'buy', item))

                elif action == 's':
                    if not player.inventory:
                        print("You have no items to sell.")
                        continue

                    print("\nYour Inventory:")
                    for idx, (item_name, details) in enumerate(player.inventory.items(), 1):
                        print(f"{idx}. {item_name} - {details['description']}")

                    item_input = input("Item to sell ('back' to cancel): ")
                    if item_input.lower() == 'back':
                        continue

                    # Normalize item input (case-insensitive match)
                    matched_item = None
                    for key in player.inventory:
                        if key.lower() == item_input.lower():
                            matched_item = key
                            break

                    if not matched_item:
                        print("You don't have that item.")
                        continue

                    qty_input = input(f"Quantity of {matched_item}: ")
                    if not qty_input.isdigit() or int(qty_input) <= 0:
                        print("Invalid quantity.")
                        continue

                    qty = int(qty_input)
                    print(handle_exchange(npc, player, matched_item, qty))

                elif action == 't':
                    msg = input("Speak to merchant: ")
                    reply, conversation_history = npc_conversation(npc, msg, player.name, conversation_history)
                    print(f"\n🤙 {npc['name']}: {reply}")

                elif action == 'l':
                    break
                else:
                    print("Invalid option.")

    enemy = generate_enemy_encounter(current_location)
    if enemy:
        combat_sequence(player, enemy)

def game_loop():
    global player
    player_name = input("Enter your adventurer's name: ")
    player = Player(player_name)

    starter_weapon = "Rusty Sword"
    if starter_weapon in ITEMS["weapons"]:
        player.inventory[starter_weapon] = ITEMS["weapons"][starter_weapon]
        player.equip_item(starter_weapon)
        print(f"\nYou begin your journey equipped with a {starter_weapon}.")

    print(f"\n--- Quest Introduction ---\n{generate_quest(player.name)}\n--------------------------")

    while player.hp > 0:
        print(f"\nYou're at {current_location_name}. Exits: {', '.join(current_location.get('exits', {}))}")
        choice = input("Move direction (north, east...), [I]nventory or [Q]uit: ").lower()
        if choice in current_location.get("exits", {}):
            move_player(choice)
        elif choice == 'i':
            manage_inventory(player)
        elif choice == 'q':
            print("Farewell, adventurer!")
            break
        else:
            print("Invalid choice.")

    if player.hp <= 0:
        print("You have fallen in your adventures. Game Over.")

if __name__ == "__main__":
    game_loop()
