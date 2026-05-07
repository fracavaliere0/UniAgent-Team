"""Definizione degli agenti CrewAI del progetto."""

from dotenv import load_dotenv
from crewai import Agent, LLM

from src.tools import PDFSearchTool

# Carica le variabili d'ambiente dal file .env prima di inizializzare l'LLM.
load_dotenv()

# Istanza LLM nativa di CrewAI che punta direttamente a Groq
llm_groq = LLM(
    model="groq/llama-3.3-70b-versatile"
)

# Istanza LLM più piccola e veloce per compiti di formattazione
llm_groq_small = LLM(
    model="groq/llama-3.1-8b-instant"
)


def get_librarian() -> Agent:
    """
    Crea l'agente responsabile della ricerca nei documenti PDF.

    Returns:
        Agent CrewAI configurato con il tool di lettura PDF.
    """
    return Agent(
        role="Esperto Ricercatore di PDF",
        goal="Trovare le informazioni più rilevanti all'interno dei documenti di studio",
        backstory=(
            "Specialista nell'analisi di materiale accademico: individua con precisione "
            "i passaggi utili per rispondere a domande di studio."
        ),
        llm=llm_groq,
        tools=[PDFSearchTool()],
    )


def get_professor() -> Agent:
    """
    Crea l'agente docente che sintetizza e spiega i contenuti.

    Returns:
        Agent CrewAI senza tool, basato solo sui dati forniti dal Librarian.
    """
    return Agent(
        role="Professore Universitario Senior",
        goal=(
            "Spiegare concetti complessi in modo chiaro e accademico "
            "basandosi unicamente sui dati forniti dal Librarian"
        ),
        backstory=(
            "Docente con approccio rigoroso e didattico, trasforma informazioni "
            "tecniche in spiegazioni comprensibili mantenendo accuratezza accademica."
        ),
        llm=llm_groq,
    )


def get_examiner() -> Agent:
    """
    Crea l'agente esaminatore che interroga lo studente in stile socratico.

    Returns:
        Agent CrewAI senza tool, dedicato a interrogazione e valutazione.
    """
    return Agent(
        role="Esaminatore Socratico",
        goal=(
            "Interrogare lo studente in modo mirato e valutare le sue risposte "
            "con severità ma in modo didattico, assegnando un voto da 1 a 10"
        ),
        backstory=(
            "Esaminatore universitario di lunga esperienza, applica il metodo socratico: "
            "pone domande progressive per smascherare lacune, fornisce feedback rigoroso "
            "ma costruttivo e conclude sempre con una valutazione numerica da 1 a 10."
        ),
        llm=llm_groq,
    )


def get_mapper() -> Agent:
    """
    Crea l'agente che converte appunti testuali in diagrammi Mermaid.js.

    Returns:
        Agent CrewAI senza tool, specializzato nella visualizzazione gerarchica.
    """
    return Agent(
        role="Architetto dell'Informazione",
        goal="Trasformare concetti testuali in diagrammi di flusso visivi",
        backstory=(
            "Sei un esperto di visualizzazione dati. Conosci perfettamente la sintassi "
            "di Mermaid.js. Il tuo unico scopo è prendere appunti e convertirli in un "
            "diagramma gerarchico chiaro e conciso."
        ),
        llm=llm_groq_small,
    )