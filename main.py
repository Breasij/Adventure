import json, random
from player import Player
from enemy import Enemy
from combat import combat_sequence
from quest import generate_quest
from llm_api import query_llm
from npc import npc_greeting, npc_conversation, merchant_interaction
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

# Initial player location
current_location_name = "Marketplace"
current_region = REGIONS["Kingdom of Lorum"]
current_location = current_region["locations"][current_location_name]

# Generate random enemy encounter based on location
def generate_enemy_encounter(location):
    enemy_names = location.get("enemies", [])
    if enemy_names and random.random() < 0.5:
        enemy_data = ENEMIES.get(random.choice(enemy_names))
        if enemy_data:
            return Enemy(**enemy_data)
    return None

# Manage inventory clearly with equip/use options
def manage_inventory(player):
    while True:
        if not player.inventory:
            print("\nYour inventory is empty.")
            break

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
                    player.equip_weapon(item_data)
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

    # NPC interactions
    npcs_here = [npc for npc in NPCS.values() if npc["location"] == current_location_name]
    for npc in npcs_here:
        greeting = npc_greeting(npc, player.name)
        print(f"\n🧙 {npc['name']} says: '{greeting}'")

        conversation_history = [f"{npc['name']}: {greeting}"]

        if "shop" in npc:
            merchant_interaction(player, npc)

        # Further conversation option
        while True:
            interact_choice = input(f"Do you want to speak further with {npc['name']}? (y/n): ").lower()
            if interact_choice == 'y':
                player_input = input(f"What do you say to {npc['name']}?: ")
                reply, conversation_history = npc_conversation(npc, player_input, player.name, conversation_history)
                print(f"\n🧙 {npc['name']} replies: '{reply}'")
            elif interact_choice == 'n':
                print(f"You end your conversation with {npc['name']}.")
                break
            else:
                print("Please choose 'y' or 'n'.")

    # Enemy encounters
    enemy = generate_enemy_encounter(current_location)
    if enemy:
        combat_sequence(player, enemy)


# Main gameplay loop
def game_loop():
    global player
    player_name = input("Enter your adventurer's name: ")
    player = Player(player_name)
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
