# Hotfix: Modelo Gemini y Autenticación

**Fecha:** 27 de julio de 2026  
**Versión:** 1.0  
**Commit:** 68fe51c

## 🎯 Problemas Resueltos

### 1. Error 404 - Modelo Gemini Incorrecto

**Problema:**
```
404 NOT_FOUND: models/gemini-1.5-flash-latest is not found for API version v1beta
```

**Causa:**
- Google deprecó completamente los modelos Gemini 1.5
- La API ahora usa Gemini 3.x (lanzado en 2026)
- El modelo `gemini-1.5-flash-latest` ya no existe

**Solución:**
- Actualizado a `gemini-3.6-flash` (modelo estable actual)
- Alternativa disponible: `gemini-3.5-flash-lite` (más rápido y barato)

**Archivos modificados:**
- `src/config/settings.py` - Línea 97
- `src/llm/gemini_provider.py` - Línea 62
- `.env.example` - Líneas 22-25

---

### 2. Login Siempre Requerido

**Problema:**
- Al cerrar y reabrir la aplicación, siempre pedía contraseña de admin
- No había forma de acceder como usuario común
- Incluso con documentos indexados, requería autenticación

**Causa:**
- El flujo de autenticación no distinguía entre setup inicial y uso normal
- No existía concepto de "usuario guest"

**Solución Implementada:**

#### Flujo de Acceso Mejorado

```python
# Lógica implementada en src/app.py
has_documents = kl_service.get_document_count() > 0

if not has_documents and not is_authenticated():
    # SETUP MODE: Requiere login admin para cargar primeros documentos
    render_login_page(setup_mode=True)
else:
    # USER MODE: Permite acceso guest o admin
    render_main_app(is_admin=is_authenticated())
```

#### Comportamiento por Rol

| Rol | Acceso | Restricciones |
|-----|--------|---------------|
| **Guest** (sin login) | ✅ Chat<br>✅ Biblioteca (ver)<br>✅ Settings (ver) | ❌ Panel Admin<br>❌ Subir documentos<br>❌ Eliminar documentos<br>❌ Cambiar configuración |
| **Admin** (con login) | ✅ Acceso completo | - |

#### Interfaz de Usuario

**Sidebar - Usuario Guest:**
```
👤 Usuario: Invitado
   Acceso de solo lectura

[🔐 Login como Admin]

📋 Menú
○ 💬 Chat
○ 📚 Biblioteca de Conocimiento
○ ⚙️ Configuración
```

**Sidebar - Usuario Admin:**
```
👤 Usuario: admin
🔑 Rol: Admin
   Sesión: 15m 30s

[🚪 Cerrar Sesión]

📋 Menú
○ 💬 Chat
○ 📚 Biblioteca de Conocimiento
○ 🔧 Panel de Administración
○ ⚙️ Configuración
```

**Archivos modificados:**
- `src/app.py` - Líneas 73-81, 87-134
- `src/ui/sidebar.py` - Líneas 35-48, 73-95

---

## 📦 Instalación de Cambios

### 1. Actualizar Código

```bash
git pull origin main
```

### 2. Actualizar Variables de Entorno

Edita tu archivo `.env` y actualiza la línea del modelo Gemini:

```bash
# ANTES (incorrecto)
GEMINI_MODEL=gemini-1.5-flash-latest

# DESPUÉS (correcto)
GEMINI_MODEL=gemini-3.6-flash
```

**Modelos Gemini 3.x disponibles:**
- `gemini-3.6-flash` - Recomendado ($1.50/1M input, $7.50/1M output)
- `gemini-3.5-flash-lite` - Más rápido y barato ($0.30/1M input, $2.50/1M output)

### 3. Reiniciar Aplicación

```bash
# Si está corriendo, detener con Ctrl+C
# Luego iniciar de nuevo
python run.py
```

### 4. Verificar Funcionamiento

#### Test 1: Primer Acceso (Sin Documentos)
1. Abre http://localhost:8501/
2. **Esperado:** Pantalla de login con mensaje "Se requiere autenticación de administrador para cargar los primeros documentos"
3. Ingresa contraseña de admin
4. Sube al menos un documento en Panel de Administración

#### Test 2: Acceso como Guest (Con Documentos)
1. Cierra sesión en la aplicación (botón "🚪 Cerrar Sesión")
2. Cierra la pestaña del navegador
3. Abre nuevamente http://localhost:8501/
4. **Esperado:** Acceso directo a la aplicación como "Usuario: Invitado"
5. Verifica que puedes:
   - ✅ Usar el chat
   - ✅ Ver la biblioteca
   - ✅ Ver settings
6. Intenta acceder a "Panel de Administración"
7. **Esperado:** Mensaje "🔒 Esta sección requiere autenticación de administrador"

#### Test 3: Login como Admin desde Guest
1. En el sidebar, click en "🔐 Login como Admin"
2. Ingresa contraseña
3. **Esperado:** Acceso completo con "Usuario: admin"
4. Verifica que ahora aparece "🔧 Panel de Administración" en el menú

#### Test 4: Gemini 3.6 Flash
1. Ve a Chat
2. Haz una pregunta relacionada con tus documentos
3. **Esperado:** Respuesta exitosa sin errores 404
4. Revisa logs - NO debe aparecer "404 NOT_FOUND"

---

## 🔍 Detalles Técnicos

### Modelos Gemini 3.x

**Cambios en la API:**
- Deprecados: `temperature`, `top_p`, `top_k`
- Nuevo: `thinking_level` (minimal, medium, high)
- Prefilled model turns ya no soportados

**Pricing (por millón de tokens):**

| Modelo | Input | Output | Uso Recomendado |
|--------|-------|--------|-----------------|
| gemini-3.6-flash | $1.50 | $7.50 | Producción, tareas complejas |
| gemini-3.5-flash-lite | $0.30 | $2.50 | Alto volumen, parsing de documentos |

**Fuente oficial:**
- https://ai.google.dev/gemini-api/docs/latest-model
- https://ai.google.dev/gemini-api/docs/models

### Estado de Sesión

```python
# session_state usado
st.session_state['is_admin'] = True/False  # Determina permisos
```

### Control de Acceso

```python
# En render_main_app()
if selected_page == "Admin":
    if is_admin:
        render_admin_panel()
    else:
        st.warning("🔒 Requiere autenticación de administrador")
        render_admin_login_link()
```

---

## 🧪 Tests de Integración

El test `test_integration.py` ahora pasa completamente:

```
Pass Rate: 5/5 (100%)

Imports: ✅ PASS
Configuration: ✅ PASS  
Services: ✅ PASS
Rag Pipeline: ✅ PASS
Llm Providers: ✅ PASS

🎉 All tests passed! System is ready.
```

**Nota:** El warning de Gemini ya NO aparece si el `.env` está actualizado.

---

## 📝 Notas Adicionales

### Compatibilidad Hacia Atrás

Si alguien todavía tiene `GEMINI_MODEL=gemini-1.5-flash-latest` en su `.env`:
- El sistema usará el default `gemini-3.6-flash`
- Aparecerá un warning en los logs
- **Acción requerida:** Actualizar `.env`

### Modo Desarrollo

Para desarrollo con múltiples usuarios:
1. Admin: Acceso completo para configuración
2. Guest: Para testear experiencia de usuario final

### Roadmap Futuro

**Posibles mejoras:**
- [ ] Sistema de usuarios múltiples con roles personalizados
- [ ] Permisos granulares por documento/colección
- [ ] API tokens para acceso programático
- [ ] Audit log de acciones de admin

---

## 🆘 Troubleshooting

### Problema: Todavía aparece error 404 de Gemini

**Solución:**
1. Verifica `.env` tiene `GEMINI_MODEL=gemini-3.6-flash`
2. Reinicia completamente la aplicación (Ctrl+C, luego `python run.py`)
3. Verifica que instalaste `google-genai` (no `google-generativeai`)

### Problema: Sigue pidiendo login incluso con documentos

**Solución:**
1. Verifica que los documentos están indexados: Ve a Panel Admin → Pestaña "Indexación"
2. Debería mostrar `> 0` chunks indexados
3. Si hay 0 chunks, re-indexa los documentos

### Problema: No aparece botón "Login como Admin"

**Solución:**
1. Verifica que estás en modo guest (sidebar debe decir "Usuario: Invitado")
2. Si no aparece, limpia session state: Cierra todas las pestañas y reabre
3. O añade `?clear_cache=1` a la URL

### Problema: Panel de Administración vacío para admin

**Solución:**
1. Verifica que hiciste login correctamente (sidebar debe decir "Usuario: admin")
2. Limpia caché del navegador y cookies de Streamlit
3. Reinicia la aplicación

---

## 📚 Referencias

- [Gemini 3.x Documentation](https://ai.google.dev/gemini-api/docs/latest-model)
- [google-genai Python SDK](https://googleapis-python-genai-70.mintlify.app/)
- [Streamlit Session State](https://docs.streamlit.io/library/api-reference/session-state)

---

**Mantenido por:** TechFlow Solutions  
**Última actualización:** 27 de julio de 2026
