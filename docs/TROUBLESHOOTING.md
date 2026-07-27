# Guía de Resolución de Problemas

Esta guía documenta problemas comunes y sus soluciones para TechFlow Solutions RAG Agent.

## Tabla de Contenidos
- [Errores de Importación](#errores-de-importación)
- [Errores de Configuración](#errores-de-configuración)
- [Errores de Dependencias](#errores-de-dependencias)
- [Errores de Base de Datos](#errores-de-base-de-datos)
- [Errores de LLM/API](#errores-de-llmapi)

---

## Errores de Importación

### Error: `ImportError: cannot import name 'DATA_DIR' from 'src.config'`

**Síntoma:**
```bash
python setup.py
Traceback (most recent call last):
  File "setup.py", line 24, in <module>
    from src.config import DATA_DIR
ImportError: cannot import name 'DATA_DIR' from 'src.config'
```

**Causa:**
Las constantes de paths (DATA_DIR, LOGS_DIR, etc.) ya no se exportan directamente desde `src.config`. Ahora están encapsuladas en la clase `Paths` y se acceden a través de la función `get_paths()`.

**Solución:**
Cambiar la forma de importar:

```python
# ❌ Antiguo (incorrecto)
from src.config import DATA_DIR, LOGS_DIR

# ✅ Nuevo (correcto)
from src.config import get_paths

paths = get_paths()
data_dir = paths.DATA_DIR
logs_dir = paths.LOGS_DIR
```

**Archivos afectados (ya corregidos):**
- `setup.py`
- `run.py`
- `test_integration.py`
- `src/ui/theme.py`

**Nota:** Este error fue corregido en el commit `33402fb`.

---

### Error: `ImportError: cannot import name 'setup_logging' from 'src.utils'`

**Síntoma:**
```bash
python setup.py
Traceback (most recent call last):
  File "setup.py", line 27, in <module>
    from src.utils import get_logger, setup_logging
ImportError: cannot import name 'setup_logging' from 'src.utils'
```

**Causa:**
La función `setup_logging()` no existe en el módulo `src.utils`. El logger se configura automáticamente al llamar a `get_logger()`.

**Solución:**
Eliminar la importación y llamada a `setup_logging`:

```python
# ❌ Antiguo (incorrecto)
from src.utils import get_logger, setup_logging

setup_logging()
logger = get_logger()

# ✅ Nuevo (correcto)
from src.utils import get_logger

logger = get_logger()  # El logger se configura automáticamente
```

**Archivos afectados (ya corregidos):**
- `setup.py`
- `test_integration.py`

**Nota:** Este error fue corregido en el commit `1f6839d`.

---

### Error: `ImportError: cannot import name 'get_gemini_provider' from 'src.llm'`

**Síntoma:**
```bash
python test_integration.py
Traceback (most recent call last):
  File "test_integration.py", line 53, in <module>
    from src.llm import get_gemini_provider, get_cohere_provider
ImportError: cannot import name 'get_gemini_provider' from 'src.llm'
```

**Causa:**
Las funciones factory `get_gemini_provider()` y `get_cohere_provider()` no existían. Solo estaban las clases `GeminiProvider` y `CohereProvider`.

**Solución:**
Se agregaron funciones singleton en cada módulo de provider:

```python
# En src/llm/gemini_provider.py
def get_gemini_provider() -> GeminiProvider:
    """Get singleton GeminiProvider instance."""
    global _gemini_provider_instance
    
    if _gemini_provider_instance is None:
        from src.config import get_settings
        settings = get_settings()
        
        _gemini_provider_instance = GeminiProvider(
            model=settings.GEMINI_MODEL,
            api_key=settings.GEMINI_API_KEY
        )
    
    return _gemini_provider_instance
```

Y se actualizó `src/llm/__init__.py` para exportarlas:

```python
from .gemini_provider import GeminiProvider, get_gemini_provider
from .cohere_provider import CohereProvider, get_cohere_provider

__all__ = [
    'BaseProvider',
    'GeminiProvider',
    'CohereProvider',
    'get_gemini_provider',  # ← Agregado
    'get_cohere_provider',  # ← Agregado
]
```

**Archivos afectados (ya corregidos):**
- `src/llm/gemini_provider.py` (función agregada)
- `src/llm/cohere_provider.py` (función agregada)
- `src/llm/__init__.py` (exportaciones actualizadas)

**Archivos que dependían de esto:**
- `test_integration.py`
- `src/services/chat_service.py`

**Nota:** Este error fue corregido en el commit `3174d74`.

---

### Error: `ImportError: cannot import name 'DEFAULT_TOP_K' from 'src.config'`

**Síntoma:**
```bash
python src/rag/pipeline.py
Traceback (most recent call last):
  File "src/rag/pipeline.py", line 13, in <module>
    from src.config import DEFAULT_TOP_K
ImportError: cannot import name 'DEFAULT_TOP_K' from 'src.config'
```

**Causa:**
Las constantes de configuración RAG (`DEFAULT_TOP_K`, `DEFAULT_CHUNK_SIZE`, etc.) existían en `src/config/constants.py` pero **no se exportaban** en `src/config/__init__.py`.

**Solución:**
Actualizar `src/config/__init__.py` para exportar todas las constantes RAG:

```python
from .constants import (
    # ... otras importaciones ...
    
    # RAG Configuration
    DEFAULT_CHUNK_SIZE,
    DEFAULT_CHUNK_OVERLAP,
    DEFAULT_TOP_K,
    DEFAULT_TEMPERATURE,
    MIN_DOCUMENTS_FOR_RAG,
    MIN_CHUNK_SIZE,
    MAX_CHUNK_SIZE,
    MIN_TOP_K,
    MAX_TOP_K,
    MIN_TEMPERATURE,
    MAX_TEMPERATURE,
    
    # ...
)
```

**Archivos afectados (ya corregidos):**
- `src/config/__init__.py` (exportaciones agregadas)

**Archivos que dependían de esto:**
- `src/rag/pipeline.py`
- Cualquier módulo que use constantes de configuración RAG

**Nota:** Este error fue corregido en el commit `3174d74`.

---

## Errores de Configuración

### Error: `.env file not found`

**Síntoma:**
```
⚠️  .env file not found (using defaults)
```

**Solución:**
```bash
# Copiar el archivo de ejemplo
cp .env.example .env

# En Windows
copy .env.example .env

# Editar con tus API keys
notepad .env  # o tu editor preferido
```

### Error: `ADMIN_PASSWORD not set`

**Síntoma:**
```
⚠️  Admin password not set
ℹ️  Default password will be used
```

**Solución:**
Agregar en tu archivo `.env`:
```bash
ADMIN_PASSWORD=tu_password_seguro
```

---

## Errores de Dependencias

### Error: `Streamlit not installed`

**Síntoma:**
```
❌ Streamlit not installed
Run: pip install -r requirements.txt
```

**Solución:**
```bash
# Asegúrate de estar en el entorno virtual
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Instalar dependencias
pip install -r requirements.txt
```

### Error: Versión de Python incorrecta

**Síntoma:**
```
❌ Python 3.9 or higher is required
```

**Solución:**
1. Verificar versión actual:
   ```bash
   python --version
   ```

2. Si es menor a 3.9, instalar Python 3.9+ desde [python.org](https://www.python.org/downloads/)

3. Recrear el entorno virtual:
   ```bash
   # Eliminar entorno viejo
   rm -rf venv  # Linux/Mac
   rmdir /s venv  # Windows
   
   # Crear nuevo con Python 3.9+
   python3.9 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

---

## Errores de Base de Datos

### Error: `ChromaDB connection failed`

**Síntoma:**
```
❌ Failed to connect to ChromaDB
```

**Solución:**
1. Verificar que el directorio existe:
   ```bash
   python -c "from src.config import get_paths; print(get_paths().CHROMADB_DIR)"
   ```

2. Si no existe, ejecutar setup:
   ```bash
   python setup.py
   ```

3. Si el problema persiste, eliminar y recrear:
   ```bash
   # Backup primero
   mv data/chromadb data/chromadb.backup
   
   # Recrear
   python setup.py
   ```

### Error: `Database locked`

**Síntoma:**
```
sqlite3.OperationalError: database is locked
```

**Solución:**
1. Cerrar todas las instancias de la aplicación
2. Eliminar archivos de lock:
   ```bash
   find data/chromadb -name "*.lock" -delete  # Linux/Mac
   del /s data\chromadb\*.lock  # Windows
   ```
3. Reiniciar la aplicación

---

## Errores de LLM/API

### Error: `Gemini API key not found`

**Síntoma:**
```
⚠️  Gemini: API key not configured
```

**Solución:**
1. Obtener API key en [Google AI Studio](https://makersuite.google.com/app/apikey)

2. Agregar a `.env`:
   ```bash
   GEMINI_API_KEY=tu_api_key_aqui
   ```

3. Reiniciar la aplicación

### Error: `Cohere API key not found`

**Síntoma:**
```
⚠️  Cohere: API key not configured
```

**Solución:**
1. Obtener API key en [Cohere Dashboard](https://dashboard.cohere.com/api-keys)

2. Agregar a `.env`:
   ```bash
   COHERE_API_KEY=tu_api_key_aqui
   ```

3. Reiniciar la aplicación

### Error: `API rate limit exceeded`

**Síntoma:**
```
Error: 429 Too Many Requests
```

**Solución:**
1. Esperar unos minutos antes de reintentar
2. Verificar límites de tu plan API
3. Considerar cambiar a otro provider temporalmente
4. Ajustar configuración de rate limiting en `.env`:
   ```bash
   REQUEST_DELAY_SECONDS=2
   ```

---

## Problemas de Instalación

### Error durante `pip install`

**Síntoma:**
```
ERROR: Failed building wheel for some-package
```

**Solución:**
1. Actualizar pip y setuptools:
   ```bash
   pip install --upgrade pip setuptools wheel
   ```

2. Instalar dependencias del sistema (Linux):
   ```bash
   # Ubuntu/Debian
   sudo apt-get install python3-dev build-essential
   
   # Fedora/CentOS
   sudo yum install python3-devel gcc
   ```

3. Reintentar instalación:
   ```bash
   pip install -r requirements.txt
   ```

### Error: `No module named 'src'`

**Síntoma:**
```
ModuleNotFoundError: No module named 'src'
```

**Solución:**
Asegúrate de ejecutar comandos desde la raíz del proyecto:
```bash
# Ver dónde estás
pwd  # Linux/Mac
cd    # Windows

# Si no estás en la raíz, navegar allí
cd /ruta/a/techflow-rag-agent

# Verificar que estás en el lugar correcto
ls  # Debes ver: src/, data/, requirements.txt, etc.
```

---

## Problemas de Rendimiento

### La aplicación es lenta

**Causas comunes:**
1. **Muchos documentos indexados:** ChromaDB puede ser lento con miles de documentos
2. **Modelo de embedding grande:** Cambiar a modelo más pequeño en configuración
3. **Recursos limitados:** Verificar uso de CPU/RAM

**Soluciones:**
1. Limitar documentos activos
2. Usar modelo embedding más rápido
3. Ajustar `chunk_size` y `top_k` en configuración
4. Cerrar otras aplicaciones

### Out of Memory

**Síntoma:**
```
MemoryError: Unable to allocate array
```

**Solución:**
1. Reducir `chunk_size` en configuración (ej: de 1000 a 500)
2. Reducir `top_k` (ej: de 10 a 5)
3. Procesar menos documentos a la vez
4. Aumentar swap/virtual memory del sistema

---

## Obtener Ayuda

Si ninguna solución funciona:

1. **Verificar logs:**
   ```bash
   cat data/logs/application.log
   tail -f data/logs/application.log  # Ver en tiempo real
   ```

2. **Ejecutar tests de integración:**
   ```bash
   python test_integration.py
   ```

3. **Reportar el problema:**
   - Abrir un issue en [GitHub](https://github.com/AlejandroMedina-Ar/Alura-Challenge-Agente-AI/issues)
   - Incluir:
     - Output del error completo
     - Versión de Python (`python --version`)
     - Sistema operativo
     - Pasos para reproducir
     - Logs relevantes

4. **Buscar en issues existentes:**
   - Puede que alguien ya haya reportado el mismo problema
   - [Ver issues cerrados](https://github.com/AlejandroMedina-Ar/Alura-Challenge-Agente-AI/issues?q=is%3Aissue+is%3Aclosed)

---

## Información de Debug Útil

### Script de Validación Pre-Setup (NUEVO)

Antes de ejecutar `setup.py`, puedes ejecutar el script de validación para detectar problemas de importación:

```bash
python validate_imports.py
```

Este script verifica:
- ✅ Todas las importaciones de módulos principales
- ✅ Exportaciones en `__init__.py` de cada paquete
- ✅ Funciones factory de LLM (get_gemini_provider, get_cohere_provider)
- ✅ Constantes de configuración (DEFAULT_TOP_K, etc.)
- ✅ Imports en setup.py, run.py, test_integration.py

**Salida esperada si todo está bien:**
```
======================================================================
TechFlow Solutions - Import Validation
======================================================================

🔍 Validating config package...
   ✅ config package OK
🔍 Validating utils package...
   ✅ utils package OK
🔍 Validating storage package...
   ✅ storage package OK
🔍 Validating auth package...
   ✅ auth package OK
🔍 Validating llm package...
   ✅ llm package OK
🔍 Validating rag package...
   ✅ rag package OK
🔍 Validating services package...
   ✅ services package OK
🔍 Validating ui package...
   ✅ ui package OK
🔍 Validating main scripts...
   ✅ setup.py imports OK
   ✅ run.py imports OK
   ✅ test_integration.py imports OK
🔍 Checking LLM factory functions...
   ✅ LLM factory functions found in src.llm
🔍 Checking config constants...
   ✅ All required config constants present

======================================================================
Validation Results
======================================================================

Checks Passed: 11/11
Success Count: [número]

✅ ALL IMPORTS ARE VALID!

You can now safely run:
  1. python setup.py
  2. python test_integration.py
  3. python run.py
```

**Si hay errores:**
El script listará exactamente qué imports fallan y por qué. Esto te ayudará a diagnosticar problemas antes de intentar ejecutar setup.py.

**Nota:** Este script requiere que tengas las dependencias instaladas (`pip install -r requirements.txt`). Si no las tienes, verás errores de módulos como `streamlit`, `chromadb`, etc., pero aún así detectará problemas de estructura del proyecto.

---

### Verificar instalación completa

```bash
# Ejecutar test de integración
python test_integration.py

# Ver configuración de paths
python -c "from src.config import get_paths; import json; print(json.dumps(get_paths().get_summary(), indent=2))"

# Ver configuración actual
python -c "from src.storage import ConfigRepository; import json; print(json.dumps(ConfigRepository().load(), indent=2))"

# Verificar versión
python -c "from src.config import APP_VERSION; print(APP_VERSION)"
```

### Logs importantes

- **Aplicación general:** `data/logs/application.log`
- **Errores específicos:** `data/logs/error.log` (si existe)
- **Streamlit:** Terminal donde ejecutaste `streamlit run`

### Limpiar y reiniciar desde cero

```bash
# ADVERTENCIA: Esto eliminará todos los datos
rm -rf data/  # Linux/Mac
rmdir /s data  # Windows

# Recrear estructura
python setup.py

# Reiniciar aplicación
python run.py
```

---

**Versión del documento:** 1.0.0  
**Última actualización:** 2025-01-25  
**Mantenido por:** TechFlow Solutions Team
