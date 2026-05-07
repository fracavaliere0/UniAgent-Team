"""Interfaccia Streamlit dell'app UniAgent - Mentore Socratico e Mappa Concettuale."""

import re

import streamlit as st
import streamlit.components.v1 as components
from crewai import Crew, Process

from src.tasks import (
    create_evaluation_tasks,
    create_map_tasks,
    create_question_tasks,
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

# Inizializzazione dello stato di sessione condiviso tra le modalità.
if "step" not in st.session_state:
    st.session_state.step = 1
if "domanda_generata" not in st.session_state:
    st.session_state.domanda_generata = ""
if "argomento" not in st.session_state:
    st.session_state.argomento = ""


def reset_simulazione() -> None:
    """Riporta la modalità Mentore Socratico allo step 1, pulendo i dati correnti."""
    st.session_state.step = 1
    st.session_state.domanda_generata = ""
    st.session_state.argomento = ""


# ------------------------------- SIDEBAR -------------------------------
with st.sidebar:
    st.header("⚙️ Configurazione")

    nome_pdf: str = st.text_input(
        "Nome del file PDF (in data/raw_pdfs/)",
        value="test.pdf",
    )

    modalita: str = st.radio(
        "Modalità di Studio",
        options=["Mentore Socratico", "Mappa Concettuale"],
        index=0,
    )


# ----------------------- MODALITÀ: MENTORE SOCRATICO -----------------------
if modalita == "Mentore Socratico":
    st.title("🎓 UniAgent - Mentore Socratico")

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

    # STEP 2: risposta dello studente e valutazione.
    elif st.session_state.step == 2:
        st.subheader("Step 2 · Rispondi alla domanda dell'Examiner")

        st.markdown("**Domanda d'esame:**")
        st.markdown(st.session_state.domanda_generata)

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

                    st.markdown("### 📋 Valutazione")
                    st.markdown(str(risultato_valutazione))

        with colonna_reset:
            if st.button("Cambia Argomento"):
                reset_simulazione()
                st.rerun()


# ----------------------- MODALITÀ: MAPPA CONCETTUALE -----------------------
elif modalita == "Mappa Concettuale":
    st.title("🗺️ UniAgent - Mappa Concettuale")

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

            render_mermaid(str(risultato_mappa))
