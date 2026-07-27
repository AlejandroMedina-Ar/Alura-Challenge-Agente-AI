# Guía de Inicio del Proyecto

**Fecha:** 2026-07-27  
**Propósito:** Diferentes formas de iniciar la aplicación TechFlow RAG Agent

---

## 🚀 Formas de Iniciar la Aplicación

### **Opción 1: Usar run.py (Recomendado)** ✅

Este script hace verificaciones previas antes de iniciar:

```bash
python run.py
```

**Ventajas:**
- ✅ Verifica versión de Python
- ✅ Verifica que Streamlit esté instalado
- ✅ Verifica que el setup se haya ejecutado
- ✅ Configura automáticamente los parámetros de Streamlit

---

### **Opción 2: Streamlit desde el root del proyecto** ✅

```bash
streamlit run src/app.py
```

**Ventajas:**
- ✅ Comando estándar de Streamlit
- ✅ Funciona correctamente gracias al fix en app.py

---

### **Opción 3: Streamlit con parámetros personalizados** ✅

Para producción o cuando necesites control total:

```bash
streamlit run src/app.py \
  --server.port 8501 \
  --server.address 0.0.0.0 \
  --server.headless true \
  --browser.gatherUsageStats false
```

**Parámetros útiles:**
- `--server.port XXXX` - Cambiar puerto (default: 8501)
- `--server.address 0.0.0.0` - Permitir acceso remoto
- `--server.headless true` - Modo sin interfaz (servidores)
- `--browser.gatherUsageStats false` - Deshabilitar telemetría

---

### **Opción 4: Desde el directorio src/** ❌ NO RECOMENDADO

```bash
cd src
streamlit run app.py
```

**⚠️ NO usar este método:**
- Los paths relativos fallarán
- No encontrará `data/` correctamente
- Puede causar errores de configuración

**Siempre ejecutar desde el root del proyecto.**

---

## 🔧 Solución de Problemas

### Error: `ModuleNotFoundError: No module named 'src'`

**Causa:** Python no encuentra el módulo `src` en el path.

**Solución:** Ya está corregido en `src/app.py`. Asegúrate de tener la última versión:

```bash
git pull origin main
```

El archivo `app.py` ahora incluye:
```python
import sys
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
```

---

### Error: `FileNotFoundError: data/config.json`

**Causa:** No se ejecutó el setup.

**Solución:**
```bash
python setup.py
```

---

### Error: Streamlit no abre el navegador

**Causa:** Puede estar en modo headless o ya hay una instancia corriendo.

**Solución:**
1. Verificar si ya hay una instancia en http://localhost:8501
2. Si no abre automáticamente, abrir manualmente: http://localhost:8501
3. Para forzar apertura del navegador, eliminar `--server.headless=true`

---

### Puerto 8501 ya en uso

**Causa:** Otra instancia de Streamlit está corriendo.

**Solución 1:** Cerrar la instancia anterior (Ctrl+C en la terminal)

**Solución 2:** Usar otro puerto:
```bash
streamlit run src/app.py --server.port 8502
```

---

## 📋 Checklist de Pre-inicio

Antes de iniciar la aplicación, verifica:

- [ ] Python 3.9+ instalado
- [ ] Dependencias instaladas (`pip install -r requirements.txt`)
- [ ] Archivo `.env` creado (o copiado de `.env.example`)
- [ ] Setup ejecutado (`python setup.py`)
- [ ] API keys configuradas en `.env` (GEMINI_API_KEY o COHERE_API_KEY)

---

## 🔐 Primer Inicio

Al iniciar por primera vez:

1. La aplicación se abrirá en http://localhost:8501
2. Verás la pantalla de login
3. **Contraseña por defecto:** La configurada en `.env` (variable `ADMIN_PASSWORD`)
4. Si no configuraste contraseña, revisar logs para ver la contraseña default

---

## 🌐 Acceso Remoto

Para permitir acceso desde otra computadora en la red:

```bash
streamlit run src/app.py --server.address 0.0.0.0
```

Luego acceder desde otra computadora:
```
http://<IP-DE-TU-COMPUTADORA>:8501
```

**Obtener tu IP:**
- Windows: `ipconfig` (buscar "IPv4 Address")
- Linux/Mac: `ifconfig` o `ip addr`

---

## 🐳 Docker (Futuro)

> **Nota:** Docker support está planeado pero aún no implementado.

Cuando esté disponible:
```bash
docker-compose up
```

---

## 📝 Notas Importantes

1. **Siempre ejecutar desde el root del proyecto**
   ```
   ✅ CORRECTO: /path/to/Alura-Challenge-Agente-AI$ streamlit run src/app.py
   ❌ INCORRECTO: /path/to/Alura-Challenge-Agente-AI/src$ streamlit run app.py
   ```

2. **El archivo `.streamlit/config.toml` contiene configuración por defecto**
   - Puedes modificarlo para cambiar tema, puerto, etc.
   - No commitearlo si contiene configuración local específica

3. **Logs de la aplicación:**
   - Se guardan en `data/logs/application.log`
   - Útiles para debugging

4. **ChromaDB:**
   - Se inicializa en `data/chromadb/`
   - Se crea automáticamente en el primer indexado

---

## 🆘 Soporte

Si sigues teniendo problemas:

1. Revisar [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
2. Revisar [FAQ.md](FAQ.md)
3. Ejecutar `python test_integration.py` para diagnosticar
4. Revisar logs en `data/logs/application.log`

---

**Última actualización:** 2026-07-27  
**Mantenido por:** TechFlow Solutions Team
