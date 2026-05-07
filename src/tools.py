"""Strumenti personalizzati per CrewAI."""

from pathlib import Path

from crewai.tools import BaseTool
from langchain_community.document_loaders import PyPDFLoader


class PDFSearchTool(BaseTool):
    """Tool CrewAI che legge un PDF dalla cartella data/raw_pdfs/."""

    name: str = "pdf_search_tool"
    description: str = (
        "Riceve il nome di un file PDF presente in data/raw_pdfs/ e "
        "restituisce il testo completo estratto."
    )

    def _run(self, nome_file_pdf: str) -> str:
        """
        Carica ed estrae il testo di un PDF.

        Args:
            nome_file_pdf: Nome del file PDF (es. 'manuale.pdf').

        Returns:
            Testo completo estratto dal PDF.
        """
        # Individua la root del progetto partendo da questo file (src/tools.py).
        root_progetto: Path = Path(__file__).resolve().parent.parent
        cartella_pdf: Path = root_progetto / "data" / "raw_pdfs"

        nome_pulito: str = Path(nome_file_pdf).name
        if not nome_pulito.lower().endswith(".pdf"):
            raise ValueError(
                "Il file indicato deve avere estensione .pdf "
                f"(ricevuto: '{nome_file_pdf}')."
            )

        percorso_pdf: Path = cartella_pdf / nome_pulito
        if not percorso_pdf.exists():
            raise FileNotFoundError(
                f"File non trovato in data/raw_pdfs/: '{nome_pulito}'."
            )

        loader: PyPDFLoader = PyPDFLoader(str(percorso_pdf))
        pagine = loader.load()

        testo_estratto: str = "\n\n".join(
            pagina.page_content.strip()
            for pagina in pagine
            if pagina.page_content and pagina.page_content.strip()
        ).strip()

        if not testo_estratto:
            raise ValueError(
                f"Il PDF '{nome_pulito}' non contiene testo estraibile."
            )

        return testo_estratto
