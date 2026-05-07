"""Definizione dei task CrewAI per il flusso di studio."""

from crewai import Task

from src.agents import get_librarian, get_professor


def create_study_tasks(domanda_studente: str, nome_file_pdf: str) -> list[Task]:
    """
    Crea i task necessari per ricerca e spiegazione didattica.

    Args:
        domanda_studente: Quesito posto dallo studente.
        nome_file_pdf: Nome del PDF presente in data/raw_pdfs/.

    Returns:
        Lista ordinata dei task da eseguire nel workflow CrewAI.
    """
    librarian = get_librarian()
    professor = get_professor()

    # Primo task: ricerca delle informazioni nel PDF tramite tool dedicato.
    task_ricerca: Task = Task(
        description=(
            f"Usa il tuo tool per leggere il file PDF '{nome_file_pdf}' e cerca tutte "
            f"le informazioni utili per rispondere alla seguente domanda dello studente: "
            f"'{domanda_studente}'."
        ),
        expected_output=(
            "Un riassunto in formato testo con i passaggi chiave estratti dal documento"
        ),
        agent=librarian,
    )

    # Secondo task: trasformazione degli appunti in una spiegazione completa.
    task_spiegazione: Task = Task(
        description=(
            f"Prendi gli appunti forniti dal Librarian e crea una lezione per lo "
            f"studente basata sulla seguente domanda: '{domanda_studente}'."
        ),
        expected_output=(
            "Una spiegazione discorsiva, formattata in Markdown, "
            "chiara e con tono accademico"
        ),
        agent=professor,
    )

    return [task_ricerca, task_spiegazione]
