# src/tools/bibtex_tools.py
# Herramientas para la generación y escritura de archivos BibTeX.

from crewai.tools import tool

class BibtexTools:

    @tool
    def generate_bibtex_entry(article_data: dict) -> str:
        """
        Genera una entrada BibTeX a partir de los metadatos de un artículo.
        article_data debe contener al menos 'title', 'authors', 'year', 'journal' o 'url'.
        """
        title = article_data.get("title", "N/A")
        authors = article_data.get("authors", "N/A")
        year = article_data.get("year", "N/A")
        journal = article_data.get("journal", "N/A")
        url = article_data.get("url", "N/A")
        
        # Crear una clave BibTeX simple
        first_author_surname = authors.split(',')[0].split()[-1] if authors != "N/A" else "Anon"
        bib_key = f"{first_author_surname}{year}{title[:5].replace(' ', '')}"

        bibtex_entry = f"""@article{{{bib_key},
    title = {{{title}}},
    author = {{{authors}}},
    journal = {{{journal}}},
    year = {{{year}}},
    url = {{{url}}}
"""
        return bibtex_entry

    @tool
    def write_bibtex_file(bibtex_entries: list, filename: str = "investigacion_stroke_mri.bib") -> str:
        """
        Escribe una lista de entradas BibTeX en un archivo.
        """
        try:
            with open(filename, "w", encoding="utf-8") as f:
                for entry in bibtex_entries:
                    f.write(entry + "\n\n")
            return f"Archivo BibTeX '{filename}' creado exitosamente."
        except Exception as e:
            return f"Error al escribir el archivo BibTeX: {e}"