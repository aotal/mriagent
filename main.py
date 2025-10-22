# main.py
# Punto de entrada principal para ejecutar el crew.

from src.crew import ResearchCrew
from dotenv import load_dotenv
import os

load_dotenv() # Cargar variables de entorno

def main():
    print("Iniciando el sistema de investigación académica...")
    research_topic = "Segmentación automática de lesiones por ictus (stroke) en imágenes de Resonancia Magnética (MRI)"
    
    # Asegúrate de que la API Key de Google esté configurada
    if not os.getenv("GOOGLE_API_KEY"):
        print("Error: La variable de entorno 'GOOGLE_API_KEY' no está configurada.")
        print("Por favor, crea un archivo .env en la raíz del proyecto con GOOGLE_API_KEY=tu_api_key_aqui")
        return

    # Asegúrate de que el email para Entrez esté configurado
    if not os.getenv("ENTREZ_EMAIL"):
        print("Advertencia: La variable de entorno 'ENTREZ_EMAIL' no está configurada.")
        print("Se usará 'your.email@example.com' por defecto para PubMed. Se recomienda configurar un email real.")
        
    crew = ResearchCrew(research_topic)
    result = crew.run()
    print("\n################################################")
    print("## Proceso de investigación completado ##")
    print("################################################\n")
    print(result)

if __name__ == "__main__":
    main()