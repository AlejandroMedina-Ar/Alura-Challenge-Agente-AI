# Modelos LLM FREE Disponibles

## Fecha: 2026-07-27

## Resumen

Este documento lista los modelos LLM de **tier gratuito** disponibles para el proyecto TechFlow Solutions RAG Agent, incluyendo configuración correcta y limitaciones.

---

## 🤖 Arquitectura de LLM

```
┌─────────────────────────────────────────────────┐
│  TechFlow Solutions RAG Agent                   │
│                                                 │
│  ┌───────────────────────────────────────────┐ │
│  │  PRIMARY LLM                              │ │
│  │  Google Gemini 3.6 Flash (FREE)          │ │
│  │  - Modelo principal para chat             │ │
│  │  - Alta velocidad                         │ │
│  │  - 1M token context window                │ │
│  └───────────────────────────────────────────┘ │
│                                                 │
│  ┌───────────────────────────────────────────┐ │
│  │  FALLBACK LLM                             │ │
│  │  Cohere Command-R7B (FREE)                │ │
│  │  - Respaldo si Gemini falla               │ │
│  │  - Activado automáticamente               │ │
│  │  - 128K token context window              │ │
│  └───────────────────────────────────────────┘ │
└─────────────────────────────────────────────────┘
```

---

## 🔵 Google Gemini (PRIMARY)

### **Modelos FREE Disponibles**

| Modelo | Estado | Velocidad | Context Window | Recomendado |
|--------|--------|-----------|----------------|-------------|
| **`gemini-3.6-flash`** | ✅ Estable | Muy alta | 1M tokens | ✅ **SÍ** (recomendado) |
| **`gemini-3.5-flash-lite`** | ✅ Estable | Ultra alta | 1M tokens | ✅ Para baja latencia |
| ~~`gemini-1.5-flash`~~ | ❌ Deprecado | - | - | ❌ **NO** (usar 3.6) |

### **Configuración Recomendada**

```bash
# .env
GEMINI_API_KEY=tu-api-key-aqui
GEMINI_MODEL=gemini-3.6-flash
```

### **Obtener API Key (FREE)**

1. Ir a: https://makersuite.google.com/app/apikey
2. Hacer clic en "Create API Key"
3. Copiar la key (formato: `AIza...`)
4. Pegar en `.env`

### **Rate Limits (FREE Tier)**

- **Requests por minuto:** 15 RPM
- **Requests por día:** 1,500 RPD
- **Tokens por minuto:** 1,000,000 TPM
- **Tokens por día:** 1,500,000,000 TPD

### **Características**

✅ **Ventajas:**
- Completamente gratis
- Sin tarjeta de crédito requerida
- 1 millón de tokens de contexto
- Multilenguaje (español incluido)
- Muy rápido
- Excelente calidad de respuestas

❌ **Limitaciones:**
- Rate limits en tier gratuito
- Puede experimentar throttling en uso intensivo

---

## 🟠 Cohere (FALLBACK)

### **Modelos FREE Disponibles**

| Modelo | Estado | Velocidad | Context Window | Recomendado |
|--------|--------|-----------|----------------|-------------|
| **`command-r7b-12-2024`** | ✅ Estable | Alta | 128K tokens | ✅ **SÍ** |
| ~~`command-r`~~ | ❌ Deprecado | - | - | ❌ **NO USAR** |

### **Configuración Recomendada**

```bash
# .env
COHERE_API_KEY=tu-api-key-aqui
COHERE_MODEL=command-r7b-12-2024
```

### **⚠️ IMPORTANTE: command-r Deprecado**

```
❌ command-r fue REMOVIDO el 15 de Septiembre de 2025
✅ Usar command-r7b-12-2024 en su lugar
```

### **Obtener API Key (FREE)**

1. Ir a: https://dashboard.cohere.com/api-keys
2. Registrarse (gratis)
3. Crear API key en "API Keys" → "Create API Key"
4. Copiar la key
5. Pegar en `.env`

### **Rate Limits (FREE Tier - Trial)**

- **Requests por mes:** 1,000 requests
- **Trial endpoint calls:** 20 calls (se renueva mensualmente)

### **Características**

✅ **Ventajas:**
- Gratis para desarrollo/pruebas
- No requiere tarjeta de crédito
- 128K tokens de contexto
- Buen soporte multilenguaje
- Buena calidad de respuestas

❌ **Limitaciones:**
- **Solo 1,000 requests/mes** (mucho menos que Gemini)
- Trial endpoint tiene límite de 20 calls
- Después del trial, requiere plan de pago para producción

---

## ⚙️ Configuración en el Proyecto

### **Archivo: `.env`**

```bash
########################################################
# Proveedores de LLM
########################################################

# PRIMARY: Google Gemini (FREE)
GEMINI_API_KEY=AIza...tu-key-aqui
GEMINI_MODEL=gemini-3.6-flash

# FALLBACK: Cohere (FREE)
COHERE_API_KEY=tu-cohere-key-aqui
COHERE_MODEL=command-r7b-12-2024

########################################################
# Configuración de Chat
########################################################

TEMPERATURE=0.7
MAX_OUTPUT_TOKENS=2000
MAX_CONTEXT_TOKENS=8000
```

### **Archivo: `src/config/settings.py`**

```python
# Defaults (FREE tier models)
self.GEMINI_MODEL: str = os.getenv('GEMINI_MODEL', 'gemini-1.5-flash')
self.COHERE_MODEL: str = os.getenv('COHERE_MODEL', 'command-r7b-12-2024')
```

---

## 🔄 Lógica de Fallback

El sistema usa **fallback automático**:

```python
# 1. Intenta Gemini (primary)
try:
    response = gemini_provider.chat(query)
except RateLimitError:
    # 2. Si Gemini falla, usa Cohere (fallback)
    response = cohere_provider.chat(query)
```

### **Casos de Activación de Fallback:**

1. ✅ Gemini rate limit excedido (15 RPM)
2. ✅ Gemini API error (timeout, network)
3. ✅ Gemini API key inválida/expirada
4. ❌ **NO** se activa si ambos fallan → muestra error al usuario

---

## 📊 Comparación FREE Tier

| Característica | Gemini 1.5 Flash | Cohere Command-R7B |
|----------------|------------------|-------------------|
| **Costo** | Gratis | Gratis (trial) |
| **Requests/mes** | ~45,000 (1500/día) | 1,000 |
| **Context Window** | 1M tokens | 128K tokens |
| **Velocidad** | Muy alta | Alta |
| **Calidad** | Excelente | Buena |
| **Multilenguaje** | Excelente | Bueno |
| **Recomendado para** | Producción (low-med traffic) | Desarrollo/Fallback |

**Conclusión:** Gemini es **MUCHO mejor** para FREE tier (45,000 vs 1,000 requests/mes).

---

## 🚫 Modelos NO FREE (Evitar)

| Modelo | Proveedor | Problema |
|--------|-----------|----------|
| `command-r-plus` | Cohere | 💰 Requiere plan de pago |
| `command-r-plus-08-2024` | Cohere | 💰 Requiere plan de pago |
| `gpt-4` | OpenAI | 💰 Requiere plan de pago |
| `gpt-3.5-turbo` | OpenAI | 💰 Requiere plan de pago |

---

## 🧪 Testing de Modelos

### **Verificar que Gemini funciona:**

```python
from src.llm import get_gemini_provider

provider = get_gemini_provider()
response = provider.chat_completion([
    {'role': 'user', 'content': 'Hola, ¿cómo estás?'}
])
print(response)
```

### **Verificar que Cohere funciona:**

```python
from src.llm import get_cohere_provider

provider = get_cohere_provider()
response = provider.chat_completion([
    {'role': 'user', 'content': 'Hola, ¿cómo estás?'}
])
print(response)
```

### **Test de integración:**

```bash
python test_integration.py
```

**Output esperado:**
```
✅ Gemini working (0.5s)
✅ Cohere working (0.8s)
```

---

## 🔧 Troubleshooting

### **Problema: "Rate limit exceeded for Gemini"**

**Causa:** Has excedido 15 requests/minuto.

**Solución:**
1. Esperar 1 minuto
2. El sistema automáticamente usa Cohere como fallback
3. Reducir frecuencia de requests

### **Problema: "model 'command-r' was removed"**

**Causa:** Tu `.env` usa modelo deprecado.

**Solución:**
```bash
# Cambiar en .env:
COHERE_MODEL=command-r7b-12-2024
```

### **Problema: "API key invalid"**

**Causa:** API key incorrecta o no configurada.

**Solución:**
1. Verificar que la key está en `.env`
2. Verificar que no tiene espacios extra
3. Regenerar key si es necesario

### **Problema: Cohere "404 Not Found"**

**Causa:** Modelo no existe o es de pago.

**Solución:**
Usar solo modelos FREE:
- ✅ `command-r7b-12-2024`
- ❌ NO usar `command-r-plus`

---

## 📝 Recomendaciones

### **Para Desarrollo:**
```bash
GEMINI_MODEL=gemini-1.5-flash      # Principal
COHERE_MODEL=command-r7b-12-2024   # Fallback
```

### **Para Producción (Low Traffic):**
```bash
GEMINI_MODEL=gemini-1.5-flash      # Suficiente para < 1500 users/día
COHERE_MODEL=command-r7b-12-2024   # Respaldo de emergencia
```

### **Para Producción (High Traffic):**
Considerar planes de pago:
- Gemini: $0.075 / 1M input tokens
- Cohere: Planes desde $0.40 / 1M tokens

---

## ✅ Checklist de Configuración

- [ ] API key de Gemini configurada en `.env`
- [ ] Modelo Gemini: `gemini-1.5-flash`
- [ ] API key de Cohere configurada en `.env`
- [ ] Modelo Cohere: `command-r7b-12-2024`
- [ ] **NO** usar `command-r` (deprecado)
- [ ] **NO** usar `command-r-plus` (pago)
- [ ] Test de integración pasa correctamente
- [ ] Fallback funciona cuando Gemini falla

---

## 📚 Referencias

- **Gemini API:** https://ai.google.dev/pricing
- **Cohere Models:** https://docs.cohere.com/docs/models
- **Gemini Free Tier:** https://ai.google.dev/gemini-api/docs/models/gemini
- **Cohere Free Trial:** https://cohere.com/pricing

---

**Fecha de Actualización:** 2026-07-27  
**Modelos Verificados:** ✅ Todos FREE tier confirmados
