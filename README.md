# HelpDesk Actividad PRO

## Descripción

Este proyecto es un sistema de helpdesk inteligente para la aplicación móvil **Actividad PRO**, desarrollado por Profuturo. Utiliza técnicas de Retrieval-Augmented Generation (RAG) para proporcionar respuestas precisas y contextuales basadas en la documentación oficial de la aplicación. El sistema permite a los usuarios hacer preguntas sobre funcionalidades, flujos de trabajo, resolución de problemas y guías de uso de Actividad PRO.

## Características Principales

- **Chat Interactivo**: Interfaz de chat en tiempo real con streaming de respuestas.
- **Búsqueda Inteligente**: Utiliza embeddings y búsqueda vectorial para encontrar información relevante.
- **Procesamiento de Imágenes**: Soporte para OCR (Reconocimiento Óptico de Caracteres) en español para procesar capturas de pantalla o imágenes relacionadas con la app.
- **Base de Conocimiento**: Alimentado por documentos Markdown y Excel que contienen manuales, guías y documentación de Actividad PRO.
- **Arquitectura Modular**: Backend en Python con FastAPI y frontend en Next.js con React.

## Arquitectura del Sistema

### Backend (Python/FastAPI)
- **API Routes**: Endpoints para búsqueda y chat con streaming.
- **RAG Pipeline**: Pipeline completo que incluye retrieval, prompting y generación de respuestas.
- **Servicios**:
  - Embedding Service: Genera embeddings usando modelos de lenguaje.
  - Qdrant Service: Base de datos vectorial para almacenamiento y búsqueda de chunks.
  - Ollama Client: Cliente para modelos de lenguaje local (LLM).
- **Ingestion**: Scripts para procesar y cargar documentos Markdown y Excel al sistema.

### Frontend (Next.js/React)
- **Interfaz de Chat**: Componente principal para la conversación con el usuario.
- **Panel Lateral**: Navegación y contexto adicional.
- **Panel Derecho**: Muestra chunks relevantes y fuentes de información.
- **Header**: Barra superior con información del sistema.

### Base de Datos
- **Qdrant**: Base de datos vectorial para almacenar embeddings de documentos.
- **Documentos**: Archivos Markdown con manuales de Actividad PRO y datos en Excel.

## Tecnologías Utilizadas

### Backend
- **Python 3.x**
- **FastAPI**: Framework web para APIs REST.
- **Qdrant**: Base de datos vectorial.
- **Ollama**: Para modelos de lenguaje local.
- **EasyOCR**: Para reconocimiento óptico de caracteres en español.
- **Pandas**: Para procesamiento de archivos Excel.
- **LangChain** (probablemente): Para pipelines RAG.

### Frontend
- **Next.js 16**: Framework React.
- **React 19**: Biblioteca para interfaces de usuario.
- **TypeScript**: Tipado estático.
- **Tailwind CSS**: Framework de estilos.
- **ESLint**: Linting de código.

## Instalación y Configuración

### Prerrequisitos
- Python 3.8+
- Node.js 18+
- Ollama instalado y configurado con un modelo compatible (ej. llama2)
- Qdrant corriendo (local o remoto)

### Backend Setup
1. Navega al directorio `BackEnd`:
   ```bash
   cd BackEnd
   ```

2. Crea un entorno virtual:
   ```bash
   python -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   ```

3. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```

4. Configura Qdrant y Ollama según sea necesario.

5. Ejecuta el servidor:
   ```bash
   python main.py
   ```

### Frontend Setup
1. Navega al directorio `frontend/actividadpro`:
   ```bash
   cd frontend/actividadpro
   ```

2. Instala las dependencias:
   ```bash
   npm install
   ```

3. Ejecuta el servidor de desarrollo:
   ```bash
   npm run dev
   ```

### Ingestion de Datos
Para cargar los documentos al sistema:
1. Asegúrate de que Qdrant esté corriendo.
2. Ejecuta los scripts de ingestion en `BackEnd/ingestion/`:
   ```bash
   python ingestion/load_md.py
   python ingestion/load_excel.py
   python ingestion/ingest_to_qdrant.py
   ```

## Uso

1. Inicia el backend y frontend como se describe arriba.
2. Abre el navegador en `http://localhost:3000` (o el puerto configurado para Next.js).
3. En la interfaz de chat, escribe preguntas sobre Actividad PRO.
4. El sistema buscará información relevante en la base de conocimiento y generará respuestas usando el modelo de lenguaje.
5. Opcionalmente, sube imágenes para que el sistema extraiga texto usando OCR.

## Estructura del Proyecto

```
/
├── BackEnd/
│   ├── main.py                 # Punto de entrada del servidor FastAPI
│   ├── api/
│   │   └── routes.py           # Endpoints de la API
│   ├── data/
│   │   ├── excel/              # Archivos Excel con datos
│   │   └── md/                 # Archivos Markdown con manuales
│   ├── ingestion/              # Scripts para cargar datos
│   ├── models/                 # Esquemas de datos
│   ├── rag/                    # Pipeline RAG
│   └── services/               # Servicios (embedding, Qdrant, Ollama)
├── frontend/
│   └── actividadpro/           # Aplicación Next.js
│       ├── app/                # Páginas y layouts
│       ├── components/         # Componentes React
│       └── public/             # Archivos estáticos
├── a.json                      # Configuración adicional
├── a.py                        # Script auxiliar
└── README.md                   # Este archivo
```

## Contribución

Este proyecto está diseñado para funcionar de manera específica con la documentación de Actividad PRO. Para modificaciones o mejoras, asegúrate de mantener la compatibilidad con los formatos de datos existentes y las dependencias.

## Licencia

[Especifica la licencia si aplica]

## Contacto

Para soporte o preguntas sobre Actividad PRO, consulta la documentación oficial o contacta al equipo de desarrollo.