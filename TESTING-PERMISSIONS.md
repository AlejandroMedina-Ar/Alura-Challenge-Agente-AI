# 🔒 Testing de Permisos - Guest vs Admin

**Fecha:** 27 de julio de 2026  
**Commit:** cc91f9e  
**Prioridad:** 🔴 CRÍTICO

---

## 🎯 Objetivo

Verificar que usuarios Guest NO puedan realizar operaciones de administración:
- ❌ Subir documentos
- ❌ Eliminar documentos
- ❌ Indexar/reindexar documentos
- ❌ Modificar configuración
- ✅ Solo lectura y chat

---

## 🧪 Tests de Verificación

### ✅ Test 1: Vista de Biblioteca (Guest)

**Pasos:**
```bash
1. Acceder como guest (sin login)
2. Ir a "📚 Biblioteca de Conocimiento"
3. Observar la interfaz
```

**Resultado esperado:**
```
✅ Título: "📚 Biblioteca de Conocimiento"
✅ Caption: "Estadísticas de la biblioteca"
✅ Mensaje: "🔒 Acceso Restringido: La gestión de documentos requiere permisos admin"
✅ Mensaje: "💡 Como invitado puedes: Consultar usando Chat, Ver estadísticas"
✅ Sección "📊 Estadísticas de la Biblioteca"
✅ Métricas: Total Documentos, Documentos Indexados, Tamaño Total
✅ Botón: "Iniciar Sesión como Administrador"
❌ NO aparece lista de documentos
❌ NO aparece uploader
❌ NO aparecen botones de gestión
```

**Vista esperada:**
```
📚 Biblioteca de Conocimiento
Estadísticas de la biblioteca

🔒 Acceso Restringido: La gestión de documentos 
   requiere permisos de administrador.

💡 Como usuario invitado, puedes:
   - Consultar documentos usando el 💬 Chat
   - Ver estadísticas de la biblioteca abajo

────────────────────────────────────────────

📊 Estadísticas de la Biblioteca

┌──────────────┬──────────────────┬──────────────┐
│ Total Docs   │ Docs Indexados   │ Tamaño Total │
│      3       │        3         │   2.4 MB     │
└──────────────┴──────────────────┴──────────────┘

────────────────────────────────────────────

🔐 ¿Necesitas gestionar documentos?

[  Iniciar Sesión como Administrador  ]
```

---

### ✅ Test 2: Botón Login Admin (Guest)

**Pasos:**
```bash
1. Como guest, en sidebar
2. Click en "🔐 Login como Admin"
3. Observar comportamiento
```

**Resultado esperado:**
```
✅ Redirige a pantalla de login
✅ Muestra formulario de login admin
✅ Input de contraseña visible
✅ Botón "Iniciar Sesión" visible
✅ SI hay docs: Botón "👥 Continuar como Invitado" visible
❌ NO vuelve automáticamente a guest
```

**Flujo completo:**
```
Guest → Click "Login Admin" → Login Page → Ingresar password → Admin Mode
```

---

### ✅ Test 3: Panel de Administración (Guest)

**Pasos:**
```bash
1. Como guest, buscar en sidebar "🔧 Panel de Administración"
```

**Resultado esperado:**
```
❌ NO aparece en el menú del sidebar

Sidebar Guest:
┌──────────────────────────┐
│ 👤 Usuario: Invitado     │
│    Acceso de solo lectura│
│ [🔐 Login como Admin]    │
├──────────────────────────┤
│ 📋 Menú                  │
│ ○ 💬 Chat                │
│ ○ 📚 Biblioteca          │  ← Sin botones
│ ○ ⚙️ Configuración       │  ← Read-only
└──────────────────────────┘
```

---

### ✅ Test 4: Settings Panel (Guest)

**Pasos:**
```bash
1. Como guest, ir a "⚙️ Configuración"
2. Intentar cambiar configuración LLM
3. Click "💾 Guardar Configuración LLM"
```

**Resultado esperado:**
```
✅ Aparece banner: "👁️ Modo de solo lectura: Estás viendo..."
✅ Puede ver configuración actual
❌ Al guardar: "🔒 Esta operación requiere permisos de administrador"
❌ Configuración NO se modifica
```

---

### ✅ Test 5: Vista de Biblioteca (Admin)

**Pasos:**
```bash
1. Login como admin
2. Ir a "📚 Biblioteca de Conocimiento"
3. Observar la interfaz
```

**Resultado esperado:**
```
✅ Aparece sección "⬆️ Subir Documento"
✅ File uploader visible
✅ Lista de documentos con botones:
   - 🗑️ Eliminar (columna 2)
   - ⚡ Indexar / 🔄 Re-indexar (columna 3)
```

**Vista esperada:**
```
📚 Gestión de Documentos

⬆️ Subir Documento
[Selecciona un documento]
📎 Arrastra archivo aquí o haz click

─────────────────────────────────

📄 Documentos Subidos

┌──────────────────────┬────────────┬──────────────┐
│ 📄 manual.pdf        │ [🗑️ Elim] │ [🔄 Reindex] │
│ 245.3 KB | 2026-07-27│            │              │
│ ✅ Indexado (42)     │            │              │
└──────────────────────┴────────────┴──────────────┘
```

---

### ✅ Test 6: Panel Admin (Admin)

**Pasos:**
```bash
1. Como admin, ir a "🔧 Panel de Administración"
2. Navegar por las tabs
```

**Resultado esperado:**
```
✅ Tab "📊 Dashboard": Accesible
✅ Tab "📚 Documentos": Upload + botones visibles
✅ Tab "⚡ Indexación": Accesible
✅ Tab "🧪 Pruebas": Accesible
```

---

### ✅ Test 7: Tab Indexación (Guest desde Admin Panel)

**NOTA:** Este test solo aplica si un guest de alguna forma accede al admin panel (no debería poder).

**Pasos:**
```bash
1. Como guest, intentar ir a tab "⚡ Indexación"
```

**Resultado esperado:**
```
✅ Mensaje: "🔒 Esta sección requiere autenticación de administrador"
✅ Mensaje: "💡 Las operaciones de indexación están restringidas..."
❌ NO aparecen botones de operaciones batch
❌ NO aparecen estadísticas de indexación
```

---

### ✅ Test 8: Alternar entre Admin y Guest

**Pasos:**
```bash
1. Login como admin
2. Ir a Biblioteca → Verificar botones visibles
3. Click "👥 Modo Usuario" en sidebar
4. Verificar que botones desaparecen
5. Click "🔐 Login como Admin"
6. Login y verificar que botones reaparecen
```

**Resultado esperado:**
```
Como Admin:
✅ Botones visibles (Eliminar, Indexar)
✅ Upload visible

Como Guest (después de "Modo Usuario"):
❌ Botones NO visibles
❌ Upload NO visible

Después de re-login:
✅ Botones vuelven a aparecer
```

---

## 📊 Matriz de Permisos

| Función | Guest | Admin | Verificación |
|---------|-------|-------|--------------|
| **Ver documentos** | ❌ | ✅ | Solo stats para guest |
| **Subir documentos** | ❌ | ✅ | Uploader oculto/visible |
| **Eliminar documentos** | ❌ | ✅ | Botón oculto/visible |
| **Indexar documentos** | ❌ | ✅ | Botón oculto/visible |
| **Re-indexar documentos** | ❌ | ✅ | Botón oculto/visible |
| **Ver estadísticas biblioteca** | ✅ | ✅ | Métricas agregadas |
| **Ver settings** | ✅ | ✅ | Configuración visible |
| **Modificar settings** | ❌ | ✅ | Mensaje de error/éxito |
| **Usar chat** | ✅ | ✅ | Chat funcional |
| **Ver indexación** | ❌ | ✅ | Tab bloqueada/accesible |
| **Batch operations** | ❌ | ✅ | Botones no visibles |

---

## 🔒 Capas de Seguridad

### Capa 1: UI (Visibilidad)
```python
if is_admin:
    # Mostrar upload
    # Mostrar botones de acción
else:
    # Solo mostrar información
```

### Capa 2: Handlers (Validación)
```python
def handle_document_delete(...):
    is_admin = st.session_state.get(SessionKey.IS_ADMIN, False)
    if not is_admin:
        render_info_message("🔒 Requiere admin", "error")
        logger.warning("Unauthorized delete attempt")
        return
```

### Capa 3: Logs (Auditoría)
```
2026-07-27 14:23:45 - WARNING - Attempted to delete document without admin permissions
2026-07-27 14:24:12 - WARNING - Attempted to upload document without admin permissions
```

---

## 🐛 Si Falla Algún Test

### Debug: Verificar is_admin
```python
# Agregar temporalmente en admin_panel.py:
st.write(f"DEBUG: is_admin={st.session_state.get(SessionKey.IS_ADMIN, False)}")
```

### Debug: Verificar SessionKey
```python
# Verificar en Python console:
from src.config import SessionKey
print(SessionKey.IS_ADMIN)  # Debe ser "is_admin"
```

### Debug: Logs
```bash
# Buscar en logs intentos no autorizados:
grep "Attempted to" data/logs/application.log
```

---

## ✅ Checklist de Verificación

- [ ] **Test 1:** Guest ve documentos sin botones
- [ ] **Test 2:** Guest NO ve uploader
- [ ] **Test 3:** Guest NO ve Panel Admin en sidebar
- [ ] **Test 4:** Guest NO puede modificar settings
- [ ] **Test 5:** Admin ve uploader y botones
- [ ] **Test 6:** Admin accede a todas las tabs
- [ ] **Test 7:** Tab Indexación bloqueada para guest
- [ ] **Test 8:** Alternar admin/guest funciona

---

## 📝 Reporte de Estado

**Completar después de testing:**

```
Guest Permissions:
[ ] ✅ CORRECTO - Guest solo read-only
[ ] ❌ FALLA - Guest puede: __________

Admin Permissions:
[ ] ✅ CORRECTO - Admin acceso completo
[ ] ❌ FALLA - Admin no puede: __________

Alternar Modos:
[ ] ✅ CORRECTO - Permisos cambian correctamente
[ ] ❌ FALLA - Permisos no cambian
```

---

**Última actualización:** 27 de julio de 2026  
**Commit de prueba:** cc91f9e  
**Prioridad:** 🔴 VERIFICAR AHORA
