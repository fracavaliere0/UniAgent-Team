"""Definizione dei task CrewAI per i flussi di interrogazione e valutazione."""

from crewai import Task

from src.agents import get_examiner, get_librarian, get_mapper


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


def create_map_tasks(argomento: str, nome_file_pdf: str) -> list[Task]:
    """
    Crea i task per generare una mappa concettuale in sintassi Mermaid.js.

    Flusso:
        1. Il Librarian estrae dal PDF i concetti chiave e le loro relazioni.
        2. Il Mapper trasforma i concetti in un diagramma 'graph LR' Mermaid.

    Args:
        argomento: Argomento di studio scelto dallo studente.
        nome_file_pdf: Nome del PDF presente in data/raw_pdfs/.

    Returns:
        Lista ordinata dei task da eseguire nel workflow CrewAI.
    """
    librarian = get_librarian()
    mapper = get_mapper()

    # 1) Estrazione concetti e relazioni logiche dal PDF.
    task_estrazione_relazioni: Task = Task(
        description=(
            f"Usa il tuo tool per leggere il file PDF '{nome_file_pdf}' e individua "
            f"i concetti chiave relativi all'argomento '{argomento}' insieme alle "
            f"loro relazioni logiche (gerarchie, dipendenze, cause-effetto). "
            f"Restituisci un elenco strutturato che evidenzi sia i concetti sia "
            f"i collegamenti tra di essi."
        ),
        expected_output=(
            "Un testo strutturato con i concetti chiave e le loro relazioni logiche, "
            "pronto per essere convertito in un diagramma."
        ),
        agent=librarian,
    )

    # 2) Conversione dei concetti in un diagramma Mermaid 'graph LR'.
    task_generazione_mappa: Task = Task(
        description=(
            f"Prendi i concetti e le relazioni forniti dal Librarian sull'argomento "
            f"'{argomento}' e generali sotto forma di diagramma a blocchi in "
            f"sintassi Mermaid.js.\n\n"
            f"REGOLE FERREE per la generazione del codice Mermaid:\n"
            f"1. DIREZIONE ORIZZONTALE: usa OBBLIGATORIAMENTE 'graph LR' "
            f"(Left to Right) e MAI 'graph TD'.\n"
            f"2. TESTO BREVISSIMO: ogni nodo deve contenere MASSIMO 3 o 4 parole. "
            f"Usa acronimi o parole chiave. MAI frasi lunghe o descrizioni estese.\n"
            f"3. STRUTTURA GERARCHICA SEMPLICE: non creare troppi incroci complessi, "
            f"mantieni un flusso pulito da sinistra a destra senza ramificazioni "
            f"intricate.\n"
            f"4. Evita caratteri speciali strani nei nomi dei nodi "
            f"(no accenti grafici, parentesi non bilanciate, virgolette doppie, "
            f"trattini lunghi, emoji, simboli matematici): preferisci nomi brevi "
            f"in lettere semplici e numeri.\n"
            f"5. Restituisci ESCLUSIVAMENTE il blocco di codice markdown Mermaid, "
            f"senza testo aggiuntivo prima o dopo."
        ),
        expected_output=(
            "Un blocco di codice markdown formattato RIGOROSAMENTE come segue, "
            "che inizia con ```mermaid e termina con ```, con direzione 'graph LR' "
            "e nodi composti da MASSIMO 3-4 parole ciascuno:\n\n"
            "```mermaid\n"
            "graph LR\n"
            "    A[Concetto Chiave] --> B[Sotto Concetto 1]\n"
            "    A --> C[Sotto Concetto 2]\n"
            "```\n\n"
            "Nessun testo deve essere presente al di fuori del blocco di codice."
        ),
        agent=mapper,
    )

    return [task_estrazione_relazioni, task_generazione_mappa]
