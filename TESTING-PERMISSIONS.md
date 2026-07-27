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
✅ Título: "📚 Gestión de Documentos"
❌ NO aparece sección "⬆️ Subir Documento"
✅ Aparece: "📄 Documentos Subidos"
✅ Lista de documentos visible
❌ NO aparecen botones: "🗑️ Eliminar", "⚡ Indexar", "🔄 Re-indexar"
✅ Solo información: nombre, tamaño, fecha, estado de indexación
```

**Vista esperada:**
```
📚 Gestión de Documentos

📄 Documentos Subidos

┌─────────────────────────────────────────┐
│ 📄 manual_empleado.pdf                  │
│ Tamaño: 245.3 KB | Subido: 2026-07-27  │
│ ✅ Indexado (42 fragmentos)             │
├─────────────────────────────────────────┤
│ 📄 politicas_ti.pdf                     │
│ Tamaño: 189.7 KB | Subido: 2026-07-27  │
│ ✅ Indexado (35 fragmentos)             │
└─────────────────────────────────────────┘
```

---

### ✅ Test 2: Intento de Subir Documento (Guest)

**Pasos:**
```bash
1. Como guest, ir a Biblioteca
2. Buscar sección "⬆️ Subir Documento"
```

**Resultado esperado:**
```
❌ Sección NO existe
❌ NO hay uploader visible
✅ Solo lista de documentos (read-only)
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
| **Ver documentos** | ✅ | ✅ | Lista visible |
| **Subir documentos** | ❌ | ✅ | Uploader oculto/visible |
| **Eliminar documentos** | ❌ | ✅ | Botón oculto/visible |
| **Indexar documentos** | ❌ | ✅ | Botón oculto/visible |
| **Re-indexar documentos** | ❌ | ✅ | Botón oculto/visible |
| **Ver dashboard** | ✅ | ✅ | Estadísticas visibles |
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
