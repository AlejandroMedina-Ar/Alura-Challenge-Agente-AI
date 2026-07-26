# 🤖 TechFlow AI - Corporate Knowledge Agent

> **RAG-powered AI assistant for enterprise knowledge management**

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/streamlit-1.30+-red.svg)](https://streamlit.io)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Status](https://img.shields.io/badge/status-in%20development-orange.svg)]()

---

## 📋 Descripción

**TechFlow AI** es un agente de conocimiento corporativo potenciado por RAG (Retrieval-Augmented Generation) que permite a las empresas interactuar con su base de conocimiento mediante lenguaje natural.

### ✨ Características Principales

- 💬 **Interfaz de chat intuitiva** similar a ChatGPT/Claude
- 📚 **Gestión de knowledge library** (PDF, TXT, MD)
- 🔍 **Búsqueda semántica** con embeddings multilingües
- 🤖 **Dual LLM** (Gemini 2.0 Flash + Cohere fallback)
- 🔐 **Autenticación de administrador**
- 🎨 **Temas claro/oscuro** (Tokyo Night palette)
- 🌐 **100% free tier** (desarrollo/demo)

---

## 🚀 Estado del Proyecto

**Fase actual:** ✅ **Fase 5 completa** - UI Layer implementada  
**Próximo paso:** 🟡 **Fase 6** - Integration & Testing

Para ver el progreso detallado: **[📊 BUILD PLAN](docs/BUILD-PLAN.md)**

```
Progreso general: ████████████████░░░░ 80% (5/9 fases)
```

### ✅ Completado

- ✅ Fase 0: Especificación y arquitectura (100%)
- ✅ Fase 1: Fundaciones - config, utils, storage (100%)
- ✅ Fase 2: Core Logic - auth, llm providers (100%)
- ✅ Fase 3: RAG Pipeline - embeddings, retrieval, prompts (100%)
- ✅ Fase 4: Services - business logic (100%)
- ✅ Fase 5: UI - Streamlit interface (100%)

### 🟡 En Progreso

- 🟡 Fase 6: Integration & Testing
- ⏸️ Fase 7: Documentation
- ⏸️ Fase 8: Deployment

---

## 📚 Documentación

### 🎯 Inicio Rápido

- **[📊 BUILD PLAN](docs/BUILD-PLAN.md)** - Plan completo de implementación con checklist
- **[📍 PROJECT STATUS](docs/PROJECT-STATUS.md)** - Estado actual del proyecto
- **[🔧 IMPLEMENTATION OPTIONS](docs/IMPLEMENTATION-OPTIONS.md)** - Opciones de agente para implementación

### 📖 Especificaciones Técnicas

- [000 - Project Overview](specs/000-project-overview.md)
- [001 - Chat Interface](specs/001-chat-interface.md)
- [002 - Knowledge Base Management](specs/002-knowledge-base-management.md)
- [003 - Authentication](specs/003-authentication.md)
- [004 - RAG Pipeline](specs/004-rag-pipeline.md)
- [005 - Configuration](specs/005-configuration.md)
- [006 - Deployment](specs/006-deployment.md)

### 🏗️ Arquitectura

- [Architecture](architecture/Architecture.md) - Visión general del sistema
- [Source Code Structure](architecture/Source-Code-Structure.md) - Organización del código
- [Glossary](architecture/Glossary.md) - Terminología canónica

### 📄 Documentación Adicional

- [FINAL SUMMARY](docs/FINAL-SUMMARY.md) - Resumen completo del proyecto
- [AGENT AUDIT RESOLUTION](docs/AGENT-AUDIT-RESOLUTION.md) - Auditoría resuelta
- [UI ARCHITECTURE](docs/UI-ARCHITECTURE-CLARIFICATION.md) - Arquitectura UI clarificada
- [READY FOR IMPLEMENTATION](docs/READY-FOR-IMPLEMENTATION.md) - Confirmación de preparación

---

## 🛠️ Stack Tecnológico

### Backend
- **Python 3.11+** - Lenguaje principal
- **Streamlit** - Framework UI
- **ChromaDB** - Vector database (local)
- **LangChain** - Framework RAG
- **PyMuPDF** - Procesamiento de PDFs

### LLMs & Embeddings
- **Google Gemini 1.5 Flash** - LLM principal (free tier)
- **Cohere Command-R** - LLM fallback (free tier)
- **multilingual-e5-base** - Modelo de embeddings (768 dim, optimizado español)

### Deployment
- **Streamlit Community Cloud** - Hosting gratuito

---

## 📦 Instalación

### Prerrequisitos

- Python 3.11 o superior
- pip o uv
- Git

### Pasos

```bash
# 1. Clonar el repositorio
git clone https://github.com/AlejandroMedina-Ar/Alura-Challenge-Agente-AI.git
cd Alura-Challenge-Agente-AI

# 2. Crear entorno virtual
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Configurar variables de entorno
cp .env.example .env
# Editar .env con tus API keys

# 5. Ejecutar setup
python setup.py

# 6. Ejecutar tests (opcional)
python test_integration.py

# 7. Iniciar la aplicación
python run.py
# o directamente: streamlit run src/app.py
```

---

## 🔑 Configuración

### Variables de Entorno (`.env`)

```bash
# LLM API Keys
GEMINI_API_KEY=tu_api_key_aqui
COHERE_API_KEY=tu_api_key_aqui

# Modelos
GEMINI_MODEL=gemini-1.5-flash
COHERE_MODEL=command-r

# Embeddings
EMBEDDING_MODEL=intfloat/multilingual-e5-base

# Autenticación
ADMIN_PASSWORD_HASH=bcrypt_hash_aqui

# RAG
CHUNK_SIZE=1000
CHUNK_OVERLAP=200
TOP_K_RESULTS=5
```

### Configuración Runtime (`data/config.json`)

```json
{
  "ui": {
    "theme": "dark",
    "language": "es"
  },
  "limits": {
    "max_pdf_size_mb": 50,
    "max_txt_size_mb": 10
  }
}
```

---

## 📂 Estructura del Proyecto

```
techflow-rag-agent/
├── src/                      # Código fuente
│   ├── config/              # Configuración
│   ├── utils/               # Utilidades
│   ├── storage/             # Persistencia
│   ├── auth/                # Autenticación
│   ├── llm/                 # Proveedores LLM
│   ├── rag/                 # Pipeline RAG
│   ├── services/            # Lógica de negocio
│   ├── ui/                  # Interfaz Streamlit
│   └── app.py               # Entry point
│
├── data/                     # Datos persistentes
│   ├── chromadb/            # Base vectorial
│   ├── knowledge_library/   # Documentos
│   ├── logs/                # Logs
│   └── config.json          # Config runtime
│
├── assets/                   # Recursos estáticos
│   └── css/                 # Estilos (dark/light)
│
├── docs/                     # Documentación
├── specs/                    # Especificaciones
├── architecture/             # Arquitectura
├── prompts/                  # Reglas de implementación
│
├── .env                      # Variables de entorno
├── requirements.txt          # Dependencias
└── README.md                 # Este archivo
```

---

## 🎯 Uso

### Para Usuarios Finales

1. Abrir la aplicación en el navegador
2. Hacer preguntas en lenguaje natural
3. El sistema buscará en la knowledge library y generará respuestas contextualizadas

### Para Administradores

1. Iniciar sesión con credenciales de admin
2. Acceder a "Knowledge Library"
3. Subir documentos (PDF, TXT, MD)
4. El sistema los indexará automáticamente
5. Configurar preferencias en "Settings"

---

## 🧪 Testing

```bash
# Ejecutar todos los tests
pytest

# Tests con coverage
pytest --cov=src --cov-report=html

# Ver reporte de coverage
open htmlcov/index.html  # En Windows: start htmlcov/index.html
```

---

## 🚀 Deployment

### Streamlit Community Cloud

1. Push del código a GitHub
2. Conectar repositorio en [share.streamlit.io](https://share.streamlit.io)
3. Configurar secrets (API keys) en Streamlit dashboard
4. Deploy automático

Ver especificación completa: [specs/006-deployment.md](specs/006-deployment.md)

---

## 🤝 Contribución

### Para Desarrolladores

Si quieres contribuir al proyecto:

1. **Lee la documentación:**
   - [BUILD PLAN](docs/BUILD-PLAN.md) - Estado actual
   - [Implementation Rules](prompts/implementation-rules.md) - Reglas de código
   - [Architecture](architecture/Architecture.md) - Arquitectura

2. **Elige una fase/módulo** del BUILD PLAN que esté pendiente

3. **Implementa siguiendo las especificaciones**

4. **Actualiza el BUILD PLAN** con tu progreso

5. **Crea un pull request**

---

## 📜 Licencia

Este proyecto está bajo la licencia MIT. Ver [LICENSE](LICENSE) para más detalles.

---

## 🙏 Créditos

**Proyecto:** Alura Challenge - Immersion AI + Google Gemini  
**Desarrollado por:** [Tu nombre]  
**Especificado y arquitecturado por:** Kiro AI

### Stack Créditos

- [Streamlit](https://streamlit.io) - Framework UI
- [LangChain](https://langchain.com) - Framework RAG
- [ChromaDB](https://www.trychroma.com) - Vector database
- [Google Gemini](https://deepmind.google/technologies/gemini/) - LLM principal
- [Cohere](https://cohere.com) - LLM fallback
- [HuggingFace](https://huggingface.co) - Modelos de embeddings

---

## 📞 Contacto y Soporte

**Issues:** [GitHub Issues](https://github.com/tu-usuario/techflow-rag-agent/issues)  
**Documentación:** [docs/](docs/)  
**Build Plan:** [docs/BUILD-PLAN.md](docs/BUILD-PLAN.md)

---

## 🗺️ Roadmap

- [x] **Fase 0:** Especificación completa ✅
- [x] **Fase 1:** Fundaciones (config, utils, storage) ✅
- [x] **Fase 2:** Core logic (auth, LLM) ✅
- [x] **Fase 3:** RAG pipeline ✅
- [x] **Fase 4:** Business services ✅
- [x] **Fase 5:** User interface ✅
- [ ] **Fase 6:** Integration & Testing (en progreso)
- [ ] **Fase 7:** Documentation
- [ ] **Fase 8:** Deployment

Ver progreso detallado: **[BUILD PLAN](docs/BUILD-PLAN.md)**

---

## 💡 Filosofía del Proyecto

Este proyecto sigue el principio **"Free Tier First"**:

- Todas las herramientas y servicios usados tienen free tier funcional
- El proyecto es completamente operativo sin costos
- Solo se considerarán servicios pagos cuando el proyecto escale

Esto hace que sea ideal para:
- 🎓 Aprendizaje y experimentación
- 🏗️ Proyectos de demostración
- 🚀 MVPs y prototipos
- 💼 Small business con presupuesto limitado

---

**⭐ Si este proyecto te es útil, dale una estrella en GitHub!**

---

**Última actualización:** 2026-07-25  
**Versión:** 1.0.0-beta  
**Estado:** 🚀 80% completo - Listo para testing y deployment
