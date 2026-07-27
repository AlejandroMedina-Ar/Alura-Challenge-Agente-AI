# Migración del SDK de Gemini

## Fecha: 2026-07-27

## 🚨 Cambio Crítico: Nuevo SDK Oficial de Google

Google ha **deprecado** el SDK `google-generativeai` y lo ha reemplazado con el **nuevo SDK oficial** `google-genai` desde el lanzamiento de Gemini 2.0 a finales de 2024.

---

## 📋 Resumen del Cambio

| Aspecto | Antes (Deprecado) | Ahora (Oficial) |
|---------|-------------------|-----------------|
| **Librería** | `google-generativeai` | `google-genai` |
| **Instalación** | `pip install google-generativeai` | `pip install google-genai` |
| **Import** | `import google.generativeai as genai` | `from google import genai` |
| **Arquitectura** | GenerativeModel directo | Client object centralizado |
| **Generación** | `model.generate_content()` | `client.models.generate_content()` |
| **Streaming** | `model.generate_content(stream=True)` | `client.models.generate_content_stream()` |
| **Estado** | ⚠️ Deprecado | ✅ Oficial y soportado |

---

## 🔍 Por Qué Este Cambio

### **Problema Original**

El proyecto usaba `google-generativeai>=0.8.0` que está deprecado y causaba:

```
404 models/gemini-1.5-flash is not found for API version v1beta
```

### **Causa Raíz**

Google cambió completamente la arquitectura del SDK con Gemini 2.0. El viejo SDK ya no funciona correctamente con los modelos actuales.

### **Solución**

Migrar al nuevo SDK oficial `google-genai` que es la única forma soportada de usar Gemini API.

---

## 📦 Cambios en requirements.txt

### **Antes:**

```txt
# Google Gemini (proveedor LLM primario)
google-generativeai>=0.8.0
```

### **Ahora:**

```txt
# Google Gemini (proveedor LLM primario) - NUEVO SDK OFICIAL
google-genai>=1.0.0
```

---

## 🔧 Cambios en gemini_provider.py

### **Arquitectura Anterior (Deprecada)**

```python
import google.generativeai as genai

# Configurar API key globalmente
genai.configure(api_key=api_key)

# Crear modelo directamente
model = genai.GenerativeModel('gemini-1.5-flash')

# Generar contenido
response = model.generate_content(messages)

# Streaming
for chunk in model.generate_content(messages, stream=True):
    print(chunk.text)
```

### **Nueva Arquitectura (Oficial)**

```python
from google import genai
from google.genai import types

# Crear client centralizado
client = genai.Client(api_key=api_key)

# Generar contenido through client
response = client.models.generate_content(
    model='gemini-1.5-flash-latest',
    contents=messages,
    config=types.GenerateContentConfig(...)
)

# Streaming con método dedicado
for chunk in client.models.generate_content_stream(
    model='gemini-1.5-flash-latest',
    contents=messages,
    config=config
):
    print(chunk.text)
```

---

## 🎯 Cambios Clave en el Código

### **1. Import Statements**

```python
# ❌ Viejo (deprecado)
import google.generativeai as genai

# ✅ Nuevo (oficial)
from google import genai
from google.genai import types
```

### **2. Inicialización del Cliente**

```python
# ❌ Viejo
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-1.5-flash')

# ✅ Nuevo
client = genai.Client(api_key=api_key)
```

### **3. Generación de Contenido**

```python
# ❌ Viejo
response = model.generate_content(messages)

# ✅ Nuevo
response = client.models.generate_content(
    model='gemini-1.5-flash-latest',
    contents=messages
)
```

### **4. Streaming**

```python
# ❌ Viejo
for chunk in model.generate_content(messages, stream=True):
    yield chunk.text

# ✅ Nuevo
for chunk in client.models.generate_content_stream(
    model='gemini-1.5-flash-latest',
    contents=messages
):
    yield chunk.text
```

### **5. Configuración**

```python
# ❌ Viejo
model = genai.GenerativeModel(
    'gemini-1.5-flash',
    generation_config=genai.GenerationConfig(
        temperature=0.7,
        max_output_tokens=1000
    )
)

# ✅ Nuevo
config = types.GenerateContentConfig(
    temperature=0.7,
    max_output_tokens=1000
)

response = client.models.generate_content(
    model='gemini-1.5-flash-latest',
    contents=messages,
    config=config
)
```

### **6. Conteo de Tokens**

```python
# ❌ Viejo
result = model.count_tokens(text)
count = result.total_tokens

# ✅ Nuevo
response = client.models.count_tokens(
    model='gemini-1.5-flash-latest',
    contents=text
)
count = response.total_tokens
```

---

## ✅ Beneficios del Nuevo SDK

### **1. Arquitectura Mejorada**

- **Client Object Centralizado:** Todas las operaciones a través de un solo client
- **Gestión Consistente:** Credenciales y configuración en un solo lugar
- **Mejor Organización:** Servicios separados (`models`, `files`, `caches`, etc.)

### **2. Developer Experience**

- **API más clara:** Métodos explícitos y bien estructurados
- **Mejor documentación:** Documentación oficial actualizada
- **Type hints:** Mejor soporte de tipos con `types` module

### **3. Transición Simplificada**

- **Dev → Enterprise:** Más fácil migrar de Gemini API a Vertex AI
- **Código portátil:** Misma API para diferentes backends
- **Menos boilerplate:** Menos código repetitivo

### **4. Features Adicionales**

- **Streaming mejorado:** Método dedicado `generate_content_stream()`
- **Pydantic models:** Objetos retornados son clases pydantic
- **Async support:** Soporte completo para asyncio via `client.aio`

---

## 🧪 Testing de la Migración

### **Test Estructural**

```bash
python test_code_structure.py
```

**Resultado esperado:**
```
✅ src/llm/gemini_provider.py
Pass Rate: 6/6 (100%)
🎉 All code structure tests passed!
```

### **Test de Integración** (requiere dependencias instaladas)

```bash
pip install -r requirements.txt
python test_integration.py
```

---

## 📝 Instrucciones para el Usuario

### **1. Actualizar Código**

```bash
git pull origin main
```

### **2. Reinstalar Dependencias**

```bash
# Desinstalar SDK viejo
pip uninstall google-generativeai -y

# Instalar SDK nuevo
pip install -r requirements.txt
```

### **3. Verificar API Key**

Tu API key de Gemini sigue siendo la misma, pero asegúrate que esté en `.env`:

```bash
GEMINI_API_KEY=tu-api-key-aqui
GEMINI_MODEL=gemini-1.5-flash-latest
```

### **4. Ejecutar Aplicación**

```bash
python run.py
```

---

## 🔍 Troubleshooting

### **Error: "No module named 'google.genai'"**

**Causa:** No has instalado el nuevo SDK.

**Solución:**
```bash
pip install google-genai>=1.0.0
```

### **Error: "Client object has no attribute 'generate_content'"**

**Causa:** Estás usando sintaxis del viejo SDK.

**Solución:** El nuevo SDK usa `client.models.generate_content()` (nota el `.models`).

### **Error: "404 models/gemini-1.5-flash not found"**

**Causa:** Nombre de modelo incorrecto para el nuevo SDK.

**Solución:** Usa `gemini-1.5-flash-latest` en vez de `gemini-1.5-flash`.

### **Error: "google.generativeai conflicts with google.genai"**

**Causa:** Tienes ambos SDKs instalados.

**Solución:**
```bash
pip uninstall google-generativeai -y
pip install google-genai>=1.0.0
```

---

## 📚 Referencias

### **Documentación Oficial**

- **Guía de Migración:** https://ai.google.dev/gemini-api/docs/migrate
- **Documentación API:** https://ai.google.dev/gemini-api/docs
- **API Reference:** https://googleapis.github.io/python-genai/

### **Cambios Específicos**

- **Installation:** `pip install google-genai`
- **Import:** `from google import genai`
- **Client pattern:** `client = genai.Client(api_key=...)`
- **Generate:** `client.models.generate_content(...)`
- **Stream:** `client.models.generate_content_stream(...)`

---

## ⚖️ Comparación Completa

| Operación | SDK Viejo | SDK Nuevo |
|-----------|-----------|-----------|
| **Instalar** | `pip install google-generativeai` | `pip install google-genai` |
| **Import** | `import google.generativeai as genai` | `from google import genai` |
| **Config** | `genai.configure(api_key=...)` | `client = genai.Client(api_key=...)` |
| **Modelo** | `genai.GenerativeModel('gemini-1.5-flash')` | `client.models` (no objeto separado) |
| **Generar** | `model.generate_content(...)` | `client.models.generate_content(model=..., ...)` |
| **Stream** | `model.generate_content(..., stream=True)` | `client.models.generate_content_stream(...)` |
| **Tokens** | `model.count_tokens(...)` | `client.models.count_tokens(model=..., ...)` |
| **Files** | `genai.upload_file(...)` | `client.files.upload(...)` |
| **Caches** | `caching.CachedContent.create(...)` | `client.caches.create(...)` |

---

## 🎉 Conclusión

La migración al nuevo SDK oficial `google-genai` es **necesaria** para que Gemini funcione correctamente. Este cambio:

✅ **Soluciona** el error 404 de modelo no encontrado  
✅ **Usa** la API oficialmente soportada por Google  
✅ **Mejora** la arquitectura del código  
✅ **Facilita** el mantenimiento futuro  
✅ **Garantiza** compatibilidad con Gemini 2.0+  

El proyecto ahora está actualizado y listo para usar Gemini 1.5 Flash con el tier gratuito (45,000 requests/mes).

---

**Fecha de Migración:** 2026-07-27  
**SDK Anterior:** google-generativeai 0.8.0 (deprecado)  
**SDK Actual:** google-genai 1.0.0+ (oficial)  
**Estado:** ✅ COMPLETADO
