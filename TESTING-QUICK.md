# 🧪 Testing Rápido - Acceso Guest Automático

**Fecha:** 27 de julio de 2026  
**Commit:** d8803e7  
**Estado:** CRÍTICO - Verificar inmediatamente

---

## ⚠️ Problema Reportado

Al cargar libros, indexarlos, y volver a entrar:
- ❌ Sigue pidiendo login de admin
- ❌ No carga sesión de usuario ordinario automáticamente
- ❌ No hay opción visible para entrar como guest

---

## ✅ Solución Implementada

### Cambios en `src/app.py`:

**ANTES (lógica compleja que fallaba):**
```python
if auth_service.is_authenticated():
    render_main_app(is_admin=True)
elif guest_mode or (has_documents and not auth_service.is_authenticated()):
    # Lógica compleja que nunca se ejecutaba correctamente
    render_main_app(is_admin=False)
elif not has_documents:
    render_login_page(setup_mode=True)
else:
    render_login_page(setup_mode=False)  # ← Fallback problemático
```

**DESPUÉS (lógica simple que funciona):**
```python
if auth_service.is_authenticated():
    # Admin autenticado
    render_main_app(is_admin=True)
elif has_documents:
    # SIEMPRE permitir guest si hay documentos
    st.session_state[SessionKey.GUEST_MODE] = True
    render_main_app(is_admin=False)
else:
    # Sin documentos = setup requerido
    render_login_page(setup_mode=True)
```

**Clave:** Eliminado el `else` fallback que causaba que siempre pidiera login.

---

## 🧪 Test de Verificación

### Test 1: Primera Vez (Sin Documentos)
```bash
# Limpar datos (opcional)
Remove-Item -Recurse -Force data/chromadb
Remove-Item -Recurse -Force data/knowledge_library/documents/*

# Iniciar app
python run.py

# Abrir: http://localhost:8501/
```

**Resultado esperado:**
- ✅ Muestra login de admin obligatorio
- ✅ Mensaje: "Se requiere autenticación de administrador para cargar los primeros documentos"
- ✅ NO hay botón "Continuar como Invitado"

---

### Test 2: Subir Documentos
```bash
# En la app:
1. Login con contraseña de admin
2. Ir a "Panel de Administración"
3. Subir al menos 1 documento (PDF, TXT, MD)
4. Esperar que indexe
5. Verificar en tab "Indexación" que chunks > 0
```

**Resultado esperado:**
- ✅ Documento se sube y indexa correctamente
- ✅ Chunks > 0 en ChromaDB

---

### Test 3: Acceso Guest Automático (EL TEST CRÍTICO)
```bash
# IMPORTANTE: NO cerrar sesión, solo cerrar pestaña

1. Cerrar toda la pestaña del navegador (o ventana completa)
2. Esperar 5 segundos
3. Abrir navegador nuevo
4. Ir a: http://localhost:8501/
```

**Resultado esperado:**
- ✅ **Entra DIRECTO a la aplicación** (sin login)
- ✅ Sidebar muestra: "👤 Usuario: Invitado"
- ✅ Caption: "Acceso de solo lectura"
- ✅ Botón: "🔐 Login como Admin"
- ✅ Menú: Chat, Biblioteca, Configuración (SIN Panel Admin)

**SI FALLA:**
- Revisar logs en consola de Python
- Buscar: `"Auto-enabled guest mode (documents available)"`
- Buscar: `"Auth check: authenticated=False, has_documents=True"`

---

### Test 4: Funcionalidad Guest
```bash
1. Ir a "💬 Chat"
2. Hacer pregunta relacionada con documentos
3. Verificar respuesta del LLM
```

**Resultado esperado:**
- ✅ Chat funciona
- ✅ LLM responde sin error 404
- ✅ Respuesta basada en documentos

---

### Test 5: Login Admin desde Guest
```bash
1. Estando como guest, click "🔐 Login como Admin"
2. Ingresar contraseña
3. Click "Iniciar Sesión"
```

**Resultado esperado:**
- ✅ Login exitoso
- ✅ Sidebar: "👤 Usuario: admin"
- ✅ Aparece en menú: "🔧 Panel de Administración"

---

### Test 6: Modelos Gemini Correctos
```bash
1. Login como admin
2. Ir a "⚙️ Configuración"
3. Tab "🤖 Configuración LLM"
4. Proveedor: Gemini
5. Verificar modelos en dropdown
```

**Resultado esperado:**
- ✅ Modelos mostrados:
  - gemini-3.6-flash
  - gemini-3.5-flash-lite
- ❌ NO debe aparecer: gemini-1.5-flash, gemini-1.5-pro

---

## 🐛 Debugging

### Si sigue pidiendo login:

**1. Verificar que hay documentos:**
```python
# En Python console o en el código temporalmente:
from src.services import get_knowledge_library_service
kl_service = get_knowledge_library_service()
print(f"Document count: {kl_service.get_document_count()}")
```

**Debe mostrar:** `Document count: 1` (o más)

**2. Verificar session_state:**
```python
# Agregar temporalmente en app.py después de línea 96:
st.write("DEBUG:", {
    "authenticated": auth_service.is_authenticated(),
    "has_documents": has_documents,
    "guest_mode": guest_mode
})
```

**Debe mostrar:**
```
DEBUG: {'authenticated': False, 'has_documents': True, 'guest_mode': False}
```

**3. Verificar logs:**
```bash
# Buscar en la terminal donde corre la app:
# Debe aparecer:
"Auto-enabled guest mode (documents available)"
"Rendering main app as guest (is_admin=False)"
```

---

## 📊 Checklist de Verificación

- [ ] **Test 1:** Sin docs → Login obligatorio ✅
- [ ] **Test 2:** Subir docs → Indexación OK ✅
- [ ] **Test 3:** **Recargar → Guest automático** ✅ ← CRÍTICO
- [ ] **Test 4:** Chat funciona como guest ✅
- [ ] **Test 5:** Login admin desde guest ✅
- [ ] **Test 6:** Modelos Gemini 3.6 en UI ✅

---

## 🔧 Cambios Técnicos

### SessionManager Initialization
```python
def initialize_session_state():
    # NUEVO: Inicializar SessionManager
    from src.auth import get_session_manager
    session_manager = get_session_manager()
    session_manager.initialize_session()
```

### Lógica Simplificada
```python
# Orden de prioridad:
# 1. Autenticado → Admin
# 2. Hay docs → Guest (auto)
# 3. Sin docs → Setup

if is_authenticated():
    admin_mode()
elif has_documents:
    auto_guest_mode()  # ← SIEMPRE
else:
    setup_mode()
```

---

## 📝 Notas Importantes

1. **Session State se resetea:** Al cerrar pestaña, Streamlit limpia session_state. Por eso necesitamos auto-detectar.

2. **`has_documents` es la clave:** Si `> 0`, siempre permitir guest.

3. **No hay cache de autenticación:** Cada carga de página re-verifica estado.

4. **Logs ayudan:** Los logs de debug muestran exactamente qué path toma la lógica.

---

## ⚡ Si Todavía Falla

**Opción 1: Limpiar completamente**
```bash
# Detener app (Ctrl+C)
# Eliminar session state de Streamlit
Remove-Item -Recurse -Force ~/.streamlit

# Reiniciar app
python run.py
```

**Opción 2: Verificar archivos actualizados**
```bash
git status
git log --oneline -1
# Debe mostrar: d8803e7 fix: CRÍTICO - Corregir acceso automático guest
```

**Opción 3: Reinstalar dependencias**
```bash
pip install -r requirements.txt --force-reinstall
```

---

## 📞 Reporte de Estado

**Si funciona:**
```
✅ Test 3 PASÓ - Guest automático funciona
   - Documentos: X documentos
   - Acceso: Directo como guest
   - Sidebar: "Usuario: Invitado"
```

**Si falla:**
```
❌ Test 3 FALLÓ - Sigue pidiendo login
   - Documentos: X documentos
   - Comportamiento: [Describe qué ves]
   - Logs: [Copia logs relevantes]
```

---

**Última actualización:** 27 de julio de 2026  
**Commit de prueba:** d8803e7  
**Prioridad:** 🔴 CRÍTICO
