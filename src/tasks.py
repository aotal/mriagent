# src/tasks.py
# Definition of all tasks for the research system.

from crewai import Task
from .tools.pubmed_tools import PubMedTools
from .tools.arxiv_tools import ArxivTools
from .tools.bibtex_tools import BibtexTools
from .tools.analysis_tools import AnalysisTools
from .tools.summary_tools import SummaryTools
from .agents import (
    ResearchCoordinatorAgent,
    PubMedSearchAgent,
    ArXivSearchAgent,
    ContentFilteringAgent,
    MethodologyAnalysisAgent,
    PrioritizationAgent,
    BibTeXGeneratorAgent,
    SummaryGeneratorAgent
)
import re # For creating safe filenames

class ResearchTasks:

    def __init__(self, research_topic: str, methodologies: list[str]):
            self.research_topic = research_topic
            self.methodologies = methodologies
            
            slug = re.sub(r'[^a-z0-9_]+', '', self.research_topic.lower().replace(' ', '_'))
            slug = slug[:50]
            
            self.bib_filename = f"research_{slug}.bib"
            self.summary_filename = f"summary_{slug}.md"

    def search_pubmed_task(self):
        return Task(
            # MODIFICADO: Se elimina la restricción de excluir revisiones.
            description=f"Search PubMed for all potentially relevant articles on '{self.research_topic}'. The search must be exhaustive.",
            # MODIFICADO: El output esperado ahora incluye todo.
            expected_output="A list of dictionaries (ID, title, authors, year, URL, abstract) of all potentially relevant articles found, including originals and reviews.",
            agent=PubMedSearchAgent,
            tools=[PubMedTools.search_pubmed, PubMedTools.fetch_pubmed_details]
        )

    def search_arxiv_task(self):
        return Task(
            # MODIFICADO: Se elimina la restricción de excluir revisiones.
            description=f"Search arXiv for relevant preprints and articles on '{self.research_topic}'. Focus on the latest innovations.",
            # MODIFICADO: El output esperado ahora incluye todo.
            expected_output="A list of dictionaries (ID, title, authors, year, URL, abstract) of all potentially relevant preprints found, including originals and reviews.",
            agent=ArXivSearchAgent,
            tools=[ArxivTools.search_arxiv]
        )

    def consolidate_and_filter_task(self, context):
        # Esta tarea no cambia. Su descripción ya es correcta,
        # ahora es la ÚNICA responsable de filtrar reviews.
        return Task(
            description=f"Consolidate the results from PubMed and arXiv for the topic '{self.research_topic}'. "
                        "Strictly filter out articles that are 'review', 'systematic review', or 'meta-analysis' based on the title and abstract. "
                        "Only original contributions must be kept.",
            expected_output="A consolidated list of dictionaries of original and relevant articles.",
            agent=ContentFilteringAgent,
            context=context,
            tools=[AnalysisTools.classify_article_type]
        )

    def analyze_methodology_task(self, context):
        # Join the list of methodologies for the description
        method_list_str = ", ".join(self.methodologies)
        
        return Task(
            description=f"Analyze the abstracts of the filtered articles to identify the presence and relevance of specific methodologies (such as: {method_list_str}) "
                        f"and assess the availability of public code or datasets.",
            expected_output=f"The same list of article dictionaries, but each dictionary enriched with additional fields: `identified_methodologies` (list of strings from the list: {method_list_str}), `code_available` (boolean), `datasets_available` (boolean).",
            agent=MethodologyAnalysisAgent,
            context=context,
            tools=[AnalysisTools.extract_methodologies_and_data_availability]
        )

    def prioritize_and_label_task(self, context):
        return Task(
            description="Prioritize and label the articles based on their publication date (most recent first) and methodological relevance (presence of advanced methodologies).",
            expected_output="The COMPLETE list of article dictionaries (including all fields), sorted by priority and with the additional fields `priority` (string: 'High', 'Medium', 'Low') and `tags` (list of strings).",
            agent=PrioritizationAgent,
            context=context
        )

    def generate_bibtex_task(self, context):
        return Task(
            description=f"Generate a BibTeX entry for each prioritized article and consolidate them into a single file named '{self.bib_filename}'. "
                        f"Ensure the 'write_bibtex_file' tool is called with this filename.",
            expected_output=f"A confirmation message indicating that the '{self.bib_filename}' file has been successfully created.",
            agent=BibTeXGeneratorAgent,
            context=context,
            tools=[BibtexTools.generate_bibtex_entry, BibtexTools.write_bibtex_file]
        )
        
    def generate_summary_task(self, context):
        return Task(
            description=f"Analyze the final list of prioritized articles. Identify key trends (e.g., predominant methodologies, publication years, resource availability) and the 2-3 most relevant articles. "
                        f"Write an executive summary (2-3 paragraphs) and save it using the 'write_summary_file' tool with the filename '{self.summary_filename}'.",
            expected_output=f"A text string containing an executive summary, successfully saved as '{self.summary_filename}'.",
            agent=SummaryGeneratorAgent,
            context=context,
            tools=[SummaryTools.write_summary_file] 
        )