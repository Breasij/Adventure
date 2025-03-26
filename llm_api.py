import requests
import json

OLLAMA_URL = 'http://localhost:11434/api/generate'
MODEL = 'orca-mini'

def query_llm(prompt):
    data = {"model": MODEL, "prompt": prompt, "stream": True}
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
                continue

    return complete_response.strip()