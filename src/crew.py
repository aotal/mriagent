# src/crew.py
# Orchestration of the crew (agents, tasks, process) for the research system.

from crewai import Crew, Process
from .agents import (
    ResearchCoordinatorAgent,
    PubMedSearchAgent,
    ArXivSearchAgent,
    ContentFilteringAgent,
    MethodologyAnalysisAgent,
    PrioritizationAgent,
    BibTeXGeneratorAgent,
    SummaryGeneratorAgent,
    llm_config
)
from .tasks import ResearchTasks
from typing import List

class ResearchCrew:
    def __init__(self, research_topic: str, methodologies: List[str]):
        self.research_topic = research_topic
        self.methodologies = methodologies
        self.tasks_manager = ResearchTasks(research_topic, methodologies)

        # --- 1. Definir todos los AGENTES ---
        # Los definimos aquí para poder seleccionarlos fácilmente en el 'run'
        self.coordinator = ResearchCoordinatorAgent
        self.pubmed_searcher = PubMedSearchAgent
        self.arxiv_searcher = ArXivSearchAgent
        self.filterer = ContentFilteringAgent
        self.analyzer = MethodologyAnalysisAgent
        self.prioritizer = PrioritizationAgent
        self.bibtex_gen = BibTeXGeneratorAgent
        self.summary_gen = SummaryGeneratorAgent
        
        # --- 2. Definir todas las TAREAS ---
        # Definimos todas las tareas y sus dependencias (context)
        self.search_pubmed_task = self.tasks_manager.search_pubmed_task()
        self.search_arxiv_task = self.tasks_manager.search_arxiv_task()
        
        self.consolidate_and_filter_task = self.tasks_manager.consolidate_and_filter_task(
            context=[self.search_pubmed_task, self.search_arxiv_task]
        )
        
        self.analyze_methodology_task = self.tasks_manager.analyze_methodology_task(
            context=[self.consolidate_and_filter_task]
        )
        
        self.prioritize_and_label_task = self.tasks_manager.prioritize_and_label_task(
            context=[self.analyze_methodology_task]
        )
        
        self.generate_bibtex_task = self.tasks_manager.generate_bibtex_task(
            context=[self.prioritize_and_label_task]
        )
        self.generate_summary_task = self.tasks_manager.generate_summary_task(
             context=[self.prioritize_and_label_task]
        )

    def run(self):
        
        # ####################################################################
        # ## PRUEBAS PASO A PASO: Modifica estas dos listas ##
        # ####################################################################
        #
        # Instrucciones:
        # 1. Descomenta los AGENTES que quieres que participen.
        # 2. Descomenta las TAREAS que quieres ejecutar.
        # 3. ¡El 'self.coordinator' debe estar SIEMPRE en 'active_agents'!
        
        # --- AGENTES ACTIVOS ---
        active_agents = [
            self.coordinator,
            self.pubmed_searcher,
            #self.arxiv_searcher,
            # self.filterer,
            # self.analyzer,
            # self.prioritizer,
            self.bibtex_gen,
            self.summary_gen,
        ]
        
        # --- TAREAS ACTIVAS ---
        active_tasks = [
            self.search_pubmed_task,
            #self.search_arxiv_task,
            # self.consolidate_and_filter_task,
            # self.analyze_methodology_task,
            # self.prioritize_and_label_task,
            self.generate_bibtex_task,
            self.generate_summary_task,
        ]
        
        # ####################################################################


        # Instanciar el Crew con las listas activas
        crew = Crew(
            agents=active_agents,
            tasks=active_tasks,
            process=Process.hierarchical,
            manager_llm=llm_config, # El manager usa el LLM configurado
            verbose=True
        )

        result = crew.kickoff()
        return result