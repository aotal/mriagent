Gemini
Conversación temporal

Nueva conversación
Gems

Storybook

A
ADKyFASTMCP

Descubrir Gems
Reciente
Instalación DCM4CHEE en Ubuntu
Conversación fijada
Diseñar API para PACS dcm4chee
Conversación fijada
Braquiterapia: Planificación con Esferas Osculatrices
Conversación fijada
Investigación sobre Esferas Osculatrices para Braquiterapia
Conversación fijada
Superficie y Envolvente Esférica Investigación
Conversación fijada
Diseño de Meta-Agente CrewAI Científico
Prompt para Prueba de Control de Calidad DX19
Prueba DX19: Umbral de Sensibilidad
Investigación de Segmentación de Lesiones Cerebrales
Preparación de Workstation para Trabajo Remoto
Guía KNX para Instalador Domótico
Setas para revuelto: Rebozuelos y Camagrocs
Creación de Favicon para FastAPI QA
Investigación: Arquitecturas de Agentes LLM
Investigación IA Multimodal: Espacio Embedding
Plan de Investigación: Fiabilidad y Anclaje
Corrección y Ampliación DX09-4 HVL
Instalación Ubuntu en Workstation Lenovo

Actividad

Configuración y ayuda
Lérida, España
Según tus sitios (trabajo)
Actualizar ubicación
Conversación con Gemini
Puedes corregirme el fichero para que en github se vea el esquema en mermaid?

¡Claro! La sintaxis que tienes en tu README.md para el diagrama de Mermaid es correcta.

GitHub renderiza automáticamente los bloques de código que están marcados con la etiqueta mermaid.

El bloque de código en tu archivo ya está formateado correctamente. Para que se vea en GitHub, no necesitas cambiar nada. Este es el bloque exacto de tu archivo, y es la forma correcta de hacerlo:

Markdown
## Esquema de Agentes y Flujo de Tareas

El sistema opera bajo un **proceso jerárquico** (`Process.hierarchical`), donde un agente coordinador gestiona el flujo de trabajo y delega tareas a un equipo de especialistas.

El flujo de trabajo es el siguiente:

```mermaid
graph TD
    A[AgenteCoordinadorDeBusqueda] -- Delega Tareas --> B(1. Buscar PubMed);
    A --> C(1. Buscar ArXiv);

    B -- Realizada por --> D{AgenteBuscadorPubMed};
    C -- Realizada por --> E{AgenteBuscadorArXiv};

    D -- Resultados --> F[Lista de Artículos PubMed];
    E -- Resultados --> G[Lista de Preprints ArXiv];

    A -- Delega Tarea 2 --> H(2. Consolidar y Filtrar Revisiones);
    F --> H;
    G --> H;
    H -- Realizada por --> I{AgenteFiltradorDeContenido};
    I -- Resultados --> J[Lista de Artículos Filtrados (Solo Originales)];

    A -- Delega Tarea 3 --> K(3. Analizar Metodología);
    J --> K;
    K -- Realizada por --> L{AgenteAnalistaMetodologico};
    L -- Resultados --> M[Artículos Enriquecidos (con metodologías y disponibilidad)];

    A -- Delega Tarea 4 --> N(4. Priorizar y Etiquetar);
    M --> N;
    N -- Realizada por --> O{AgentePriorizadorYEtiquetador};
    O -- Resultados --> P[Artículos Priorizados y Etiquetados];

    %% Tareas finales en paralelo o secuenciales según dependencia %%
    A -- Delega Tarea 5 --> Q(5. Generar BibTeX);
    P --> Q;
    Q -- Realizada por --> R{AgenteGeneradorBibTeX};
    R -- Resultados --> S[Archivo investigacion_stroke_mri.bib];

    A -- Delega Tarea 6 --> T(6. Generar Resumen);
    P --> T; %% Usa la misma entrada que BibTeX %%
    T -- Realizada por --> U{AgenteGeneradorResumen};
    U -- Resultados --> V[Archivo research_summary.md];


---

## ¿Por qué podría no estar viéndolo? 🤔

Si has subido este archivo a GitHub y *aún* no ves el diagrama renderizado, las razones más probables son:

1.  **Estás viendo el archivo "Raw" (Crudo):** Si haces clic en el botón "Raw" en GitHub, verás el texto plano del `README.md`, no la versión renderizada. Asegúrate de estar en la página principal de tu repositorio (la pestaña "Code").
2.  **Estás viendo el archivo en un editor local:** Si estás viendo el `README.md` en un editor de texto simple (como Notepad) o un editor de código (como VS Code) *sin* un plugin de previsualización de Markdown y Mermaid, solo verás el código.

**En resumen:** Tu código es correcto. Simplemente haz `git commit` y `git push` de tu `README.md` y GitHub lo mostrará perfectamente.



Gemini puede cometer errores, incluso sobre personas, así que verifica sus respuestas. Tu privacidad y GeminiSe abre en una ventana nueva

Archivos
Creado
Todavía no has creado nada
Añadido
Icono de MD
README
MD

# Agente de Investigación Académica sobre Ictus (Stroke) y MRI

Este proyecto implementa un equipo (Crew) de agentes de IA utilizando `crewAI` para automatizar un proceso completo de revisión de literatura científica. El objetivo es investigar el tema "Segmentación automática de lesiones por ictus (stroke) en imágenes de Resonancia Magnética (MRI)", asegurando que solo se consideren contribuciones originales, generando una bibliografía BibTeX de alta calidad y un resumen ejecutivo de los hallazgos.

## Características Principales

* **Búsqueda Multi-Fuente:** Realiza búsquedas en paralelo en **PubMed** y **arXiv** para una cobertura amplia.
* **Filtrado Estricto de Revisiones:** Utiliza un agente LLM para analizar y **descartar explícitamente artículos de revisión** (reviews, systematic reviews, meta-analysis) y quedarse solo con investigación original.
* **Análisis Metodológico:** Identifica automáticamente la presencia de metodologías clave de Deep Learning (CNNs, U-Net, Transformers) en los artículos.
* **Detección de Reproducibilidad:** Evalúa si los artículos mencionan la disponibilidad de **código fuente o datasets públicos**.
* **Priorización Inteligente:** Ordena los artículos relevantes basándose en la fecha de publicación y la relevancia metodológica.
* **Generación de Bibliografía:** Crea automáticamente un archivo `.bib` con todas las entradas BibTeX de los artículos seleccionados.
* **Resumen Ejecutivo:** Genera un resumen conciso de las tendencias y artículos clave encontrados durante la investigación.

## Esquema de Agentes y Flujo de Tareas

El sistema opera bajo un **proceso jerárquico** (`Process.hierarchical`), donde un agente coordinador gestiona el flujo de trabajo y delega tareas a un equipo de especialistas.

El flujo de trabajo es el siguiente:

```mermaid
graph TD
    A[AgenteCoordinadorDeBusqueda] -- Delega Tareas --> B(1. Buscar PubMed);
    A --> C(1. Buscar ArXiv);

    B -- Realizada por --> D{AgenteBuscadorPubMed};
    C -- Realizada por --> E{AgenteBuscadorArXiv};

    D -- Resultados --> F[Lista de Artículos PubMed];
    E -- Resultados --> G[Lista de Preprints ArXiv];

    A -- Delega Tarea 2 --> H(2. Consolidar y Filtrar Revisiones);
    F --> H;
    G --> H;
    H -- Realizada por --> I{AgenteFiltradorDeContenido};
    I -- Resultados --> J[Lista de Artículos Filtrados (Solo Originales)];

    A -- Delega Tarea 3 --> K(3. Analizar Metodología);
    J --> K;
    K -- Realizada por --> L{AgenteAnalistaMetodologico};
    L -- Resultados --> M[Artículos Enriquecidos (con metodologías y disponibilidad)];

    A -- Delega Tarea 4 --> N(4. Priorizar y Etiquetar);
    M --> N;
    N -- Realizada por --> O{AgentePriorizadorYEtiquetador};
    O -- Resultados --> P[Artículos Priorizados y Etiquetados];

    %% Tareas finales en paralelo o secuenciales según dependencia %%
    A -- Delega Tarea 5 --> Q(5. Generar BibTeX);
    P --> Q;
    Q -- Realizada por --> R{AgenteGeneradorBibTeX};
    R -- Resultados --> S[Archivo investigacion_stroke_mri.bib];

    A -- Delega Tarea 6 --> T(6. Generar Resumen);
    P --> T; %% Usa la misma entrada que BibTeX %%
    T -- Realizada por --> U{AgenteGeneradorResumen};
    U -- Resultados --> V[Archivo research_summary.md];

```

## Árbol de Directorios

La estructura del proyecto está organizada de la siguiente manera:

```
mriagent/
├── .venv/                   # Entorno virtual de Python
├── src/
│   ├── __pycache__/
│   ├── tools/
│   │   ├── __init__.py
│   │   ├── analysis_tools.py  # Herramientas de clasificación y extracción de metodologías
│   │   ├── api_key_tools.py   # Herramientas PENDIENTES (Scopus, IEEE)
│   │   ├── arxiv_tools.py     # Herramienta para buscar en ArXiv
│   │   ├── bibtex_tools.py    # Herramientas para generar BibTeX
│   │   ├── pubmed_tools.py    # Herramientas para buscar en PubMed
│   │   └── summary_tools.py   # Herramienta para escribir el resumen en archivo <-- NUEVO
│   ├── __init__.py
│   ├── agents.py              # Definición de los 8 agentes del crew <-- ACTUALIZADO
│   ├── crew.py                # Orquestación del Crew, agentes y tareas
│   └── tasks.py               # Definición de las 7 tareas <-- ACTUALIZADO
├── .env                       # (¡IMPORTANTE!) Contiene las API keys
├── main.py                    # Punto de entrada para ejecutar el crew
├── requirements.txt           # Dependencias del proyecto
├── investigacion_stroke_mri.bib # Archivo de salida generado
└── research_summary.md        # Archivo de resumen generado <-- NUEVO
```

## Proceso de Instalación

Sigue estos pasos para poner en marcha el proyecto:

1.  **Clonar el Repositorio**

    ```bash
    git clone <URL-DEL-REPOSITORIO>
    cd mriagent
    ```

2.  **Crear y Activar un Entorno Virtual**
    Se recomienda `uv` o `venv`:

      * Usando `uv` (Recomendado, más rápido):
        ```bash
        uv venv
        source .venv/bin/activate
        ```
      * Usando `venv` (Estándar de Python):
        ```bash
        python3 -m venv .venv
        source .venv/bin/activate
        ```

3.  **Instalar Dependencias**
    Asegúrate de que tu archivo `requirements.txt` contenga lo siguiente:

    ```txt
    # requirements.txt
    crewai
    # crewai-tools (ya no es necesario, viene con crewai)
    litellm
    python-dotenv
    biopython
    arxiv
    requests # Necesario para herramientas futuras o dependencias internas
    ```

    Luego, instálalo:

    ```bash
    uv pip install -r requirements.txt
    # o si usas venv:
    # pip install -r requirements.txt
    ```

4.  **Configurar Variables de Entorno**
    Crea un archivo `.env` en la raíz del proyecto. Este paso es **crucial**.

    ```ini
    # .env
    GOOGLE_API_KEY=tu_api_key_de_google_ai_studio_para_gemini
    ENTREZ_EMAIL=tu_email_real@dominio.com
    ```

      * `GOOGLE_API_KEY`: Es necesaria para que el LLM Gemini funcione (usado por todos los agentes y herramientas de análisis).
      * `ENTREZ_EMAIL`: Es un requisito de la API de PubMed (Entrez).

## Modo de Uso

1.  **Revisar el Punto de Entrada (`main.py`)**
    Asegúrate de que tu archivo `main.py` importe y ejecute el `ResearchCrew`. El ejemplo proporcionado anteriormente sigue siendo válido.

    ```python
    # main.py
    from src.crew import ResearchCrew
    import os

    def main():
        print("Iniciando el sistema de investigación académica...")

        topic = "Segmentación automática de lesiones por ictus (stroke) en imágenes de Resonancia Magnética (MRI)"

        if not os.getenv("GOOGLE_API_KEY") or not os.getenv("ENTREZ_EMAIL"):
            print("Error: GOOGLE_API_KEY o ENTREZ_EMAIL no están configuradas en el archivo .env")
            return

        crew = ResearchCrew(topic)
        result = crew.run()

        print("\n################################################")
        print("## Proceso de investigación completado ##")
        print("################################################\n")

        # El resultado final del crew ahora podría ser el resumen o una confirmación múltiple
        print("Resultado final del Crew:")
        print(result)

        print(f"\nSe ha generado el archivo 'investigacion_stroke_mri.bib' con las referencias.")
        print(f"Se ha generado el archivo 'research_summary.md' con el resumen ejecutivo.")

    if __name__ == "__main__":
        main()
    ```

2.  **Ejecutar el Crew**
    Con tu entorno virtual activado (`source .venv/bin/activate`), ejecuta:

    ```bash
    uv run python main.py
    # o si usas venv:
    # python main.py
    ```

3.  **Verificar los Resultados**
    El proceso puede tardar varios minutos. Al finalizar, verás la salida en la consola y deberías encontrar dos nuevos archivos en la raíz del proyecto:

      * `investigacion_stroke_mri.bib`: Contiene las entradas BibTeX de los artículos relevantes.
      * `research_summary.md`: Contiene el resumen ejecutivo de la investigación.

## Detalle de Agentes

El equipo está compuesto ahora por **8 agentes especializados**:

1.  **AgenteCoordinadorDeBusqueda** (Manager): Orquesta el proceso.
2.  **AgenteBuscadorPubMed**: Busca en PubMed.
3.  **AgenteBuscadorArXiv**: Busca en arXiv.
4.  **AgenteFiltradorDeContenido**: Filtra revisiones.
5.  **AgenteAnalistaMetodologico**: Analiza metodologías y disponibilidad.
6.  **AgentePriorizadorYEtiquetador**: Prioriza y etiqueta artículos.
7.  **AgenteGeneradorBibTeX**: Genera el archivo `.bib`.
8.  **AgenteGeneradorResumen** (**NUEVO**): Genera el resumen ejecutivo.

## Futuras Mejoras

  * **Implementar Herramientas Pendientes:** Activar las herramientas `scopus_search` y `ieee_xplore_search`.
  * **Entrada de Tema Dinámica:** Aceptar el tema de investigación como argumento.
  * **Persistencia de Resultados:** Guardar resultados intermedios (ej. JSON).
  * **Integración Crossref:** Utilizar DOIs y la API de Crossref para obtener datos BibTeX más fiables (como discutimos).
  * **Mejora del Resumen:** Permitir configurar la longitud o el enfoque del resumen generado.
