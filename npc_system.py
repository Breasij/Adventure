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
        f"An NPC currently feels {get_tone_from_mood(current_mood)} toward the player.\n"
        f"The player just said: \"{player_input}\"\n"
        "How should the NPC feel now? Respond with one of: enthusiastic, friendly, neutral, irritated, hostile."
    )
    response = query_llm(prompt).strip().lower()
    tones = {
        "enthusiastic": 7,
        "friendly": 3,
        "neutral": 0,
        "irritated": -3,
        "hostile": -7
    }
    return tones.get(response, current_mood)

def npc_greeting(npc, player_name):
    name = npc.get('name', 'NPC')
    personality = npc.get('personality', '')
    mood_value = npc.get('mood', 0)
    tone = get_tone_from_mood(mood_value)
    npc['tone'] = tone

    if 'merchant' in npc.get('role', '').lower():
        if tone in ['friendly', 'enthusiastic']:
            return f"{name}: Hello! Welcome, traveler. Please, take a look at my wares."
        elif tone == 'neutral':
            return f"{name}: Hello. Looking for something specific?"
        elif tone in ['irritated', 'hostile']:
            return f"{name}: What do you want? Buy something or move along."
        else:
            return f"{name}: Hello."
    else:
        if tone in ['friendly', 'enthusiastic']:
            return f"{name}: Hello there! {personality.capitalize()}" if personality else f"{name}: Hello there! It's good to see you."
        elif tone == 'neutral':
            return f"{name}: Hello."
        elif tone == 'irritated':
            return f"{name}: Yes? What is it?"
        elif tone == 'hostile':
            return f"{name}: What do you want?"
        else:
            return f"{name}: Hello."

def npc_conversation(npc, player_input, player_name, history=None):
    name = npc.get('name', 'NPC')
    personality = npc.get('personality', '').lower()
    role = npc.get('role', 'npc').lower()
    mood = npc.get('mood', 0)

    mood = infer_mood_change_from_input(player_input, mood)
    npc['mood'] = max(-10, min(10, mood))
    npc['tone'] = get_tone_from_mood(npc['mood'])

    if history is None:
        history = []

    history.append(f"Player: {player_input.strip()}")

    tone = npc['tone']
    tone_style_map = {
        "enthusiastic": "You speak with passion, often smiling or laughing. You get excited easily.",
        "friendly": "You're warm and casual. You use relaxed and open language.",
        "neutral": "You respond plainly and without much emotion.",
        "irritated": "You're annoyed or impatient. You're sarcastic, snappy, and clearly frustrated.",
        "hostile": "You're angry, aggressive, or threatening. You might raise your voice or insult back."
    }
    emotional_state = tone_style_map.get(tone, "You respond naturally.")

    quirks = {
        'grumpy': "You're naturally short-tempered and roll your eyes often.",
        'friendly': "You're warm and enjoy connecting with people.",
        'jovial': "You joke and laugh even in tense moments.",
        'serious': "You're to-the-point and don't waste time.",
        'sarcastic': "You respond with biting wit or mockery.",
        'aloof': "You're emotionally distant and hard to engage."
    }
    quirk = quirks.get(personality, "")

    persona = (
        f"You are {name}, a {personality} {role} in a fantasy world.\n"
        f"Current mood: {tone}. {emotional_state} {quirk}\n"
        f"You're in a real-time conversation with an adventurer named {player_name}.\n"
        f"Reply in character. Never repeat yourself. Never restate what the player said.\n"
        f"React like a real person in this world, using your mood and personality.\n"
        f"If you're angry, lash out. If you're flattered, soften. Stay grounded."
    )

    conversation_context = "\n".join(history[-6:])
    prompt = f"{persona}\n\n{conversation_context}\n{name}:"

    response = query_llm(prompt)
    npc_reply = response.strip().split("\n")[0] if response else "..."
    history.append(f"{name}: {npc_reply}")

    return npc_reply, history

def merchant_interaction(npc, player, action='list', item_name=None):
    if 'inventory' not in npc or not isinstance(npc['inventory'], dict):
        return "This NPC has no items for sale."

    name = npc.get('name', 'Merchant')
    inventory = npc['inventory']
    action = action.lower()

    if action == 'list':
        if not inventory:
            return "No items available."
        items_str = []
        for item, data in inventory.items():
            price = data['price'] if isinstance(data, dict) else data
            items_str.append(f"{item} - {price} gold")
        return "; ".join(items_str)

    elif action == 'buy':
        if player is None:
            return "No player specified for purchase."
        if not item_name or item_name not in inventory:
            polite = (npc.get('tone') not in ['hostile', 'irritated'])
            return f"I don't have that item, {'sir' if polite else 'buddy'}."

        item_data = inventory[item_name]
        price = item_data['price'] if isinstance(item_data, dict) else item_data
        stock = item_data.get('stock', None) if isinstance(item_data, dict) else None
        player_gold = player.get('gold', 0)

        if player_gold < price:
            return "You don't have enough gold for that."
        if stock is not None and stock <= 0:
            return "Sorry, I'm out of stock for that item."

        player['gold'] = player_gold - price
        player_inventory = player.get('inventory', {})
        player_inventory[item_name] = player_inventory.get(item_name, 0) + 1
        player['inventory'] = player_inventory
        if stock is not None:
            inventory[item_name]['stock'] -= 1
        npc['mood'] = npc.get('mood', 0) + 1
        npc['tone'] = get_tone_from_mood(npc['mood'])
        return f"Thank you for your purchase of {item_name}!"

    elif action == 'sell':
        return "I don't buy items, sorry."

    else:
        return "I can't help with that."
