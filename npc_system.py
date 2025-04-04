import random
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass
from llm_api import query_llm
from utils import GAME_DATA

@dataclass
class NPCState:
    """Track NPC state"""
    mood: float = 0
    tone: str = "neutral"
    conversation_history: List[str] = None
    
    def __post_init__(self):
        if self.conversation_history is None:
            self.conversation_history = []

class NPCSystem:
    def __init__(self):
        self.npc_states: Dict[str, NPCState] = {}
        self.personality_modifiers = {
            'friendly': 0.1,
            'greedy': -0.1,
            'generous': 0.15,
            'shrewd': -0.15,
            'neutral': 0
        }

    def get_npc_state(self, npc_name: str) -> NPCState:
        """Get or create NPC state"""
        if npc_name not in self.npc_states:
            self.npc_states[npc_name] = NPCState()
        return self.npc_states[npc_name]

    def get_tone_from_mood(self, mood: float) -> str:
        """Convert mood value to tone"""
        if isinstance(mood, (int, float)):
            if mood > 5:
                return "enthusiastic"
            elif mood > 1:
                return "friendly"
            elif mood < -5:
                return "hostile"
            elif mood < -1:
                return "irritated"
            return "neutral"
        elif isinstance(mood, str):
            return mood.lower()
        return "neutral"

    def infer_mood_change(self, player_input: str, current_mood: float) -> float:
        """Determine mood change based on player input"""
        prompt = (
            f"NPC feels {self.get_tone_from_mood(current_mood)}.\n"
            f"Player said: '{player_input}'\n"
            "NPC mood now? enthusiastic, friendly, neutral, irritated, hostile."
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

    def calculate_haggle_modifier(self, npc: Dict, player_charisma: int = 10) -> float:
        """Calculate haggling price modifier"""
        mood_modifier = (npc.get('mood', 0) + player_charisma - 10) / 35
        personality = npc.get('personality', 'neutral').lower()
        personality_mod = self.personality_modifiers.get(personality, 0)
        return personality_mod + mood_modifier

    def handle_exchange(self, npc: Dict, player: Any, item_name: str, 
                       quantity: int, haggle: bool = False) -> str:
        """Handle selling items to NPC"""
        state = self.get_npc_state(npc['name'])
        
        # Validate item
        item_name_key = item_name.strip().lower()
        matching_items = [key for key in player.inventory if key.lower() == item_name_key]
        if not matching_items:
            return f"You don't have any {item_name} to sell."

        item_key = matching_items[0]
        owned_qty = (player.inventory.get(item_key, {}).get("quantity", 1) 
                    if isinstance(player.inventory[item_key], dict) else 1)

        if quantity > owned_qty:
            return f"You don't have enough {item_key}."

        # Calculate price
        item_data = player.inventory[item_key]
        price_per_item = (npc.get('exchange_rate', {}).get(item_key) or 
                         round(item_data.get("value", 1) * 0.4))

        # Handle haggling
        if haggle:
            if state.mood < -5 or (npc.get('personality', '').lower() == 'shrewd' 
                                 and random.random() < 0.3):
                return f"{npc['name']} refuses to haggle. 'My price is firm!'"
            
            haggle_modifier = self.calculate_haggle_modifier(npc)
            price_per_item = round(price_per_item * (1 + haggle_modifier))
            state.mood -= 1

        # Complete transaction
        total = price_per_item * quantity
        self._remove_items_from_inventory(player, item_key, quantity)
        player.gold += total

        if haggle:
            reaction = self._get_haggle_reaction(npc, quantity, item_key, "sell")
            return f"{npc['name']} buys {quantity} {item_key}(s) for {total} gold. {reaction}"

        return f"{npc['name']} buys {quantity} {item_key}(s) for {total} gold."

    def merchant_interaction(self, npc: Dict, player: Any, action: str = 'list', 
                           item_name: Optional[str] = None, haggle: bool = False) -> str:
        """Handle merchant interactions"""
        state = self.get_npc_state(npc['name'])
        inventory = npc.get('inventory', {})

        if action == 'list':
            return "; ".join([f"{item} - {details['price']} gold" 
                            for item, details in inventory.items()])

        if action == 'buy':
            return self._handle_buying(npc, player, inventory, item_name, haggle, state)

        return "Invalid action."

    def npc_greeting(self, npc: Dict, player_name: str) -> str:
        """Generate NPC greeting"""
        state = self.get_npc_state(npc['name'])
        state.tone = self.get_tone_from_mood(state.mood)
        
        greeting_prompt = (
            f"You're {npc['name']} ({npc['role']}). Mood: {state.tone}. "
            f"Greet adventurer {player_name} briefly."
        )
        return f"{npc['name']}: {query_llm(greeting_prompt)}"

    def npc_conversation(self, npc: Dict, player_input: str, 
                        player_name: str) -> Tuple[str, List[str]]:
        """Handle NPC conversation"""
        state = self.get_npc_state(npc['name'])
        
        # Update mood and tone
        state.mood = self.infer_mood_change(player_input, state.mood)
        state.tone = self.get_tone_from_mood(state.mood)

        # Add to history
        state.conversation_history.append(f"Player: {player_input.strip()}")

        # Generate response
        persona = self._create_persona(npc, player_name, state)
        conversation_context = "\n".join(state.conversation_history[-6:])
        prompt = f"{persona}\n{conversation_context}\n{npc['name']}:"
        
        npc_reply = query_llm(prompt).split("\n")[0].strip()
        state.conversation_history.append(f"{npc['name']}: {npc_reply}")

        return npc_reply, state.conversation_history

    def _remove_items_from_inventory(self, player: Any, item_key: str, quantity: int) -> None:
        """Remove items from player inventory"""
        if quantity == 1 or "quantity" not in player.inventory[item_key]:
            del player.inventory[item_key]
        else:
            player.inventory[item_key]["quantity"] -= quantity
            if player.inventory[item_key]["quantity"] <= 0:
                del player.inventory[item_key]

    def _get_haggle_reaction(self, npc: Dict, quantity: int, 
                           item_name: str, action: str) -> str:
        """Get NPC reaction to haggling"""
        state = self.get_npc_state(npc['name'])
        reaction_prompt = (
            f"{npc['name']} is a {npc.get('personality', 'neutral')} merchant. "
            f"Player haggled to {action} {quantity} {item_name}. "
            f"Mood: {state.mood}. Respond in character, briefly."
        )
        return query_llm(reaction_prompt).split("\n")[0].strip()

    def _create_persona(self, npc: Dict, player_name: str, state: NPCState) -> str:
        """Create NPC persona for conversation"""
        persona = (
            f"{npc['name']} is a {npc.get('personality', '')} {npc['role']} "
            f"with mood {state.tone}."
        )
        if 'inventory' in npc:
            persona += f"\nInventory: {npc.get('inventory', {})}"
        if 'exchange_rate' in npc:
            persona += f"\nExchange rates: {npc.get('exchange_rate', {})}"
        persona += f"\nIn conversation with {player_name}. Respond in character."
        return persona

    def _handle_buying(self, npc: Dict, player: Any, inventory: Dict, 
                      item_name: str, haggle: bool, state: NPCState) -> str:
        """Handle buying items from merchant"""
        matched_item = next((item for item in inventory 
                           if item.lower() == item_name.lower()), None)
        
        if not matched_item:
            return f"{npc['name']} doesn't have that item."

        item_data = inventory[matched_item]
        price = item_data['price']

        if haggle:
            if state.mood < -5 or (npc.get('personality', '').lower() == 'shrewd' 
                                 and random.random() < 0.3):
                return f"{npc['name']} refuses to haggle. 'My price is firm!'"
            
            haggle_modifier = self.calculate_haggle_modifier(npc)
            price = round(price * (1 - haggle_modifier))
            state.mood -= 1

        if item_data.get('stock', 1) <= 0:
            return f"{npc['name']} is out of {matched_item}."
        if player.gold < price:
            return "You don't have enough gold."

        # Complete transaction
        player.gold -= price
        player.inventory[matched_item] = player.inventory.get(matched_item, item_data.copy())
        if 'quantity' in player.inventory[matched_item]:
            player.inventory[matched_item]['quantity'] += 1
        inventory[matched_item]['stock'] -= 1
        state.mood += 1

        if haggle:
            reaction = self._get_haggle_reaction(npc, 1, matched_item, "buy")
            return f"Purchased {matched_item} for {price} gold. {reaction}"

        return f"Purchased {matched_item} for {price} gold."

# Create global instance
npc_system = NPCSystem()

# For backwards compatibility
def get_tone_from_mood(mood):
    return npc_system.get_tone_from_mood(mood)

def infer_mood_change_from_input(player_input, current_mood):
    return npc_system.infer_mood_change(player_input, current_mood)

def handle_exchange(npc, player, item_name, quantity, haggle=False):
    return npc_system.handle_exchange(npc, player, item_name, quantity, haggle)

def merchant_interaction(npc, player, action='list', item_name=None, haggle=False):
    return npc_system.merchant_interaction(npc, player, action, item_name, haggle)

def npc_greeting(npc, player_name):
    return npc_system.npc_greeting(npc, player_name)

def npc_conversation(npc, player_input, player_name, history=None):
    return npc_system.npc_conversation(npc, player_input, player_name)