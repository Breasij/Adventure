from llm_api import query_llm

def generate_quest(player_name):
    prompt = (
        f"You are a Dungeon Master narrating the start of a fantasy quest. "
        f"Briefly describe an exciting quest introduction for the adventurer {player_name}."
    )
    response = query_llm(prompt)
    return response if response else "You find yourself in a small village, rumors of danger and adventure abound!"
