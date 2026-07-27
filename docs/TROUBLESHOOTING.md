# 🔧 Guía de Resolución de Problemas

**Solución de problemas comunes en TechFlow Solutions RAG Agent**

---

## 📑 Tabla de Contenidos

1. [Problemas de Instalación](#problemas-de-instalación)
2. [Problemas de Autenticación](#problemas-de-autenticación)
3. [Problemas con Documentos](#problemas-con-documentos)
4. [Problemas con el Chat](#problemas-con-el-chat)
5. [Problemas de Configuración](#problemas-de-configuración)
6. [Errores de API/LLM](#errores-de-apillm)
7. [Problemas de Rendimiento](#problemas-de-rendimiento)

---

## 🔨 Problemas de Instalación

### Error: ModuleNotFoundError

**Síntoma:**
```bash
ModuleNotFoundError: No module named 'streamlit'
ModuleNotFoundError: No module named 'chromadb'
```

**Causa:** Dependencias no instaladas

**Solución:**
```bash
# Activar entorno virtual
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# Instalar dependencias
pip install -r requirements.txt
```

---

### Error: Python version incompatible

**Síntoma:**
```bash
ERROR: This package requires Python 3.11 or higher
```

**Causa:** Versión de Python muy antigua

**Solución:**
```bash
# Verificar versión
python --version

# Debe ser Python 3.11+
# Si es menor, instala Python 3.11 o superior
```

---

## 🔐 Problemas de Autenticación

### No puedo hacer login

**Síntoma:** Contraseña rechazada, "Invalid credentials"

**Soluciones:**

1. **Verificar contraseña en `.env`:**
   ```bash
   # Abrir .env
   notepad .env  # Windows
   nano .env     # Linux/Mac
   
   # Verificar línea:
   ADMIN_PASSWORD=tu_contraseña_aqui
   ```

2. **Sin espacios extra:**
   ```bash
   # ❌ Incorrecto
   ADMIN_PASSWORD= mi_password  
   
   # ✅ Correcto
   ADMIN_PASSWORD=mi_password
   ```

3. **Reiniciar después de cambiar:**
   ```bash
   # Detener app (Ctrl+C)
   # Volver a ejecutar
   python run.py
   ```

---

### Sesión se cierra sola

**Síntoma:** Logout automático después de inactividad

**Causa:** Comportamiento normal de seguridad

**Solución:** 
- Volver a hacer login
- Para sesiones más largas, mantén la pestaña activa

---

## 📄 Problemas con Documentos

### No puedo subir documentos

**Síntoma:** Upload falla, "Error al subir documento"

**Soluciones:**

1. **Verificar tamaño:**
   ```
   Límites:
   - PDF: 50MB máximo
   - TXT/MD: 10MB máximo
   - DOCX: 25MB máximo
   ```

2. **Verificar formato:**
   ```
   Soportados: .pdf, .txt, .md, .docx
   No soportados: .doc, .rtf, .odt, imágenes
   ```

3. **Verificar permisos:**
   - Solo administradores pueden subir
   - Hacer login como admin primero

4. **Verificar espacio en disco:**
   ```bash
   # Windows
   dir data\knowledge_library\documents
   
   # Linux/Mac
   du -sh data/knowledge_library/documents/
   ```

---

### Documento no se indexa

**Síntoma:** "Indexing Error", documento queda pendiente

**Soluciones:**

1. **Verificar que el archivo tiene texto:**
   - PDFs escaneados (solo imágenes) no funcionan
   - Necesita texto extraíble

2. **Revisar logs:**
   ```bash
   # Ver últimos errores
   tail -50 data/logs/application.log
   ```

3. **Intentar re-subir:**
   - Eliminar documento
   - Subir de nuevo

4. **Probar con archivo más pequeño:**
   - Dividir documentos grandes
   - Indexar por partes

---

### "Documento sin nombre" en lista

**Síntoma:** Lista muestra "Documento sin nombre" en vez del nombre real

**Causa:** Este error fue corregido en versión actual

**Solución:**
- Actualizar a la última versión del código
- `git pull origin main`

---

## 💬 Problemas con el Chat

### Chat no responde

**Síntoma:** Sin respuesta o error al enviar mensaje

**Soluciones:**

1. **Verificar documentos indexados:**
   - Ir a Biblioteca
   - Verificar que hay documentos con ✅ Indexado

2. **Verificar API key:**
   ```bash
   # En .env
   GEMINI_API_KEY=tu_key_aqui
   ```

3. **Probar proveedor LLM:**
   - Admin Panel → Testing
   - Click "Test Gemini"
   - Ver si responde

4. **Verificar internet:**
   ```bash
   ping google.com
   ```

5. **Revisar logs:**
   ```bash
   tail -50 data/logs/application.log | grep ERROR
   ```

---

### Respuestas no relacionadas

**Síntoma:** El agente responde cosas no relacionadas con los documentos

**Soluciones:**

1. **Re-indexar documentos:**
   - Admin Panel → Indexación
   - Click "Indexar Todos los Pendientes"

2. **Ajustar top-k:**
   - Configuración → RAG Settings
   - Aumentar Top K a 7-10

3. **Ser más específico en la pregunta:**
   ```
   ❌ "Dime sobre IT"
   ✅ "¿Cuál es el horario de la Mesa de Ayuda IT?"
   ```

4. **Verificar documentos relevantes están subidos:**
   - Si preguntas sobre vacaciones, necesitas manual de RR.HH.

---

### Chat muy lento

**Síntoma:** Respuestas tardan mucho

**Soluciones:**

1. **Reducir top-k:**
   - Configuración → RAG Settings
   - Reducir Top K a 3-5

2. **Verificar conexión:**
   - Velocidad de internet
   - Latencia a APIs

3. **Reiniciar aplicación:**
   ```bash
   # Ctrl+C para detener
   python run.py
   ```

---

## ⚙️ Problemas de Configuración

### Configuración no se guarda

**Síntoma:** Cambios en configuración no persisten

**Soluciones:**

1. **Verificar permisos del archivo:**
   ```bash
   # Windows
   icacls data\config.json
   
   # Linux/Mac
   ls -la data/config.json
   ```

2. **Verificar espacio en disco:**
   ```bash
   df -h  # Linux/Mac
   ```

3. **Revisar logs:**
   ```bash
   grep "config" data/logs/application.log
   ```

---

### Tema no cambia

**Síntoma:** Al cambiar tema, no se aplica

**Solución:**
- Recargar página (F5)
- Limpiar caché del navegador (Ctrl+Shift+Del)

---

## 🔌 Errores de API/LLM

### "LLM Provider Failed"

**Síntoma:** Error al intentar usar el chat

**Soluciones:**

1. **Verificar API key válida:**
   ```bash
   # En .env
   GEMINI_API_KEY=AIza...
   
   # Debe empezar con AIza para Gemini
   ```

2. **Verificar cuota de API:**
   - Ir a [Google AI Studio](https://makersuite.google.com/)
   - Verificar que no alcanzaste el límite

3. **Probar fallback:**
   - Si Gemini falla, debería usar Cohere
   - Verificar: `COHERE_API_KEY` en `.env`

4. **Test manual:**
   - Admin Panel → Testing
   - Probar ambos proveedores

---

### "Rate limit exceeded"

**Síntoma:** Error de límite de tasa alcanzado

**Causa:** Demasiadas consultas en poco tiempo

**Solución:**
- Esperar 1 minuto
- Reducir frecuencia de consultas
- Actualizar a tier pagado de API

---

### Gemini API key inválida

**Síntoma:** "Invalid API key" o "Authentication failed"

**Solución:**
1. Generar nueva API key:
   - Ir a [Google AI Studio](https://makersuite.google.com/app/apikey)
   - Create API key
   
2. Copiar key a `.env`:
   ```bash
   GEMINI_API_KEY=tu_nueva_key_aqui
   ```

3. Reiniciar aplicación

---

## 🐌 Problemas de Rendimiento

### Aplicación muy lenta

**Soluciones:**

1. **Reducir top-k:**
   - Configuración → Top K: 3-5

2. **Limpiar ChromaDB:**
   - Admin Panel → Indexación
   - "Limpiar Todos los Índices" (⚠️ destructivo)
   - Re-indexar documentos necesarios

3. **Reiniciar aplicación:**
   ```bash
   # Detener (Ctrl+C)
   python run.py
   ```

4. **Verificar recursos del sistema:**
   ```bash
   # Windows
   taskmgr
   
   # Linux/Mac
   top
   ```

---

### ChromaDB crece mucho

**Síntoma:** Carpeta `data/chromadb/` muy grande

**Solución:**
- Es normal si hay muchos documentos
- Para limpiar:
  1. Backup documentos importantes
  2. Admin Panel → "Limpiar Todos los Índices"
  3. Re-indexar solo necesarios

---

## 🔍 Mensajes de Error Comunes

### "Knowledge Library is Empty"

**Significa:** No hay documentos indexados

**Solución:**
1. Ir a Biblioteca de Conocimiento
2. Subir al menos un documento
3. Esperar a que se indexe

---

### "Document already exists"

**Significa:** Documento con ese nombre ya existe

**Solución:**
- Renombrar archivo antes de subir
- O eliminar el documento existente primero

---

### "Indexing failed"

**Posibles causas:**
- Archivo corrupto
- Formato no soportado
- Sin texto extraíble (PDF escaneado)
- Falta de espacio en disco

**Solución:** Revisar logs específicos

---

## 📝 Cómo Reportar un Problema

Si ninguna solución funciona:

1. **Recopilar información:**
   ```bash
   # Últimas líneas del log
   tail -100 data/logs/application.log > error_log.txt
   ```

2. **Incluir en reporte:**
   - Versión de Python: `python --version`
   - Sistema operativo
   - Pasos para reproducir
   - Mensaje de error exacto
   - Log relevante (sin API keys)

3. **Reportar en:**
   - GitHub Issues: https://github.com/AlejandroMedina-Ar/Alura-Challenge-Agente-AI/issues

---

## 🆘 Último Recurso: Reset Completo

Si todo falla, reset completo:

```bash
# 1. Backup documentos importantes
# (copiar data/knowledge_library/documents/)

# 2. Detener aplicación (Ctrl+C)

# 3. Eliminar datos
Remove-Item -Recurse data\chromadb\*  # Windows
Remove-Item -Recurse data\knowledge_library\*
Remove-Item data\config.json

# Linux/Mac:
# rm -rf data/chromadb/*
# rm -rf data/knowledge_library/*
# rm data/config.json

# 4. Re-ejecutar setup
python setup.py

# 5. Reiniciar app
python run.py

# 6. Re-subir e indexar documentos
```

---

**Versión:** 1.0.0  
**Última Actualización:** Julio 2026
