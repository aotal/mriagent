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
