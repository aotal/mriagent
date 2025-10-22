# src/tasks.py
# Definición de todas las tareas (descripciones, expected_output) para el sistema de investigación.

from crewai import Task
from .tools.pubmed_tools import PubMedTools
from .tools.arxiv_tools import ArxivTools
from .tools.bibtex_tools import BibtexTools
from .tools.analysis_tools import AnalysisTools
from .tools.summary_tools import SummaryTools
from .tools.crossref_tools import CrossrefTools
from .agents import (
    AgenteCoordinadorDeBusqueda,
    AgenteBuscadorPubMed,
    AgenteBuscadorArXiv,
    AgenteFiltradorDeContenido,
    AgenteAnalistaMetodologico,
    AgentePriorizadorYEtiquetador,
    AgenteGeneradorBibTeX,
    AgenteGeneradorResumen
)

class ResearchTasks:

    def __init__(self, research_topic: str):
        self.research_topic = research_topic

    def tarea_buscar_pubmed(self):
        return Task(
            description=f"Buscar artículos relevantes en PubMed sobre '{self.research_topic}'. "
                        "La búsqueda debe ser exhaustiva y enfocarse en contribuciones originales, "
                        "excluyendo explícitamente artículos de revisión, revisiones sistemáticas y meta-análisis.",
            expected_output="Una lista de diccionarios, donde cada diccionario contiene el ID de PubMed, título, autores, año, URL y el abstract completo de artículos potencialmente relevantes, excluyendo explícitamente cualquier tipo de revisión.",
            agent=AgenteBuscadorPubMed,
            tools=[PubMedTools.search_pubmed, PubMedTools.fetch_pubmed_details]
        )

    def tarea_buscar_arxiv(self):
        return Task(
            description=f"Buscar preprints y artículos relevantes en arXiv sobre '{self.research_topic}'. "
                        "La búsqueda debe enfocarse en las últimas innovaciones y excluir cualquier tipo de revisión.",
            expected_output="Una lista de diccionarios, donde cada diccionario contiene el ID de arXiv, título, autores, año, URL y el abstract completo de preprints potencialmente relevantes, excluyendo explícitamente cualquier tipo de revisión.",
            agent=AgenteBuscadorArXiv,
            tools=[ArxivTools.search_arxiv]
        )

    def tarea_consolidar_y_filtrar_reviews(self, context):
        return Task(
            description="Consolidar los resultados de PubMed y arXiv, y filtrar estrictamente los artículos que sean 'review', 'systematic review' o 'meta-analysis' basándose en el título y el abstract. "
                        "Solo se deben mantener las contribuciones originales.",
            expected_output="Una lista consolidada de diccionarios de artículos (ID, título, autores, año, URL, abstract) que son contribuciones originales y relevantes, sin incluir ningún tipo de revisión.",
            agent=AgenteFiltradorDeContenido,
            context=context,
            tools=[AnalysisTools.classify_article_type]
        )

    def tarea_analizar_metodologia_y_disponibilidad(self, context):
        return Task(
            description="Analizar los abstracts de los artículos filtrados para identificar la presencia y relevancia de metodologías específicas (Deep Learning, CNNs, U-Net, Transformers) y evaluar la disponibilidad de código o datasets públicos.",
            expected_output="La misma lista de diccionarios de artículos, pero cada diccionario enriquecido con campos adicionales: `metodologias_identificadas` (lista de strings), `codigo_disponible` (booleano), `datasets_disponibles` (booleano).",
            agent=AgenteAnalistaMetodologico,
            context=context,
            tools=[AnalysisTools.extract_methodologies_and_data_availability]
        )

    def tarea_priorizar_y_etiquetar(self, context):
        return Task(
            description="Priorizar y etiquetar los artículos basándose en su fecha de publicación (más recientes primero) y la relevancia metodológica (presencia de metodologías avanzadas).",
            expected_output="La lista COMPLETA de diccionarios de artículos (incluyendo todos los campos originales como id, title, authors, year, url, abstract, journal, además de metodologias_identificadas, codigo_disponible, datasets_disponibles), ahora ordenada por prioridad y con los campos adicionales `prioridad` (string: 'Alta', 'Media', 'Baja') y `etiquetas` (lista de strings).",
            agent=AgentePriorizadorYEtiquetador,
            context=context
            # No se necesitan herramientas adicionales aquí, el agente usará su LLM para razonar y priorizar
        )

    def tarea_generar_bibtex(self, context):
        return Task(
            description="Generar una entrada BibTeX para cada artículo priorizado y relevante, y consolidarlas en un único archivo BibTeX.",
            expected_output="Un mensaje de confirmación indicando que el archivo `investigacion_stroke_mri.bib` ha sido creado exitosamente, conteniendo todas las entradas BibTeX de los artículos seleccionados.",
            agent=AgenteGeneradorBibTeX,
            context=context,
            tools=[BibtexTools.generate_bibtex_entry, BibtexTools.write_bibtex_file]
        )
        
    def tarea_generar_resumen(self, context):
        return Task(
            description="Analizar la lista final de artículos priorizados y etiquetados. Identificar tendencias clave (ej. metodologías predominantes, años de publicación, disponibilidad de recursos) y los 2-3 artículos más relevantes. Escribir un resumen ejecutivo (2-3 párrafos) destacando estos hallazgos.",
            expected_output="Un documento de texto (string) que contenga un resumen ejecutivo de la investigación realizada, mencionando las tendencias principales y los artículos más destacados.",
            agent=AgenteGeneradorResumen,
            context=context,
            # Podrías crear una herramienta específica si necesitas guardar el resumen en un archivo .txt o .md
            tools=[SummaryTools.write_summary_file] 
        )
