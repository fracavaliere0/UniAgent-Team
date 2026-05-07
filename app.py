"""Interfaccia Streamlit dell'app UniAgent - Simulatore Socratico."""

import streamlit as st
from crewai import Crew, Process

from src.tasks import create_evaluation_tasks, create_question_tasks


st.set_page_config(page_title="UniAgent", page_icon="🎓")
st.title("🎓 UniAgent - Simulatore Socratico")

# Inizializzazione dello stato della sessione (step corrente e dati persistenti).
if "step" not in st.session_state:
    st.session_state.step = 1
if "domanda_generata" not in st.session_state:
    st.session_state.domanda_generata = ""
if "nome_pdf" not in st.session_state:
    st.session_state.nome_pdf = "test.pdf"
if "argomento" not in st.session_state:
    st.session_state.argomento = ""


def reset_simulazione() -> None:
    """Riporta l'app allo step 1, pulendo i dati dell'interrogazione corrente."""
    st.session_state.step = 1
    st.session_state.domanda_generata = ""
    st.session_state.argomento = ""


# ----------------------------- STEP 1: Domanda -----------------------------
if st.session_state.step == 1:
    st.subheader("Step 1 · Scegli il materiale e l'argomento")

    nome_pdf: str = st.text_input(
        "Nome del file PDF (presente in data/raw_pdfs/)",
        value=st.session_state.nome_pdf,
    )
    argomento: str = st.text_input(
        "Argomento da ripassare",
        value=st.session_state.argomento,
        placeholder="Esempio: Teorema di Bayes",
    )

    if st.button("Genera Domanda", type="primary"):
        if not nome_pdf.strip() or not argomento.strip():
            st.warning("Inserisci sia il nome del PDF sia l'argomento da ripassare.")
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

            st.session_state.nome_pdf = nome_pdf
            st.session_state.argomento = argomento
            st.session_state.domanda_generata = str(domanda_finale)
            st.session_state.step = 2
            st.rerun()


# ---------------------------- STEP 2: Risposta ----------------------------
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
                st.warning("Scrivi una risposta prima di chiedere la valutazione.")
            else:
                with st.spinner("L'Examiner sta valutando la tua risposta..."):
                    task_valutazione = create_evaluation_tasks(
                        argomento=st.session_state.argomento,
                        nome_file_pdf=st.session_state.nome_pdf,
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
