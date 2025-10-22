# src/tools/arxiv_tools.py
# Herramientas específicas para interactuar con la base de datos arXiv.

from crewai.tools import tool
import arxiv

class ArxivTools:

    @tool
    def search_arxiv(query: str) -> list:
        """
        Busca artículos en arXiv usando la librería arxiv.
        Retorna una lista de diccionarios con los detalles de cada artículo.
        """
        search = arxiv.Search(
            query=query,
            max_results=100, # Limitar a 100 resultados
            sort_by=arxiv.SortCriterion.Relevance,
            sort_order=arxiv.SortOrder.Descending
        )

        articles_details = []
        for result in search.results():
            authors_list = [author.name for author in result.authors]
            authors = ", ".join(authors_list)
            
            articles_details.append({
                "id": result.entry_id.split('/')[-1], # Extraer ID de la URL
                "title": result.title,
                "authors": authors,
                "abstract": result.summary,
                "journal": "arXiv", # En arXiv no hay journal, se usa "arXiv"
                "year": result.published.year,
                "url": result.entry_id
            })
        return articles_details