# Contribuir al Agente RAG de TechFlow Solutions

¡Gracias por tu interés en contribuir a TechFlow Solutions! Este documento proporciona pautas e instrucciones para contribuir.

---

## Tabla de Contenidos

1. [Código de Conducta](#código-de-conducta)
2. [Primeros Pasos](#primeros-pasos)
3. [Configuración de Desarrollo](#configuración-de-desarrollo)
4. [Cómo Contribuir](#cómo-contribuir)
5. [Estándares de Código](#estándares-de-código)
6. [Pruebas](#pruebas)
7. [Documentación](#documentación)
8. [Proceso de Pull Request](#proceso-de-pull-request)

---

## Código de Conducta

### Nuestro Compromiso

Estamos comprometidos a proporcionar una comunidad acogedora e inspiradora para todos. Por favor, sé respetuoso y constructivo en tus interacciones.

### Comportamiento Esperado

- Sé respetuoso e inclusivo
- Da la bienvenida a los nuevos participantes
- Sé paciente y servicial
- Enfócate en lo mejor para la comunidad
- Muestra empatía hacia los demás

### Comportamiento Inaceptable

- Acoso o lenguaje discriminatorio
- Ataques personales
- Trolling o comentarios insultantes
- Publicar información privada de otros
- Cualquier conducta que razonablemente pueda considerarse inapropiada

---

## Primeros Pasos

### Prerequisitos

- Python 3.9 o superior
- Git
- Conocimiento básico de Python, Streamlit y conceptos RAG
- Familiaridad con la arquitectura del proyecto (ver [Arquitectura](architecture/Architecture.md))

### Primeras Contribuciones

Los buenos primeros issues están etiquetados con `good first issue` en GitHub. Estos típicamente incluyen:
- Mejoras en la documentación
- Corrección de bugs
- Adición de funcionalidades pequeñas
- Mejoras en la cobertura de tests

---

## Configuración de Desarrollo

### 1. Fork y Clone

```bash
# Haz fork del repositorio en GitHub
# Luego clona tu fork
git clone https://github.com/TU-USUARIO/Alura-Challenge-Agente-AI.git
cd Alura-Challenge-Agente-AI

# Agrega el remote upstream
git remote add upstream https://github.com/AlejandroMedina-Ar/Alura-Challenge-Agente-AI.git
```

### 2. Crear Entorno Virtual

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# o
venv\Scripts\activate  # Windows
```

### 3. Instalar Dependencias

```bash
# Instalar requirements
pip install -r requirements.txt

# Instalar dependencias de desarrollo (opcional)
pip install black flake8 isort pytest pytest-cov
```

### 4. Configurar Entorno

```bash
cp .env.example .env
# Edita .env con tus claves API
```

### 5. Ejecutar Setup

```bash
python setup.py
```

### 6. Ejecutar Tests

```bash
python test_integration.py
```

---

## Cómo Contribuir

### Reportar Bugs

**Antes de enviar un reporte de bug:**
1. Verifica los issues existentes para evitar duplicados
2. Prueba con la última versión
3. Verifica que no sea un problema de configuración

**El reporte de bug debe incluir:**
- Título claro y descriptivo
- Pasos para reproducir
- Comportamiento esperado vs comportamiento actual
- Capturas de pantalla (si aplica)
- Información del entorno (SO, versión de Python)
- Logs relevantes (elimina datos sensibles)

**Ejemplo:**
```markdown
**Bug:** El chat no responde cuando no hay documentos indexados

**Pasos para reproducir:**
1. Instalación limpia
2. Login
3. Ir a página de Chat
4. Escribir una pregunta

**Esperado:** Mensaje de error o estado vacío
**Actual:** La aplicación crashea

**Entorno:**
- SO: Ubuntu 22.04
- Python: 3.11.2
- Navegador: Chrome 120

**Logs:**
```
[ERROR] RAGPipeline query failed: vector store is empty
```
```

### Sugerir Funcionalidades

**Las solicitudes de funcionalidades deben incluir:**
- Descripción clara de la funcionalidad
- Casos de uso y beneficios
- Enfoque potencial de implementación
- Alternativas consideradas

**Ejemplo:**
```markdown
**Funcionalidad:** Versionado de documentos

**Descripción:**
Permitir que múltiples versiones del mismo documento coexistan en la biblioteca de conocimiento.

**Caso de uso:**
- Rastrear cambios en documentos a lo largo del tiempo
- Comparar diferentes versiones
- Revertir a versiones anteriores

**Ideas de implementación:**
- Agregar campo de versión a metadatos
- Almacenar versiones como docs separados con convención de nombres
- Agregar UI para gestionar versiones

**Alternativas:**
- Renombrado manual (workaround actual)
- Control de versiones externo
```

### Contribuir Código

1. **Crear una rama:**
   ```bash
   git checkout -b feature/nombre-de-tu-funcionalidad
   # o
   git checkout -b bugfix/numero-de-issue
   ```

2. **Hacer cambios:**
   - Seguir estándares de código (ver abajo)
   - Agregar/actualizar tests
   - Actualizar documentación

3. **Probar tus cambios:**
   ```bash
   python test_integration.py
   ```

4. **Commit:**
   ```bash
   git add .
   git commit -m "Descripción de los cambios"
   ```

5. **Push:**
   ```bash
   git push origin feature/nombre-de-tu-funcionalidad
   ```

6. **Crear Pull Request:**
   - Ir a GitHub
   - Clic en "New Pull Request"
   - Completar el template
   - Vincular issues relacionados

---

## Estándares de Código

### Guía de Estilo Python

Seguir **PEP 8** con estas especificaciones:

**Formato:**
- 4 espacios para indentación (sin tabs)
- Longitud máxima de línea: 100 caracteres
- Usar comas finales en estructuras multi-línea

**Ejemplo:**
```python
def process_document(
    file_path: str,
    chunk_size: int = 512,
    chunk_overlap: int = 50
) -> dict:
    """
    Procesa un documento para indexación.
    
    Args:
        file_path: Ruta al documento
        chunk_size: Tamaño de los fragmentos
        chunk_overlap: Superposición entre fragmentos
    
    Returns:
        dict: Resultados del procesamiento
    """
    # Implementación
    pass
```

### Type Hints

**Siempre usar type hints:**
```python
# Bueno
def add_numbers(a: int, b: int) -> int:
    return a + b

# Malo
def add_numbers(a, b):
    return a + b
```

### Docstrings

**Usar docstrings estilo Google:**
```python
def function_name(param1: str, param2: int) -> bool:
    """
    Descripción breve de la función.
    
    Descripción más larga si es necesaria, explicando qué
    hace la función con más detalle.
    
    Args:
        param1: Descripción de param1
        param2: Descripción de param2
    
    Returns:
        Descripción del valor de retorno
    
    Raises:
        ValueError: Cuando param1 está vacío
    
    Example:
        >>> function_name("test", 42)
        True
    """
    pass
```

### Convenciones de Nombres

- **Funciones/Variables:** `snake_case`
- **Clases:** `PascalCase`
- **Constantes:** `UPPER_SNAKE_CASE`
- **Privados:** `_guion_bajo_inicial`

```python
# Bueno
class DocumentProcessor:
    MAX_FILE_SIZE = 10_000_000
    
    def __init__(self):
        self._cache = {}
    
    def process_file(self, file_path: str) -> dict:
        pass
```

### Organización del Código

**Orden de imports:**
1. Biblioteca estándar
2. Paquetes de terceros
3. Módulos locales

```python
# Biblioteca estándar
import os
from pathlib import Path

# Terceros
import streamlit as st
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Locales
from src.config import get_paths
from src.utils import get_logger

# Uso:
paths = get_paths()
data_dir = paths.DATA_DIR
```

### Manejo de Errores

**Usar excepciones específicas:**
```python
# Bueno
try:
    result = process_document(path)
except FileNotFoundError:
    logger.error(f"Archivo no encontrado: {path}")
    raise DocumentNotFoundError(path)
except PermissionError:
    logger.error(f"Permiso denegado: {path}")
    raise

# Malo
try:
    result = process_document(path)
except Exception as e:
    print(f"Error: {e}")
```

### Logging

**Usar niveles de log apropiados:**
```python
logger.debug(f"Procesando documento", filename=filename)
logger.info(f"Documento indexado", doc_id=doc_id, chunks=42)
logger.warning(f"Documento grande", size_mb=size/1024/1024)
logger.error(f"Indexación falló", error=str(e), exc_info=True)
```

---

## Pruebas

### Ejecutar Tests

```bash
# Ejecutar todos los tests de integración
python test_integration.py

# Ejecutar test específico
python -m pytest tests/test_specific.py

# Ejecutar con cobertura
pytest --cov=src --cov-report=html
```

### Escribir Tests

**Estructura de test:**
```python
def test_function_name():
    """Descripción del test."""
    # Preparar (Arrange)
    input_data = "test"
    expected = "result"
    
    # Actuar (Act)
    result = function_to_test(input_data)
    
    # Afirmar (Assert)
    assert result == expected
```

**Nombres de test:**
- `test_<funcion>_<escenario>_<esperado>`
- Ejemplo: `test_upload_document_duplicate_raises_error`

---

## Documentación

### Cuándo Actualizar Documentación

- Al agregar nuevas funcionalidades
- Al cambiar funcionalidad existente
- Al corregir bugs que afecten el uso
- Al agregar opciones de configuración

### Qué Documentar

1. **Guía de Usuario** (`docs/USER-GUIDE.md`)
   - Cómo usar nuevas funcionalidades
   - Cambios de configuración
   - Nuevos flujos de trabajo

2. **Documentación Técnica** (`docs/TECHNICAL-DOCS.md`)
   - Cambios en API
   - Actualizaciones de arquitectura
   - Nuevos módulos

3. **FAQ** (`docs/FAQ.md`)
   - Problemas comunes
   - Nuevos pasos de troubleshooting

4. **README** (`README.md`)
   - Cambios mayores
   - Nuevas funcionalidades (alto nivel)

5. **Changelog** (`CHANGELOG.md`)
   - Todos los cambios
   - Seguir formato Keep a Changelog

---

## Proceso de Pull Request

### Antes de Enviar

**Checklist:**
- [ ] El código sigue la guía de estilo
- [ ] Los tests pasan localmente
- [ ] Agregados/actualizados tests para cambios
- [ ] Actualizada documentación relevante
- [ ] Commits son limpios y descriptivos
- [ ] La rama está actualizada con main

### Template de PR

```markdown
## Descripción
Descripción breve de los cambios

## Tipo de Cambio
- [ ] Corrección de bug
- [ ] Nueva funcionalidad
- [ ] Cambio breaking
- [ ] Actualización de documentación

## Testing
- [ ] Tests de integración pasan
- [ ] Testing manual completado
- [ ] Agregados nuevos tests

## Checklist
- [ ] El código sigue la guía de estilo
- [ ] Documentación actualizada
- [ ] Sin nuevas advertencias
- [ ] Commits están limpios

## Issues Relacionados
Fixes #123
Related to #456

## Capturas de Pantalla (si aplica)
[Agregar capturas aquí]
```

### Proceso de Revisión

1. **Verificaciones automatizadas:**
   - Pipeline CI/CD ejecuta tests
   - Verificaciones de linting
   - Verificación de build

2. **Revisión de código:**
   - Maintainer revisa el código
   - Solicita cambios si es necesario
   - Aprueba cuando está listo

3. **Merge:**
   - Squash and merge (por defecto)
   - Mantener historial limpio

### Después del Merge

- Elimina tu rama
- Actualiza tu repo local:
  ```bash
  git checkout main
  git pull upstream main
  ```

---

## ¿Preguntas?

- Revisa el [FAQ](docs/FAQ.md)
- Lee la [Documentación Técnica](docs/TECHNICAL-DOCS.md)
- Pregunta en GitHub Discussions
- Abre un issue para bugs

---

## Licencia

Al contribuir, aceptas que tus contribuciones serán licenciadas bajo la Licencia MIT.

---

**¡Gracias por contribuir a TechFlow Solutions!** 🎉

**Versión:** 1.0.0  
**Última Actualización:** 2025-01-25
