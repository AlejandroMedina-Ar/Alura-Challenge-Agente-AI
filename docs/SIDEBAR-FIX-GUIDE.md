# Guía de Solución: Sidebar No Aparece

**Fecha:** 2026-07-27  
**Problema:** La sidebar desaparece y no vuelve a aparecer  
**Causa:** Streamlit guarda el estado "collapsed" en el localStorage del navegador

---

## 🔧 Solución Rápida (2 Opciones)

### **Opción 1: Desde la Consola del Navegador** ⭐ RECOMENDADO

1. En la aplicación (http://localhost:8501), presionar **F12** (abrir DevTools)

2. Ir a la pestaña **"Console"**

3. Pegar y ejecutar este código:
   ```javascript
   // Limpiar localStorage
   for (let i = localStorage.length - 1; i >= 0; i--) {
       const key = localStorage.key(i);
       if (key && (key.includes('sidebar') || key.includes('Sidebar'))) {
           console.log('Removing:', key);
           localStorage.removeItem(key);
       }
   }
   
   // Limpiar sessionStorage
   for (let i = sessionStorage.length - 1; i >= 0; i--) {
       const key = sessionStorage.key(i);
       if (key && (key.includes('sidebar') || key.includes('Sidebar'))) {
           console.log('Removing:', key);
           sessionStorage.removeItem(key);
       }
   }
   
   console.log('✅ Sidebar state cleared! Reload the page (F5)');
   ```

4. Recargar la página (**F5** o **Ctrl+R**)

5. ✅ La sidebar debería aparecer

---

### **Opción 2: Limpiar Todo el Caché del Navegador**

**Chrome/Edge:**
1. Presionar **Ctrl + Shift + Delete**
2. Seleccionar **"Imágenes y archivos en caché"** y **"Cookies y otros datos de sitios"**
3. Rango de tiempo: **"Últimas 24 horas"** o **"Todo"**
4. Hacer clic en **"Borrar datos"**
5. Recargar la aplicación

**Firefox:**
1. Presionar **Ctrl + Shift + Delete**
2. Seleccionar **"Cookies"** y **"Caché"**
3. Rango de tiempo: **"Todo"**
4. Hacer clic en **"Limpiar ahora"**
5. Recargar la aplicación

---

## 🛡️ Prevención: Sidebar Ahora Siempre Visible

**Con la última actualización (Commit 4666674):**

✅ **La sidebar ahora está FORZADA a estar siempre visible**
- El botón de collapse (`<<<`) está **completamente oculto**
- CSS y JavaScript fuerzan la sidebar a permanecer expandida
- localStorage se limpia automáticamente en cada carga

**Esto significa:**
- ❌ Ya NO puedes colapsar la sidebar (por diseño)
- ✅ La sidebar SIEMPRE estará visible
- ✅ No más problemas de "sidebar desaparecida"

---

## 🔍 Verificar que el Fix Funciona

Después de actualizar el código (git pull):

1. **Verificar que NO hay botón de collapse:**
   - La sidebar NO debería tener el botón `<<<` en la esquina superior

2. **Verificar que la sidebar es fija:**
   - Intenta hacer clic donde estaba el botón → No debería pasar nada
   - La sidebar permanece siempre visible

3. **Verificar el ancho:**
   - La sidebar debería tener un ancho fijo de 21rem (336px)

---

## 🎯 Sobre el Botón "Ir a Biblioteca de Conocimiento"

**Problema que reportaste:**
> "Al hacer clic en 'Ir a la biblioteca de conocimiento' nada ocurre"

**Explicación:**
El botón SÍ funciona, lo que hace es:
```python
st.session_state.update({'current_page': 'Knowledge'})
```

Esto **cambia la página activa EN LA SIDEBAR** a "Biblioteca de Conocimiento".

**Por qué parecía que no funcionaba:**
- La sidebar estaba colapsada (oculta)
- El botón cambió la página, pero no podías verla porque la sidebar no estaba visible
- Era como cambiar de canal en una TV apagada

**Ahora que la sidebar está siempre visible:**
✅ Hacer clic en "Ir a Biblioteca de Conocimiento" → Cambia inmediatamente a esa vista
✅ Puedes ver el cambio porque la sidebar está visible

---

## 📝 Cambios Técnicos Implementados

### 1. **src/ui/theme.py**
```python
# Agregado JavaScript para limpiar localStorage automáticamente
# Agregado CSS para forzar sidebar visible con !important
# Ocultado completamente el botón de collapse
```

### 2. **src/app.py**
```python
# Agregado script para limpiar localStorage en cada carga
# Configurado menu_items para ocultar menús de Streamlit
```

### 3. **assets/css/dark.css** y **light.css**
```css
/* Sidebar forzada a estar visible */
[data-testid="stSidebar"] {
    display: block !important;
    visibility: visible !important;
    opacity: 1 !important;
    transform: none !important;
    margin-left: 0 !important;
}

/* Botón de collapse oculto */
[data-testid="collapsedControl"] {
    display: none !important;
}
```

---

## ⚠️ Si Aún No Aparece

### Paso 1: Verificar que tienes la última versión

```bash
git pull origin main
git log --oneline -1
# Debería mostrar: 85f2315 chore: eliminar clear_sidebar_state.html
```

### Paso 2: Limpiar localStorage (usando opción 1 o 2 arriba)

### Paso 3: Forzar recarga completa

**Chrome/Edge:**
- Windows/Linux: `Ctrl + Shift + R`
- Mac: `Cmd + Shift + R`

**Firefox:**
- Windows/Linux: `Ctrl + F5`
- Mac: `Cmd + Shift + R`

### Paso 4: Reiniciar el servidor

```bash
# Detener aplicación (Ctrl+C)
# Reiniciar
python run.py
```

### Paso 5: Usar modo incógnito

Si nada funciona, probar en ventana de incógnito:
- Chrome: `Ctrl + Shift + N`
- Firefox: `Ctrl + Shift + P`

El modo incógnito NO tiene localStorage previo, así que debería funcionar.

---

## 🐛 Debug: Verificar Estado de localStorage

Ejecutar en la consola del navegador (F12 → Console):

```javascript
// Ver todas las claves de localStorage
console.log('localStorage keys:', Object.keys(localStorage));

// Ver claves relacionadas con sidebar
for (let i = 0; i < localStorage.length; i++) {
    const key = localStorage.key(i);
    if (key && key.includes('sidebar')) {
        console.log('Sidebar key:', key, '=', localStorage.getItem(key));
    }
}

// Ver si sidebar está colapsada en el DOM
const sidebar = document.querySelector('[data-testid="stSidebar"]');
console.log('Sidebar element:', sidebar);
console.log('Sidebar display:', sidebar?.style.display);
console.log('Sidebar visibility:', sidebar?.style.visibility);
console.log('Sidebar aria-expanded:', sidebar?.getAttribute('aria-expanded'));
```

**Salida esperada:**
```
localStorage keys: [...]  // No debería haber claves con 'sidebar'
Sidebar element: <section>...</section>
Sidebar display: block
Sidebar visibility: visible
Sidebar aria-expanded: true
```

---

## ✅ Checklist de Solución

Marcar cada paso que hayas completado:

- [ ] Git pull de la última versión (commit 85f2315)
- [ ] Limpiado localStorage (opción 1 o 2)
- [ ] Forzado recarga completa (Ctrl+Shift+R)
- [ ] Reiniciado servidor (Ctrl+C, python run.py)
- [ ] Verificado que botón `<<<` NO aparece
- [ ] Verificado que sidebar está visible
- [ ] Probado botón "Ir a Biblioteca de Conocimiento"
- [ ] ✅ Sidebar funciona correctamente

---

## 📞 Si Aún Necesitas Ayuda

Si después de seguir TODOS los pasos la sidebar aún no aparece:

1. **Tomar captura de pantalla** de la aplicación
2. **Ejecutar el código de debug** (arriba) y copiar la salida de la consola
3. **Verificar versión del navegador:**
   - Chrome: `chrome://version`
   - Firefox: `about:support`
4. **Reportar** con toda esta información

---

**Actualizado:** 2026-07-27  
**Commit:** 85f2315  
**Estado:** ✅ RESUELTO (sidebar forzada siempre visible)
