# 🔄 REINICIO COMPLETO DE LA APLICACIÓN

**CRÍTICO:** Streamlit cachea el código Python. Los cambios NO se aplican hasta reiniciar completamente.

---

## ⚠️ Problema Actual

Los cambios están en el código pero **Streamlit está usando una versión cacheada vieja**.

**Síntomas:**
- Guest todavía puede ver botones en Biblioteca
- Botón "Login como Admin" no funciona
- Los cambios no se reflejan en la UI

---

## ✅ Solución: Reinicio Forzado

### Paso 1: Detener la Aplicación
```bash
# En la terminal donde corre la app:
# Presiona: Ctrl + C

# Espera a que se detenga completamente
```

### Paso 2: Limpiar Caché de Streamlit
```bash
# Eliminar caché de Streamlit:
Remove-Item -Recurse -Force ~/.streamlit/cache
```

### Paso 3: Limpiar Caché de Python
```bash
# Eliminar archivos .pyc compilados:
Get-ChildItem -Path . -Filter *.pyc -Recurse | Remove-Item -Force
Get-ChildItem -Path . -Filter __pycache__ -Recurse | Remove-Item -Force -Recurse
```

### Paso 4: Verificar Git
```bash
git status
# Debe decir: "Your branch is ahead of 'origin/main' by 4 commits"

git log --oneline -3
# Debe mostrar:
# 78a090f docs: Actualizar testing de permisos
# 7ed6f8a fix: Bloquear Biblioteca para guests y corregir botón Login
# 9d37502 docs: Agregar guía completa de testing de permisos
```

### Paso 5: Reiniciar la Aplicación
```bash
# Iniciar de nuevo:
python run.py

# O directamente:
streamlit run src/app.py
```

### Paso 6: Forzar Recarga en Navegador
```bash
# En el navegador:
1. Ctrl + Shift + R (forzar recarga sin caché)
2. O F5 varias veces

# Si no funciona:
3. Cerrar TODAS las pestañas de localhost:8501
4. Cerrar el navegador completamente
5. Reabrir y visitar http://localhost:8501
```

---

## 🧪 Verificación

Después del reinicio, verifica:

### Test 1: Guest en Biblioteca
```bash
1. Acceder como guest
2. Ir a "📚 Biblioteca de Conocimiento"
3. Debe mostrar:
   ✅ Mensaje: "🔒 Acceso Restringido"
   ✅ Solo estadísticas (3 métricas)
   ✅ Botón "Iniciar Sesión como Administrador"
   ❌ NO debe mostrar: lista de documentos
   ❌ NO debe mostrar: botones Eliminar/Indexar
```

### Test 2: Botón Login Admin
```bash
1. Como guest, en sidebar
2. Click "🔐 Login como Admin"
3. Debe:
   ✅ Redirigir a pantalla de login
   ✅ Mostrar formulario de contraseña
   ❌ NO volver a guest automáticamente
```

---

## 🐛 Si Todavía No Funciona

### Debug 1: Verificar que Streamlit leyó el código nuevo
```bash
# Agregar temporalmente en src/app.py línea 280:
st.write("🔍 DEBUG VERSION: 2024-07-27-v2")

# Si NO aparece en la app, Streamlit no leyó el archivo nuevo
```

### Debug 2: Verificar is_admin en Biblioteca
```bash
# Agregar temporalmente en src/app.py línea 283:
st.write(f"🔍 DEBUG: is_admin = {st.session_state.get(SessionKey.IS_ADMIN, False)}")

# Como guest debe mostrar: is_admin = False
# Como admin debe mostrar: is_admin = True
```

### Debug 3: Logs
```bash
# Buscar en la consola donde corre la app:
# Debe aparecer:
"User requested admin login from guest mode"  # Al click Login Admin
"Auto-enabled guest mode (documents available)" # Al iniciar como guest
```

---

## 🔄 Procedimiento Completo

```bash
# 1. Detener app
Ctrl + C

# 2. Limpiar cachés
Remove-Item -Recurse -Force ~/.streamlit/cache
Get-ChildItem -Path . -Filter __pycache__ -Recurse | Remove-Item -Force -Recurse

# 3. Verificar código
git log --oneline -1
# Debe ser: 78a090f docs: Actualizar testing de permisos

# 4. Reiniciar
python run.py

# 5. En navegador
Ctrl + Shift + R (forzar recarga)

# 6. Probar
- Guest → Biblioteca → Solo stats
- Guest → Login Admin → Login page
```

---

## ⚡ Alternativa: Usar Puerto Diferente

Si el problema persiste, puede ser que el navegador tenga cache persistente:

```bash
# Detener app (Ctrl + C)

# Iniciar en puerto diferente:
streamlit run src/app.py --server.port 8502

# Abrir en navegador:
http://localhost:8502
```

---

## 📝 Checklist

- [ ] App detenida (Ctrl+C)
- [ ] Caché Streamlit eliminado
- [ ] Caché Python eliminado
- [ ] Git verificado (commits recientes)
- [ ] App reiniciada
- [ ] Navegador recargado (Ctrl+Shift+R)
- [ ] Test Biblioteca ejecutado
- [ ] Test Login Admin ejecutado

---

**Si después de esto todavía no funciona**, necesito que:
1. Copies el output de `git log --oneline -3`
2. Copies lo que ves en la pantalla de Biblioteca como guest
3. Copies los logs de la consola donde corre la app

---

**Última actualización:** 27 de julio de 2026  
**Prioridad:** 🔴 CRÍTICO - REINICIAR AHORA
