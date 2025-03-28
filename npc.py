import random
from llm_api import query_llm
from items import get_item, ITEMS  # ← Add ITEMS import here!

def npc_greeting(npc, player_name):
    dialogue = random.choice(npc["dialogue"])
    personality = npc.get("personality", "friendly")
    role = npc.get("role", "local")
    location = npc.get("location", "area")
    voice = npc.get("voice", "natural and in-character")

    prompt = (
        f"You are {npc['name']}, a {personality} {role} in the {location}. "
        f"Speak in a {voice} voice. "
        f"The adventurer {player_name} just entered. "
        f"Greet them naturally and warmly. You might say something like: \"{dialogue}\". "
        "Respond directly as if you were there. Do not introduce yourself. Do not mention being a character or NPC."
    )

    response = query_llm(prompt)
    return response.strip() if response else dialogue


def npc_conversation(npc, player_input, player_name, history=None):
    personality = npc.get("personality", "friendly")
    role = npc.get("role", "local")
    location = npc.get("location", "area")
    voice = npc.get("voice", "natural")

    if history is None:
        history = []

    # Add the latest player input to the history
    history.append(f"{player_name}: {player_input}")

    # Build conversation prompt
    prompt = (
        f"You are {npc['name']}, a {personality} {role} in the {location}. "
        f"Speak in a {voice} voice. Respond as if you are speaking directly to {player_name}. "
        f"Never mention being an NPC, AI, or simulation.\n\n"
        f"Here is the conversation so far:\n"
    )
    prompt += "\n".join(history)
    prompt += f"\n{npc['name']} replies:"

    response = query_llm(prompt)
    if response:
        history.append(f"{npc['name']}: {response.strip()}")
    else:
        history.append(f"{npc['name']}: I'm not sure what to say to that.")

    return response.strip() if response else "I'm not sure what to say to that.", history






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
 