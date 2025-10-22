# src/tools/pubmed_tools.py
# Herramientas específicas para interactuar con la base de datos PubMed.

from crewai.tools import tool
from Bio import Entrez
import os

# Configura tu email para Entrez
Entrez.email = os.getenv("ENTREZ_EMAIL", "your.email@example.com") # Reemplaza con un email real o configúralo en .env

class PubMedTools:

    @tool
    def search_pubmed(query: str) -> str:
        """
        Busca artículos en PubMed usando la API de Entrez.
        Retorna una lista de IDs de PubMed.
        """
        handle = Entrez.esearch(db="pubmed", term=query, retmax="100") # Limitar a 100 resultados
        record = Entrez.read(handle)
        handle.close()
        return record["IdList"]

    @tool
    def fetch_pubmed_details(pubmed_ids: list) -> list:
        """
        Recupera los detalles (título, autores, abstract, etc.) de artículos de PubMed
        dado una lista de IDs de PubMed.
        Retorna una lista de diccionarios con los detalles de cada artículo.
        """
        if not pubmed_ids:
            return []

        handle = Entrez.efetch(db="pubmed", id=pubmed_ids, retmode="xml")
        records = Entrez.read(handle)
        handle.close()

        articles_details = []
        for pubmed_article in records['PubmedArticle']:
            article = pubmed_article['MedlineCitation']['Article']
            
            title = article.get('ArticleTitle', 'N/A')
            abstract_sections = article.get('Abstract', {}).get('AbstractText', [])
            abstract = " ".join(abstract_sections) if isinstance(abstract_sections, list) else abstract_sections

            authors_list = []
            if 'AuthorList' in article:
                for author in article['AuthorList']:
                    if 'LastName' in author and 'ForeName' in author:
                        authors_list.append(f"{author['ForeName']} {author['LastName']}")
                    elif 'CollectiveName' in author:
                        authors_list.append(author['CollectiveName'])
            authors = ", ".join(authors_list)

            journal = article.get('Journal', {}).get('Title', 'N/A')
            pub_date = article.get('Journal', {}).get('JournalIssue', {}).get('PubDate', {})
            year = pub_date.get('Year', 'N/A')
            
            # Construir URL de PubMed
            pubmed_id = pubmed_article['MedlineCitation']['PMID']
            url = f"https://pubmed.ncbi.nlm.nih.gov/{pubmed_id}/"

            articles_details.append({
                "id": pubmed_id,
                "title": title,
                "authors": authors,
                "abstract": abstract,
                "journal": journal,
                "year": year,
                "url": url
            })
        return articles_details