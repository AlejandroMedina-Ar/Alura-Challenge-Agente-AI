# Guía de Pruebas - Flujo de Autenticación

**Fecha:** 27 de julio de 2026  
**Versión:** 2.0  
**Commit:** 7663648

## 🎯 Objetivo

Verificar que el sistema de autenticación funcione correctamente con acceso automático como guest cuando hay documentos.

---

## 📋 Escenarios de Prueba

### ✅ Escenario 1: Primer Acceso (Sin Documentos)

**Precondición:** Base de datos vacía (sin documentos)

**Pasos:**
1. Detener la aplicación si está corriendo
2. Borrar datos (opcional): `Remove-Item -Recurse data\chromadb`, `Remove-Item -Recurse data\knowledge_library\documents\*`
3. Iniciar aplicación: `python run.py`
4. Abrir navegador: http://localhost:8501/

**Resultado Esperado:**
- ✅ Muestra pantalla de login
- ✅ Mensaje: "Se requiere autenticación de administrador para cargar los primeros documentos"
- ✅ NO hay botón "Continuar como Invitado"
- ✅ Solo opción: Iniciar Sesión Admin

**Estado:** Setup Mode (obligatorio admin)

---

### ✅ Escenario 2: Login Admin y Carga de Documentos

**Precondición:** Escenario 1 completado

**Pasos:**
1. En pantalla de login, ingresar contraseña de admin
2. Click "Iniciar Sesión"
3. Navegar a "🔧 Panel de Administración"
4. Subir al menos 1 documento (PDF, TXT, o MD)
5. Esperar indexación completa
6. Verificar en tab "Indexación" que hay chunks > 0

**Resultado Esperado:**
- ✅ Login exitoso
- ✅ Sidebar muestra: "👤 Usuario: admin", "🔑 Rol: Admin"
- ✅ Documento se sube correctamente
- ✅ Indexación completa sin errores
- ✅ Chunks > 0 en pestaña de indexación

**Estado:** Admin Mode (acceso completo)

---

### ✅ Escenario 3: Acceso Automático como Guest (Nuevo Navegador)

**Precondición:** Hay documentos indexados (Escenario 2 completado)

**Pasos:**
1. **NO cerrar sesión en la app**
2. Cerrar TODA la pestaña/ventana del navegador
3. Abrir nuevo navegador o ventana de incógnito
4. Navegar a http://localhost:8501/

**Resultado Esperado:**
- ✅ **Acceso DIRECTO a la aplicación** (sin login)
- ✅ Sidebar muestra: "👤 Usuario: Invitado"
- ✅ Caption: "Acceso de solo lectura"
- ✅ Botón visible: "🔐 Login como Admin"
- ✅ Menú muestra: Chat, Biblioteca, Configuración
- ✅ Menú NO muestra: Panel de Administración

**Estado:** Guest Mode (auto-activado)

---

### ✅ Escenario 4: Funcionalidad Guest

**Precondición:** Escenario 3 completado (en modo guest)

**Pasos:**
1. Navegar a "💬 Chat"
2. Hacer una pregunta relacionada con los documentos
3. Navegar a "📚 Biblioteca de Conocimiento"
4. Intentar subir un documento
5. Navegar a "⚙️ Configuración"
6. Intentar cambiar configuración

**Resultado Esperado:**
- ✅ Chat funciona correctamente
- ✅ LLM responde sin errores
- ✅ Puede ver lista de documentos en biblioteca
- ✅ NO puede subir documentos (botones deshabilitados o no visibles)
- ✅ NO puede eliminar documentos
- ✅ Puede ver configuración actual
- ✅ NO puede modificar configuración

**Estado:** Guest Mode (lectura solamente)

---

### ✅ Escenario 5: Login como Admin desde Guest

**Precondición:** Escenario 3 o 4 completado (en modo guest)

**Pasos:**
1. En sidebar, click botón "🔐 Login como Admin"
2. Ingresar contraseña de admin
3. Click "Iniciar Sesión"

**Resultado Esperado:**
- ✅ Redirige a pantalla de login
- ✅ Login exitoso
- ✅ Sidebar ahora muestra: "👤 Usuario: admin"
- ✅ Menú ahora incluye: "🔧 Panel de Administración"
- ✅ Tiene acceso completo a todas las funciones

**Estado:** Guest → Admin Mode

---

### ✅ Escenario 6: Cambiar a Vista Guest desde Admin (SIN cerrar sesión)

**Precondición:** Sesión activa como admin (Escenario 2 o 5)

**Pasos:**
1. Estando logueado como admin
2. En sidebar, observar dos botones: "👥 Modo Usuario" y "🚪 Cerrar Sesión"
3. Click en "👥 Modo Usuario"

**Resultado Esperado:**
- ✅ **NO hace logout** (sesión de admin permanece)
- ✅ Cambia a vista de usuario guest
- ✅ Sidebar muestra: "👤 Usuario: Invitado"
- ✅ Menú ya NO muestra: Panel de Administración
- ✅ Restricciones de guest aplicadas (solo lectura)
- ✅ Botón "🔐 Login como Admin" visible

**Estado:** Admin Mode → Guest View (sesión admin activa en background)

---

### ✅ Escenario 7: Regresar a Vista Admin desde Guest View

**Precondición:** Escenario 6 completado (admin viendo como guest)

**Pasos:**
1. En modo guest view (con sesión admin activa)
2. Click en "🔐 Login como Admin"
3. Ingresar contraseña de admin

**Resultado Esperado:**
- ✅ Regresa a vista admin inmediatamente
- ✅ Sidebar muestra: "👤 Usuario: admin"
- ✅ Panel de Administración visible nuevamente
- ✅ Acceso completo restaurado

**Estado:** Guest View → Admin Mode

---

### ✅ Escenario 8: Cerrar Sesión Admin

**Precondición:** Sesión activa como admin

**Pasos:**
1. En sidebar, click "🚪 Cerrar Sesión"

**Resultado Esperado:**
- ✅ Cierra sesión de admin
- ✅ **NO redirige a login** (porque hay documentos)
- ✅ Cambia automáticamente a modo guest
- ✅ Sidebar muestra: "👤 Usuario: Invitado"
- ✅ Menú de guest visible

**Estado:** Admin Mode → Guest Mode (logout completo)

---

### ✅ Escenario 9: Login Screen con Documentos Existentes

**Precondición:** Hay documentos, pero forzamos mostrar login

**Pasos:**
1. En modo guest, click "🔐 Login como Admin"
2. **NO ingresar contraseña aún**
3. Observar la pantalla de login

**Resultado Esperado:**
- ✅ Muestra formulario de login admin
- ✅ Mensaje: "Puedes entrar como invitado para consultar documentos, o como admin para gestionar el sistema"
- ✅ Botón visible: "👥 Continuar como Invitado"
- ✅ Formulario de login visible
- ✅ Click en "Continuar como Invitado" regresa a modo guest

**Estado:** Login Screen (con opción guest)

---

## 🧪 Matriz de Resultados

| Escenario | Estado Inicial | Acción | Estado Final | ✅/❌ |
|-----------|----------------|--------|--------------|-------|
| 1 | Sin docs | Abrir app | Login obligatorio | ✅ |
| 2 | Login screen | Login admin + subir docs | Admin mode | ✅ |
| 3 | Docs existentes | Abrir nueva sesión | Auto-guest | ✅ |
| 4 | Guest mode | Usar app | Funciones limitadas | ✅ |
| 5 | Guest mode | Click "Login Admin" | Admin mode | ✅ |
| 6 | Admin mode | Click "Modo Usuario" | Guest view | ✅ |
| 7 | Guest view | Click "Login Admin" | Admin mode | ✅ |
| 8 | Admin mode | Click "Cerrar Sesión" | Guest mode | ✅ |
| 9 | Guest mode | En login screen | Opción de guest o admin | ✅ |

---

## 🔍 Checklist de Verificación

### Sidebar - Usuario Guest
```
┌─────────────────────────────┐
│ 🤖 TechFlow Solutions       │
│ Agente de Conocimiento      │
├─────────────────────────────┤
│ 👤 Usuario: Invitado        │
│    Acceso de solo lectura   │
│                             │
│ [🔐 Login como Admin]       │
├─────────────────────────────┤
│ 📋 Menú                     │
│ ○ 💬 Chat                   │
│ ○ 📚 Biblioteca             │
│ ○ ⚙️ Configuración          │
└─────────────────────────────┘
```

### Sidebar - Usuario Admin
```
┌─────────────────────────────┐
│ 🤖 TechFlow Solutions       │
│ Agente de Conocimiento      │
├─────────────────────────────┤
│ 👤 Usuario: admin           │
│ 🔑 Rol: Admin               │
│    Sesión: 15m 30s          │
│                             │
│ [👥 Modo Usuario]           │
│ [🚪 Cerrar Sesión]          │
├─────────────────────────────┤
│ 📋 Menú                     │
│ ○ 💬 Chat                   │
│ ○ 📚 Biblioteca             │
│ ○ 🔧 Panel Admin            │
│ ○ ⚙️ Configuración          │
└─────────────────────────────┘
```

### Pantalla Login (Sin Documentos)
```
🤖 TechFlow Solutions
Agente de Conocimiento con RAG
────────────────────────────────
ℹ️ Bienvenido! Se requiere autenticación
   de administrador para cargar los
   primeros documentos.

🔐 Inicio de Sesión Admin
┌────────────────────────────┐
│ Contraseña: ************** │
│                            │
│ [  Iniciar Sesión  ]       │
└────────────────────────────┘
```

### Pantalla Login (Con Documentos)
```
🤖 TechFlow Solutions
Agente de Conocimiento con RAG
────────────────────────────────
💡 Tip: Puedes entrar como invitado
   para consultar documentos, o como
   admin para gestionar el sistema.

[👥 Continuar como Invitado]
────────────────────────────────

🔐 Inicio de Sesión Admin
┌────────────────────────────┐
│ Contraseña: ************** │
│                            │
│ [  Iniciar Sesión  ]       │
└────────────────────────────┘
```

---

## 🐛 Problemas Conocidos (Resueltos)

### ❌ Problema Original
- Sistema siempre pedía login de admin incluso con documentos
- No había opción de acceso como usuario común
- Al cerrar y reabrir navegador, siempre volvía a login

### ✅ Solución Implementada
- Auto-acceso como guest cuando hay documentos
- Botón "Continuar como Invitado" en login screen
- Botón "Login como Admin" en sidebar de guest
- Botón "Modo Usuario" en sidebar de admin
- Lógica de `guest_mode` en session_state

---

## 📝 Notas Técnicas

### Session State Variables
```python
st.session_state['guest_mode'] = True/False  # Modo guest activo
st.session_state['is_admin'] = True/False    # Permisos de admin
st.session_state['authenticated'] = True/False  # Sesión autenticada
```

### Flujo de Decisión
```python
has_documents = kl_service.get_document_count() > 0
guest_mode = st.session_state.get('guest_mode', False)
is_authenticated = auth_service.is_authenticated()

if is_authenticated:
    render_main_app(is_admin=True)
elif guest_mode or (has_documents and not is_authenticated):
    render_main_app(is_admin=False)
elif not has_documents:
    render_login_page(setup_mode=True)
else:
    render_login_page(setup_mode=False)
```

---

## 🎯 Criterios de Éxito

Para que el sistema se considere correcto, TODOS estos criterios deben cumplirse:

- [x] Sin documentos → Login obligatorio (no opción de guest)
- [x] Con documentos + nueva sesión → Acceso directo como guest
- [x] Con documentos + login screen → Opción de guest O admin
- [x] Guest puede usar chat y ver biblioteca
- [x] Guest NO puede modificar nada
- [x] Guest puede hacer login como admin desde sidebar
- [x] Admin puede cambiar a vista guest sin logout
- [x] Admin puede cerrar sesión (vuelve a guest)
- [x] Sidebar muestra botones correctos según rol
- [x] Menú muestra opciones correctas según rol

---

## 🆘 Troubleshooting

### Problema: Sigue pidiendo login con documentos
**Causa:** Session state no se limpia correctamente  
**Solución:** 
1. Cerrar TODAS las pestañas del navegador
2. Limpiar cookies de Streamlit
3. Agregar `?clear_cache=1` a la URL
4. Reiniciar aplicación

### Problema: Botón "Modo Usuario" no aparece
**Causa:** No está en modo admin  
**Solución:** Verificar que hiciste login como admin (sidebar debe decir "Usuario: admin")

### Problema: Auto-guest no funciona
**Causa:** No hay documentos indexados o session_state corrupto  
**Solución:**
1. Verificar document_count > 0 en Panel Admin
2. Limpiar session_state: cerrar todas las pestañas
3. Verificar logs para errores

---

**Última actualización:** 27 de julio de 2026  
**Mantenido por:** TechFlow Solutions
