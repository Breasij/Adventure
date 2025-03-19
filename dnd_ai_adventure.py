
import requests
import random
import json
import re

OLLAMA_URL = 'http://localhost:11434/api/generate'
MODEL = 'orca-mini'

class Player:
    def __init__(self, name):
        self.name = name
        self.hp = 100
        self.attack_power = 15
        self.inventory = []

    def attack(self):
        return random.randint(5, self.attack_power)

class Enemy:
    def __init__(self, name, hp, attack_power):
        self.name = name
        self.hp = hp
        self.attack_power = attack_power

    def attack(self):
        return random.randint(5, self.attack_power)

def query_llm(prompt):
    data = {
        "model": MODEL,
        "prompt": prompt,
        "stream": True  
    }
    response = requests.post(OLLAMA_URL, json=data, stream=True)

    complete_response = ""
    for line in response.iter_lines():
        if line:
            json_line = line.decode('utf-8')
            try:
                json_data = json.loads(json_line)
                complete_response += json_data.get('response', '')
                if json_data.get('done', False):
                    break
            except json.JSONDecodeError:
                continue  #

    return complete_response.strip()


def generate_quest(player_name):
    prompt = (
        f"You are a Dungeon Master narrating the start of a fantasy quest. "
        f"Briefly describe an exciting quest introduction for the adventurer {player_name}."
    )
    response = query_llm(prompt)
    if not response:
        response = "You find yourself in a small village, rumors of danger and adventure abound!"
    return response


def generate_enemy_encounter():
    prompt = (
        "You are a Dungeon Master generating a SINGLE enemy for a D&D encounter.\n"
        "Respond exactly in this format:\n"
        "Name: [Enemy Name]; HP: [number]; Attack: [number]\n"
        "Example:\n"
        "Name: Giant Spider; HP: 20; Attack: 5\n"
        "DO NOT provide any narrative, explanations, or other text."
    )

    response = query_llm(prompt)
    print(f"LLM raw response: '{response}'")  # debugging clearly

    # Now explicitly parse this strict format:
    match = re.search(r"Name:\s*(.+?);\s*HP:\s*(\d+);\s*Attack:\s*(\d+)", response)

    if match:
        name, hp, attack_power = match.groups()
        return Enemy(name.strip(), int(hp), int(attack_power))
    else:
        print("Parsing failed, default Goblin used.")
        return Enemy("Goblin", 30, 10)


def combat_sequence(player, enemy):
    print(f"A wild {enemy.name} appears! ({enemy.hp} HP)")
    while player.hp > 0 and enemy.hp > 0:
        action = input("Do you [A]ttack or [R]un? ").lower()
        if action == 'a':
            damage = player.attack()
            enemy.hp -= damage
            print(f"You dealt {damage} damage to the {enemy.name}! (Enemy HP: {enemy.hp})")
        elif action == 'r':
            if random.random() > 0.5:
                print("You successfully escaped!")
                return
            else:
                print("Escape failed!")

        if enemy.hp > 0:
            enemy_damage = enemy.attack()
            player.hp -= enemy_damage
            print(f"The {enemy.name} attacks you for {enemy_damage} damage! (Your HP: {player.hp})")

    if player.hp <= 0:
        print("You were defeated...")
    else:
        print(f"You defeated the {enemy.name}!")

def game_loop():
    name = input("Enter your adventurer's name: ")
    player = Player(name)

    quest = generate_quest(name)
    print("\n--- Quest Introduction ---")
    print(quest)
    print("--------------------------\n")

    playing = True
    while playing and player.hp > 0:
        print("\nWhat will you do next?")
        choice = input("[E]xplore or [Q]uit: ").lower()

        if choice == 'e':
            enemy = generate_enemy_encounter()
            combat_sequence(player, enemy)
        elif choice == 'q':
            print("Your adventure ends here. Farewell!")
            playing = False
        else:
            print("Invalid choice.")

    if player.hp <= 0:
        print("Game Over!")

if __name__ == "__main__":
    game_loop()
