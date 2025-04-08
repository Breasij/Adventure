# Eisen en Wensen

*De eisen en wensen zijn verwerkt in de user stories.*

De gebruiker wil een **text-based adventure RPG** met **replayability**. Er is geen voorkeur opgegeven voor programmeertaal of visuele stijl, wat volledige creatieve vrijheid geeft. De beschikbare tijd voor het project is **2 weken**.

## Eisen van de klant/gebruiker

---

### ✅ De gebruiker wil een personage kunnen creëren

- **Wie:** Bruno  
- **Prioriteit:** **HOOG**  
- **Tijd:** 1 dag (1/14)  
- **Realistisch:** Ja. Dit is haalbaar met een `Player` class/object. Zelfs zonder ervaring in Python moet dit lukken door kennis van OOP in andere talen.

---

### ✅ De gebruiker wil verschillende locaties bezoeken

- **Wie:** Bruno  
- **Prioriteit:** **HOOG**  
- **Tijd:** 1 dag (2/14)  
- **Realistisch:** Ja. Met lists of JSON-bestanden kan dit binnen een dag worden gerealiseerd.

---

### ✅ De gebruiker wil een werkend combat-systeem vergelijkbaar met Dungeons & Dragons

- **Wie:** Bruno  
- **Prioriteit:** **HOOG**  
- **Tijd:** 3 dagen (5/14)  
- **Realistisch:** Mogelijk, maar onzeker. Er is beperkte ervaring met het bouwen van combat-systemen. De logica achter het D&D-systeem vereist extra onderzoek.

---

### ✅ De gebruiker wil een online back-up en mogelijkheid tot het volgen van wijzigingen

- **Wie:** Bruno  
- **Prioriteit:** **HOOG**  
- **Tijd:** 2 uur (5/14)  
- **Realistisch:** Ja. Tools zoals **GitHub** maken dit eenvoudig en er zijn voldoende tutorials beschikbaar.

---

### ✅ De gebruiker wil classes kunnen kiezen of toegewezen krijgen

- **Wie:** Bruno  
- **Prioriteit:** **MIDDEL**  
- **Tijd:** 2 dagen (7-8/14)  
- **Realistisch:** Ja. Online uitleg is beschikbaar. Deze functionaliteit maakt het combatsysteem wel complexer.

---

# Ontwerp

### *De user stories zijn vertaald naar een passend, eenduidig en volledig ontwerp.*

De opdracht: een **text-based adventure RPG met replayability en een back-upmogelijkheid**. Hiervoor is gekozen voor de volgende tools en technologieën:

- **Taal:** Python  
- **Dataopslag:** JSON-bestanden  
- **AI-integratie:** LLM (Large Language Models)  
- **Versiebeheer:** GitHub  
- **IDE:** Visual Studio Code

---

## Waarom Python?

### Voordelen:
- Snel prototypen van mechanics  
- Uitstekende LLM/AI-integratie  
- Eenvoudige tekstverwerking  
- Grote community en veel tutorials  
- Flexibel en geschikt voor text-based games  

### Nadelen:
- Langzamer dan C++ of Java  
- Hogere geheugengebruik  
- Fouten worden pas zichtbaar tijdens het uitvoeren  

 **Opmerking:** 
 Deze nadelen zijn niet kritisch, omdat:
 - Het project relatief klein is  
 - Performance geen sleutelrol speelt  
 - De taal juist uitblinkt in tekstverwerking en AI-integratie  

---

## Waarom JSON?

### Voordelen:
- **Leesbaar en bewerkbaar:**  
  Makkelijk aan te passen, ook voor niet-programmeurs. Handig voor het handmatig toevoegen van NPC’s, vijanden, items en locaties.  
- **Lichtgewicht:**  
  Snelle laadtijden, ideaal voor kleinere games.  
- **Scheidt data van logica:**  
  Houdt je code schoon en overzichtelijk.  
- **Platformonafhankelijk:**  
  Ondersteund door vrijwel elke programmeertaal.  
- **Makkelijk te debuggen:**  
  Fouten zijn snel te vinden en op te lossen.

### Nadelen:
- **Geen validatie of typecontrole:**  
  Typfouten kunnen pas bij runtime fouten veroorzaken.  
  _Voorbeeld:_ `"Magic Scroll "` i.p.v. `"Magic Scroll"` faalt bij opzoeken.
- **Beperkt bij complexe structuren:**  
  Relaties tussen NPC’s of quests moeten handmatig worden afgehandeld.  
- **Minder geschikt voor grotere projecten:**  
  Bij uitbreiding kan onderhoud lastiger worden.

---

