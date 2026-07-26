# Guía de Localización - TechFlow AI RAG Agent

## 📋 Estado de Localización

### ✅ Completado (100%)

**Interfaz de Usuario (UI)** - Todos los textos visibles al usuario
- ✅ `src/app.py` - Página principal, login, navegación
- ✅ `src/ui/chat.py` - Interfaz de chat, mensajes
- ✅ `src/ui/admin_panel.py` - Panel de administración
- ✅ `src/ui/settings_panel.py` - Panel de configuración
- ✅ `src/ui/sidebar.py` - Barra lateral, menús
- ✅ `src/ui/components.py` - Componentes reutilizables
- ✅ `src/rag/prompt_builder.py` - DEFAULT_SYSTEM_INSTRUCTION en español

**Commit:** `b3565a7 - feat: Localización UI completa al español`

### 🔄 Pendiente (Opcional)

**Documentación de Código (Docstrings)**
- ⏳ `src/rag/*.py` (6 archivos) - Comentarios y docstrings
- ⏳ `src/services/*.py` (6 archivos) - Comentarios y docstrings
- ⏳ `src/auth/*.py` (3 archivos) - Comentarios y docstrings
- ⏳ `src/config/*.py` (4 archivos) - Comentarios y docstrings
- ⏳ `src/storage/*.py` (5 archivos) - Comentarios y docstrings
- ⏳ `src/utils/*.py` (4 archivos) - Comentarios y docstrings

**Documentación del Proyecto (.md)**
- ⏳ `README.md` - Ya está en español ✅
- ⏳ `docs/*.md` (4 archivos) - Ya están en español ✅
- ⏳ `specs/*.md` (7 archivos) - Podrían traducirse
- ⏳ `architecture/*.md` (2 archivos) - Podrían traducirse

---

## 🎯 Prioridades

### Alta Prioridad (Ya Completado ✅)
**Textos visibles al usuario** - 100% traducido
- Formularios de login
- Mensajes de error/éxito
- Etiquetas de botones
- Títulos y encabezados
- Placeholders de inputs
- Mensajes del sistema al usuario
- Menús de navegación

### Prioridad Media (Opcional)
**Comentarios en código Python**
- Docstrings de clases y funciones
- Comentarios inline explicativos
- Ejemplos en docstrings

### Prioridad Baja (Opcional)
**Documentación técnica**
- Archivos de especificaciones
- Documentación de arquitectura
- Comentarios de desarrollo

---

## 📝 Guía de Traducción

### Qué Traducir ✅

1. **Textos de UI (YA COMPLETADO)**
   ```python
   # ✅ Traducido
   st.title("🤖 TechFlow AI")
   st.markdown("### Agente de Conocimiento con RAG")
   st.button("Subir Documento")
   st.error("❌ Error al cargar archivo")
   ```

2. **Docstrings de funciones (OPCIONAL)**
   ```python
   def upload_document(file_path: str) -> dict:
       """
       Sube un documento a la biblioteca de conocimiento.
       
       Args:
           file_path: Ruta al archivo a subir
           
       Returns:
           dict: Metadatos del documento subido
       """
   ```

3. **Comentarios explicativos (OPCIONAL)**
   ```python
   # Inicializar el servicio de embeddings
   embedding_service = EmbeddingService()
   ```

### Qué NO Traducir ❌

1. **Nombres de variables, funciones, clases**
   ```python
   # ❌ NO traducir
   def upload_document():  # ✅ Mantener en inglés
   class DocumentRepository:  # ✅ Mantener en inglés
   file_path = "doc.pdf"  # ✅ Mantener en inglés
   ```

2. **Código lógico**
   ```python
   # ❌ NO traducir nombres
   if document_exists:
       return upload_result
   ```

3. **Imports y dependencias**
   ```python
   # ❌ NO traducir
   from src.services import get_chat_service
   import streamlit as st
   ```

---

## 🔧 Herramientas para Traducción Batch

### Buscar Textos de UI
```bash
# Buscar strings en st.* que podrían necesitar traducción
grep -r "st\\.title\|st\\.header\|st\\.button\|st\\.markdown" src/

# Buscar docstrings
grep -r '"""' src/ | head -20
```

### Patrón de Reemplazo
Para VSCode o editor similar:

**Buscar:** `"""(.*?)"""`  
**Reemplazar:** Traducción manual caso por caso

---

## 📂 Archivos Restantes Detallados

### src/rag/ (6 archivos)
```
src/rag/
├── chunker.py           # Fragmentación de documentos
├── embedding_service.py # Generación de embeddings
├── pipeline.py          # Pipeline RAG completo
├── prompt_builder.py    # ✅ Ya tiene prompt en español
├── retriever.py         # Recuperación de documentos
└── vector_store.py      # Gestión de ChromaDB
```

### src/services/ (6 archivos)
```
src/services/
├── authentication_service.py     # Autenticación
├── chat_service.py               # Servicio de chat
├── configuration_service.py      # Configuración
├── indexing_service.py           # Indexación
├── knowledge_base_service.py     # Biblioteca conocimiento
└── __init__.py
```

### src/auth/ (3 archivos)
```
src/auth/
├── authentication.py  # Lógica de autenticación
├── session.py         # Gestión de sesión
└── __init__.py
```

### src/config/ (4 archivos)
```
src/config/
├── constants.py  # Constantes del proyecto
├── paths.py      # Rutas de archivos
├── settings.py   # Configuración general
└── __init__.py
```

### src/storage/ (5 archivos)
```
src/storage/
├── config_repository.py     # Almacenamiento config
├── document_repository.py   # Almacenamiento docs
├── file_manager.py          # Gestión de archivos
├── metadata_repository.py   # Almacenamiento metadata
└── __init__.py
```

### src/utils/ (4 archivos)
```
src/utils/
├── exceptions.py  # Excepciones personalizadas
├── helpers.py     # Funciones helper
├── logger.py      # Sistema de logging
├── validators.py  # Validadores
└── __init__.py
```

---

## 🚀 Procedimiento Recomendado

### Si quieres traducir docstrings y comentarios:

1. **Por módulo:**
   ```bash
   # Ejemplo para src/rag/
   # 1. Lee el archivo
   # 2. Traduce docstrings (""")
   # 3. Traduce comentarios (#)
   # 4. NO toques código
   # 5. Commit
   git add src/rag/chunker.py
   git commit -m "docs: Traducir docstrings en chunker.py"
   ```

2. **Patrón de traducción:**
   ```python
   # Antes
   """
   Chunk text into smaller pieces.
   
   Args:
       text: Input text
       
   Returns:
       list: List of chunks
   """
   
   # Después
   """
   Fragmenta texto en piezas más pequeñas.
   
   Args:
       text: Texto de entrada
       
   Returns:
       list: Lista de fragmentos
   """
   ```

3. **Verificación:**
   ```bash
   # Asegúrate de que el código sigue funcionando
   python -m pytest tests/  # Si tienes tests
   streamlit run src/app.py  # Probar la aplicación
   ```

---

## ✨ Ejemplo Completo de Traducción

### Antes (Inglés)
```python
def upload_document(file_path: str, metadata: dict = None) -> dict:
    """
    Upload document to knowledge library.
    
    Processes the document, extracts text, and stores metadata.
    
    Args:
        file_path: Path to document file
        metadata: Optional document metadata
        
    Returns:
        dict: Document metadata with doc_id
        
    Raises:
        DocumentAlreadyExistsError: If document already exists
        InvalidDocumentError: If document is invalid
        
    Example:
        >>> result = upload_document("path/to/doc.pdf")
        >>> print(result['doc_id'])
    """
    # Check if document exists
    if self.document_exists(file_path):
        raise DocumentAlreadyExistsError(f"Document already exists: {file_path}")
    
    # Process document
    doc_id = self._process_document(file_path, metadata)
    
    return {'doc_id': doc_id, 'status': 'uploaded'}
```

### Después (Español)
```python
def upload_document(file_path: str, metadata: dict = None) -> dict:
    """
    Sube documento a la biblioteca de conocimiento.
    
    Procesa el documento, extrae texto y almacena metadatos.
    
    Args:
        file_path: Ruta al archivo del documento
        metadata: Metadatos opcionales del documento
        
    Returns:
        dict: Metadatos del documento con doc_id
        
    Raises:
        DocumentAlreadyExistsError: Si el documento ya existe
        InvalidDocumentError: Si el documento es inválido
        
    Ejemplo:
        >>> result = upload_document("path/to/doc.pdf")
        >>> print(result['doc_id'])
    """
    # Verificar si el documento existe
    if self.document_exists(file_path):
        raise DocumentAlreadyExistsError(f"Document already exists: {file_path}")
    
    # Procesar documento
    doc_id = self._process_document(file_path, metadata)
    
    return {'doc_id': doc_id, 'status': 'uploaded'}
```

**Nota:** Los nombres de funciones, variables y strings en raise/return NO se traducen.

---

## 📊 Estadísticas de Localización

### Líneas Traducidas
- **Archivos UI:** ~2,000 líneas (100% ✅)
- **Docstrings pendientes:** ~3,500 líneas (Opcional)
- **Documentación .md:** ~1,500 líneas (Mayormente completo ✅)

### Tiempo Estimado
- ✅ **UI (Completado):** ~2-3 horas
- ⏳ **Docstrings (Opcional):** ~4-6 horas
- ⏳ **Documentación (Opcional):** ~1-2 horas

---

## ✅ Checklist de Verificación

Después de cualquier traducción:

- [ ] La aplicación inicia sin errores
- [ ] Todos los textos de UI están en español
- [ ] Los nombres de código permanecen en inglés
- [ ] No hay caracteres especiales rotos (tildes, ñ)
- [ ] Los docstrings mantienen el formato correcto
- [ ] Git commit con mensaje descriptivo

---

## 🎉 Conclusión

**Estado actual:**
- ✅ **Interfaz de usuario:** 100% localizada al español
- ✅ **Experiencia de usuario:** Completamente en español
- ✅ **Prompts del sistema:** En español
- ⏳ **Documentación de código:** Opcional

**La aplicación está lista para usuarios hispanohablantes.** La traducción de docstrings y comentarios es opcional y puede hacerse gradualmente según las necesidades del equipo de desarrollo.

---

## 📞 Soporte

Para preguntas sobre la localización:
- Revisa los archivos ya traducidos en `src/ui/` como referencia
- Mantén la consistencia con términos ya establecidos
- No traduzcas términos técnicos específicos (RAG, embeddings, chunks, etc.)

**Fecha de última actualización:** Enero 2025  
**Versión:** 1.0.0
