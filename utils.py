import os
import json
from typing import Dict, Any, Optional

class GameData:
    """Central class to manage all game data"""
    def __init__(self):
        self.data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
        self.items = self._load_json("items.json")
        self.enemies = self._load_json("enemies.json").get("enemies", {})
        self.regions = self._load_json("locations.json").get("regions", {})
        self.npcs = self._load_json("npc.json")

    def _load_json(self, filename: str) -> Dict:
        """Load a JSON file from data directory"""
        try:
            with open(os.path.join(self.data_dir, filename), 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Error: {filename} not found in data directory!")
            return {}
        except json.JSONDecodeError:
            print(f"Error: {filename} contains invalid JSON!")
            return {}

    def get_item(self, category: str, item_name: str) -> Optional[Dict]:
        """Get item data from category"""
        return self.items.get(category, {}).get(item_name)

    def get_enemy(self, enemy_name: str) -> Optional[Dict]:
        """Get enemy data"""
        return self.enemies.get(enemy_name)

    def get_location(self, region: str, location: str) -> Optional[Dict]:
        """Get location data"""
        return self.regions.get(region, {}).get('locations', {}).get(location)

    def get_npc(self, npc_name: str) -> Optional[Dict]:
        """Get NPC data"""
        return self.npcs.get(npc_name)

# Create a global instance
GAME_DATA = GameData()