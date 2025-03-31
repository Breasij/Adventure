import random
from llm_api import query_llm
from items import get_item, ITEMS

def get_tone_from_mood(mood):
    if isinstance(mood, (int, float)):
        if mood > 5:
            return "enthusiastic"
        elif mood > 1:
            return "friendly"
        elif mood < -5:
            return "hostile"
        elif mood < -1:
            return "irritated"
        else:
            return "neutral"
    elif isinstance(mood, str):
        return mood.lower()
    else:
        return "neutral"

def infer_mood_change_from_input(player_input, current_mood):
    prompt = (
        f"NPC feels {get_tone_from_mood(current_mood)}.\n"
        f"Player said: '{player_input}'\n"
        "NPC mood now? enthusiastic, friendly, neutral, irritated, hostile."
    )
    response = query_llm(prompt).strip().lower()
    tones = {"enthusiastic": 7, "friendly": 3, "neutral": 0, "irritated": -3, "hostile": -7}
    return tones.get(response, current_mood)

def handle_exchange(npc, player, item_name, quantity):
    exchange_rate = npc.get('exchange_rate', {})
    if item_name in exchange_rate:
        player_qty = player.inventory.get(item_name, 0)
        if player_qty >= quantity:
            total_gold = exchange_rate[item_name] * quantity
            player.inventory[item_name] -= quantity
            if player.inventory[item_name] <= 0:
                del player.inventory[item_name]
            player.gold += total_gold
            npc['mood'] += 1
            return f"{npc['name']} buys {quantity} {item_name} for {total_gold} gold."
        else:
            return f"You don't have enough {item_name}."
    else:
        return f"{npc['name']} doesn't buy {item_name}."

def merchant_interaction(npc, player, action='list', item_name=None):
    inventory = npc.get('inventory', {})
    
    if action == 'list':
        return "; ".join([f"{item} - {details['price']} gold" for item, details in inventory.items()])

    elif action == 'buy':
        matched_item = next((item for item in inventory if item.lower() == item_name.lower()), None)
        if not matched_item:
            return f"{npc['name']} doesn't have that item."
        
        item_data = inventory[matched_item]
        price = item_data['price']
        stock = item_data.get('stock', 1)
        
        if stock <= 0:
            return f"{npc['name']} is out of {matched_item}."
        if player.gold < price:
            return "You don't have enough gold."
        
        player.gold -= price
        player.inventory[matched_item] = player.inventory.get(matched_item, 0) + 1
        inventory[matched_item]['stock'] -= 1
        npc['mood'] += 1
        
        return f"Purchased {matched_item} for {price} gold."

def npc_greeting(npc, player_name):
    tone = get_tone_from_mood(npc.get('mood', 0))
    npc['tone'] = tone
    greeting_prompt = (
        f"You're {npc['name']} ({npc['role']}). Mood: {tone}. Greet adventurer {player_name} briefly."
    )
    return f"{npc['name']}: {query_llm(greeting_prompt)}"

def npc_conversation(npc, player_input, player_name, history=None):
    npc['mood'] = infer_mood_change_from_input(player_input, npc.get('mood', 0))
    npc['tone'] = get_tone_from_mood(npc['mood'])

    if history is None:
        history = []
    history.append(f"Player: {player_input.strip()}")

    persona = (
        f"{npc['name']} is a {npc.get('personality', '')} {npc['role']} with mood {npc['tone']}.\n"
        f"Inventory: {npc.get('inventory', {})}\n"
        f"Exchange rates: {npc.get('exchange_rate', {})}\n"
        f"In conversation with {player_name}. Respond in character."
    )
    conversation_context = "\n".join(history[-6:])
    prompt = f"{persona}\n{conversation_context}\n{npc['name']}:"
    npc_reply = query_llm(prompt).split("\n")[0].strip()
    history.append(f"{npc['name']}: {npc_reply}")

    return npc_reply, history
