# TechFlow Solutions - Agente RAG Corporativo

Asistente inteligente basado en Retrieval-Augmented Generation (RAG) para consultar documentos corporativos internos. Permite indexar documentos (PDF, TXT, MD, DOCX), generar embeddings vectoriales y realizar consultas en lenguaje natural que el agente responde utilizando exclusivamente el contenido de los documentos de la empresa.

---

## 📋 Características Principales

### 🔐 Acceso Inteligente
- **Modo Guest automático:** Acceso directo al chat cuando hay documentos indexados
- **Modo Admin:** Gestión completa de documentos y configuración
- **Login flexible:** Cambio entre modos sin cerrar sesión
- **Seguridad:** Contraseñas hasheadas con bcrypt

### 💬 Chat con RAG
- Respuestas contextualizadas desde tus documentos
- Historial de conversación persistente
- Indicación de fuentes consultadas
- Detección inteligente de saludos y consultas fuera de contexto

### 📚 Gestión de Documentos
- Soporte multi-formato: PDF, TXT, MD, DOCX
- Detección de duplicados por checksum SHA-256
- Indexación automática al subir
- Operaciones por lotes (indexar múltiples documentos)
- Re-indexación selectiva

### ⚙️ Configuración Flexible
- Dual LLM: Gemini 3.6 Flash + Cohere Command-R
- Parámetros RAG ajustables (chunk_size, top_k, temperature)
- Tema claro/oscuro
- Exportar/importar configuración

### 🔄 Sistema de Fallback
- Cambio automático a Cohere si Gemini falla
- Cooldown inteligente de 5 minutos
- Manejo de rate limits y timeouts

---

## 🚀 Instalación Local

### Requisitos

- **Python 3.11+**
- **API Key de Gemini** (gratuita en [Google AI Studio](https://makersuite.google.com/app/apikey))
- **API Key de Cohere** (opcional, gratuita en [Cohere Dashboard](https://dashboard.cohere.com/api-keys))

### Paso a Paso

```bash
# 1. Clonar el repositorio
git clone https://github.com/AlejandroMedina-Ar/Alura-Challenge-Agente-AI.git
cd Alura-Challenge-Agente-AI

# 2. Crear entorno virtual
python -m venv venv

# 3. Activar entorno virtual
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# 4. Instalar dependencias
pip install -r requirements.txt

# 5. Configurar variables de entorno
# Windows:
copy .env.example .env
# Linux/Mac:
cp .env.example .env

# 6. Editar .env con tus API keys
# GEMINI_API_KEY=tu-api-key-aqui
# ADMIN_PASSWORD=tu-password-segura

# 7. Ejecutar configuración inicial
python setup.py

# 8. (Opcional) Tests de integración
python test_integration.py

# 9. Iniciar aplicación
python run.py
```

La aplicación se abrirá automáticamente en `http://localhost:8501`

### ⚡ Primera Configuración

**Al abrir por primera vez:**
1. El sistema pedirá login de administrador (no hay documentos)
2. Ingresa la contraseña de `.env` (ADMIN_PASSWORD)
3. Ve a **"Panel de Administración"** → **"Documentos"**
4. Sube documentos PDF, TXT, MD o DOCX
5. Espera a que se indexen automáticamente

**Accesos posteriores:**
- El sistema abrirá directamente en **Modo Guest** (acceso al chat)
- Para gestionar documentos, usa **"🔐 Login como Admin"** en el sidebar

---

## ☁️ Despliegue en Fly.io

### ¿Por qué Fly.io?

Fly.io es la plataforma recomendada para desplegar TechFlow RAG Agent porque ofrece:
- ✅ **Persistencia de datos** con volúmenes
- ✅ **Free tier generoso** (3GB volumen + 256MB RAM incluidos)
- ✅ **Despliegue global** en múltiples regiones
- ✅ **HTTPS automático** con certificados SSL
- ✅ **Health checks y auto-scaling**
- ✅ **CLI potente** para gestión

### Requisitos Previos

1. **Cuenta en Fly.io**
   - Regístrate en [fly.io](https://fly.io/app/sign-up)
   - Free tier incluye: 3 VMs compartidas, 3GB volumen persistente
   - Se requiere tarjeta de crédito (no se cobra en free tier)

2. **Instalar flyctl (CLI de Fly.io)**
   
   ```bash
   # Windows (PowerShell)
   iwr https://fly.io/install.ps1 -useb | iex
   
   # macOS/Linux
   curl -L https://fly.io/install.sh | sh
   
   # Verificar instalación
   flyctl version
   ```

3. **Autenticarse**
   
   ```bash
   flyctl auth login
   ```

### Pasos para Desplegar

#### 1. Preparar el Proyecto

El proyecto ya incluye los archivos necesarios:
- ✅ `fly.toml` - Configuración de Fly.io
- ✅ `Dockerfile` - Imagen Docker optimizada
- ✅ `.dockerignore` - Exclusiones para build

#### 2. Crear la Aplicación en Fly.io

```bash
# Navegar al directorio del proyecto
cd techflow-rag-agent

# Lanzar la aplicación (usa fly.toml existente)
flyctl launch --no-deploy

# Esto creará la app pero NO la desplegará aún
# Responde las preguntas:
# - Use existing fly.toml? YES
# - Would you like to set up a PostgreSQL database? NO
# - Would you like to set up an Upstash Redis database? NO
```

#### 3. Crear Volumen Persistente

```bash
# Crear volumen de 3GB para datos (incluido en free tier)
flyctl volumes create techflow_data --size 3 --region mia

# Verificar que se creó
flyctl volumes list
```

#### 4. Configurar Secrets (Variables de Entorno)

```bash
# Configurar API keys y contraseña de admin
flyctl secrets set GEMINI_API_KEY="tu-api-key-de-gemini"
flyctl secrets set COHERE_API_KEY="tu-api-key-de-cohere"
flyctl secrets set ADMIN_PASSWORD="tu-password-segura"

# Opcional: Configurar modelos específicos
flyctl secrets set GEMINI_MODEL="gemini-3.6-flash"
flyctl secrets set COHERE_MODEL="command-r7b-12-2024"

# Ver secrets configurados (valores ocultos)
flyctl secrets list
```

#### 5. Desplegar la Aplicación

```bash
# Primera vez (puede tomar 5-10 minutos)
flyctl deploy

# La aplicación se construirá y desplegará automáticamente
```

#### 6. Verificar el Despliegue

```bash
# Abrir la aplicación en el navegador
flyctl open

# Ver logs en tiempo real
flyctl logs

# Ver estado de la aplicación
flyctl status

# Ver información de la máquina
flyctl machine list
```

Tu aplicación estará disponible en: `https://techflow-rag-agent.fly.dev`

### Actualizaciones y Mantenimiento

#### Actualizar la Aplicación

```bash
# Después de hacer cambios en el código
git add .
git commit -m "Descripción de cambios"

# Re-desplegar
flyctl deploy

# Fly.io reconstruirá y desplegará automáticamente
```

#### Ver Logs

```bash
# Logs en tiempo real
flyctl logs

# Últimas 100 líneas
flyctl logs --lines 100

# Filtrar por nivel
flyctl logs --level error
```

#### Gestionar Secrets

```bash
# Actualizar un secret
flyctl secrets set ADMIN_PASSWORD="nueva-password"

# Eliminar un secret
flyctl secrets unset NOMBRE_SECRET

# Listar secrets
flyctl secrets list
```

#### Escalar Recursos

```bash
# Cambiar tamaño de VM (si necesitas más recursos)
flyctl scale vm shared-cpu-2x --memory 1024

# Ver configuración actual
flyctl scale show
```

#### Gestionar Volumen

```bash
# Ver volúmenes
flyctl volumes list

# Crear snapshot (backup)
flyctl volumes snapshots create techflow_data

# Listar snapshots
flyctl volumes snapshots list
```

### Monitoreo y Debugging

```bash
# Ver métricas
flyctl dashboard

# SSH a la máquina (para debugging avanzado)
flyctl ssh console

# Ver estado de health checks
flyctl checks list

# Reiniciar la aplicación
flyctl apps restart techflow-rag-agent
```

### Consideraciones Importantes

#### ✅ Ventajas de Fly.io

- **Persistencia:** Los datos se mantienen entre despliegues (volumen persistente)
- **Escalabilidad:** Fácil aumentar recursos cuando lo necesites
- **Global:** Despliega en la región más cercana a tus usuarios
- **HTTPS:** Certificados SSL automáticos
- **CLI:** Herramientas poderosas para gestión

#### ⚠️ Limitaciones del Free Tier

- **3 VMs compartidas:** Suficiente para proyectos pequeños/medianos
- **256MB RAM por VM:** Puede ser limitado para muchos documentos
- **Solución:** Upgrade a máquinas más grandes ($5-10/mes)

#### 💰 Costos Estimados

- **Free Tier:** $0/mes
  - 3 VMs compartidas (shared-cpu-1x)
  - 3GB volumen persistente
  - 160GB tráfico de salida/mes
  
- **Producción Básica:** ~$5-10/mes
  - shared-cpu-2x con 512MB-1GB RAM
  - 3GB volumen
  - Suficiente para 10-50 usuarios concurrentes

- **Producción Media:** ~$15-25/mes
  - dedicated-cpu-1x con 2GB RAM
  - 10GB volumen
  - Para 50-200 usuarios concurrentes

### Troubleshooting

#### La aplicación no inicia

```bash
# Ver logs detallados
flyctl logs

# Verificar configuración
flyctl config display

# Verificar health checks
flyctl checks list
```

#### Sin memoria

```bash
# Aumentar RAM
flyctl scale vm shared-cpu-2x --memory 512

# O cambiar a máquina más grande
flyctl scale vm shared-cpu-4x --memory 1024
```

#### Problemas con volumen

```bash
# Verificar que el volumen existe
flyctl volumes list

# Si no existe, crear
flyctl volumes create techflow_data --size 3 --region mia
```

#### Secrets no se cargan

```bash
# Verificar secrets
flyctl secrets list

# Re-configurar si es necesario
flyctl secrets set GEMINI_API_KEY="tu-key"
```

### Eliminar la Aplicación

```bash
# CUIDADO: Esto eliminará la app y todos los datos
flyctl apps destroy techflow-rag-agent

# Confirmar cuando se solicite
```

---

## 🖥️ Despliegue Alternativo en VPS/Cloud

**Nota:** Fly.io es la opción recomendada. Usa VPS solo si necesitas control total del servidor.

### Instalación en Servidor

```bash
# Actualizar sistema
sudo apt update && sudo apt upgrade -y

# Instalar dependencias
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

# Iniciar aplicación
streamlit run src/app.py --server.port 8501 --server.address 0.0.0.0 --server.headless true
```

### Servicio Systemd (Opcional)

Crear `/etc/systemd/system/techflow-rag.service`:

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

Activar:
```bash
sudo systemctl daemon-reload
sudo systemctl enable techflow-rag
sudo systemctl start techflow-rag
sudo systemctl status techflow-rag
```

---

## 🏗️ Arquitectura del Sistema

### Flujo de una Consulta (Query Flow)

```
Usuario → Chat
    ↓
EmbeddingService (multilingual-e5-base)
    ↓
ChromaDB (búsqueda por similitud)
    ↓
Retriever (top 5 fragmentos)
    ↓
PromptBuilder (construcción de contexto)
    ↓
LLM (Gemini 3.6 Flash → Cohere fallback)
    ↓
Respuesta + Fuentes
```

### Flujo de Indexación

```
Admin → Upload documento
    ↓
FileManager (guardar en data/knowledge_library/)
    ↓
DocumentRepository (checksum SHA-256)
    ↓
TextChunker (chunk_size=1000, overlap=200)
    ↓
EmbeddingService (768 dimensiones)
    ↓
ChromaDB (almacenar chunks + embeddings)
    ↓
MetadataRepository (metadata JSON)
```

### Diagrama de Componentes

```
┌──────────────────────────────────────────────────────┐
│           Interfaz Web (Streamlit)                    │
│  ┌─────────┐  ┌─────────┐  ┌──────────────────────┐ │
│  │  Chat   │  │  Admin  │  │  Configuración       │ │
│  └────┬────┘  └────┬────┘  └─────────┬────────────┘ │
└───────┼────────────┼──────────────────┼──────────────┘
        │            │                  │
┌───────┼────────────┼──────────────────┼──────────────┐
│       ▼            ▼                  ▼              │
│  ChatService  IndexingService  ConfigService        │
└───────┼────────────┼──────────────────┼──────────────┘
        │            │                  │
┌───────┼────────────┼──────────────────┼──────────────┐
│       ▼            ▼                  ▼              │
│  LLM Layer    RAG Pipeline    Storage Layer         │
│  • Gemini     • Retriever     • Documents           │
│  • Cohere     • Chunker       • Metadata            │
│               • Embeddings    • Config              │
└───────┼────────────┼──────────────────┼──────────────┘
        │            ▼                  │
        │    ┌──────────────┐           │
        └───▶│  ChromaDB    │◀──────────┘
             └──────────────┘
```

Para más detalles, ver [Architecture.md](architecture/Architecture.md)

---

## 📂 Estructura del Proyecto

```
techflow-rag-agent/
├── src/
│   ├── app.py                  # Entry point Streamlit
│   ├── config/                 # Configuración
│   ├── utils/                  # Utilidades
│   ├── storage/                # Persistencia
│   ├── auth/                   # Autenticación
│   ├── llm/                    # Proveedores LLM
│   ├── rag/                    # Pipeline RAG
│   ├── services/               # Lógica de negocio
│   └── ui/                     # Interfaz Streamlit
├── data/
│   ├── chromadb/               # Vector store
│   ├── knowledge_library/      # Documentos
│   ├── logs/                   # Logs
│   └── config.json             # Config runtime
├── architecture/               # Docs arquitectura
├── specs/                      # Especificaciones
├── docs/                       # Documentación
├── .env                        # Variables entorno
├── requirements.txt            # Dependencias
├── setup.py                    # Setup inicial
├── run.py                      # Inicializador
└── test_integration.py         # Tests
```

Ver [Source-Code-Structure.md](architecture/Source-Code-Structure.md) para detalles completos.

---

## 🛠️ Tecnologías

| Componente | Tecnología | Versión | Propósito |
|------------|-----------|---------|-----------|
| **Framework Web** | Streamlit | 1.47.1 | Interfaz interactiva |
| **LLM Principal** | Google Gemini | 3.6 Flash | Generación de respuestas |
| **LLM Fallback** | Cohere Command-R | command-r7b-12-2024 | Backup |
| **Embeddings** | Sentence Transformers | multilingual-e5-base | Embeddings (768d) |
| **Vector Store** | ChromaDB | 1.0.16 | Base de datos vectorial |
| **Framework RAG** | LangChain | 0.3.27 | Orquestación RAG |
| **PDF Parser** | PyMuPDF | 1.23+ | Extracción de texto |
| **Auth** | bcrypt | 5.0+ | Hash de contraseñas |
| **Lenguaje** | Python | 3.11+ | Base del proyecto |

---

## 👥 Modos de Acceso

### Modo Guest (Usuario Común)

**Acceso:** Automático cuando hay documentos indexados

**Permisos:**
- ✅ Usar chat para consultar documentos
- ✅ Ver biblioteca de conocimiento
- ✅ Ver configuración (read-only)
- ✅ Cambiar tema (claro/oscuro)
- ❌ Subir o eliminar documentos
- ❌ Modificar configuración
- ❌ Acceder a Panel de Administración

**Interfaz:**
- Sidebar: "👤 Usuario: Invitado"
- Botón: "🔐 Login como Admin" disponible

### Modo Admin (Administrador)

**Acceso:** Login con contraseña de admin

**Permisos:**
- ✅ Todas las funciones de Guest
- ✅ Gestión completa de documentos
- ✅ Modificar configuración del sistema
- ✅ Panel de Administración completo
- ✅ Métricas y estadísticas
- ✅ Cambiar a vista Guest sin cerrar sesión

**Interfaz:**
- Sidebar: "👤 Usuario: admin" + "🔑 Rol: Admin"
- Botones: "👥 Modo Usuario" y "🚪 Cerrar Sesión"

---

## 💡 Ejemplos de Uso

### Preguntas Técnicas
- ¿Cómo solicito una notebook nueva en la empresa?
- ¿Cuál es el horario de atención de la Mesa de Ayuda?
- ¿Cómo me conecto a la VPN corporativa?
- ¿Qué hago si olvido mi contraseña corporativa?

### Preguntas Corporativas
- ¿Cuál es la misión de TechFlow Solutions?
- ¿Qué modalidad de trabajo aplica en la empresa?
- ¿Cuál es el código de vestimenta?
- ¿Cómo es el proceso de onboarding?

### Ejemplo de Respuesta

**Pregunta:** ¿Cómo solicito una notebook nueva?

**Respuesta:**
> Para solicitar una notebook nueva en TechFlow Solutions:
>
> 1. Ingresa al Portal de Tickets
> 2. Categoría: "Hardware / Equipamiento"
> 3. Completa el formulario indicando el motivo
> 4. Si es equipamiento adicional, necesitas aprobación de tu responsable
>
> **Tiempo de entrega:** 1-2 días hábiles en oficina, hasta 5 días para remotos
>
> **Fuente:** Manual de TI - Capítulo 4

---

## 🔧 Configuración Avanzada

### Parámetros RAG

| Parámetro | Default | Descripción |
|-----------|---------|-------------|
| `chunk_size` | 1000 | Tamaño de cada fragmento |
| `chunk_overlap` | 200 | Solapamiento entre fragmentos |
| `top_k` | 5 | Fragmentos recuperados |
| `temperature` | 0.7 | Creatividad del LLM |
| `embedding_dim` | 768 | Dimensión del embedding |

### Variables de Entorno (.env)

```bash
# LLM API Keys
GEMINI_API_KEY=tu-gemini-api-key
COHERE_API_KEY=tu-cohere-api-key

# Modelos (configuración por defecto)
GEMINI_MODEL=gemini-3.6-flash
COHERE_MODEL=command-r7b-12-2024

# Autenticación
ADMIN_PASSWORD=tu-password-segura

# RAG Parameters (opcional)
CHUNK_SIZE=1000
CHUNK_OVERLAP=200
TOP_K=5
TEMPERATURE=0.7

# Embeddings
EMBEDDING_MODEL=intfloat/multilingual-e5-base
```

---

## 📚 Documentación Adicional

| Documento | Descripción |
|-----------|-------------|
| [Architecture.md](architecture/Architecture.md) | Arquitectura general del sistema |
| [Source-Code-Structure.md](architecture/Source-Code-Structure.md) | Estructura del código fuente |
| [USER-GUIDE.md](docs/USER-GUIDE.md) | Guía de usuario completa |
| [TECHNICAL-DOCS.md](docs/TECHNICAL-DOCS.md) | Documentación técnica detallada |
| [TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md) | Solución de problemas |
| [FAQ.md](docs/FAQ.md) | Preguntas frecuentes |
| [DEPLOYMENT.md](docs/DEPLOYMENT.md) | Guía de despliegue |
| [SECURITY-NOTES.md](docs/SECURITY-NOTES.md) | Consideraciones de seguridad |

---

## 🐛 Solución de Problemas

### Error: "ModuleNotFoundError: No module named 'X'"
```bash
pip install -r requirements.txt
```

### Error: "API Key inválida"
Verifica que `.env` tenga las API keys correctas:
```bash
GEMINI_API_KEY=tu-api-key-aqui
```

### ChromaDB no persiste datos
Verifica que `data/chromadb/` existe y tiene permisos de escritura:
```bash
ls -la data/chromadb/
```

### App no abre automáticamente
Abre manualmente: `http://localhost:8501`

Ver [TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md) para más detalles.

---

## 🆕 Historial de Actualizaciones

### Julio 2026 - v1.0.0

#### Migración a Gemini 3.6 Flash
- ✅ Actualizado a **Gemini 3.6 Flash** (última versión)
- ✅ Modelos Gemini 1.5 deprecados
- ✅ Mejor rendimiento y reducción de costos

#### Sistema de Autenticación Mejorado
- ✅ **Acceso automático como Guest** cuando hay documentos
- ✅ Login solo necesario para funciones de administración
- ✅ Alternancia entre modos sin cerrar sesión
- ✅ Flujo de onboarding optimizado

#### Embeddings Locales
- ✅ Migración a **Sentence Transformers** (multilingual-e5-base)
- ✅ Embeddings sin dependencia de APIs externas
- ✅ 768 dimensiones optimizadas
- ✅ Soporte multilingüe mejorado

#### UI y UX
- ✅ Tema claro por defecto
- ✅ Sidebar siempre visible
- ✅ Gestión de documentos mejorada
- ✅ Panel de administración completo
- ✅ Operaciones por lotes

#### Correcciones y Optimizaciones
- ✅ Corrección de duplicate keys en componentes
- ✅ Validación defensiva de datos
- ✅ CSS completo para temas claro/oscuro
- ✅ Logging mejorado para troubleshooting
- ✅ Manejo robusto de errores

---

## 📄 Licencia

Este proyecto es de uso interno para **TechFlow Solutions**.

---

## 👤 Créditos

**Proyecto:** Alura Challenge - Agente RAG con IA  
**Empresa:** TechFlow Solutions  
**Desarrollado por:** [Oscar Alejandro Medina](https://github.com/AlejandroMedina-Ar)

---

## 🌟 Stack de Tecnologías

Construido con las mejores herramientas del ecosistema de IA:

- [Streamlit](https://streamlit.io) - Framework web para IA/ML
- [LangChain](https://langchain.com) - Framework RAG y orquestación LLM
- [ChromaDB](https://www.trychroma.com) - Base de datos vectorial
- [Google Gemini](https://deepmind.google/technologies/gemini/) - LLM de última generación
- [Cohere](https://cohere.com) - LLM enterprise y embeddings
- [HuggingFace](https://huggingface.co) - Modelos open-source

---

**⭐ TechFlow Solutions - Transformación Digital con Inteligencia Artificial**
