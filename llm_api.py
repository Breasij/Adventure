import requests
import json

OLLAMA_URL = 'http://localhost:11434/api/generate'
MODEL = 'mistral' 

def query_llm(prompt):
    data = {
        "model": MODEL,
        "prompt": prompt,
        "stream": False  # Set to False for cleaner response handling
    }
    
    response = requests.post(OLLAMA_URL, json=data)
    
    if response.status_code == 200:
        try:
            result = response.json()
            return result.get('response', '').strip()
        except json.JSONDecodeError:
            return "[Error decoding response]"
    else:
        return f"[LLM Error {response.status_code}]"
