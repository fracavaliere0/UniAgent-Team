"""Interfaccia Streamlit dell'app UniAgent - Spiegazione, Mentore e Mappa."""

import re

import streamlit as st
import streamlit.components.v1 as components
from crewai import Crew, Process

from src.tasks import (
    create_evaluation_tasks,
    create_map_tasks,
    create_question_tasks,
    create_study_tasks,
)


def render_mermaid(payload: str) -> None:
    """
    Visualizza un diagramma Mermaid nell'app usando il CDN di Mermaid.js.

    Se il payload contiene un blocco ```mermaid ... ``` ne estrae solo il codice;
    altrimenti usa l'intero testo come definizione del grafico.
    """
    # Estrae solo il codice tra i tag mermaid se presenti
    pattern = r"```mermaid\s*(.*?)\s*```"
    match = re.search(pattern, payload, re.DOTALL)
    codice_pulito = match.group(1) if match else payload

    html_code = f"""
    <div class="mermaid" style="width: 100%; overflow-x: auto; background-color: white; padding: 20px; border-radius: 10px;">
        {codice_pulito}
    </div>
    <script type="module">
        import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs';
        mermaid.initialize({{ startOnLoad: true, theme: 'default' }});
    </script>
    """
    components.html(html_code, height=500, scrolling=True)


st.set_page_config(page_title="UniAgent", page_icon="🎓")

# Stile globale dell'app: bottoni personalizzati e UI più pulita.
st.markdown(
    """
<style>
    /* Stile per i bottoni */
    div.stButton > button:first-child {
        background-color: #4F46E5;
        color: white;
        border-radius: 8px;
        border: none;
        padding: 0.5rem 1rem;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    div.stButton > button:first-child:hover {
        background-color: #4338CA;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    /* Nascondi il menu di default di Streamlit per un look più pulito */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""",
    unsafe_allow_html=True,
)

# Inizializzazione dello stato di sessione condiviso tra le modalità.
if "step" not in st.session_state:
    st.session_state.step = 1
if "domanda_generata" not in st.session_state:
    st.session_state.domanda_generata = ""
if "argomento" not in st.session_state:
    st.session_state.argomento = ""

# Risultati persistenti: restano visibili anche cambiando modalità nella sidebar.
if "res_spiegazione" not in st.session_state:
    st.session_state.res_spiegazione = ""
if "res_mappa" not in st.session_state:
    st.session_state.res_mappa = ""
if "res_valutazione" not in st.session_state:
    st.session_state.res_valutazione = ""


def pulisci_risultati() -> None:
    """Resetta a stringa vuota tutti i risultati persistenti delle modalità."""
    st.session_state.res_spiegazione = ""
    st.session_state.res_mappa = ""
    st.session_state.res_valutazione = ""


def reset_simulazione() -> None:
    """Riporta la modalità Mentore Socratico allo step 1, pulendo i dati correnti."""
    st.session_state.step = 1
    st.session_state.domanda_generata = ""
    st.session_state.argomento = ""


# ------------------------------- SIDEBAR -------------------------------
with st.sidebar:
    st.header("Impostazioni Studio 📚")

    nome_pdf: str = st.text_input(
        "Nome del file PDF (in data/raw_pdfs/)",
        value="test.pdf",
    )

    st.divider()

    modalita: str = st.radio(
        "Modalità di Studio",
        options=[
            "Spiegazione Accademica",
            "Mentore Socratico",
            "Mappa Concettuale",
        ],
        index=0,
    )

    st.divider()

    if st.button("Pulisci Risultati"):
        pulisci_risultati()
        st.rerun()


# --------------------- MODALITÀ: SPIEGAZIONE ACCADEMICA ---------------------
if modalita == "Spiegazione Accademica":
    st.title("📖 UniAgent - Spiegazione Accademica")

    # --- INPUT: in cima alla pagina ---
    argomento_studio: str = st.text_area(
        "Argomento o domanda (lascia vuoto per un riassunto generale)",
        height=120,
        placeholder="Esempio: Spiegami in dettaglio il teorema di Bayes",
    )

    if st.button("Genera Spiegazione", type="primary"):
        if not nome_pdf.strip():
            st.warning("Inserisci il nome del file PDF nella sidebar.")
        else:
            with st.spinner("Il Professore sta preparando la spiegazione..."):
                task_studio = create_study_tasks(
                    domanda_studente=argomento_studio,
                    nome_file_pdf=nome_pdf,
                )
                crew_studio: Crew = Crew(
                    tasks=task_studio,
                    process=Process.sequential,
                )
                risultato_studio = crew_studio.kickoff()

            st.session_state.res_spiegazione = str(risultato_studio)
            st.rerun()

    # --- OUTPUT: in fondo alla pagina ---
    if st.session_state.res_spiegazione:
        st.divider()
        st.success("Ecco la tua spiegazione:")
        st.markdown(st.session_state.res_spiegazione)


# ----------------------- MODALITÀ: MENTORE SOCRATICO -----------------------
elif modalita == "Mentore Socratico":
    st.title("🎓 UniAgent - Mentore Socratico")

    # --- INPUT: in cima alla pagina ---
    # STEP 1: scelta dell'argomento e generazione della domanda d'esame.
    if st.session_state.step == 1:
        st.subheader("Step 1 · Scegli l'argomento da ripassare")

        argomento: str = st.text_input(
            "Argomento da ripassare",
            value=st.session_state.argomento,
            placeholder="Esempio: Teorema di Bayes",
        )

        if st.button("Genera Domanda", type="primary"):
            if not nome_pdf.strip() or not argomento.strip():
                st.warning(
                    "Inserisci sia il nome del PDF sia l'argomento da ripassare."
                )
            else:
                with st.spinner("L'Examiner sta preparando una domanda sfidante..."):
                    task_domanda = create_question_tasks(
                        argomento=argomento,
                        nome_file_pdf=nome_pdf,
                    )
                    crew_domanda: Crew = Crew(
                        tasks=task_domanda,
                        process=Process.sequential,
                    )
                    domanda_finale = crew_domanda.kickoff()

                st.session_state.argomento = argomento
                st.session_state.domanda_generata = str(domanda_finale)
                st.session_state.step = 2
                st.rerun()

    # STEP 2: domanda dell'Examiner, risposta dello studente e valutazione.
    elif st.session_state.step == 2:
        st.subheader("Step 2 · Rispondi alla domanda dell'Examiner")

        # La domanda dell'Examiner resta sopra l'area di risposta.
        st.info(
            f"🎓 **Il Professore chiede:**\n\n{st.session_state.domanda_generata}"
        )

        risposta_studente: str = st.text_area(
            "La tua risposta",
            height=220,
            placeholder="Scrivi qui la tua risposta in modo chiaro e completo...",
        )

        colonna_valuta, colonna_reset = st.columns(2)

        with colonna_valuta:
            if st.button("Valuta", type="primary"):
                if not risposta_studente.strip():
                    st.warning(
                        "Scrivi una risposta prima di chiedere la valutazione."
                    )
                else:
                    with st.spinner("L'Examiner sta valutando la tua risposta..."):
                        task_valutazione = create_evaluation_tasks(
                            argomento=st.session_state.argomento,
                            nome_file_pdf=nome_pdf,
                            domanda=st.session_state.domanda_generata,
                            risposta_studente=risposta_studente,
                        )
                        crew_valutazione: Crew = Crew(
                            tasks=task_valutazione,
                            process=Process.sequential,
                        )
                        risultato_valutazione = crew_valutazione.kickoff()

                    st.session_state.res_valutazione = str(risultato_valutazione)
                    st.rerun()

        with colonna_reset:
            if st.button("Cambia Argomento"):
                reset_simulazione()
                st.rerun()

    # --- OUTPUT: il feedback finale appare sempre in fondo al blocco. ---
    if st.session_state.res_valutazione:
        st.divider()
        st.success("Ecco il tuo ultimo feedback:")
        st.markdown(st.session_state.res_valutazione)


# ----------------------- MODALITÀ: MAPPA CONCETTUALE -----------------------
elif modalita == "Mappa Concettuale":
    st.title("🗺️ UniAgent - Mappa Concettuale")

    # --- INPUT: in cima alla pagina ---
    argomento_mappa: str = st.text_area(
        "Argomento da mappare",
        height=120,
        placeholder="Esempio: Reti Neurali Convoluzionali",
    )

    if st.button("Genera Mappa", type="primary"):
        if not nome_pdf.strip() or not argomento_mappa.strip():
            st.warning("Inserisci sia il nome del PDF sia l'argomento da mappare.")
        else:
            with st.spinner("Il Mapper sta costruendo la mappa concettuale..."):
                task_mappa = create_map_tasks(
                    argomento=argomento_mappa,
                    nome_file_pdf=nome_pdf,
                )
                crew_mappa: Crew = Crew(
                    tasks=task_mappa,
                    process=Process.sequential,
                )
                risultato_mappa = crew_mappa.kickoff()

            st.session_state.res_mappa = str(risultato_mappa)
            st.rerun()

    # --- OUTPUT: in fondo alla pagina ---
    if st.session_state.res_mappa:
        st.divider()
        render_mermaid(st.session_state.res_mappa)
