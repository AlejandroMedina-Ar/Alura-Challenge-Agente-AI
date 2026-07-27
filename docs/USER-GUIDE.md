# 📖 Guía de Usuario - TechFlow Solutions RAG Agent

**Guía completa para usar el Agente RAG de TechFlow Solutions**

---

## 📑 Tabla de Contenidos

1. [Primeros Pasos](#primeros-pasos)
2. [Modos de Acceso](#modos-de-acceso)
3. [Chat con el Agente](#chat-con-el-agente)
4. [Biblioteca de Conocimiento](#biblioteca-de-conocimiento)
5. [Panel de Administración](#panel-de-administración)
6. [Configuración](#configuración)
7. [Mejores Prácticas](#mejores-prácticas)
8. [Solución de Problemas](#solución-de-problemas)

---

## 🚀 Primeros Pasos

### Primera Vez (Sin Documentos)

Cuando abres la aplicación por primera vez:

1. **Pantalla de Login** aparecerá automáticamente
2. Ingresa la contraseña de administrador (configurada en `.env`)
3. Serás redirigido al Panel de Administración
4. **Sube tus primeros documentos:**
   - Panel de Administración → Documentos
   - Arrastra archivos o click en "Selecciona un documento"
   - Espera a que se indexen automáticamente

### Accesos Posteriores (Con Documentos)

Una vez que hay documentos indexados:

- **Acceso automático como Guest:** La app se abre directamente al chat
- **No necesitas contraseña** para consultar documentos
- **Para gestionar documentos:** Click en "🔐 Login como Admin" en el sidebar

---

## 👥 Modos de Acceso

### Modo Guest (Usuario Común)

**Acceso:** Automático cuando hay documentos

**Puedes:**
- ✅ Usar el chat para consultar documentos
- ✅ Ver la biblioteca de conocimiento
- ✅ Ver configuración (solo lectura)
- ✅ Cambiar tema (claro/oscuro)

**NO puedes:**
- ❌ Subir documentos
- ❌ Eliminar documentos
- ❌ Modificar configuración
- ❌ Acceder al Panel de Administración

**Interfaz:**
- Sidebar muestra: "👤 Usuario: Invitado"
- Botón disponible: "🔐 Login como Admin"

### Modo Admin (Administrador)

**Acceso:** Click en "Login como Admin" + contraseña

**Puedes:**
- ✅ Todas las funciones de Guest
- ✅ Subir y eliminar documentos
- ✅ Modificar configuración del sistema
- ✅ Acceder al Panel de Administración
- ✅ Ver métricas y estadísticas
- ✅ Cambiar entre modos sin cerrar sesión

**Interfaz:**
- Sidebar muestra: "👤 Usuario: admin" + "🔑 Rol: Admin"
- Botones: "👥 Modo Usuario" (cambiar a vista guest) y "🚪 Cerrar Sesión"

---

## 💬 Chat con el Agente

### Usar el Chat

1. **Ir a Chat:**
   - Sidebar → "💬 Chat con el Agente"

2. **Escribir pregunta:**
   - Escribe en el input inferior
   - Presiona Enter o click en el botón de envío

3. **Ver respuesta:**
   - La respuesta aparece en streaming (palabra por palabra)
   - Incluye fuentes consultadas al final

### Características del Chat

#### Historial de Conversación
- El chat mantiene contexto de mensajes anteriores
- Puedes hacer preguntas de seguimiento
- Ejemplo:
  ```
  Usuario: ¿Cuál es el horario de la Mesa de Ayuda?
  Agente: El horario es...
  Usuario: ¿Y para urgencias?
  Agente: [responde basándose en contexto anterior]
  ```

#### Indicación de Fuentes
- Cada respuesta muestra los documentos consultados
- Formato: `**Fuente:** Manual de TI - Capítulo 3`
- Ayuda a verificar información

#### Limpiar Conversación
- Click en "🗑️ Limpiar Chat" (si disponible)
- O recarga la página para empezar de nuevo

### Ejemplos de Preguntas

#### Preguntas Efectivas
```
✅ "¿Cómo solicito una notebook nueva?"
✅ "¿Cuál es el proceso de onboarding?"
✅ "¿Qué dice el manual sobre trabajo remoto?"
✅ "Resume las políticas de vacaciones"
```

#### Preguntas a Evitar
```
❌ "Hola" (saludo simple)
❌ "Cuéntame algo" (demasiado vago)
❌ "¿Qué hora es?" (fuera del conocimiento)
❌ Preguntas sobre información no indexada
```

### Respuestas del Agente

#### Cuando HAY información
```
El agente responde con:
1. Respuesta directa basada en documentos
2. Detalles específicos
3. Fuentes consultadas
```

#### Cuando NO hay información
```
"No tengo esa información en los documentos disponibles."
```

**El agente es honesto:** Si no sabe algo, lo dice claramente. NO inventa información.

---

## 📚 Biblioteca de Conocimiento

### Vista Guest

Como usuario guest, ves:
- 📊 **Estadísticas:**
  - Total de documentos
  - Documentos indexados
  - Tamaño total
- 🔒 **Mensaje:** "Acceso restringido para gestión"
- 💡 **Sugerencia:** Usar el chat para consultas

### Vista Admin

Como administrador, ves:
- ⬆️ **Subir Documentos:**
  - Botón de selección de archivos
  - Drag & drop disponible
- 📄 **Lista de Documentos:**
  - Nombre, tamaño, fecha
  - Estado de indexación
  - Botones de acción por documento

### Subir Documentos (Admin)

1. **Navegar a Biblioteca:**
   - Sidebar → "📚 Biblioteca de Conocimiento"

2. **Seleccionar archivo:**
   - Click en "Selecciona un documento"
   - O arrastra y suelta

3. **Formatos soportados:**
   - **PDF** (.pdf) - Máx 50MB
   - **TXT** (.txt) - Máx 10MB
   - **Markdown** (.md) - Máx 10MB
   - **Word** (.docx) - Máx 25MB

4. **Esperar indexación:**
   - El documento se indexa automáticamente
   - ✅ Aparece confirmación cuando está listo

### Acciones sobre Documentos (Admin)

**Por cada documento:**
- 🗑️ **Eliminar:** Borra el documento y su índice
- ⚡ **Indexar:** (si no está indexado) Procesa el documento
- 🔄 **Re-indexar:** (si ya está indexado) Vuelve a procesar

---

## 🔧 Panel de Administración

**Acceso:** Solo para administradores

### Tab: Documentos

**Vista completa de gestión:**
- Subir múltiples documentos
- Ver lista detallada
- Acciones por documento
- Operaciones por lotes

### Tab: Indexación

**Control de indexación:**

**Estadísticas:**
- Documentos indexados
- Documentos pendientes
- Total de fragmentos

**Documentos Pendientes:**
- Lista de archivos sin indexar
- Nombres de archivos visibles

**Operaciones:**
- ⚡ **Indexar Todos los Pendientes:** Procesa todos de una vez
- 🗑️ **Limpiar Todos los Índices:** Borra todo el índice (⚠️ destructivo)

### Tab: Testing

**Probar proveedores LLM:**

1. **Test de Gemini:**
   - Click en "Test Gemini"
   - Ver respuesta y tiempo
   - ✅ Verde = funciona, ❌ Rojo = error

2. **Test de Cohere:**
   - Click en "Test Cohere"
   - Verifica fallback
   - Solo necesario si Gemini falla

---

## ⚙️ Configuración

### Proveedor LLM

**Gemini 3.6 Flash (Principal):**
- Modelo más reciente de Google
- Rápido y eficiente
- Requiere API key gratuita

**Cohere Command-R (Fallback):**
- Backup automático si Gemini falla
- Se activa automáticamente
- 5 minutos de cooldown antes de reintentar Gemini

### Parámetros RAG

**Chunk Size (Tamaño de Fragmento):**
- Rango: 100-5000 caracteres
- Default: 1000
- Más pequeño = más precisión
- Más grande = más contexto

**Chunk Overlap (Solapamiento):**
- Rango: 0-200 caracteres
- Default: 200
- Previene pérdida de contexto en bordes

**Top K (Fragmentos Recuperados):**
- Rango: 1-20
- Default: 5
- Más fragmentos = más contexto, más lento

**Temperature (Temperatura):**
- Rango: 0.0-2.0
- Default: 0.7
- 0.0-0.5: Respuestas precisas
- 0.5-1.0: Balanceado
- 1.0-2.0: Creativo

### Tema

**Modo Claro (Light):**
- Fondo blanco
- Texto oscuro
- Mejor para ambientes iluminados
- **Default por defecto**

**Modo Oscuro (Dark):**
- Fondo oscuro
- Texto claro
- Mejor para ambientes con poca luz

**Cambio inmediato:**
- Click en el selector de tema
- Se aplica instantáneamente
- Se guarda para la próxima sesión

---

## 💡 Mejores Prácticas

### Preparar Documentos

**Antes de subir:**
1. ✅ Revisa que no haya información sensible
2. ✅ Verifica que el texto sea legible (no imágenes escaneadas)
3. ✅ Usa nombres de archivo descriptivos
4. ✅ Divide documentos muy largos (>10MB)

**Formato ideal:**
- Con encabezados claros (H1, H2, H3)
- Párrafos bien estructurados
- Tabla de contenidos (opcional)
- Sin información duplicada

### Hacer Mejores Preguntas

**Sé específico:**
```
❌ "Dime sobre RR.HH."
✅ "¿Cuál es la política de vacaciones para empleados tiempo completo?"
```

**Usa contexto:**
```
✅ "Según el manual del empleado, ¿cuántos días de vacaciones tengo?"
✅ "En el reporte de ventas 2024, ¿cuál fue el producto más vendido?"
```

**Divide preguntas complejas:**
```
En lugar de:
❌ "¿Cuál es el proceso completo de solicitud de equipamiento, 
   los tiempos de entrega y qué hacer si falla?"

Pregunta:
✅ 1. "¿Cómo solicito equipamiento nuevo?"
✅ 2. "¿Cuánto tarda en llegar?"
✅ 3. "¿Qué hago si el equipo falla?"
```

### Estrategia de Indexación

**Cuándo indexar:**
- Inmediatamente después de subir documentos
- Después de actualizar un documento
- Si las respuestas parecen desactualizadas

**Indexación por lotes:**
- Sube varios documentos primero
- Luego indexa todos de una vez
- Más eficiente que uno por uno

**Re-indexación:**
- Cuando actualizas un documento
- Si la calidad de búsqueda baja
- Después de cambiar parámetros de chunk

### Ajustar Configuración

**Para respuestas precisas:**
- Chunk size: 500-800
- Top K: 7-10
- Temperature: 0.3-0.5

**Para respuestas creativas:**
- Chunk size: 1000-1500
- Top K: 5
- Temperature: 0.7-1.0

**Para rendimiento rápido:**
- Chunk size: 1000
- Top K: 3-5
- Temperature: 0.7

---

## 🐛 Solución de Problemas

### No Puedo Hacer Login

**Problema:** La contraseña no funciona

**Soluciones:**
1. Verifica el archivo `.env` → `ADMIN_PASSWORD`
2. Asegúrate de no tener espacios extra
3. Reinicia la aplicación después de cambiar `.env`
4. Verifica mayúsculas/minúsculas

### El Chat No Responde

**Problema:** No hay respuesta o aparece error

**Soluciones:**
1. ✅ Verifica que hay documentos indexados (Biblioteca)
2. ✅ Comprueba tu conexión a internet
3. ✅ Prueba los proveedores LLM (Admin → Testing)
4. ✅ Revisa logs en `data/logs/application.log`
5. ✅ Verifica que tu API key de Gemini esté activa

### No Puedo Subir Documentos

**Problema:** La subida falla

**Soluciones:**
1. ✅ Verifica el tamaño (PDF máx 50MB, TXT/MD máx 10MB)
2. ✅ Confirma el formato (PDF, TXT, MD, DOCX)
3. ✅ Revisa que el nombre no tenga caracteres especiales
4. ✅ Comprueba espacio en disco
5. ✅ Intenta con otro archivo

### La Indexación Falla

**Problema:** El documento no se indexa

**Soluciones:**
1. ✅ Verifica que el archivo no esté corrupto
2. ✅ Asegúrate de que tiene texto (no solo imágenes)
3. ✅ Revisa logs para error específico
4. ✅ Intenta re-subir el documento
5. ✅ Comprueba espacio en disco

### Respuestas Incorrectas

**Problema:** El agente no encuentra información relevante

**Soluciones:**
1. ✅ Re-indexa los documentos
2. ✅ Aumenta Top K en Configuración (por ej. a 7-10)
3. ✅ Reformula la pregunta de forma más específica
4. ✅ Verifica que los documentos relevantes estén subidos
5. ✅ Prueba con diferentes parámetros de chunk

### La App Va Lenta

**Problema:** Respuestas tardan mucho

**Soluciones:**
1. ✅ Reduce Top K a 3-5
2. ✅ Limpia caché del navegador
3. ✅ Reinicia la aplicación
4. ✅ Verifica recursos del sistema
5. ✅ Considera reducir número de documentos indexados

### Mensajes de Error Comunes

**"Knowledge Library is Empty"**
- Necesitas subir e indexar al menos un documento
- Ve a Biblioteca → Sube un documento

**"LLM Provider Failed"**
- Verifica tu API key en `.env`
- Prueba la conexión en Admin → Testing
- Comprueba tu conexión a internet
- Revisa tu cuota de API

**"Indexing Error"**
- El formato del archivo no es soportado
- El archivo puede estar corrupto
- Revisa logs de la aplicación
- Intenta con documentos más pequeños

---

## ⌨️ Atajos de Teclado

| Atajo | Acción |
|-------|--------|
| `Enter` | Enviar mensaje en chat |
| `Shift+Enter` | Nueva línea en chat |

---

## ✅ Resumen de Buenas Prácticas

**Hacer:**
- ✅ Hacer preguntas específicas y claras
- ✅ Subir documentos bien formateados
- ✅ Indexar documentos después de subirlos
- ✅ Probar proveedores LLM regularmente
- ✅ Mantener API keys seguras
- ✅ Cerrar sesión en computadoras públicas

**Evitar:**
- ❌ Subir información sensible sin revisar
- ❌ Hacer preguntas fuera del conocimiento
- ❌ Compartir contraseñas de admin
- ❌ Eliminar documentos sin backup
- ❌ Cambiar configuración sin entender
- ❌ Ignorar mensajes de error

---

## 📞 Obtener Ayuda

**Revisar Logs:**
```bash
data/logs/application.log
```

**Ejecutar Tests:**
```bash
python test_integration.py
```

**Documentación Adicional:**
- [Documentación Técnica](TECHNICAL-DOCS.md)
- [Solución de Problemas](TROUBLESHOOTING.md)
- [FAQ](FAQ.md)

**Reportar Problemas:**
- GitHub Issues: [Repositorio](https://github.com/AlejandroMedina-Ar/Alura-Challenge-Agente-AI/issues)
- Incluye mensaje de error
- Describe pasos para reproducir
- Adjunta logs relevantes (sin información sensible)

---

**Versión:** 1.0.0  
**Última Actualización:** Julio 2026  
**TechFlow Solutions** - Transformación Digital con IA
