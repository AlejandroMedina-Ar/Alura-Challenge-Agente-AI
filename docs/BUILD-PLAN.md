# 🏗️ BUILD PLAN - TechFlow AI RAG Agent

**Proyecto:** TechFlow AI Corporate Knowledge Agent  
**Última actualización:** 2026-07-25  
**Estado general:** 🟡 **FASE 0 COMPLETA** - Listo para iniciar implementación

---

## 📊 PROGRESO GENERAL

```
Fase 0: Especificación   ████████████████████ 100% ✅ COMPLETA
Fase 1: Fundaciones      ████████░░░░░░░░░░░░  40% 🟡 EN PROGRESO
Fase 2: Core Logic       ░░░░░░░░░░░░░░░░░░░░   0% ⏸️  PENDIENTE
Fase 3: RAG Pipeline     ░░░░░░░░░░░░░░░░░░░░   0% ⏸️  PENDIENTE
Fase 4: Services         ░░░░░░░░░░░░░░░░░░░░   0% ⏸️  PENDIENTE
Fase 5: UI               ░░░░░░░░░░░░░░░░░░░░   0% ⏸️  PENDIENTE
Fase 6: Integration      ░░░░░░░░░░░░░░░░░░░░   0% ⏸️  PENDIENTE
Fase 7: Testing          ░░░░░░░░░░░░░░░░░░░░   0% ⏸️  PENDIENTE
Fase 8: Deployment       ░░░░░░░░░░░░░░░░░░░░   0% ⏸️  PENDIENTE

TOTAL PROYECTO:          ███░░░░░░░░░░░░░░░░░  15% (1.4/9 fases)
```

---

## 🎯 PUNTO ACTUAL DE IMPLEMENTACIÓN

**📍 Ubicación:** Fase 1 - Config Module completado (40% de Fase 1)  
**🔧 Agente actual:** Kiro  
**📂 Último módulo completado:** `src/config/` (settings.py, paths.py, constants.py, __init__.py)  
**➡️ Próximo módulo:** `src/utils/logger.py`

---

## 🗺️ FASES DEL PROYECTO

---

## ✅ FASE 0: ESPECIFICACIÓN Y ARQUITECTURA

**Estado:** ✅ **COMPLETA** (100%)  
**Fecha inicio:** 2026-07-20  
**Fecha fin:** 2026-07-25  
**Responsable:** Kiro (especificación y auditoría)

### Tareas Completadas

- [x] 📋 Especificaciones técnicas (7 documentos)
- [x] 🏗️ Arquitectura del sistema definida
- [x] 📖 Glosario de terminología
- [x] 🔍 Auditoría y resolución de 20 conflictos
- [x] 🎨 Clarificación de arquitectura UI
- [x] 🔑 Configuración de API keys de desarrollo
- [x] 📝 Reglas de implementación documentadas
- [x] 🔧 Stack tecnológico definido (100% free tier)
- [x] 📊 Plan de implementación creado
- [x] 🛠️ Migración a tool-agnostic

### Entregables

- ✅ `/specs/` - 7 especificaciones completas
- ✅ `/architecture/` - Arquitectura y estructura
- ✅ `/prompts/` - Reglas y prompts
- ✅ `/docs/` - Documentación completa
- ✅ `.env` - Variables de entorno configuradas
- ✅ `data/config.json` - Configuración runtime
- ✅ `requirements.txt` - Dependencias definidas

### Documentos Clave

1. `docs/PROJECT-STATUS.md` - Estado ejecutivo
2. `docs/IMPLEMENTATION-OPTIONS.md` - Opciones de agente
3. `docs/FINAL-SUMMARY.md` - Resumen completo
4. `architecture/Architecture.md` - Arquitectura general
5. `architecture/Glossary.md` - Terminología canónica

---

## 🟡 FASE 1: FUNDACIONES

**Estado:** ⏸️ **PENDIENTE** (0%)  
**Prioridad:** 🔴 **CRÍTICA**  
**Dependencias:** Ninguna  
**Estimación:** 3-4 horas (interactivo con Kiro) o 1-2 horas (autónomo)

### Objetivo

Implementar módulos base que servirán de fundación para todo el proyecto. Sin estos módulos, nada más puede funcionar.

### Módulos a Implementar

#### 1.1 Config Module (`src/config/`)

**Archivos:**

- [x] `src/config/__init__.py` ✅
- [x] `src/config/settings.py` ✅ **COMPLETO**
- [x] `src/config/paths.py` ✅
- [x] `src/config/constants.py` ✅

**Funcionalidad:**
- Carga de variables de entorno (`.env`)
- Validación de configuración requerida
- Definición de rutas del sistema
- Constantes globales (modelos, límites, etc.)

**Especificación:** `specs/005-configuration.md`

**Complejidad:** 🟢 Baja

**Tests necesarios:**
- [ ] Test de carga de `.env`
- [ ] Test de validación de variables requeridas
- [ ] Test de paths existentes

**Estado:** ✅ **COMPLETADO** (2026-07-26)

---

#### 1.2 Utils Module (`src/utils/`)

**Archivos:**

- [ ] `src/utils/__init__.py`
- [ ] `src/utils/logger.py`
- [ ] `src/utils/exceptions.py`
- [ ] `src/utils/validators.py`
- [ ] `src/utils/helpers.py`

**Funcionalidad:**
- Sistema de logging estructurado
- Excepciones custom del proyecto
- Validadores (archivos, tamaños, formatos)
- Funciones helper (hash password, format size, etc.)

**Especificación:** Múltiples specs (002, 003, 004)

**Complejidad:** 🟢 Baja-Media

**Tests necesarios:**
- [ ] Test de logger (diferentes niveles)
- [ ] Test de validadores (casos válidos e inválidos)
- [ ] Test de helpers

---

#### 1.3 Storage Module (`src/storage/`)

**Archivos:**

- [ ] `src/storage/__init__.py`
- [ ] `src/storage/file_manager.py`
- [ ] `src/storage/document_repository.py`
- [ ] `src/storage/metadata_repository.py`
- [ ] `src/storage/config_repository.py`

**Funcionalidad:**
- Gestión de archivos (save, delete, move)
- CRUD de documentos en knowledge library
- CRUD de metadata JSON
- CRUD de configuración runtime

**Especificación:** `specs/002-knowledge-base-management.md`, `specs/005-configuration.md`

**Complejidad:** 🟡 Media

**Tests necesarios:**
- [ ] Test de file operations (CRUD)
- [ ] Test de document repository
- [ ] Test de metadata repository
- [ ] Test de config repository

---

### Criterios de Completitud Fase 1

- [ ] Todos los archivos implementados y funcionando
- [ ] Tests unitarios pasando (>80% coverage)
- [ ] Documentación inline completa (docstrings)
- [ ] Sin errores de linting (flake8/pylint)
- [ ] Validación manual exitosa:
  - [ ] `.env` se carga correctamente
  - [ ] Paths se crean automáticamente
  - [ ] Logger escribe en archivo
  - [ ] Validators rechazan datos inválidos
  - [ ] File manager guarda/lee archivos

---

## 🟡 FASE 2: CORE LOGIC

**Estado:** ⏸️ **PENDIENTE** (0%)  
**Prioridad:** 🔴 **CRÍTICA**  
**Dependencias:** Fase 1 completa  
**Estimación:** 4-5 horas

### Objetivo

Implementar autenticación y proveedores LLM (Gemini + Cohere) con fallback.

### Módulos a Implementar

#### 2.1 Auth Module (`src/auth/`)

**Archivos:**

- [ ] `src/auth/__init__.py`
- [ ] `src/auth/authentication.py`
- [ ] `src/auth/session.py`

**Funcionalidad:**
- Autenticación de administrador (password)
- Gestión de sesiones en Streamlit session_state
- Verificación de permisos

**Especificación:** `specs/003-authentication.md`

**Complejidad:** 🟢 Baja

**Tests necesarios:**
- [ ] Test de verificación de password (correcto/incorrecto)
- [ ] Test de hash de password
- [ ] Test de gestión de sesión

---

#### 2.2 LLM Module (`src/llm/`)

**Archivos:**

- [ ] `src/llm/__init__.py`
- [ ] `src/llm/base_provider.py`
- [ ] `src/llm/gemini_provider.py`
- [ ] `src/llm/cohere_provider.py`

**Funcionalidad:**
- Interfaz base abstracta (BaseProvider)
- Implementación Gemini 2.0 Flash (primary)
- Implementación Cohere Command (fallback)
- Sistema de fallback automático (5 min session-level)
- Streaming de respuestas

**Especificación:** `specs/004-rag-pipeline.md` (secciones 11-13)

**Complejidad:** 🟡 Media-Alta

**Tests necesarios:**
- [ ] Test de Gemini provider (con API key real)
- [ ] Test de Cohere provider (con API key real)
- [ ] Test de fallback logic
- [ ] Test de streaming

---

### Criterios de Completitud Fase 2

- [ ] Autenticación funciona en Streamlit
- [ ] Gemini responde correctamente
- [ ] Cohere responde correctamente
- [ ] Fallback se activa cuando Gemini falla
- [ ] Streaming funciona en ambos providers
- [ ] Tests unitarios pasando

---

## 🟡 FASE 3: RAG PIPELINE

**Estado:** ⏸️ **PENDIENTE** (0%)  
**Prioridad:** 🔴 **CRÍTICA**  
**Dependencias:** Fase 1 y 2 completas  
**Estimación:** 6-8 horas

### Objetivo

Implementar pipeline completo de RAG (embeddings, vector store, retrieval, chunking).

### Módulos a Implementar

#### 3.1 RAG Module (`src/rag/`)

**Archivos:**

- [ ] `src/rag/__init__.py`
- [ ] `src/rag/embedding_service.py`
- [ ] `src/rag/vector_store.py`
- [ ] `src/rag/document_loader.py`
- [ ] `src/rag/chunker.py`
- [ ] `src/rag/retriever.py`
- [ ] `src/rag/prompt_builder.py`
- [ ] `src/rag/pipeline.py`

**Funcionalidad:**

**embedding_service.py:**
- Cargar modelo `intfloat/multilingual-e5-base`
- Generar embeddings de texto
- Batch processing

**vector_store.py:**
- Wrapper de ChromaDB
- CRUD de vectores
- Búsqueda por similaridad

**document_loader.py:**
- Cargar PDFs (PyMuPDF)
- Cargar TXT, MD
- Detectar idioma (langdetect)
- Extraer metadata

**chunker.py:**
- Chunking semántico (RecursiveCharacterTextSplitter)
- Overlap configurable
- Preservar contexto

**retriever.py:**
- Top-k retrieval
- Reranking (opcional v2)
- Context window management

**prompt_builder.py:**
- Construcción de prompts RAG
- Inyección de contexto recuperado
- Manejo de tokens (reducción dinámica)

**pipeline.py:**
- Orquestación completa
- Query → Retrieval → Prompt → LLM → Response

**Especificación:** `specs/004-rag-pipeline.md`

**Complejidad:** 🔴 Alta

**Tests necesarios:**
- [ ] Test de embeddings (coherencia semántica)
- [ ] Test de vector store (CRUD)
- [ ] Test de document loader (PDF, TXT)
- [ ] Test de chunker (overlap, tamaños)
- [ ] Test de retriever (top-k correcto)
- [ ] Test de prompt builder
- [ ] Test de pipeline completo (end-to-end)

---

### Criterios de Completitud Fase 3

- [ ] Documento PDF se puede indexar
- [ ] ChromaDB almacena vectores correctamente
- [ ] Retrieval devuelve chunks relevantes
- [ ] Pipeline completo funciona: Query → Response
- [ ] Token limit se maneja correctamente
- [ ] Tests end-to-end pasando

---

## 🟡 FASE 4: BUSINESS SERVICES

**Estado:** ⏸️ **PENDIENTE** (0%)  
**Prioridad:** 🟡 **ALTA**  
**Dependencias:** Fase 1, 2, 3 completas  
**Estimación:** 3-4 horas

### Objetivo

Implementar capa de servicios que orquesta la lógica de negocio.

### Módulos a Implementar

#### 4.1 Services Module (`src/services/`)

**Archivos:**

- [ ] `src/services/__init__.py`
- [ ] `src/services/chat_service.py`
- [ ] `src/services/knowledge_library_service.py`
- [ ] `src/services/indexing_service.py`
- [ ] `src/services/authentication_service.py`
- [ ] `src/services/configuration_service.py`

**Funcionalidad:**

**chat_service.py:**
- Gestionar conversaciones
- Llamar RAG pipeline
- Manejar fallback LLM
- Stream de respuestas

**knowledge_library_service.py:**
- Listar documentos
- Agregar/eliminar documentos
- Validar archivos
- Gestionar metadata

**indexing_service.py:**
- Indexar documentos
- Re-indexar
- Detectar duplicados (SKIP strategy)
- Progreso de indexación

**authentication_service.py:**
- Login/logout
- Verificar sesión

**configuration_service.py:**
- Leer/escribir config.json
- Validar configuración

**Especificación:** Todas las specs (servicios orquestan funcionalidad)

**Complejidad:** 🟡 Media

**Tests necesarios:**
- [ ] Test de chat service (mock RAG)
- [ ] Test de knowledge library service
- [ ] Test de indexing service
- [ ] Test de authentication service
- [ ] Test de configuration service

---

### Criterios de Completitud Fase 4

- [ ] Chat service responde queries
- [ ] Knowledge library service gestiona documentos
- [ ] Indexing service indexa correctamente
- [ ] Authentication service valida usuarios
- [ ] Configuration service lee/escribe config
- [ ] Tests unitarios pasando

---

## 🟡 FASE 5: USER INTERFACE

**Estado:** ⏸️ **PENDIENTE** (0%)  
**Prioridad:** 🟡 **ALTA**  
**Dependencias:** Fase 1, 2, 3, 4 completas  
**Estimación:** 5-7 horas

### Objetivo

Implementar interfaz completa de Streamlit (chat, sidebar, admin panel, settings).

### Módulos a Implementar

#### 5.1 UI Module (`src/ui/`)

**Archivos:**

- [ ] `src/ui/__init__.py`
- [ ] `src/ui/theme.py`
- [ ] `src/ui/components.py`
- [ ] `src/ui/sidebar.py`
- [ ] `src/ui/chat.py`
- [ ] `src/ui/admin_panel.py`
- [ ] `src/ui/settings_panel.py`

**Funcionalidad:**

**theme.py:**
- Cargar CSS (dark.css / light.css)
- Aplicar tema según Streamlit settings

**components.py:**
- Componentes reutilizables
- File uploader custom
- Metric displays
- Status indicators

**sidebar.py:**
- Branding (logo + nombre)
- System status (métricas)
- Admin access (botones)

**chat.py:**
- Vista principal de chat
- Display de mensajes
- Input de usuario
- Streaming de respuestas
- Source citations

**admin_panel.py:**
- Vista de knowledge library
- Upload de documentos
- Eliminación de documentos
- Progreso de indexación

**settings_panel.py:**
- Configuración runtime
- Límites de archivo
- Theme toggle (via Streamlit menu)

**Especificación:** `specs/001-chat-interface.md`, `docs/UI-ARCHITECTURE-CLARIFICATION.md`

**Complejidad:** 🟡 Media-Alta

**Tests necesarios:**
- [ ] Test manual en navegador (no hay tests automatizados para Streamlit UI)

---

### Criterios de Completitud Fase 5

- [ ] Interfaz carga sin errores
- [ ] Chat muestra mensajes correctamente
- [ ] Sidebar muestra métricas
- [ ] Admin panel permite upload
- [ ] Settings panel permite cambiar config
- [ ] CSS dark/light funciona
- [ ] UI responsive (mobile-friendly)
- [ ] Validación manual completa

---

## 🟡 FASE 6: INTEGRATION & ENTRY POINT

**Estado:** ⏸️ **PENDIENTE** (0%)  
**Prioridad:** 🟡 **ALTA**  
**Dependencias:** Fase 1-5 completas  
**Estimación:** 2-3 horas

### Objetivo

Integrar todos los módulos y crear entry point principal (`app.py`).

### Módulos a Implementar

#### 6.1 Main Application

**Archivos:**

- [ ] `src/__init__.py`
- [ ] `src/app.py` ⭐ **Entry point**

**Funcionalidad:**

**app.py:**
- Inicialización de Streamlit
- Configuración de página
- Carga de tema
- Routing de vistas (chat, admin, settings)
- Inicialización de servicios
- Gestión de session_state
- Error handling global

**Especificación:** `specs/000-project-overview.md`

**Complejidad:** 🟡 Media

---

### Criterios de Completitud Fase 6

- [ ] `streamlit run src/app.py` arranca sin errores
- [ ] Todas las vistas se renderizan
- [ ] Navegación entre vistas funciona
- [ ] Session state se mantiene
- [ ] Error handling captura excepciones
- [ ] Logs se escriben correctamente

---

## 🟡 FASE 7: TESTING & DEBUGGING

**Estado:** ⏸️ **PENDIENTE** (0%)  
**Prioridad:** 🟢 **MEDIA**  
**Dependencias:** Fase 1-6 completas  
**Estimación:** 4-6 horas

### Objetivo

Testing exhaustivo, debugging, y optimización.

### Tareas

#### 7.1 Testing

- [ ] **Unit tests completos**
  - [ ] Coverage >80% en módulos críticos
  - [ ] Todos los tests pasando
  
- [ ] **Integration tests**
  - [ ] Test de flujo completo: Upload → Index → Query → Response
  - [ ] Test de fallback LLM
  - [ ] Test de authentication flow
  
- [ ] **Manual testing**
  - [ ] Casos de uso normales
  - [ ] Edge cases (archivos grandes, queries complejas)
  - [ ] Error scenarios (API down, archivo corrupto)

#### 7.2 Debugging

- [ ] Revisar y corregir bugs encontrados en testing
- [ ] Optimizar queries lentas
- [ ] Mejorar error messages
- [ ] Refactoring si es necesario

#### 7.3 Documentation

- [ ] Docstrings completos en todos los módulos
- [ ] README.md actualizado con instrucciones de uso
- [ ] Comentarios en código complejo

---

### Criterios de Completitud Fase 7

- [ ] >80% test coverage
- [ ] Todos los tests pasando
- [ ] No bugs críticos pendientes
- [ ] Documentación completa
- [ ] Performance aceptable (<5s response time)

---

## 🟡 FASE 8: DEPLOYMENT

**Estado:** ⏸️ **PENDIENTE** (0%)  
**Prioridad:** 🟢 **BAJA** (solo cuando todo funcione)  
**Dependencias:** Fase 1-7 completas  
**Estimación:** 1-2 horas

### Objetivo

Desplegar aplicación a Streamlit Community Cloud.

### Tareas

- [ ] Crear `secrets.toml` para Streamlit Cloud
- [ ] Configurar repository en GitHub (si no existe)
- [ ] Conectar Streamlit Cloud con repo
- [ ] Configurar variables de entorno en Streamlit Cloud
- [ ] Deploy inicial
- [ ] Verificar funcionamiento en producción
- [ ] Configurar dominio custom (opcional)

**Especificación:** `specs/006-deployment.md`

---

### Criterios de Completitud Fase 8

- [ ] App desplegada en Streamlit Cloud
- [ ] URL pública funcionando
- [ ] API keys configuradas correctamente
- [ ] Sin errores en logs de producción
- [ ] Performance aceptable en cloud

---

## 📋 CHECKLIST DE SESIÓN

**Usar este checklist al inicio/fin de cada sesión de implementación**

### 🏁 Inicio de Sesión

- [ ] Leer `docs/BUILD-PLAN.md` (este archivo)
- [ ] Verificar fase actual
- [ ] Leer contexto del último módulo implementado
- [ ] Verificar que dependencias estén completas
- [ ] Actualizar "Punto Actual de Implementación" arriba

### 🔚 Fin de Sesión

- [ ] Marcar tareas completadas con [x]
- [ ] Actualizar progreso de fase (%)
- [ ] Documentar problemas encontrados en sección "Notas"
- [ ] Commit de cambios a git (con mensaje descriptivo)
- [ ] Actualizar "Punto Actual de Implementación"
- [ ] Guardar este archivo

---

## 📝 NOTAS DE IMPLEMENTACIÓN

### Sesión 1 (2026-07-26)

**Agente:** Kiro  
**Duración:** ~1 hora  
**Módulos completados:** `src/config/` (completo: 4 archivos)  
**Próximo:** `src/utils/logger.py`

**Archivos creados:**
- ✅ `src/__init__.py` - Package root
- ✅ `src/config/__init__.py` - Config package
- ✅ `src/config/settings.py` - Environment variables & validation (223 líneas)
- ✅ `src/config/paths.py` - Path configuration (200 líneas)
- ✅ `src/config/constants.py` - Application constants (420 líneas)

**Validación:**
- ✅ Módulo config se importa correctamente
- ✅ `get_settings()` carga variables de `.env`
- ✅ `get_paths()` crea directorios automáticamente
- ✅ Validación de configuración funciona
- ✅ python-dotenv instalado

**Notas:**
- Config module es la base de todo el proyecto
- Singleton pattern implementado para settings y paths
- Validación exhaustiva de configuración en startup
- Todas las rutas se crean automáticamente
- Constants incluye enums, límites, y utility functions
- Listo para continuar con utils module

**Próxima sesión:** Implementar `src/utils/` (logger, exceptions, validators, helpers)

---

### Sesión 2 (Pendiente)

**Agente:** TBD  
**Duración:** -  
**Módulos completados:** -

**Notas:**
- (Agregar notas aquí)

---

## 🚨 PROBLEMAS CONOCIDOS

### Críticos
*Ninguno actualmente*

### No Críticos
*Ninguno actualmente*

---

## 🎯 DEPENDENCIAS ENTRE MÓDULOS

```
config ──┬──> utils ──┬──> storage ──┬──> auth
         │            │              │
         │            └──> llm ──────┼──> rag ──┬──> services ──> ui ──> app
         │                           │          │
         └───────────────────────────┘          │
                                                │
                                                └──> (todos los services)
```

**Regla:** No implementar un módulo hasta que sus dependencias estén completas.

---

## 💡 CONSEJOS PARA NUEVO AGENTE

**Si eres un nuevo agente retomando este proyecto:**

1. **Lee primero:**
   - `docs/PROJECT-STATUS.md` - Estado general
   - `docs/BUILD-PLAN.md` - Este archivo (punto actual)
   - `docs/FINAL-SUMMARY.md` - Resumen técnico completo

2. **Verifica:**
   - ¿Qué fase está en progreso?
   - ¿Cuál fue el último módulo completado?
   - ¿Hay tests pasando? (`pytest`)

3. **Contexto necesario por fase:**
   - **Fase 1:** `specs/005-configuration.md`, `architecture/Architecture.md`
   - **Fase 2:** `specs/003-authentication.md`, `specs/004-rag-pipeline.md` (sec 11-13)
   - **Fase 3:** `specs/004-rag-pipeline.md` (completa)
   - **Fase 4:** Todas las specs (servicios orquestan todo)
   - **Fase 5:** `specs/001-chat-interface.md`, `docs/UI-ARCHITECTURE-CLARIFICATION.md`
   - **Fase 6:** `specs/000-project-overview.md`
   - **Fase 7:** Tests existentes
   - **Fase 8:** `specs/006-deployment.md`

4. **Antes de codificar:**
   - Lee `prompts/implementation-rules.md` (reglas de implementación)
   - Lee `architecture/Glossary.md` (terminología)
   - Verifica `.env` y `data/config.json` existen

5. **Al terminar tu sesión:**
   - Actualiza este archivo con progreso
   - Documenta problemas encontrados
   - Commit cambios a git

---

## 📊 MÉTRICAS DE PROGRESO

### Por Fase

| Fase | Archivos | Líneas Est. | Complejidad | Estado |
|------|----------|-------------|-------------|--------|
| 0 | 20+ docs | N/A | - | ✅ 100% |
| 1 | 12 archivos | ~800 | Baja | ⏸️ 0% |
| 2 | 6 archivos | ~600 | Media | ⏸️ 0% |
| 3 | 8 archivos | ~1200 | Alta | ⏸️ 0% |
| 4 | 6 archivos | ~800 | Media | ⏸️ 0% |
| 5 | 7 archivos | ~1000 | Media-Alta | ⏸️ 0% |
| 6 | 2 archivos | ~300 | Media | ⏸️ 0% |
| 7 | Tests | ~500 | Media | ⏸️ 0% |
| 8 | Deploy | ~100 | Baja | ⏸️ 0% |

**Total estimado:** ~5300 líneas de código (sin contar tests)

---

## ✅ DEFINICIÓN DE "COMPLETO"

Una fase se considera completa cuando:

- [x] Todos los archivos implementados
- [x] Todos los tests unitarios pasando
- [x] Sin errores de linting
- [x] Documentación inline completa (docstrings)
- [x] Validación manual exitosa
- [x] Criterios específicos de la fase cumplidos
- [x] Commit realizado a git
- [x] Este documento actualizado

---

## 🔄 FLUJO DE TRABAJO RECOMENDADO

```
1. Elegir módulo siguiente (según dependencias)
2. Leer especificación relevante
3. Implementar código
4. Escribir tests
5. Ejecutar tests (pytest)
6. Ejecutar linter (flake8)
7. Validación manual
8. Si falla → Debug → volver a 3
9. Si pasa → Marcar completo en BUILD-PLAN.md
10. Commit a git
11. Siguiente módulo
```

---

## 📞 CONTACTO Y DECISIONES

**Para decisiones técnicas:** Consultar `architecture/Glossary.md` y specs  
**Para dudas de implementación:** Consultar `prompts/implementation-rules.md`  
**Para UI/UX:** Consultar `docs/UI-ARCHITECTURE-CLARIFICATION.md`

---

**Documento creado:** 2026-07-25  
**Última actualización:** 2026-07-25  
**Próxima revisión:** Después de completar Fase 1  
**Versión:** 1.0

---

🚀 **LISTO PARA COMENZAR FASE 1**
