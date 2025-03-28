import random
from llm_api import query_llm
from items import get_item, ITEMS  # ← Add ITEMS import here!

def npc_greeting(npc, player_name):
    dialogue = random.choice(npc["dialogue"])
    personality = npc.get("personality", "friendly")
    role = npc.get("role", "local")
    location = npc.get("location", "area")

    prompt = (
        f"{npc['name']} is a {personality} {role} in the {location}. "
        f"The adventurer {player_name} walks in. {npc['name']} greets {player_name} warmly, possibly mentioning: '{dialogue}'.\n\n"
        f"{npc['name']} says:"
    )
    response = query_llm(prompt)
    return response.strip() if response else dialogue

def npc_conversation(npc, player_input, player_name):
    personality = npc.get("personality", "friendly")
    role = npc.get("role", "local")
    location = npc.get("location", "area")

    prompt = (
        f"{npc['name']} is a {personality} {role} in the {location}. "
        f"The adventurer {player_name} says: '{player_input}'.\n\n"
        f"{npc['name']} replies:"
    )
    response = query_llm(prompt)
    return response.strip() if response else "Hmm, can't say I know about that."




def merchant_interaction(player, merchant):
    shop = merchant.get("shop", {})
    items = shop.get("items", [])
    prices = shop.get("prices", {})

    print("\nMerchant's goods:")
    for idx, item in enumerate(items, start=1):
        price = prices.get(item, 'unknown')
        print(f"{idx}. {item} - {price} gold")

    choice = input("Select an item number to buy or [N] to exit: ").lower()
    if choice.isdigit():
        choice_idx = int(choice) - 1
        if 0 <= choice_idx < len(items):
            selected_item = items[choice_idx]
            price = prices[selected_item]
            if player.gold >= price:
                category = ("weapons" if selected_item in ITEMS["weapons"] else
                            "potions" if selected_item in ITEMS["potions"] else
                            "misc")
                item_data = get_item(category, selected_item)
                player.add_item(selected_item, item_data)
                player.gold -= price
                print(f"You bought {selected_item} for {price} gold. Gold left: {player.gold}")
            else:
                print("Not enough gold!")
        else:
            print("Invalid selection.")
    else:
        print("Maybe next time!")
 