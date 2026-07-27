# ❓ Preguntas Frecuentes (FAQ)

**Respuestas a preguntas comunes sobre TechFlow Solutions RAG Agent**

---

## Preguntas Generales

### ¿Qué es TechFlow Solutions?

TechFlow Solutions es un agente de conocimiento potenciado por RAG (Generación Aumentada por Recuperación) que te permite conversar con tu colección de documentos usando lenguaje natural. Combina búsqueda de documentos con modelos de lenguaje IA para proporcionar respuestas precisas y contextuales.

### ¿Qué significa RAG?

RAG significa Retrieval-Augmented Generation (Generación Aumentada por Recuperación). Es una técnica que:
1. **Recupera** información relevante de tus documentos
2. **Aumenta** el conocimiento de la IA con esa información
3. **Genera** respuestas precisas basadas en tus datos

### ¿Es gratis de usar?

¡Sí! Todo el stack utiliza servicios gratuitos:
- **Google Gemini 3.6 Flash** (plan gratuito)
- **Cohere Command-R** (plan gratuito, fallback)
- **ChromaDB local** (código abierto, gratuito)
- **Embeddings locales** (multilingual-e5-base, ejecuta en tu máquina)

Solo necesitas claves API gratuitas de Google y Cohere.

### ¿Qué idiomas soporta?

El sistema está optimizado para **español** pero también funciona bien con:
- Inglés
- Portugués
- Otros idiomas principales

Los embeddings multilingual-e5 soportan más de 100 idiomas.

### ¿Hay modo invitado y administrador?

**Sí, dos modos de acceso:**

**Modo Invitado (Guest):**
- Sin necesidad de contraseña
- Acceso al chat con el LLM
- Consulta de documentos indexados
- **No puede:** cargar, modificar o eliminar documentos

**Modo Administrador (Admin):**
- Requiere contraseña (configurada en `.env`)
- Acceso completo al chat
- **Puede:** cargar, indexar, eliminar documentos
- Acceso al Panel de Administración
- Gestión completa de la base de conocimiento

Para acceder como Admin, haz clic en "Admin" en la barra lateral y ingresa la contraseña.

---

## Instalación y Configuración

### ¿Cuáles son los requisitos del sistema?

**Mínimos:**
- Python 3.9 o superior
- 2GB RAM
- 1GB de espacio libre en disco
- Conexión a Internet

**Recomendados:**
- Python 3.11+
- 4GB RAM
- 5GB de espacio libre
- Conexión estable a Internet

### ¿Cómo obtengo las claves API?

**Google Gemini:**
1. Ve a https://makersuite.google.com/app/apikey
2. Inicia sesión con tu cuenta Google
3. Haz clic en "Create API Key"
4. Copia la clave

**Cohere:**
1. Ve a https://dashboard.cohere.com
2. Regístrate para una cuenta gratuita
3. Navega a la sección API Keys
4. Copia tu clave

### ¿Dónde coloco las claves API?

En el archivo `.env` en la raíz del proyecto:

```bash
GEMINI_API_KEY=tu_clave_gemini_aqui
COHERE_API_KEY=tu_clave_cohere_aqui
ADMIN_PASSWORD=tu_contraseña_admin
```

### ¿Necesito ambas claves API?

**Recomendado:** Sí, para tener fallback automático.

**Mínimo:** Solo una (Gemini o Cohere) funcionará, pero sin protección de respaldo.

### ¿Cómo sé si la configuración fue exitosa?

Ejecuta la suite de pruebas:

```bash
python test_integration.py
```

Si ves "Pass Rate: 80-100%", la configuración es exitosa.

---

## Preguntas de Uso

### ¿Qué formatos de archivo son soportados?

**Soportados:**
- PDF (.pdf)
- Texto (.txt)
- Markdown (.md)
- Word (.docx)

**Tamaño máximo:** 10MB por archivo

### ¿Por qué no puedo cargar mi archivo?

**Razones comunes:**
1. El archivo es muy grande (>10MB)
2. Formato no soportado
3. El archivo está corrupto
4. El nombre tiene caracteres especiales
5. **No estás en modo Admin** (solo Admin puede cargar archivos)

**Solución:** Intenta convertir a PDF o dividir documentos grandes. Asegúrate de estar autenticado como Admin.

### ¿Necesito indexar documentos después de cargarlos?

**¡Sí!** Cargar solo almacena el archivo. Indexar lo procesa para búsqueda:
1. Carga el documento (en modo Admin)
2. Haz clic en "Indexar" en el Panel de Administración
3. Espera a que complete la indexación
4. Ahora puedes conversar sobre él

### ¿Cuánto tiempo toma la indexación?

**Tiempos típicos:**
- Documento de 1MB: 10-30 segundos
- Documento de 5MB: 1-2 minutos
- Documento de 10MB: 2-5 minutos

Depende de la complejidad del documento y el rendimiento del sistema.

### ¿Puedo cargar múltiples documentos a la vez?

**Carga:** Uno a la vez actualmente.

**Indexación:** ¡Sí! Usa "Indexar Todos los Pendientes" en el Panel de Administración para procesar múltiples documentos en lote.

**Nota:** Solo disponible en modo Admin.

### ¿Por qué mis respuestas no referencian mis documentos?

**Posibles razones:**
1. Documentos aún no indexados
2. Pregunta no específica suficiente
3. Información relevante no está en los documentos
4. Top-K muy bajo (aumenta en Configuración)

**Intenta:**
- Re-indexar documentos
- Hacer preguntas más específicas
- Aumentar Top-K a 7-10
- Verificar que los documentos se cargaron exitosamente

---

## Preguntas Técnicas

### ¿Cómo funciona el pipeline RAG?

**Paso a paso:**
1. **Carga:** Subes un documento (solo Admin)
2. **Chunking:** El documento se divide en fragmentos de ~512 caracteres con solapamiento
3. **Embedding:** Cada fragmento se convierte en un vector de 768 dimensiones (multilingual-e5-base, local)
4. **Almacenamiento:** Los vectores se guardan en ChromaDB (local)
5. **Consulta:** Tu pregunta también se convierte en un vector
6. **Búsqueda:** Se recuperan los vectores (fragmentos) similares
7. **Prompt:** Los fragmentos recuperados se agregan como contexto
8. **Generación:** El LLM (Gemini 3.6 Flash) genera una respuesta usando el contexto

### ¿Qué es el tamaño de chunk y solapamiento?

**Tamaño de Chunk:**
- Cuántos caracteres por fragmento
- Por defecto: 512 caracteres
- Más pequeño = más preciso, más fragmentos
- Más grande = más contexto, menos fragmentos

**Solapamiento:**
- Caracteres compartidos entre fragmentos consecutivos
- Por defecto: 50 caracteres
- Previene pérdida de contexto en los límites

### ¿Qué es Top-K?

**Top-K** es el número de fragmentos más relevantes recuperados por consulta.

- **K=3:** Rápido, menos contexto
- **K=5:** Equilibrado (por defecto)
- **K=10:** Más lento, más contexto

Mayor K = más contexto pero respuestas más lentas.

### ¿Qué controla la temperatura?

**Temperatura** (0.0-2.0) controla la creatividad de la respuesta:

- **0.0-0.5:** Determinista, enfocado, consistente
- **0.5-1.0:** Equilibrado (por defecto: 0.7)
- **1.0-2.0:** Creativo, variado, menos predecible

Para Q&A factual, mantenerla baja (0.3-0.7).

### ¿Cómo funciona el fallback automático?

Si Gemini falla (error de API, cuota, timeout):
1. El sistema automáticamente intenta con Cohere
2. La respuesta continúa sin interrupciones
3. El usuario no nota el cambio
4. Se registra para monitoreo

### ¿Dónde se almacenan mis datos?

**Localmente en tu máquina:**
- Documentos: `data/knowledge_library/documents/`
- Metadatos: `data/knowledge_library/metadata/`
- Base de datos vectorial: `data/chromadb/`
- Configuración: `data/config.json`
- Logs: `data/logs/`

**No se envía a ningún lugar** excepto:
- Fragmentos de documentos al modelo de embeddings (local)
- Prompts a las APIs LLM (Gemini/Cohere)

---

## Resolución de Problemas

### Error "Module not found" al iniciar

**Causa:** Dependencias faltantes

**Solución:**
```bash
pip install -r requirements.txt
```

### El chat no responde

**Causas:**
1. No hay claves API configuradas
2. No hay documentos indexados
3. Problema de conexión a Internet
4. Cuota de API excedida

**Solución:**
1. Verifica que `.env` tenga claves API válidas
2. Indexa al menos un documento
3. Verifica conexión a Internet
4. Prueba los proveedores en el Panel de Administración

### "LLM provider test failed"

**Causas:**
1. Clave API inválida
2. Sin conexión a Internet
3. Servicio API caído
4. Cuota excedida

**Solución:**
1. Verifica claves API en `.env`
2. Prueba: `curl https://google.com`
3. Espera y reintenta
4. Revisa el dashboard de API para la cuota

### La indexación falla silenciosamente

**Revisa los logs:**
```bash
cat data/logs/application.log | grep ERROR
```

**Causas comunes:**
1. Archivo corrupto
2. Archivo sin texto extraíble
3. Sin espacio en disco
4. Problema de conexión con ChromaDB

### Las respuestas son lentas

**Optimización:**
1. Reduce Top-K (Configuración → RAG)
2. Usa menor tamaño de chunk
3. Limpia caché del navegador
4. Verifica velocidad de Internet
5. Prueba diferente proveedor LLM

### No puedo hacer login como Admin

**Ubicación de contraseña:** archivo `.env`

**Pasos para resetear:**
1. Abre el archivo `.env`
2. Cambia `ADMIN_PASSWORD=nueva_contraseña`
3. Guarda el archivo
4. Reinicia la aplicación

### La aplicación se cierra al iniciar

**Pasos:**
1. Verifica versión de Python: `python --version` (necesita 3.9+)
2. Ejecuta setup: `python setup.py`
3. Revisa logs: `data/logs/application.log`
4. Reinstala dependencias: `pip install -r requirements.txt --force-reinstall`

---

## Preguntas de Rendimiento

### ¿Cuántos documentos puedo cargar?

**Límites prácticos:**
- **100 documentos:** Funciona suavemente
- **1000 documentos:** Más lento pero funcional
- **10,000+ documentos:** Puede necesitar optimización

**Factores:**
- Tamaño total de documentos
- RAM disponible
- Espacio en disco

### ¿Cuánto espacio en disco necesito?

**Desglose:**
- Aplicación: ~50MB
- Documentos: Depende de tus archivos
- Base de datos vectorial: ~1KB por fragmento
- Logs: ~10-50MB

**Ejemplo:** 100 documentos (1MB cada uno, ~200 fragmentos) = ~100MB + 200KB + logs

### ¿Puedo ejecutar esto en una Raspberry Pi?

**Teóricamente sí**, pero no recomendado:
- La indexación será muy lenta
- RAM limitada puede causar problemas
- Mejor en laptop/desktop

### ¿Funciona offline?

**Parcial:**
- ✅ Indexación funciona (con embeddings locales)
- ❌ Chat requiere Internet (APIs LLM)

**Alternativa:** Usar LLM local (requiere modificación del código)

---

## Privacidad y Seguridad

### ¿Mis datos son privados?

**Sí, mayormente:**
- Documentos almacenados **solo localmente**
- Vectores almacenados **solo localmente**
- Metadatos almacenados **solo localmente**

**Enviado a la nube:**
- Fragmentos de documentos (durante consulta) → API LLM
- Preguntas → API LLM

**No enviado:**
- Documentos completos
- Información de usuario
- Nada más

### ¿Puedo usarlo para documentos sensibles?

**Consideraciones:**
1. Datos enviados a Gemini/Cohere durante el chat
2. Revisa sus políticas de privacidad
3. Para datos altamente sensibles, considera LLMs auto-alojados

**Recomendación:** Remueve info sensible antes de cargar.

### ¿Cómo se almacenan las contraseñas?

- **Hasheadas** usando bcrypt
- **No reversibles**
- **Almacenadas** en estado de sesión (temporal)
- **No registradas en logs**

### ¿Puede alguien más acceder a mis documentos?

**No**, si:
- Eres el único usuario en tu máquina
- Haces logout cuando terminas
- No compartes la contraseña de admin

**Sí**, si:
- Alguien tiene acceso físico a tu máquina
- Alguien conoce tu contraseña de admin
- La computadora está comprometida

---

## Preguntas de Personalización

### ¿Puedo cambiar el prompt del sistema?

**¡Sí!** En el código:
```python
# src/rag/prompt_builder.py
DEFAULT_SYSTEM_INSTRUCTION = "Tu prompt personalizado aquí..."
```

O vía Configuración → RAG → Instrucción del Sistema (si la UI está implementada).

### ¿Puedo agregar más proveedores LLM?

**¡Sí!** Sigue el patrón:
1. Crea `src/llm/nuevo_proveedor.py`
2. Extiende `BaseLLMProvider`
3. Implementa métodos requeridos
4. Agrega a `src/llm/__init__.py`

### ¿Puedo cambiar los colores del tema?

**¡Sí!** Edita los archivos CSS:
- Claro: `assets/css/light.css`
- Oscuro: `assets/css/dark.css`

**Tema por defecto:** El sistema inicia en modo **claro** por defecto (configurado en `src/storage/config_repository.py`).

### ¿Puedo desplegar esto como servicio?

**¡Sí!** Ver opciones de despliegue:
1. Streamlit Community Cloud (más fácil)
2. Contenedor Docker
3. VM en la nube (AWS, GCP, Azure)
4. Servidor on-premises

Ver `docs/DEPLOYMENT.md` para detalles.

---

## Preguntas de Comparación

### vs. ChatGPT?

**TechFlow Solutions:**
- ✅ Usa TUS documentos
- ✅ Privacidad (almacenamiento local)
- ✅ Plan gratuito
- ✅ Personalizable
- ❌ Modelo más pequeño
- ❌ Auto-alojado

**ChatGPT:**
- ✅ Modelo poderoso
- ✅ Alojado en la nube
- ✅ Sin configuración
- ❌ No conoce tus docs
- ❌ Preocupaciones de privacidad
- ❌ Pago para características completas

### vs. Microsoft Copilot?

**TechFlow Solutions:**
- ✅ 100% gratuito
- ✅ Control total
- ✅ Datos locales
- ❌ Configuración manual

**Copilot:**
- ✅ Integrado en Office
- ✅ Sin configuración
- ❌ Cuenta Microsoft necesaria
- ❌ Suscripción requerida

### vs. Construir desde cero?

**TechFlow Solutions:**
- ✅ Listo para usar
- ✅ Probado y funcionando
- ✅ Buena arquitectura
- ✅ Documentación
- ❌ Menos flexible

**Desde Cero:**
- ✅ Personalización completa
- ✅ Experiencia de aprendizaje
- ❌ Semanas de desarrollo
- ❌ Más bugs

---

## Preguntas Avanzadas

### ¿Puedo usar LLMs locales?

**Sí**, pero requiere cambios en el código:
1. Crea nuevo proveedor LLM para modelo local (Ollama, llama.cpp)
2. Apunta al endpoint local
3. Ajusta prompts si es necesario

### ¿Puedo usar diferentes modelos de embedding?

**¡Sí!** En el código:
```python
# src/config/constants.py
DEFAULT_EMBEDDING_MODEL = "nombre-de-tu-modelo"
```

Debe ser compatible con sentence-transformers.

### ¿Puedo exportar la base de datos vectorial?

**¡Sí!** Los datos de ChromaDB están en:
```
data/chromadb/
```

Puede ser respaldado/movido a otra máquina.

### ¿Puedo integrar con mi aplicación existente?

**¡Sí!** La capa de servicios puede ser importada:
```python
from src.services import get_chat_service

chat_service = get_chat_service()
response = chat_service.chat("consulta", stream=False)
```

### ¿Puedo contribuir al proyecto?

**¡Sí!** Contribuciones bienvenidas:
1. Haz fork del repositorio
2. Crea rama de característica
3. Haz cambios
4. Envía pull request

Ver `CONTRIBUTING.md` para lineamientos (si existe).

---

## Obteniendo Ayuda

### ¿Dónde puedo encontrar más información?

**Documentación:**
- [Guía de Usuario](USER-GUIDE.md) - Cómo usar
- [Docs Técnicos](TECHNICAL-DOCS.md) - Referencia para desarrolladores
- [Arquitectura](../architecture/Architecture.md) - Diseño del sistema

**Código:**
- [Repositorio GitHub](https://github.com/AlejandroMedina-Ar/Alura-Challenge-Agente-AI)
- [Issues](https://github.com/AlejandroMedina-Ar/Alura-Challenge-Agente-AI/issues)

### ¿Cómo reporto un bug?

1. Verifica si ya fue reportado: [Issues](https://github.com/AlejandroMedina-Ar/Alura-Challenge-Agente-AI/issues)
2. Si no, crea un nuevo issue con:
   - Pasos para reproducir
   - Comportamiento esperado vs actual
   - Mensajes de error
   - Info del sistema (OS, versión Python)
   - Logs relevantes

### ¿Cómo solicito una característica?

1. Abre un issue en GitHub
2. Etiqueta con "enhancement"
3. Describe:
   - Qué quieres
   - Por qué es útil
   - Cómo podría funcionar

### ¿Puedo obtener soporte comercial?

**Actualmente:** Solo soporte de la comunidad (GitHub Issues)

**Futuro:** Soporte comercial puede estar disponible para usuarios empresariales.

---

**¿Tienes una pregunta no respondida aquí?** ¡Abre un issue en GitHub!

**Versión:** 1.0.0  
**Última Actualización:** 2026-07-25
