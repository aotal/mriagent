# src/tools/api_key_tools.py
# Herramientas conceptuales para bases de datos que requieren API Key (ej. Scopus, IEEE Xplore).
# Marcadas como 'PENDIENTES' para futuras implementaciones.

from crewai.tools import tool

class APIKeyTools:

    @tool
    def scopus_search(query: str) -> str:
        """
        (PENDIENTE) Realiza búsquedas en Scopus usando su API.
        Requiere una API Key de Scopus.
        """
        return "Esta herramienta está pendiente de implementación y requiere una API Key de Scopus."

    @tool
    def ieee_xplore_search(query: str) -> str:
        """
        (PENDIENTE) Realiza búsquedas en IEEE Xplore usando su API.
        Requiere una API Key de IEEE Xplore.
        """
        return "Esta herramienta está pendiente de implementación y requiere una API Key de IEEE Xplore."