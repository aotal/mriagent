# src/crew.py
# Orquestación del crew (agentes, tareas, proceso) para el sistema de investigación.

from crewai import Crew, Process
from .agents import (
    AgenteCoordinadorDeBusqueda,
    AgenteBuscadorPubMed,
    AgenteBuscadorArXiv,
    AgenteFiltradorDeContenido,
    AgenteAnalistaMetodologico,
    AgentePriorizadorYEtiquetador,
    AgenteGeneradorBibTeX,
    AgenteGeneradorResumen,
    llm_config
)
from .tasks import ResearchTasks

class ResearchCrew:
    def __init__(self, research_topic: str):
        self.research_topic = research_topic
        self.tasks = ResearchTasks(research_topic)

    def run(self):
        # Definir las tareas
        buscar_pubmed_task = self.tasks.tarea_buscar_pubmed()
        buscar_arxiv_task = self.tasks.tarea_buscar_arxiv()
        
        # Las tareas de búsqueda se ejecutan en paralelo y sus resultados se consolidan
        # El contexto para la tarea de filtrado será el resultado de ambas búsquedas
        consolidar_y_filtrar_reviews_task = self.tasks.tarea_consolidar_y_filtrar_reviews(
            context=[buscar_pubmed_task, buscar_arxiv_task]
        )
        
        analizar_metodologia_y_disponibilidad_task = self.tasks.tarea_analizar_metodologia_y_disponibilidad(
            context=[consolidar_y_filtrar_reviews_task]
        )
        
        priorizar_y_etiquetar_task = self.tasks.tarea_priorizar_y_etiquetar(
            context=[analizar_metodologia_y_disponibilidad_task]
        )
        
        generar_bibtex_task = self.tasks.tarea_generar_bibtex(
            context=[priorizar_y_etiquetar_task]
        )
        generar_resumen_task = self.tasks.tarea_generar_resumen(
             context=[priorizar_y_etiquetar_task] # Usar el mismo contexto que BibTeX
        )

        # Instanciar el Crew con un proceso jerárquico
        crew = Crew(
            agents=[
                AgenteCoordinadorDeBusqueda,
                AgenteBuscadorPubMed,
                AgenteBuscadorArXiv,
                AgenteFiltradorDeContenido,
                AgenteAnalistaMetodologico,
                AgentePriorizadorYEtiquetador,
                AgenteGeneradorBibTeX,
                AgenteGeneradorResumen
            ],
            tasks=[
                buscar_pubmed_task,
                buscar_arxiv_task,
                consolidar_y_filtrar_reviews_task,
                analizar_metodologia_y_disponibilidad_task,
                priorizar_y_etiquetar_task,
                generar_bibtex_task
            ],
            process=Process.hierarchical,
            manager_llm=llm_config, # El manager usa el LLM configurado directamente
            verbose=True
        )

        result = crew.kickoff()
        return result