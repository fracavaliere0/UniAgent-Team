"""Definizione dei task CrewAI per i flussi di studio, interrogazione e mappa."""

from crewai import Task

from src.agents import get_examiner, get_librarian, get_mapper, get_professor


def create_study_tasks(domanda_studente: str, nome_file_pdf: str) -> list[Task]:
    """
    Crea i task per produrre una spiegazione accademica a partire da un PDF.

    Flusso:
        1. Il Librarian estrae dal PDF le informazioni utili.
        2. Il Professor le rielabora in una spiegazione accademica in Markdown.

    Se ``domanda_studente`` è vuoto, viene chiesto un riassunto generale
    dei contenuti del documento.

    Args:
        domanda_studente: Quesito o argomento; se vuoto si genera un riassunto.
        nome_file_pdf: Nome del PDF presente in data/raw_pdfs/.

    Returns:
        Lista ordinata dei task da eseguire nel workflow CrewAI.
    """
    librarian = get_librarian()
    professor = get_professor()

    # Se la domanda è assente, chiede un riassunto generale del documento.
    domanda_effettiva: str = (
        domanda_studente.strip()
        if domanda_studente and domanda_studente.strip()
        else "Fornisci un riassunto generale dei contenuti principali del documento."
    )

    # 1) Ricerca delle informazioni rilevanti nel PDF.
    task_ricerca: Task = Task(
        description=(
            f"Usa il tuo tool per leggere il file PDF '{nome_file_pdf}' e cerca tutte "
            f"le informazioni utili per rispondere alla seguente richiesta dello "
            f"studente: '{domanda_effettiva}'."
        ),
        expected_output=(
            "Un riassunto in formato testo con i passaggi chiave estratti dal documento."
        ),
        agent=librarian,
    )

    # 2) Rielaborazione in spiegazione accademica formattata in Markdown.
    task_spiegazione: Task = Task(
        description=(
            f"Prendi gli appunti forniti dal Librarian e crea una lezione per lo "
            f"studente basata sulla seguente richiesta: '{domanda_effettiva}'. "
            f"Mantieni un tono accademico e chiaro, basandoti unicamente sui dati "
            f"forniti dal Librarian.\n\n"
            f"ATTENZIONE ALLA FORMATTAZIONE MARKDOWN: Quando crei un elenco "
            f"puntato, devi ASSOLUTAMENTE andare a capo prima di ogni nuovo "
            f"punto. Non scrivere mai gli asterischi o i trattini sulla stessa "
            f"riga del testo precedente."
        ),
        expected_output=(
            "Una spiegazione discorsiva, formattata in Markdown, "
            "chiara e con tono accademico."
        ),
        agent=professor,
    )

    return [task_ricerca, task_spiegazione]


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

    # 2) Conversione dei concetti in un diagramma Mermaid 'graph LR' semplice.
    task_generazione_mappa: Task = Task(
        description=(
            f"Prendi i concetti VERI estratti dal Librarian sull'argomento "
            f"'{argomento}' e convertili in un diagramma semplice in sintassi "
            f"Mermaid.js.\n\n"
            f"REGOLE FERREE (rispettarle alla lettera):\n"
            f"1. DIREZIONE: usa OBBLIGATORIAMENTE 'graph LR' (Left to Right). "
            f"MAI 'graph TD'.\n"
            f"2. SOLO COLLEGAMENTI SEMPLICI tra i nodi principali. NIENTE "
            f"subgraph, NIENTE forme geometriche speciali: usa esclusivamente "
            f"la sintassi 'A[Testo]' per tutti i nodi.\n"
            f"3. ETICHETTE SULLE FRECCE: ogni relazione DEVE avere un'etichetta "
            f"che spieghi il legame nel formato "
            f"'A[Concetto1] -->|verbo o relazione| B[Concetto2]' "
            f"(es. 'A[Java] -->|è orientato a| B[Oggetti]'). Niente frecce "
            f"mute.\n"
            f"4. USA I VERI CONCETTI ESTRATTI DAL PDF: i nodi devono contenere "
            f"i nomi reali dei concetti individuati dal Librarian "
            f"(es. 'Java', 'Polimorfismo', 'JVM'). NON usare MAI segnaposto "
            f"generici come 'Concetto', 'Nodo', 'Categoria Principale' o "
            f"simili.\n"
            f"5. UNA RELAZIONE PER RIGA: non concatenare nodi sulla stessa "
            f"riga. ERRATO: 'A --> B --> C'. CORRETTO: 'A --> B' a capo "
            f"'B --> C'.\n"
            f"6. ID DEI NODI: usa identificatori alfanumerici brevi (A, B, "
            f"C1, ...). Il testo reale visibile va SOLO dentro le parentesi "
            f"quadre.\n"
            f"7. TESTO NEI NODI: massimo 3-4 parole. Se contiene spazi o "
            f"caratteri speciali, racchiudilo tra virgolette doppie "
            f"(es. A[\"Programmazione Orientata Oggetti\"]).\n"
            f"8. Restituisci ESCLUSIVAMENTE il blocco di codice markdown "
            f"Mermaid, senza testo aggiuntivo prima o dopo."
        ),
        expected_output=(
            "Un blocco di codice markdown formattato RIGOROSAMENTE come segue, "
            "che inizia con ```mermaid e termina con ```, con direzione "
            "'graph LR', nodi nella sola forma 'A[Testo]' contenenti i VERI "
            "concetti del PDF, una relazione per riga ed etichette esplicative "
            "sopra ogni freccia (es. 'A[Java] -->|è orientato a| B[Oggetti]'):"
            "\n\n"
            "```mermaid\n"
            "graph LR\n"
            "    A[Java] -->|è orientato a| B[Oggetti]\n"
            "    A -->|gira su| C[JVM]\n"
            '    B -->|"supporta"| D[Polimorfismo]\n'
            "```\n\n"
            "Nessun testo deve essere presente al di fuori del blocco di codice."
        ),
        agent=mapper,
    )

    return [task_estrazione_relazioni, task_generazione_mappa]
