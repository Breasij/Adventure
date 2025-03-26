import random
from llm_api import query_llm
from items import get_item, ITEMS  # ← Add ITEMS import here!

def npc_greeting(npc, player_name):
    dialogue = random.choice(npc["dialogue"])
    personality = npc.get("personality", "friendly")
    prompt = (
        f"You are {npc['name']}, a character in the {npc['location']} of a medieval fantasy world. "
        f"You have a '{personality}' personality. The adventurer '{player_name}' has just entered. "
        f"Greet them warmly, naturally, and immersively, possibly mentioning: '{dialogue}'. "
        "NEVER mention being an NPC or AI."
    )
    response = query_llm(prompt)
    return response.strip() if response else dialogue


def npc_conversation(npc, player_input, player_name):
    personality = npc.get("personality", "friendly")
    prompt = (
        f"You are {npc['name']}, a character living in the medieval fantasy world, currently in {npc['location']}. "
        f"You have a '{personality}' personality. "
        f"The adventurer '{player_name}' just said to you: '{player_input}'. "
        f"Respond ONLY as {npc['name']} would in this situation, naturally and in-character. "
        "NEVER break character or mention being an NPC, AI, or chatbot under any circumstances."
    )
    response = query_llm(prompt)
    return response.strip() if response else "Hmm, I don't know much about that."


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
 