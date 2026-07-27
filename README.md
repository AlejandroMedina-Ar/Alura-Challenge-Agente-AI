# TechFlow Solutions - Agente RAG Corporativo

Asistente inteligente basado en Retrieval-Augmented Generation (RAG) para consultar documentos corporativos internos. Permite indexar documentos (PDF, TXT, MD), generar embeddings vectoriales y realizar consultas en lenguaje natural que el agente responde utilizando exclusivamente el contenido de los documentos de la empresa.

## 🆕 Actualizaciones Recientes (Julio 2026)

### Gemini 3.6 Flash
- ✅ Actualizado a **Gemini 3.6 Flash** (versión más reciente de Google)
- ✅ Modelos Gemini 1.5 deprecados y reemplazados
- ✅ Mejor rendimiento en tareas multimodales y de código
- ✅ Reducción de costos ($1.50/1M tokens de input vs $2.00 anterior)

### Sistema de Autenticación Mejorado
- ✅ **Acceso automático como Guest** cuando hay documentos
- ✅ Ya NO pide contraseña en cada acceso
- ✅ Usuarios comunes pueden usar el chat sin login
- ✅ Administradores pueden alternar entre vista admin y usuario
- ✅ Flujo de onboarding mejorado para primera configuración

### Embeddings Optimizados
- ✅ Migrado a **Sentence Transformers (multilingual-e5-base)**
- ✅ Embeddings locales (sin dependencia de APIs externas)
- ✅ 768 dimensiones (optimizado para velocidad)
- ✅ Soporte multilingüe mejorado

---

## Arquitectura

```
┌─────────────────────────────────────────────────────────────────────┐
│                     Interfaz Web (Streamlit)                        │
│                                                                     │
│  ┌──────────────┐  ┌──────────────┐  ┌───────────────────────────┐ │
│  │  Chat        │  │  Admin Panel │  │  Configuración            │ │
│  │  - Historial │  │  - Documentos│  │  - LLM Settings           │ │
│  │  - Input     │  │  - Indexación│  │  - RAG Parameters         │ │
│  │  - Export    │  │  - Métricas  │  │  - Tema (Dark/Light)      │ │
│  └──────┬───────┘  └──────┬───────┘  └───────┬───────────────────┘ │
│         │                 │                   │                     │
└─────────┼─────────────────┼───────────────────┼─────────────────────┘
          │                 │                   │
          ▼                 ▼                   ▼
┌─────────────────────────────────────────────────────────────────────┐
│                     Services Layer (Business Logic)                 │
│                                                                     │
│  ┌─────────────────┐  ┌──────────────────┐  ┌──────────────────┐  │
│  │  ChatService    │  │  IndexingService │  │  ConfigService   │  │
│  │  - RAG Pipeline │  │  - Chunking      │  │  - Settings      │  │
│  │  - LLM Provider │  │  - Embeddings    │  │  - Validation    │  │
│  │  - Fallback     │  │  - Vector Store  │  │  - Export/Import │  │
│  └────────┬────────┘  └────────┬─────────┘  └────────┬─────────┘  │
│           │                    │                      │            │
└───────────┼────────────────────┼──────────────────────┼────────────┘
            │                    │                      │
            ▼                    ▼                      ▼
┌─────────────────────────────────────────────────────────────────────┐
│                         Core Components                             │
│                                                                     │
│  ┌──────────────┐     ┌─────────────────┐     ┌─────────────────┐ │
│  │  LLM Layer   │     │  RAG Pipeline   │     │  Storage Layer  │ │
│  │              │     │                 │     │                 │ │
│  │  • Gemini    │────▶│  • Retriever    │────▶│  • Documents    │ │
│  │    3.6 Flash │     │  • Chunker      │     │  • Metadata     │ │
│  │              │     │  • Embeddings   │     │  • Config       │ │
│  │  • Cohere    │     │  • PromptBuilder│     │  • FileManager  │ │
│  │    Command-R │     │                 │     │                 │ │
│  │  (fallback)  │     └─────────┬───────┘     └─────────────────┘ │
│  └──────────────┘               │                                 │
│                                 ▼                                 │
│                    ┌──────────────────────────┐                   │
│                    │   ChromaDB (Vector DB)   │                   │
│                    │                          │                   │
│                    │  • Embeddings: E5-base   │                   │
│                    │    (multilingual, 768d)  │                   │
│                    │  • Similarity Search     │                   │
│                    │  • Metadata Filtering    │                   │
│                    └──────────────────────────┘                   │
└─────────────────────────────────────────────────────────────────────┘
```

### Flujo de una consulta (Query Flow)

1. **Usuario** escribe una pregunta en el chat.
2. **EmbeddingService** genera el embedding de la consulta usando Sentence Transformers (multilingual-e5-base).
3. **Retriever** busca los 5 fragmentos más relevantes en ChromaDB (configurable).
4. **PromptBuilder** construye el prompt RAG con los fragmentos como contexto.
5. **ChatService** invoca el LLM (Gemini 3.6 Flash primario, Cohere Command-R como fallback).
6. El LLM genera una respuesta basándose **exclusivamente** en el contexto recuperado.
7. La respuesta se muestra en el chat con las fuentes consultadas.

### Flujo de indexación (Indexing Flow)

1. **Admin** sube documentos (PDF, TXT, MD) desde el panel de administración.
2. **FileManager** guarda los archivos en `data/knowledge_library/documents/`.
3. **DocumentRepository** calcula checksums SHA-256 para detectar duplicados.
4. **TextChunker** fragmenta los documentos (chunk_size=1000, overlap=200).
5. **EmbeddingService** genera embeddings con Sentence Transformers (multilingual-e5-base).
6. **VectorStore** almacena chunks + embeddings + metadata en ChromaDB.
7. **MetadataRepository** guarda metadata JSON para cada documento.

---

## Estructura del proyecto

```
techflow-rag-agent/
├── .env                          # Variables de entorno (API keys)
├── .env.example                  # Template de configuración
├── requirements.txt              # Dependencias Python
├── setup.py                      # Script de configuración inicial
├── run.py                        # Inicializador rápido
├── test_integration.py           # Tests de integración
├── validate_imports.py           # Validador de imports pre-setup
│
├── data/                         # Datos persistentes (no versionado)
│   ├── chromadb/                 # Base de datos vectorial
│   ├── knowledge_library/
│   │   ├── documents/            # PDFs, TXTs, MDs originales
│   │   └── metadata/             # Metadatos JSON por documento
│   ├── logs/                     # Logs de aplicación
│   └── config.json               # Configuración runtime
│
├── src/
│   ├── app.py                    # Entry point Streamlit
│   │
│   ├── config/                   # Configuración centralizada
│   │   ├── settings.py           # Variables de entorno
│   │   ├── paths.py              # Rutas del sistema
│   │   └── constants.py          # Constantes de aplicación
│   │
│   ├── utils/                    # Utilidades generales
│   │   ├── logger.py             # Sistema de logging
│   │   ├── exceptions.py         # Excepciones custom
│   │   ├── validators.py         # Validaciones
│   │   └── helpers.py            # Funciones auxiliares
│   │
│   ├── storage/                  # Capa de persistencia
│   │   ├── file_manager.py       # Gestión de archivos
│   │   ├── document_repository.py
│   │   ├── metadata_repository.py
│   │   └── config_repository.py
│   │
│   ├── auth/                     # Autenticación
│   │   ├── authentication.py     # Login/logout
│   │   └── session.py            # Gestión de sesiones
│   │
│   ├── llm/                      # Proveedores LLM
│   │   ├── base_provider.py      # Clase base abstracta
│   │   ├── gemini_provider.py    # Google Gemini 1.5 Flash
│   │   └── cohere_provider.py    # Cohere Command-R (fallback)
│   │
│   ├── rag/                      # Pipeline RAG
│   │   ├── embedding_service.py  # Generación de embeddings
│   │   ├── vector_store.py       # ChromaDB wrapper
│   │   ├── chunker.py            # Text splitting
│   │   ├── retriever.py          # Búsqueda de similitud
│   │   ├── prompt_builder.py     # Construcción de prompts
│   │   └── pipeline.py           # Orquestador RAG
│   │
│   ├── services/                 # Lógica de negocio
│   │   ├── authentication_service.py
│   │   ├── configuration_service.py
│   │   ├── knowledge_library_service.py
│   │   ├── indexing_service.py
│   │   └── chat_service.py       # Servicio principal
│   │
│   └── ui/                       # Interfaz Streamlit
│       ├── theme.py              # Gestión de temas
│       ├── components.py         # Componentes reutilizables
│       ├── sidebar.py            # Navegación lateral
│       ├── chat.py               # Página de chat
│       ├── admin_panel.py        # Panel de administración
│       └── settings_panel.py     # Configuración
│
├── architecture/                 # Documentación de arquitectura
│   ├── Architecture.md
│   ├── Source-Code-Structure.md
│   └── Glossary.md
│
├── specs/                        # Especificaciones técnicas
│   ├── 000-project-overview.md
│   ├── 001-chat-interface.md
│   ├── 002-knowledge-base-management.md
│   ├── 003-authentication.md
│   ├── 004-rag-pipeline.md
│   ├── 005-configuration.md
│   └── 006-deployment.md
│
└── docs/                         # Documentación adicional
    ├── USER-GUIDE.md
    ├── TECHNICAL-DOCS.md
    ├── TROUBLESHOOTING.md
    ├── FAQ.md
    ├── DEPLOYMENT.md
    ├── SECURITY-NOTES.md
    └── ELIMINAR.md               # Archivos eliminables post-desarrollo
```

---

## Tecnologías

| Componente | Tecnología | Versión | Propósito |
|------------|-----------|---------|-----------|
| **Interfaz** | Streamlit | 1.47.1 | Framework web interactivo |
| **LLM Principal** | Google Gemini | 3.6 Flash | Generación de respuestas (última versión) |
| **LLM Fallback** | Cohere Command-R | command-r7b-12-2024 | Backup ante fallos de Gemini |
| **Embeddings** | Sentence Transformers | multilingual-e5-base | Embeddings multilingües (768 dim) |
| **Vector Store** | ChromaDB | 1.0.16 | Base de datos vectorial local |
| **Framework RAG** | LangChain | 0.3.27 | Orquestación del pipeline RAG |
| **Carga de PDFs** | PyMuPDF | 1.23+ | Extracción de texto de PDFs |
| **Text Splitting** | RecursiveCharacterTextSplitter | LangChain | Fragmentación inteligente |
| **Auth** | bcrypt | 5.0+ | Hash de contraseñas |
| **Config** | python-dotenv | 1.1.1 | Variables de entorno |
| **Lenguaje** | Python | 3.11+ | Lenguaje base del proyecto |

### Parámetros RAG configurables

| Parámetro | Valor por defecto | Descripción |
|-----------|-------------------|-------------|
| `chunk_size` | 1000 | Tamaño de cada fragmento de texto |
| `chunk_overlap` | 200 | Solapamiento entre fragmentos |
| `top_k` | 5 | Número de fragmentos recuperados |
| `temperature` | 0.7 | Temperatura del LLM (creatividad) |
| `embedding_dim` | 768 | Dimensión del embedding de E5-base |

---

## Instalación y Ejecución Local

### Requisitos

- Python 3.11 o superior
- Al menos una API key (Gemini **o** Cohere)
  - Gemini: gratuita en [Google AI Studio](https://makersuite.google.com/app/apikey)
  - Cohere: gratuita en [Cohere Dashboard](https://dashboard.cohere.com/api-keys)

### Pasos de instalación

```bash
# 1. Clonar el repositorio
git clone https://github.com/AlejandroMedina-Ar/Alura-Challenge-Agente-AI.git
cd Alura-Challenge-Agente-AI

# 2. Crear entorno virtual
python -m venv venv

# Activar entorno virtual
# En Windows:
venv\Scripts\activate
# En Linux/Mac:
source venv/bin/activate

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Configurar variables de entorno
# En Windows:
copy .env.example .env
# En Linux/Mac:
cp .env.example .env

# Editar .env con tu API key (mínimo requerido)
# GEMINI_API_KEY=tu-clave-aqui (Gemini 3.6 Flash)
# ADMIN_PASSWORD=tu-contraseña-admin
# 
# Opcional:
# COHERE_API_KEY=tu-clave-aqui (para fallback)
# GEMINI_MODEL=gemini-3.6-flash (default, no necesitas cambiarlo)

# 5. (Opcional) Validar imports antes de continuar
python validate_imports.py

# 6. Ejecutar configuración inicial
python setup.py

# 7. (Opcional) Ejecutar tests de integración
python test_integration.py

# 8. Iniciar la aplicación
python run.py
# o directamente:
streamlit run src/app.py
```

La aplicación se abre automáticamente en `http://localhost:8501`.

### Indexar documentos

**Primera vez (Setup inicial):**

1. Al abrir la aplicación por primera vez (sin documentos), el sistema te pedirá login de administrador.
2. Ingresa la contraseña configurada en `.env` (ADMIN_PASSWORD).
3. Navegar a **"Panel de Administración"** desde la barra lateral.
4. Subir documentos PDF, TXT o MD mediante el uploader.
5. Los documentos se indexan automáticamente.
6. Esperar a que finalice la indexación (se muestra progreso en tiempo real).

**Acceso posterior (con documentos):**

- **Como usuario común (Guest):** Al abrir la aplicación, entrarás automáticamente como invitado.
  - Puedes usar el chat y consultar la biblioteca.
  - **NO** puedes subir, eliminar o modificar documentos.
  - Para acceder como admin, click en **"🔐 Login como Admin"** en el sidebar.

- **Como administrador:** Después de hacer login:
  - Acceso completo a todas las funciones.
  - Puedes cambiar a vista de usuario con **"👥 Modo Usuario"** sin cerrar sesión.
  - Para cerrar sesión completamente, usa **"🚪 Cerrar Sesión"**.

---

## Ejemplos de Uso

El asistente puede responder preguntas sobre el contenido de los documentos corporativos indexados. A continuación, ejemplos basados en los **Manuales de TechFlow Solutions** (Manual de TI y Manual del Empleado):

### Preguntas sobre Soporte IT

| Pregunta | Área temática |
|----------|---------------|
| ¿Cómo solicito una notebook nueva en la empresa? | Equipamiento tecnológico |
| ¿Cuál es el horario de atención de la Mesa de Ayuda? | Soporte técnico |
| ¿Qué información debo incluir al abrir un ticket de soporte? | Procedimientos IT |
| ¿Cómo me conecto a la VPN corporativa? | Acceso remoto |
| ¿Qué hago si olvido mi contraseña corporativa? | Gestión de accesos |
| ¿Cómo configuro la autenticación multifactor (MFA)? | Seguridad informática |
| ¿Qué equipamiento tecnológico se asigna a los empleados? | Hardware corporativo |
| ¿Cuánto tiempo tarda en llegar un equipo solicitado? | Tiempos de entrega |

### Preguntas sobre Políticas de la Empresa

| Pregunta | Área temática |
|----------|---------------|
| ¿Cuál es la misión de TechFlow Solutions? | Cultura empresarial |
| ¿Qué áreas de negocio tiene la empresa? | Estructura organizacional |
| ¿Cuáles son los valores corporativos de TechFlow? | Valores empresariales |
| ¿Qué modalidad de trabajo aplica en la empresa? | Política laboral |
| ¿Cuánto dura el período de prueba para nuevos empleados? | Onboarding |
| ¿Cuál es el código de vestimenta de la empresa? | Normas internas |
| ¿Qué debo hacer si quiero renunciar? | Procedimientos administrativos |
| ¿Cómo es el proceso de onboarding para nuevos empleados? | Incorporación |

### Preguntas sobre Procedimientos Técnicos

| Pregunta | Área temática |
|----------|---------------|
| ¿Qué configuraciones de seguridad vienen en los equipos nuevos? | Seguridad |
| ¿Cómo se realiza la indexación de documentos en el sistema? | Procesos internos |
| ¿Qué software está autorizado para instalar en mi notebook? | Políticas de software |
| ¿Cómo reporto un incidente de seguridad informática? | Ciberseguridad |
| ¿Qué hacer si mi equipo se daña o es robado? | Gestión de incidentes |

---

## Ejemplos de Respuestas

### Pregunta: ¿Cómo solicito una notebook nueva en la empresa?

> Para solicitar una notebook nueva en TechFlow Solutions, debes seguir estos pasos:
>
> 1. Ingresar al Portal de Tickets.
> 2. Seleccionar la categoría **"Hardware / Equipamiento"**.
> 3. Elegir el tipo de solicitud (equipamiento nuevo, adicional o reemplazo).
> 4. Completar el formulario indicando el tipo de equipo y el motivo de la solicitud.
> 5. Si es equipamiento adicional, necesitarás la aprobación de tu responsable directo.
>
> El tiempo estimado de entrega es de 1 a 2 días hábiles si estás en oficina, o hasta 5 días hábiles si eres empleado remoto.
>
> **Fuentes:** Manual de TI y Soporte - Capítulo 4 (Solicitud de Equipamiento Tecnológico)

---

### Pregunta: ¿Cuál es la misión de TechFlow Solutions?

> La misión de TechFlow Solutions es:
>
> **"Ayudar a las organizaciones a acelerar su transformación digital mediante soluciones tecnológicas innovadoras."**
>
> Esto significa que cada proyecto y decisión interna está orientada a generar un impacto real en la digitalización de los clientes, a través de desarrollo de software, inteligencia artificial, migración a la nube o fortalecimiento de la seguridad informática.
>
> **Fuentes:** Manual del Empleado - Capítulo 3 (Misión, Visión y Valores)

---

### Pregunta: ¿Qué hago si olvido mi contraseña corporativa?

> Si olvidaste tu contraseña corporativa, debes:
>
> 1. Abrir un ticket en el Portal de Tickets (si aún tienes acceso).
> 2. Si no puedes acceder al Portal, contactar a la Mesa de Ayuda por Slack (#it-helpdesk) o llamar al Anexo 4100.
> 3. Categoría del ticket: **"Accesos y Contraseñas"**.
> 4. El soporte técnico restablecerá tu contraseña y te enviará una temporal por correo.
>
> El tiempo de primera respuesta para este tipo de solicitud es de hasta 2 horas hábiles.
>
> **Fuentes:** Manual de TI y Soporte - Capítulo 3 (Mesa de Ayuda)

---

### Pregunta: ¿Cuántas sedes tiene la empresa?

> No tengo esa información en los documentos disponibles.

*(El agente solo responde con información presente en los documentos indexados. No inventa ni utiliza conocimiento externo.)*

---

### Pregunta: Hola

> ¡Hola! Soy el asistente de documentos corporativos de TechFlow Solutions. Puedo ayudarte a consultar información de los manuales internos. ¿En qué puedo asistirte hoy?

*(El agente detecta saludos y responde de forma amigable sin consultar la base de datos.)*

---

## Despliegue en Streamlit Community Cloud

### Requisitos previos

- Cuenta en [Streamlit Community Cloud](https://share.streamlit.io)
- Repositorio público o privado en GitHub
- API keys configuradas

### Pasos

1. **Push del código a GitHub** (si aún no lo hiciste):
   ```bash
   git add .
   git commit -m "Preparar para deployment"
   git push origin main
   ```

2. **Conectar repositorio en Streamlit Cloud**:
   - Ir a [share.streamlit.io](https://share.streamlit.io)
   - Hacer clic en **"New app"**
   - Seleccionar el repositorio GitHub
   - Main file path: `src/app.py`
   - Python version: 3.11

3. **Configurar Secrets** (API keys):
   En el dashboard de Streamlit Cloud, ir a **"Settings" → "Secrets"** y agregar:
   ```toml
   GEMINI_API_KEY = "tu-clave-aqui"
   COHERE_API_KEY = "tu-clave-aqui"
   ADMIN_PASSWORD = "tu-password-aqui"
   ```

4. **Deploy automático**:
   - Streamlit Cloud detecta cambios automáticamente y redespliega
   - La app estará disponible en `https://tu-app.streamlit.app`

### Consideraciones

- **Almacenamiento persistente**: ChromaDB se reinicia con cada redeploy. Para producción, considerar una base vectorial externa (Pinecone, Weaviate, Qdrant).
- **Documentos pre-indexados**: Subir documentos después de cada deploy o implementar un sistema de persistencia externo.
- **Límites de Streamlit Cloud**: 1 GB de RAM, sin persistencia de archivos entre reinicios.

---

## Despliegue en VPS / Servidor Propio

### Requisitos

- VPS con Ubuntu 20.04+ (o similar)
- Python 3.11+
- Al menos 1 GB de RAM
- Puerto 8501 abierto en el firewall

### Instalación en servidor

```bash
# Actualizar sistema
sudo apt update && sudo apt upgrade -y

# Instalar Python y dependencias
sudo apt install -y python3 python3-pip python3-venv git

# Clonar repositorio
git clone https://github.com/AlejandroMedina-Ar/Alura-Challenge-Agente-AI.git
cd Alura-Challenge-Agente-AI

# Crear entorno virtual
python3 -m venv venv
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt

# Configurar variables de entorno
nano .env
# (Agregar API keys)

# Ejecutar setup
python setup.py

# Ejecutar aplicación
streamlit run src/app.py --server.port 8501 --server.address 0.0.0.0 --server.headless true
```

### Ejecutar como servicio systemd (opcional)

Crear archivo `/etc/systemd/system/techflow-rag.service`:

```ini
[Unit]
Description=TechFlow RAG Agent
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/Alura-Challenge-Agente-AI
Environment="PATH=/home/ubuntu/Alura-Challenge-Agente-AI/venv/bin"
ExecStart=/home/ubuntu/Alura-Challenge-Agente-AI/venv/bin/streamlit run src/app.py --server.port 8501 --server.address 0.0.0.0 --server.headless true
Restart=always

[Install]
WantedBy=multi-user.target
```

Activar servicio:
```bash
sudo systemctl daemon-reload
sudo systemctl enable techflow-rag
sudo systemctl start techflow-rag
sudo systemctl status techflow-rag
```

---

## Modos de Acceso

### 👥 Modo Guest (Usuario Común)

**Cuándo:** Al abrir la aplicación cuando hay documentos indexados (acceso automático)

**Permisos:**
- ✅ Usar el chat para consultar documentos
- ✅ Ver la biblioteca de conocimiento
- ✅ Ver configuración actual
- ✅ Cambiar tema (claro/oscuro)
- ❌ Subir o eliminar documentos
- ❌ Modificar configuración del sistema
- ❌ Acceder al Panel de Administración

**Interfaz:**
- Sidebar muestra: "👤 Usuario: Invitado"
- Botón "🔐 Login como Admin" disponible para escalar permisos

### 🔧 Modo Admin (Administrador)

**Cuándo:** Después de hacer login con la contraseña de admin

**Permisos:**
- ✅ Todas las funciones de Guest
- ✅ Subir y eliminar documentos
- ✅ Modificar configuración del sistema
- ✅ Acceder al Panel de Administración
- ✅ Ver métricas y estadísticas
- ✅ Cambiar a vista de usuario sin cerrar sesión

**Interfaz:**
- Sidebar muestra: "👤 Usuario: admin" y "🔑 Rol: Admin"
- Botón "👥 Modo Usuario" para cambiar a vista guest
- Botón "🚪 Cerrar Sesión" para logout completo

### 🔄 Flujo de Acceso

```
Primera vez (Sin documentos)
    ↓
Login Admin obligatorio
    ↓
Subir y indexar documentos
    ↓
Cerrar sesión o pestaña
    ↓
Siguiente visita: Acceso directo como Guest ✅
    ↓
Si necesitas admin: Click "Login como Admin"
```

---

## Características Principales

### 🔐 Autenticación Inteligente

- **Acceso automático como Guest:** Cuando hay documentos indexados, los usuarios pueden acceder directamente sin contraseña
- **Login Admin opcional:** Botón "Login como Admin" disponible en sidebar para acceder a funciones de gestión
- **Modo Vista de Usuario:** Los administradores pueden cambiar a vista de usuario sin cerrar sesión
- **Sistema de roles:** Control de acceso basado en roles (admin/guest)
- **Sesión persistente:** La sesión de admin se mantiene durante la navegación
- **Contraseñas hasheadas:** Seguridad con bcrypt para almacenamiento de credenciales

### 💬 Chat Inteligente

- Respuestas contextualizadas usando RAG
- Historial de conversación por sesión
- Exportación de chat completo
- Detección de saludos y mensajes fuera de contexto
- Indicación de fuentes consultadas

### 📚 Gestión de Documentos

- Upload de múltiples formatos (PDF, TXT, MD)
- Detección de duplicados por checksum SHA-256
- Vista de documentos indexados con metadata
- Eliminación de documentos con re-indexación
- Operaciones por lotes (indexar múltiples documentos)

### ⚙️ Configuración Avanzada

- Selección de proveedor LLM (Gemini/Cohere)
- Ajuste de parámetros RAG (chunk_size, top_k, temperature)
- Configuración de embeddings
- Tema claro/oscuro (Tokyo Night palette)
- Exportar/importar configuración

### 🔄 Sistema de Fallback

- Si Gemini falla → automáticamente usa Cohere
- Registro de cambios de proveedor en logs
- Cooldown de 5 minutos antes de reintentar proveedor principal
- Manejo de errores de rate limit y timeout

### 📊 Panel de Administración

- Dashboard con métricas en tiempo real
- Gestión completa de documentos
- Sistema de indexación con progreso visual
- Testing de proveedores LLM
- Estadísticas de uso

---

## Documentación Técnica

| Documento | Descripción |
|-----------|-------------|
| [Architecture.md](architecture/Architecture.md) | Arquitectura general del sistema |
| [Source-Code-Structure.md](architecture/Source-Code-Structure.md) | Estructura del código fuente |
| [Glossary.md](architecture/Glossary.md) | Glosario de términos técnicos |
| [USER-GUIDE.md](docs/USER-GUIDE.md) | Guía de usuario completa |
| [TECHNICAL-DOCS.md](docs/TECHNICAL-DOCS.md) | Documentación técnica detallada |
| [TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md) | Solución de problemas comunes |
| [HOTFIX-GEMINI-AUTH.md](docs/HOTFIX-GEMINI-AUTH.md) | Detalles técnicos de Gemini 3.6 y autenticación |
| [TEST-AUTH-FLOW.md](docs/TEST-AUTH-FLOW.md) | Guía de pruebas del flujo de autenticación |
| [FAQ.md](docs/FAQ.md) | Preguntas frecuentes |
| [DEPLOYMENT.md](docs/DEPLOYMENT.md) | Guía de despliegue |
| [SECURITY-NOTES.md](docs/SECURITY-NOTES.md) | Consideraciones de seguridad |

---

## Licencia

Este proyecto es privado y de uso interno para **TechFlow Solutions**.

---

## Créditos

**Proyecto:** Alura Challenge - Immersion AI + Google Gemini  
**Empresa:** TechFlow Solutions  
**Desarrollado por:** [Alejandro Medina](https://github.com/AlejandroMedina-Ar)

### Stack de tecnologías

- [Streamlit](https://streamlit.io) - Framework de interfaz web
- [LangChain](https://langchain.com) - Framework RAG
- [ChromaDB](https://www.trychroma.com) - Base de datos vectorial
- [Google Gemini](https://deepmind.google/technologies/gemini/) - LLM principal
- [Cohere](https://cohere.com) - Embeddings y LLM fallback
- [HuggingFace](https://huggingface.co) - Ecosistema de modelos

---

**⭐ TechFlow Solutions - Transformación Digital con Inteligencia Artificial**
