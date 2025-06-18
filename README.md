# Text Adventure Game - Educatief Project

Een interactieve tekstavontuur game ontwikkeld als educatief project om te experimenteren met Large Language Models (LLMs) en moderne software-ontwikkeling. Dit project demonstreert de integratie van AI in game development en dient als leermiddel voor het werken met LLMs.

## Educatieve Doelen

- Demonstratie van LLM-integratie in game development
- Praktijkvoorbeeld van AI-gestuurde NPC interacties
- Leermiddel voor het werken met moderne AI-tools
- Voorbeeld van software-ontwikkeling met Python en web-technologieën

## LLM Integratie

Dit project maakt gebruik van Ollama met het Mistral model voor:
- Dynamische NPC dialogen
- Context-aware gesprekken
- Realistische karakter-interacties
- Adaptieve verhaallijnen

## Installatie

### Vereisten
- Python 3.8 of hoger
- pip (Python package manager)
- Een moderne webbrowser
- Ollama (voor LLM-integratie)

### Stap 1: Clone de Repository
```bash
git clone [repository-url]
cd [project-directory]
```

### Stap 2: Maak een Virtuele Omgeving
```bash
# Voor Windows
python -m venv venv
venv\Scripts\activate

# Voor macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Stap 3: Installeer Dependencies
```bash
pip install -r requirements.txt
```

### Stap 4: Installeer Ollama
1. Download Ollama van [ollama.ai](https://ollama.ai)
2. Installeer en start Ollama
3. Download het Mistral model:
```bash
ollama pull mistral
```

## 🎮 Het Spel Starten

### Web Versie (Aanbevolen)
1. Start de server:
```bash
python app.py
```
2. Open je webbrowser en ga naar: `http://localhost:5000`
3. Voer je naam in en begin je avontuur!

### Command-line Versie
```bash
python main.py
```

## 🎯 Leerdoelen

- **LLM Integratie**: Begrip van hoe LLMs kunnen worden geïntegreerd in applicaties
- **AI Interactie**: Leren werken met AI-gestuurde dialogen
- **Software Development**: Praktijkervaring met moderne ontwikkeltools
- **Game Design**: Inzicht in het ontwerpen van interactieve ervaringen

## 🗺️ Beschikbare Locaties

- **Marketplace**: Het centrale handelscentrum
- **Arena**: Voor gevechten en uitdagingen
- **Tavern**: Voor informatie en rust
- **Castle Lorum**: Ontmoet de koning

## 🎮 Besturing

### Web Interface
- Gebruik de knoppen op het scherm voor beweging
- Klik op NPCs om met ze te praten
- Gebruik de inventory interface voor items
- Combat interface verschijnt automatisch tijdens gevechten

### Command-line Interface
- Typ commando's zoals 'north', 'south', 'east', 'west' om te bewegen
- Gebruik 'i' voor inventory
- Typ 'q' om te stoppen

## 🛠️ Technische Details

- **Backend**: Python met Flask
- **Frontend**: HTML, CSS, JavaScript
- **AI**: Ollama met Mistral model voor NPC interacties
- **Data Storage**: JSON bestanden voor game data

## 📚 Leermaterialen

- [Ollama Documentatie](https://ollama.ai/docs)
- [Flask Documentatie](https://flask.palletsprojects.com/)
- [Python Documentatie](https://docs.python.org/)

## ⚠️ Bekende Issues

- Zorg ervoor dat Ollama draait voordat je het spel start
- Vernieuw de pagina als je een "Failed to move" error krijgt
- Gebruik de knoppen in plaats van toetsenbord input in de web versie

