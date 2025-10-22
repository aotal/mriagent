# src/tools/summary_tools.py
# Herramientas para manejar la escritura de resúmenes.

from crewai.tools import tool
import os # Importar os para manejar rutas si es necesario

class SummaryTools:

    @tool
    def write_summary_file(summary_text: str, filename: str = "research_summary.md") -> str:
        """
        Escribe un texto de resumen (summary_text) en un archivo especificado (filename).
        Por defecto, guarda el resumen en 'research_summary.md'.
        Retorna un mensaje de confirmación o de error.
        """
        try:
            # Puedes ajustar la ruta si quieres guardarlo en un directorio específico
            # filepath = os.path.join("output_directory", filename)
            filepath = filename 

            with open(filepath, "w", encoding="utf-8") as f:
                f.write(summary_text)
            
            return f"Resumen guardado exitosamente en el archivo '{filepath}'."
        except Exception as e:
            return f"Error al escribir el archivo de resumen '{filepath}': {e}"