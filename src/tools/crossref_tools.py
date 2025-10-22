# src/tools/crossref_tools.py
# Herramienta para obtener BibTeX desde la API de Crossref usando DOI.

from crewai.tools import tool
import requests
import logging # Para logging de errores

class CrossrefTools:

    @tool
    def get_bibtex_from_doi(doi: str) -> str:
        """
        Obtiene la entrada BibTeX formateada para un artículo dado su DOI,
        utilizando la API de Crossref.
        Retorna la cadena BibTeX o un mensaje de error si no se encuentra o falla.
        Asegúrate de que el DOI proporcionado sea solo el identificador (ej: '10.1000/xyz123').
        """
        if not doi or doi == 'N/A' or not isinstance(doi, str):
            return "Error: DOI inválido o no proporcionado."

        try:
            # URL de la API de Crossref para obtener BibTeX
            url = f"https://api.crossref.org/works/{doi}/transform/application/x-bibtex"
            headers = {
                'Accept': 'application/x-bibtex' 
            }
            # Añadir un email para "polite pool" (buena práctica)
            params = {'mailto': 'tu_email_real@dominio.com'} # Reemplaza con tu email (el mismo de Entrez está bien)

            response = requests.get(url, headers=headers, params=params, timeout=10) # Timeout de 10 segundos
            response.raise_for_status() # Lanza excepción para errores HTTP (4xx, 5xx)

            bibtex_entry = response.text
            # A veces Crossref devuelve entradas vacías o casi vacías si faltan datos
            if not bibtex_entry or '@' not in bibtex_entry: 
                 return f"Error: Crossref devolvió una entrada BibTeX vacía o inválida para el DOI {doi}."

            return bibtex_entry

        except requests.exceptions.HTTPError as http_err:
            if response.status_code == 404:
                return f"Error: DOI '{doi}' no encontrado en Crossref."
            else:
                logging.error(f"Error HTTP al buscar DOI '{doi}' en Crossref: {http_err}")
                return f"Error HTTP al buscar DOI '{doi}' en Crossref: {response.status_code}"
        except requests.exceptions.RequestException as req_err:
            logging.error(f"Error de red al buscar DOI '{doi}' en Crossref: {req_err}")
            return f"Error de red al buscar DOI '{doi}' en Crossref."
        except Exception as e:
            logging.error(f"Error inesperado al procesar DOI '{doi}': {e}")
            return f"Error inesperado al procesar DOI '{doi}'."