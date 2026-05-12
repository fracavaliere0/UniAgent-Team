# 🎓 UniAgent - Multi-Agent AI Study Assistant

UniAgent è un'applicazione web avanzata basata su un'architettura **Multi-Agente** e tecniche di **RAG (Retrieval-Augmented Generation)**. Progettata per rivoluzionare lo studio autonomo, analizza documenti accademici in locale per offrire tre percorsi di apprendimento interattivi e personalizzati.

## ✨ Funzionalità Principali (Le 3 Modalità di Studio)

Il sistema orchestra una "crew" di Agenti AI specializzati (Librarian, Professor, Examiner, Mapper) che collaborano per offrirti:

1. **📚 Spiegazione Accademica:** Il *Librarian* estrae i concetti dal PDF e li passa al *Professor*, che genera una lezione discorsiva, chiara e strutturata. 
   * **Esportazione:** Possibilità di scaricare la lezione istantaneamente in formato **PDF** con formattazione nativa (grassetti, liste puntate) pronta per la stampa o la lettura offline.

2. **🧠 Mentore Socratico (Active Recall):** Un vero e proprio simulatore d'esame in due fasi. L'*Examiner* ti pone una domanda aperta sfidante sul materiale. Una volta inserita la tua risposta, la confronta con i testi reali, assegnandoti un voto da 1 a 10 e fornendo un feedback costruttivo.

3. **🗺️ Mappe Concettuali Dinamiche:** Il *Mapper* sintetizza argomenti complessi e genera codice Mermaid.js, che l'applicazione renderizza nativamente a schermo creando diagrammi di flusso interattivi, orizzontali e ad alta leggibilità.
   * **Esportazione:** Possibilità di scaricare il diagramma con un clic come immagine **PNG** ad alta risoluzione.

### ⚡ User Experience Premium
* **Drag & Drop:** Carica i tuoi PDF direttamente dall'interfaccia web senza dover gestire manualmente le cartelle del progetto.
* **State Management:** I risultati generati non vengono persi cambiando modalità, grazie alla persistenza avanzata della sessione in Streamlit.

## 🛠️ Stack Tecnologico

* **Orchestrazione Agenti:** [CrewAI](https://crewai.com/)
* **LLM Engine:** Modelli Llama 3.3 (70B) per i ragionamenti e Llama 3.1 (8B) per le sintesi veloci, tramite l'API ultraveloce di [Groq](https://groq.com/) e **LiteLLM**.
* **RAG & Document Loading:** LangChain (`PyPDFLoader`).
* **Interfaccia Utente (UI/UX):** [Streamlit](https://streamlit.io/) (con Custom CSS per un look premium e gestione del `session_state`).
* **Data Visualization & Export:** Rendering nativo di diagrammi **Mermaid**, `fpdf2` e `markdown` per la generazione documentale, API `mermaid.ink` (`requests`) per il download immagini.
* **Linguaggio:** Python 3.12

## ⚙️ Installazione e Utilizzo

1. **Clona il repository:**
   ```bash
   git clone [https://github.com/fracavaliere0/UniAgent-Team.git](https://github.com/fracavaliere0/UniAgent-Team.git)
   cd UniAgent-Team

2. **Crea un ambiente virtuale e installa le dipendenze:**
```bash
python -m venv venv
# Attiva il venv:
# Su Windows: venv\Scripts\activate
# Su Mac/Linux: source venv/bin/activate
pip install -r requirements.txt
```
3. **Configura le chiavi API:**
Crea un file .env nella root del progetto e inserisci la tua chiave API di Groq:
```bash
GROQ_API_KEY=la_tua_chiave_api_qui
```

4. **Avvia l'applicazione:**
```bash
streamlit run app.py
```

5. **Inizia a studiare:**
Trascina direttamente il tuo file PDF nella barra laterale dell'applicazione web e seleziona la modalità di studio che preferisci.

## 📂 Struttura del Progetto

app.py: Core dell'applicazione Streamlit, gestione UI, custom CSS e rendering grafico.

src/agents.py: Definizione e configurazione degli agenti AI (Ruoli, Obiettivi, Backstory).

src/tasks.py: Logica di suddivisione dei task (Spiegazione, Valutazione Socratica, Generazione Mappe).

src/tools.py: Tool personalizzati per la lettura e l'estrazione locale del testo dai PDF.
