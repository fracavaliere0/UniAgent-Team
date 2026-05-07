# 🎓 UniAgent - Multi-Agent AI Study Assistant

UniAgent è un'applicazione web avanzata basata su un'architettura **Multi-Agente** e tecniche di **RAG (Retrieval-Augmented Generation)**. Progettata per rivoluzionare lo studio autonomo, analizza documenti accademici (PDF) per offrire tre percorsi di apprendimento interattivi e personalizzati.

## ✨ Funzionalità Principali (Le 3 Modalità di Studio)

Il sistema orchestra una "crew" di Agenti AI specializzati (Librarian, Professor, Examiner, Mapper) che collaborano per offrirti:

1. **📚 Spiegazione Accademica:** Il *Librarian* estrae i concetti dal PDF e li passa al *Professor*, che genera una lezione discorsiva, chiara e strutturata in Markdown.
2. **🧠 Mentore Socratico (Active Recall):** Un vero e proprio simulatore d'esame in due fasi. L'*Examiner* ti pone una domanda aperta sfidante sul materiale. Una volta inserita la tua risposta, la confronta con i testi reali, assegnandoti un voto da 1 a 10 e fornendo un feedback costruttivo.
3. **🗺️ Mappe Concettuali Dinamiche:** Il *Mapper* sintetizza argomenti complessi e genera codice Mermaid.js, che l'applicazione renderizza nativamente a schermo creando diagrammi di flusso interattivi, orizzontali e ad alta leggibilità.

## 🛠️ Stack Tecnologico

* **Orchestrazione Agenti:** [CrewAI](https://crewai.com/)
* **LLM Engine:** Modelli Llama 3.3 (70B) e Llama 3.1 (8B) tramite l'API ultraveloce di [Groq](https://groq.com/), interfacciati tramite **LiteLLM**.
* **RAG & Document Loading:** LangChain (`PyPDFLoader`).
* **Interfaccia Utente (UI/UX):** [Streamlit](https://streamlit.io/) (con Custom CSS per un look premium e gestione del `session_state` per le interazioni multi-step).
* **Data Visualization:** Integrazione JS HTML per rendering nativo di diagrammi **Mermaid**.
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

4. **Prepara i materiali:**
Inserisci i file PDF che vuoi studiare nella cartella data/raw_pdfs/.

5. **Avvia l'applicazione:**
```bash
streamlit run app.py
```

## 📂 Struttura del Progetto

app.py: Core dell'applicazione Streamlit, gestione UI, custom CSS e rendering grafico.

src/agents.py: Definizione e configurazione degli agenti AI (Ruoli, Obiettivi, Backstory).

src/tasks.py: Logica di suddivisione dei task (Spiegazione, Valutazione Socratica, Generazione Mappe).

src/tools.py: Tool personalizzati per la lettura e l'estrazione locale del testo dai PDF.
