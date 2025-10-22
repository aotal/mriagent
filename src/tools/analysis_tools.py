# src/tools/analysis_tools.py
# Herramientas auxiliares para el análisis de texto y extracción de información.

from crewai.tools import tool
import litellm  # Importar litellm
from dotenv import load_dotenv
import os
import json # Importar json

load_dotenv()

class AnalysisTools:

    @tool
    def analyze_abstract_for_keywords(abstract: str, keywords: list) -> dict:
        """
        Analiza un abstract para determinar la presencia de palabras clave específicas.
        Retorna un diccionario con las palabras clave encontradas y un booleano indicando si se encontraron.
        """
        found_keywords = [kw for kw in keywords if kw.lower() in abstract.lower()]
        return {
            "found_keywords": found_keywords,
            "has_keywords": bool(found_keywords)
        }

    @tool
    def classify_article_type(abstract: str) -> str:
        """
        Clasifica el tipo de artículo (original, review, systematic review, meta-analysis)
        basándose en el contenido del abstract. Utiliza un LLM para la clasificación.
        """
        
        prompt = f"""
        Clasifica el siguiente abstract en una de las siguientes categorías:
        - 'original_research'
        - 'review'
        - 'systematic_review'
        - 'meta_analysis'
        - 'other'

        Abstract:
        ---
        {abstract}
        ---

        Tu respuesta debe ser únicamente la categoría.
        """
        
        try:
            response = litellm.completion(
                model="gemini/gemini-2.5-flash-lite",
                messages=[{"role": "user", "content": prompt}],
                api_key=os.getenv("GOOGLE_API_KEY"),
                temperature=0.1
            )
            return response.choices[0].message.content.strip().lower()
        except Exception as e:
            print(f"Error al clasificar artículo: {e}") # Añadido para depuración
            return "other" # Default fallback

    @tool
    def extract_methodologies_and_data_availability(abstract: str) -> dict:
        """
        Extrae metodologías de Deep Learning (CNNs, U-Net, Transformers) y
        determina la disponibilidad de código o datasets públicos mencionados en el abstract.
        Utiliza un LLM para la extracción.
        """

        prompt = f"""
        Analiza el siguiente abstract y extrae la siguiente información:
        1.  **Metodologías de Deep Learning:** Identifica si se mencionan CNNs, U-Net, Transformers o Deep Learning en general. Lista todas las que encuentres.
        2.  **Disponibilidad de Código:** Indica 'True' si el abstract menciona explícitamente la disponibilidad de código fuente (ej. GitHub, repositorio público). De lo contrario, 'False'.
        3.  **Disponibilidad de Datasets:** Indica 'True' si el abstract menciona explícitamente la disponibilidad de datasets públicos (ej. ISLES challenge, repositorio de datos). De lo contrario, 'False'.

        Formato de salida (JSON):
        {{
            "metodologias": ["metodologia1", "metodologia2"],
            "codigo_disponible": true/false,
            "datasets_disponibles": true/false
        }}

        Abstract:
        ---
        {abstract}
        ---
        """
        
        try:
            response = litellm.completion(
                model="gemini/gemini-2.5-flash-lite",
                messages=[{"role": "user", "content": prompt}],
                api_key=os.getenv("GOOGLE_API_KEY"),
                temperature=0.1
            )
            # Intentar parsear la respuesta como JSON.
            return json.loads(response.choices[0].message.content.strip())
        except Exception as e:
            print(f"Error al extraer metodologías: {e}") # Añadido para depuración
            return {
                "metodologias": [],
                "codigo_disponible": False,
                "datasets_disponibles": False
            }