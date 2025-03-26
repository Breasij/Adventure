import json

with open("items.json", "r") as f:
    ITEMS = json.load(f)

def get_item(category, item_name):
    return ITEMS.get(category, {}).get(item_name)
