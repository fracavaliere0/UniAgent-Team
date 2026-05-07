"""Interfaccia Streamlit dell'app UniAgent."""

import streamlit as st
from crewai import Crew, Process

from src.tasks import create_study_tasks


st.set_page_config(page_title="UniAgent", page_icon="🎓")
st.title("🎓 UniAgent - Il tuo Team di Studio")

# Input utente: nome file PDF e domanda di studio.
nome_pdf: str = st.text_input("Nome del file PDF", value="test.pdf")
domanda: str = st.text_area(
    "Scrivi la tua domanda di studio",
    placeholder="Esempio: Puoi spiegarmi il teorema di Bayes con un esempio pratico?",
)

if st.button("Inizia lo Studio"):
    with st.spinner("Sto analizzando il materiale e preparando la spiegazione..."):
        task_studio = create_study_tasks(
            domanda_studente=domanda,
            nome_file_pdf=nome_pdf,
        )

        crew_studio: Crew = Crew(
            tasks=task_studio,
            process=Process.sequential,
        )
        risultato_finale = crew_studio.kickoff()

    st.markdown(str(risultato_finale))
