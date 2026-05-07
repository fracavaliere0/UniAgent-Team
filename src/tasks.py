"""Definizione dei task CrewAI per i flussi di interrogazione e valutazione."""

from crewai import Task

from src.agents import get_examiner, get_librarian


def create_question_tasks(argomento: str, nome_file_pdf: str) -> list[Task]:
    """
    Crea i task per generare una domanda d'esame a partire da un PDF.

    Flusso:
        1. Il Librarian estrae dal PDF i concetti chiave sull'argomento.
        2. L'Examiner usa quei concetti per formulare UNA sola domanda
           aperta e sfidante per lo studente.

    Args:
        argomento: Argomento di studio scelto dallo studente.
        nome_file_pdf: Nome del PDF presente in data/raw_pdfs/.

    Returns:
        Lista ordinata dei task da eseguire nel workflow CrewAI.
    """
    librarian = get_librarian()
    examiner = get_examiner()

    # 1) Ricerca dei concetti chiave nel PDF sull'argomento indicato.
    task_estrazione_concetti: Task = Task(
        description=(
            f"Usa il tuo tool per leggere il file PDF '{nome_file_pdf}' e individua "
            f"i concetti fondamentali relativi all'argomento: '{argomento}'. "
            f"Concentrati su definizioni, principi e relazioni utili per "
            f"un'interrogazione universitaria."
        ),
        expected_output=(
            "Un elenco ordinato dei concetti chiave estratti dal documento "
            "sull'argomento indicato, in formato testo strutturato."
        ),
        agent=librarian,
    )

    # 2) Generazione di una sola domanda aperta e sfidante per lo studente.
    task_generazione_domanda: Task = Task(
        description=(
            f"Sulla base dei concetti chiave estratti dal Librarian sull'argomento "
            f"'{argomento}', formula UNA SOLA domanda d'esame aperta, sfidante e "
            f"non banale, capace di valutare la reale comprensione dello studente. "
            f"Non fornire la risposta: restituisci esclusivamente la domanda."
        ),
        expected_output=(
            "Una singola domanda aperta, formulata in italiano accademico, "
            "senza alcuna risposta o suggerimento."
        ),
        agent=examiner,
    )

    return [task_estrazione_concetti, task_generazione_domanda]


def create_evaluation_tasks(
    argomento: str,
    nome_file_pdf: str,
    domanda: str,
    risposta_studente: str,
) -> list[Task]:
    """
    Crea i task per valutare la risposta di uno studente confrontandola col PDF.

    Flusso:
        1. Il Librarian cerca nel PDF la 'verità' relativa alla domanda.
        2. L'Examiner confronta la verità con la risposta dello studente
           e produce un feedback severo ma costruttivo, con voto da 1 a 10.

    Args:
        argomento: Argomento dell'interrogazione.
        nome_file_pdf: Nome del PDF presente in data/raw_pdfs/.
        domanda: Domanda originariamente posta allo studente.
        risposta_studente: Risposta fornita dallo studente.

    Returns:
        Lista ordinata dei task da eseguire nel workflow CrewAI.
    """
    librarian = get_librarian()
    examiner = get_examiner()

    # 1) Estrazione della 'verità' dal PDF rispetto alla domanda posta.
    task_ricerca_verita: Task = Task(
        description=(
            f"Usa il tuo tool per leggere il file PDF '{nome_file_pdf}' e individua "
            f"le informazioni corrette e complete per rispondere alla seguente "
            f"domanda relativa all'argomento '{argomento}':\n"
            f"Domanda: '{domanda}'.\n"
            f"Riporta i contenuti del documento che costituiscono la risposta "
            f"di riferimento (la 'verità')."
        ),
        expected_output=(
            "Un testo strutturato che riassume la risposta corretta secondo il PDF, "
            "con i passaggi chiave necessari per valutare lo studente."
        ),
        agent=librarian,
    )

    # 2) Confronto risposta studente vs verità + feedback e voto da 1 a 10.
    task_valutazione: Task = Task(
        description=(
            f"Confronta la risposta dello studente con la 'verità' fornita dal "
            f"Librarian e valuta la prestazione in modo severo ma didattico.\n\n"
            f"Argomento: '{argomento}'.\n"
            f"Domanda: '{domanda}'.\n"
            f"Risposta dello studente:\n'''{risposta_studente}'''\n\n"
            f"Indica chiaramente: punti corretti, errori, lacune e suggerimenti "
            f"di miglioramento. Concludi sempre assegnando un voto numerico "
            f"intero da 1 a 10."
        ),
        expected_output=(
            "Un feedback strutturato in Markdown con sezioni per punti corretti, "
            "errori, lacune, consigli di miglioramento e una riga finale "
            "nel formato 'Voto: X/10' (con X intero da 1 a 10)."
        ),
        agent=examiner,
    )

    return [task_ricerca_verita, task_valutazione]
