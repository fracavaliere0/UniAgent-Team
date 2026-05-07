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