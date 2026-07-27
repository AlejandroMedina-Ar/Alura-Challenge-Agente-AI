# 🔒 Notas de Seguridad - Claves API y Credenciales

**Actualizado:** 2026-07-25  
**Estado:** Producción Ready

---

## ⚠️ IMPORTANTE: Configuración de Claves API

Este documento explica cómo se gestionan las claves API en este proyecto para **seguridad** y **despliegue**.

---

## 📁 Archivos y Sus Propósitos

### `.env` (LOCAL SOLAMENTE - NO EN GIT)
**Ubicación:** Raíz del proyecto (e.g., `d:\techflow-rag-agent\.env`)  
**Propósito:** Contiene claves API reales para desarrollo local  
**Estado Git:** ✅ Protegido por `.gitignore` - NUNCA se commitea al repositorio  

**Contenido:**
```env
GEMINI_API_KEY=tu_clave_gemini_real_aqui
COHERE_API_KEY=tu_clave_cohere_real_aqui
ADMIN_PASSWORD=tu_contraseña_segura_aqui
```

**⚠️ IMPORTANTE:** Las claves API reales están configuradas en tu archivo `.env` local (no en Git).

---

### `.env.example` (PÚBLICO - EN GIT)
**Ubicación:** Raíz del proyecto  
**Propósito:** Template mostrando qué variables se necesitan (sin valores reales)  
**Estado Git:** ✅ Commiteado al repositorio como referencia  

**Contenido:**
```env
GEMINI_API_KEY=your_gemini_api_key_here
COHERE_API_KEY=your_cohere_api_key_here
ADMIN_PASSWORD=your_secure_password_here
```

---

## 🔐 Reglas de Seguridad

### ❌ NUNCA Hacer Esto
- Commitear archivo `.env` a Git
- Compartir claves API en canales públicos
- Hardcodear claves API en el código fuente
- Hacer push de claves API a GitHub/GitLab
- Capturar pantallas de archivos con claves API
- Enviar claves API por email o mensajes en texto plano
- Reutilizar claves de desarrollo en producción

### ✅ SIEMPRE Hacer Esto
- Mantener claves API en `.env` (local) o Secrets (cloud)
- Usar `.env.example` como template
- Verificar que `.env` esté en `.gitignore`
- Rotar claves antes del despliegue en producción
- Usar diferentes claves para dev/test/prod
- Usar contraseñas fuertes (12+ caracteres, mixtos)
- Generar nuevas claves para producción

---

## 🛠️ Configuración Actual del Stack

### Stack de Seguridad

**Autenticación:**
- Modo Guest: Sin contraseña, solo lectura
- Modo Admin: Contraseña hasheada con bcrypt
- Passwords hasheadas (no reversibles)
- Session state temporal (no persistente)

**LLM Providers:**
- Gemini 3.6 Flash (primario)
- Cohere Command-R (fallback)
- Autenticación via API keys
- Timeouts configurables

**Embeddings:**
- Modelo: intfloat/multilingual-e5-base
- Ejecución: Local (768 dimensiones)
- No requiere API externa
- Privacidad: Fragmentos no salen del servidor

**Vector Database:**
- ChromaDB 1.0.16
- Almacenamiento: Local
- Colección: techflow_knowledge_base
- No requiere autenticación (local)

**Framework:**
- Streamlit 1.47.1
- Sesiones: En memoria
- HTTPS: Recomendado para producción
- CORS: Configurado por Streamlit

---

## 🚀 Configuraciones de Despliegue

### Desarrollo Local

**Archivo:** `.env` en raíz del proyecto  
**Ubicación:** No commiteado a Git  

**Crear archivo:**
```bash
cp .env.example .env
nano .env
```

**Contenido:**
```env
# Proveedores LLM
GEMINI_API_KEY=tu_clave_gemini_desarrollo
COHERE_API_KEY=tu_clave_cohere_desarrollo

# Seguridad
ADMIN_PASSWORD=admin123_temporal

# Embeddings (opcional, usa default si no se especifica)
EMBEDDING_MODEL=intfloat/multilingual-e5-base

# Vector Database
CHROMA_DB_PATH=data/chromadb
CHROMA_COLLECTION=techflow_knowledge_base

# Chunking
CHUNK_SIZE=1000
CHUNK_OVERLAP=200

# Chat
MAX_CONTEXT_CHUNKS=4
TEMPERATURE=0.2
MAX_OUTPUT_TOKENS=1024

# Timeouts
LLM_REQUEST_TIMEOUT=30
EMBEDDING_TIMEOUT=120
CHROMADB_TIMEOUT=10

# Logging
LOG_LEVEL=INFO
LOG_FILE=data/logs/application.log
```

---

### Streamlit Community Cloud

**Método:** Secrets Management (formato TOML)

**Ubicación:** Dashboard → App Settings → Secrets

**Formato:**
```toml
# Proveedores LLM (REQUERIDO)
GEMINI_API_KEY = "tu_clave_produccion_gemini"
COHERE_API_KEY = "tu_clave_produccion_cohere"

# Seguridad (REQUERIDO)
ADMIN_PASSWORD = "contraseña_segura_12+_caracteres"

# Embeddings (opcional, usa defaults)
EMBEDDING_MODEL = "intfloat/multilingual-e5-base"

# Vector Database (opcional)
CHROMA_DB_PATH = "data/chromadb"
CHROMA_COLLECTION = "techflow_knowledge_base"

# Chunking (opcional)
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200

# Chat (opcional)
MAX_CONTEXT_CHUNKS = 4
TEMPERATURE = 0.2
MAX_OUTPUT_TOKENS = 1024

# Timeouts (opcional)
LLM_REQUEST_TIMEOUT = 30
EMBEDDING_TIMEOUT = 120
CHROMADB_TIMEOUT = 10

# Logging (opcional)
LOG_LEVEL = "INFO"
LOG_FILE = "data/logs/application.log"
```

**⚠️ ANTES DEL DESPLIEGUE:**
1. Generar nuevas claves API de producción
2. Crear contraseña admin fuerte (no "admin123")
3. Nunca reutilizar claves de desarrollo en producción
4. Verificar que secrets estén correctamente configurados
5. Probar en staging antes de producción

---

### VPS/Cloud (AWS, GCP, Azure, DigitalOcean)

**Método:** Variables de Entorno vía archivo `.env` en servidor

**Ubicación:** `/home/usuario/Alura-Challenge-Agente-AI/.env`

**Configurar:**
```bash
# SSH al servidor
ssh usuario@tu-servidor-ip

# Navegar al proyecto
cd Alura-Challenge-Agente-AI

# Crear .env
nano .env

# Agregar claves (mismo formato que desarrollo local)
# Guardar: Ctrl+O, Enter, Ctrl+X

# Verificar permisos (solo dueño puede leer)
chmod 600 .env
```

**Alternativa - Variables de Sistema:**
```bash
# Agregar a ~/.bashrc o ~/.profile
export GEMINI_API_KEY="tu_clave"
export COHERE_API_KEY="tu_clave"
export ADMIN_PASSWORD="tu_contraseña"

# Recargar
source ~/.bashrc
```

**Alternativa - Servicio Systemd:**
```ini
# /etc/systemd/system/techflow.service
[Service]
Environment="GEMINI_API_KEY=tu_clave"
Environment="COHERE_API_KEY=tu_clave"
Environment="ADMIN_PASSWORD=tu_contraseña"
```

---

### Docker (si se usa en el futuro)

**Método:** Variables de entorno en docker-compose.yml

```yaml
# docker-compose.yml
services:
  techflow:
    image: techflow-solutions:latest
    environment:
      - GEMINI_API_KEY=${GEMINI_API_KEY}
      - COHERE_API_KEY=${COHERE_API_KEY}
      - ADMIN_PASSWORD=${ADMIN_PASSWORD}
    env_file:
      - .env
```

O usar Docker secrets para mayor seguridad.

---

## 🔄 Estrategia de Rotación de Claves

### Cuándo Rotar Claves

**Inmediatamente:**
- Antes del despliegue en producción
- Si las claves son expuestas accidentalmente
- Si las claves son commiteadas a Git (incluso si se eliminan después)
- Si se sospecha acceso no autorizado
- Si un miembro del equipo con acceso deja el proyecto

**Periódicamente:**
- Cada 90 días para producción
- Cada 6 meses para desarrollo/testing
- Al cambiar de ambiente (dev → staging → prod)

### Cómo Rotar

**Google Gemini:**
1. Ve a: https://makersuite.google.com/app/apikey
2. Elimina la clave antigua
3. Crea nueva clave ("Create API Key")
4. Actualiza `.env` (local) o Secrets (cloud)
5. Reinicia la aplicación

**Cohere:**
1. Ve a: https://dashboard.cohere.com/api-keys
2. Revoca la clave antigua ("Revoke")
3. Genera nueva clave ("Create API Key")
4. Actualiza `.env` (local) o Secrets (cloud)
5. Reinicia la aplicación

**Contraseña Admin:**
1. Genera contraseña fuerte:
   ```bash
   openssl rand -base64 32
   ```
2. Actualiza en `.env` o Secrets:
   ```
   ADMIN_PASSWORD=nueva_contraseña_generada
   ```
3. Reinicia la aplicación
4. Verifica que puedes hacer login

---

## 📋 Checklist Pre-Despliegue

Antes de desplegar a producción:

### Claves API
- [ ] Generar nueva clave Gemini API (producción)
- [ ] Generar nueva clave Cohere API (producción)
- [ ] Verificar que ambas claves funcionan (test en local primero)
- [ ] Documentar fecha de creación para rotación futura

### Contraseñas
- [ ] Crear contraseña admin fuerte (mínimo 12 caracteres)
- [ ] Usar mezcla: mayúsculas, minúsculas, números, símbolos
- [ ] **NO usar:** "admin123", "password", "12345678"
- [ ] Guardar en gestor de contraseñas seguro

### Configuración Git
- [ ] Verificar `.env` está en `.gitignore`
- [ ] Verificar `.env` NO está en historial de Git
- [ ] Verificar `data/` está en `.gitignore` (contiene ChromaDB)
- [ ] Búsqueda global: `git log --all --full-history --source -- .env`

### Configuración Cloud
- [ ] Configurar Secrets en plataforma (Streamlit/AWS/etc.)
- [ ] Verificar formato correcto (TOML para Streamlit)
- [ ] Probar despliegue en staging primero
- [ ] Verificar logs de despliegue para errores

### Post-Despliegue
- [ ] Probar modo Guest funciona
- [ ] Probar modo Admin con nueva contraseña
- [ ] Verificar Gemini responde correctamente
- [ ] Verificar fallback a Cohere funciona
- [ ] Cargar documento de prueba
- [ ] Indexar y verificar funciona
- [ ] Hacer query y verificar respuesta

### Mantenimiento
- [ ] Documentar fechas de creación de claves
- [ ] Configurar recordatorios para rotación (90 días)
- [ ] Documentar ubicación de secrets/variables
- [ ] Configurar respaldos de datos
- [ ] Configurar monitoreo de logs

---

## 🚨 Qué Hacer Si Las Claves Son Expuestas

Si las claves API son expuestas accidentalmente (commiteadas a Git, compartidas públicamente, etc.):

### Acción Inmediata (en 15 minutos)

1. **Revocar inmediatamente** las claves expuestas:
   - Gemini: https://makersuite.google.com/app/apikey → Delete
   - Cohere: https://dashboard.cohere.com/api-keys → Revoke

2. **Generar nuevas claves** inmediatamente:
   - Crear nuevas en ambos dashboards
   - Usar nombres descriptivos: "Prod-2026-07-25"

3. **Actualizar** configuración:
   - Local: Actualizar `.env`
   - Cloud: Actualizar Secrets
   - Reiniciar aplicación

### Acción Secundaria (en 1 hora)

4. **Si commiteadas a Git**, eliminar del historial:
   ```bash
   # Opción 1: BFG Repo-Cleaner (recomendado)
   java -jar bfg.jar --delete-files .env
   git reflog expire --expire=now --all
   git gc --prune=now --aggressive
   git push --force

   # Opción 2: git filter-branch (más complejo)
   # O contactar administrador de repositorio para reset
   ```

5. **Revisar logs de uso**:
   - Gemini: Revisar dashboard para uso no autorizado
   - Cohere: Revisar dashboard para uso inusual
   - Si hay uso sospechoso, contactar soporte

6. **Notificar** equipo si aplica:
   - Informar qué claves fueron expuestas
   - Compartir nuevas claves de forma segura
   - Actualizar documentación

### Prevención Futura

7. **Agregar protecciones**:
   - Pre-commit hook para detectar secrets
   - Usar git-secrets o similar
   - Revisar PRs cuidadosamente

---

## 🔍 Auditoría de Seguridad

### Revisar Configuración Actual

**Verificar `.gitignore`:**
```bash
cat .gitignore | grep -E "\.env|data/"
# Debe mostrar:
# .env
# data/
```

**Verificar historial Git (buscar secrets):**
```bash
# Buscar .env en historial
git log --all --full-history --source -- .env

# Buscar posibles claves en commits
git log -p | grep -i "api_key"
```

**Verificar permisos de archivos:**
```bash
# .env debe ser 600 (solo dueño lee/escribe)
ls -la .env
# Debería mostrar: -rw------- (600)

# Si no, corregir:
chmod 600 .env
```

---

## 📊 Resumen de Estado Actual

| Componente | Configuración | Estado |
|------------|---------------|--------|
| `.env` file | Creado localmente | ✅ Listo |
| `.env` en `.gitignore` | Protegido | ✅ Confirmado |
| `.env.example` | Template público | ✅ Listo |
| Gemini API | Requiere clave | ⚠️ Configurar |
| Cohere API | Requiere clave | ⚠️ Configurar |
| Password hash | bcrypt | ✅ Implementado |
| Session state | Temporal | ✅ Seguro |
| Embeddings | Local (768d) | ✅ Sin API externa |
| ChromaDB | Local | ✅ Sin auth necesaria |
| Logs | Aplicación solo | ✅ No expone secrets |
| Tema default | Light | ✅ Configurado |

---

## 📞 Recursos de Soporte

**Si necesitas ayuda con:**

**Google Gemini:**
- Dashboard: https://makersuite.google.com/
- Documentación: https://ai.google.dev/docs
- Límites de tasa: https://ai.google.dev/pricing
- Cuota gratuita: 15 req/min, 1M tokens/día

**Cohere:**
- Dashboard: https://dashboard.cohere.com/
- Documentación: https://docs.cohere.com/
- Límites de tasa: https://cohere.com/pricing
- Cuota gratuita: 1000 req/mes

**Streamlit Cloud:**
- Dashboard: https://share.streamlit.io
- Documentación: https://docs.streamlit.io/streamlit-community-cloud
- Soporte: https://discuss.streamlit.io/

**Seguridad General:**
- OWASP Top 10: https://owasp.org/www-project-top-ten/
- API Security: https://owasp.org/www-project-api-security/

---

## 🎯 Mejores Prácticas de Seguridad

### Para Desarrollo

✅ Usar claves de prueba separadas  
✅ No compartir `.env` entre desarrolladores  
✅ Cada dev tiene sus propias claves  
✅ Commitear solo `.env.example`  
✅ Documentar cambios en variables  

### Para Producción

✅ Claves únicas para producción  
✅ Contraseñas fuertes (12+ caracteres)  
✅ HTTPS siempre (usar Nginx + Let's Encrypt)  
✅ Rotar claves cada 90 días  
✅ Monitorear logs de acceso  
✅ Respaldos cifrados  
✅ Revisar dashboards de API regularmente  

### Para Equipo

✅ Usar gestor de contraseñas compartido (1Password, LastPass)  
✅ Principio de mínimo privilegio  
✅ Revocar acceso cuando alguien deja el equipo  
✅ Documentar quién tiene acceso a qué  
✅ Auditorías periódicas de acceso  

---

**Documento mantenido por:** Equipo del Proyecto  
**Última actualización:** 2026-07-25  
**Próxima revisión:** Antes de cada despliegue a producción

**Versión:** 1.0.0  
**Estado:** Producción Ready
