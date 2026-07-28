# TechFlow Solutions - Agente RAG Corporativo

Asistente inteligente basado en Retrieval-Augmented Generation (RAG) para consultar documentos corporativos internos. Permite indexar documentos (PDF, TXT, MD, DOCX), generar embeddings vectoriales y realizar consultas en lenguaje natural que el agente responde utilizando exclusivamente el contenido de los documentos de la empresa.

---

## 🌐 Demo en Vivo

### **[http://54.205.4.104](http://54.205.4.104)**

> **Nota:** Demo desplegada en AWS EC2 Free Tier (t3.micro, 1GB RAM). Totalmente funcional y gratuita por 12 meses.

---

## 📋 Características Principales

### 🔐 Acceso Inteligente
- **Modo Guest automático:** Acceso directo al chat cuando hay documentos indexados
- **Modo Admin:** Gestión completa de documentos y configuración
- **Login flexible:** Cambio entre modos sin cerrar sesión
- **Seguridad:** Contraseñas hasheadas con bcrypt

### 💬 Chat con RAG
- Respuestas contextualizadas desde tus documentos
- Historial de conversación persistente
- Indicación de fuentes consultadas
- Detección inteligente de saludos y consultas fuera de contexto

### 📚 Gestión de Documentos
- Soporte multi-formato: PDF, TXT, MD, DOCX
- Detección de duplicados por checksum SHA-256
- Indexación automática al subir
- Operaciones por lotes (indexar múltiples documentos)
- Re-indexación selectiva

### ⚙️ Configuración Flexible
- Dual LLM: Gemini 3.6 Flash + Cohere Command-R
- Parámetros RAG ajustables (chunk_size, top_k, temperature)
- Tema claro/oscuro
- Exportar/importar configuración

### 🔄 Sistema de Fallback
- Cambio automático a Cohere si Gemini falla
- Cooldown inteligente de 5 minutos
- Manejo de rate limits y timeouts

---

## 🚀 Instalación y Despliegue

### 📦 Opción 1: Instalación Local (Desarrollo y Pruebas)

#### Requisitos

- **Python 3.11+**
- **2GB RAM** mínimo
- **API Key de Gemini** (gratuita en [Google AI Studio](https://makersuite.google.com/app/apikey))
- **API Key de Cohere** (opcional, gratuita en [Cohere Dashboard](https://dashboard.cohere.com/api-keys))

#### Paso a Paso

```bash
# 1. Clonar el repositorio
git clone https://github.com/AlejandroMedina-Ar/Alura-Challenge-Agente-AI.git
cd Alura-Challenge-Agente-AI

# 2. Crear entorno virtual
python -m venv venv

# 3. Activar entorno virtual
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# 4. Instalar dependencias
pip install -r requirements.txt

# 5. Configurar variables de entorno
# Windows:
copy .env.example .env
# Linux/Mac:
cp .env.example .env

# 6. Editar .env con tus API keys
# GEMINI_API_KEY=tu-api-key-aqui
# ADMIN_PASSWORD=tu-password-segura

# 7. Ejecutar configuración inicial
python setup.py

# 8. (Opcional) Tests de integración
python test_integration.py

# 9. Iniciar aplicación
python run.py
```

La aplicación se abrirá automáticamente en `http://localhost:8501`

#### ⚡ Primera Configuración

**Al abrir por primera vez:**
1. El sistema pedirá login de administrador (no hay documentos)
2. Ingresa la contraseña de `.env` (ADMIN_PASSWORD)
3. Ve a **"Panel de Administración"** → **"Documentos"**
4. Sube documentos PDF, TXT, MD o DOCX
5. Espera a que se indexen automáticamente

**Accesos posteriores:**
- El sistema abrirá directamente en **Modo Guest** (acceso al chat)
- Para gestionar documentos, usa **"🔐 Login como Admin"** en el sidebar

---

### ☁️ Opción 2: Despliegue en AWS EC2 Free Tier (Producción)

#### ⭐ ¿Por qué AWS EC2?

AWS EC2 Free Tier es la **mejor opción** para desplegar TechFlow RAG Agent porque ofrece:

- ✅ **GRATIS por 12 meses** (750 horas/mes, suficiente para 24/7)
- ✅ **t3.micro con 1GB RAM** (Free Tier elegible en todas las regiones)
- ✅ **Persistencia completa** de datos (30GB almacenamiento incluido)
- ✅ **IP pública** incluida
- ✅ **Escalable** después del free tier

#### 📋 Prerequisitos

1. **Cuenta AWS**
   - Crear en [aws.amazon.com](https://aws.amazon.com/free/)
   - Requiere tarjeta de crédito para verificación (no se cobra en Free Tier)

2. **API Keys**
   - [Gemini API Key](https://makersuite.google.com/app/apikey) - Gratuito
   - [Cohere API Key](https://dashboard.cohere.com/api-keys) - Gratuito (opcional)

3. **AWS CLI** (para deploy automatizado desde Windows)
   - Descargar e instalar desde [AWS CLI](https://aws.amazon.com/cli/)
   - Configurar con `aws configure`

#### 🎯 Método 1: Deploy Automatizado con PowerShell (Recomendado)

**Desde tu Windows 10:**

```powershell
# 1. Descargar script de deploy automatizado
Invoke-WebRequest -Uri "https://raw.githubusercontent.com/AlejandroMedina-Ar/Alura-Challenge-Agente-AI/main/aws/deploy-aws.ps1" -OutFile "deploy-aws.ps1"

# 2. Ejecutar (crea instancia EC2 completa en 5-10 minutos)
.\deploy-aws.ps1

# El script hará TODO automáticamente:
# ✅ Crear key pair para SSH
# ✅ Crear security group con reglas de firewall
# ✅ Buscar AMI de Ubuntu 22.04 LTS más reciente
# ✅ Lanzar instancia t3.micro
# ✅ Esperar a que esté lista
# ✅ Mostrar IP pública y próximos pasos
```

**Próximos pasos después del script:**

```powershell
# 3. Configurar permisos de la key
icacls techflow-key.pem /inheritance:r
icacls techflow-key.pem /grant:r "$($env:USERNAME):(R)"

# 4. Conectar por SSH
ssh -i techflow-key.pem ubuntu@IP-PUBLICA

# 5. Instalar la aplicación (desde SSH, dentro del servidor)
wget https://raw.githubusercontent.com/AlejandroMedina-Ar/Alura-Challenge-Agente-AI/main/aws/install.sh
chmod +x install.sh
bash install.sh

# Durante la instalación ingresa:
# - Gemini API Key
# - Cohere API Key (opcional, Enter para omitir)
# - Admin Password
```

**Tiempo total:** 15-20 minutos

**📚 Documentación completa:** [aws/CLI-DEPLOYMENT-GUIDE.md](aws/CLI-DEPLOYMENT-GUIDE.md)

---

#### 🖱️ Método 2: Deploy Manual desde Consola Web AWS

**1. Crear Instancia EC2**

En la [consola de AWS](https://console.aws.amazon.com/ec2/):

- **Launch Instance** → Ubuntu Server 22.04 LTS
- **Instance type:** `t3.micro` (⚠️ **Importante:** En la mayoría de regiones debes usar t3.micro, no t2.micro, para Free Tier)
- **Key pair:** Create new → `techflow-key.pem` (¡guarda el archivo!)
- **Network settings:**
  - Allow SSH (22) from My IP
  - Allow HTTP (80) from Anywhere
  - Allow HTTPS (443) from Anywhere
- **Storage:** 20GB gp3 (incluido en Free Tier)
- **Launch instance**

**2. Conectarse por SSH**

```bash
# Windows PowerShell
ssh -i techflow-key.pem ubuntu@TU-IP-PUBLICA

# macOS/Linux
chmod 400 techflow-key.pem
ssh -i techflow-key.pem ubuntu@TU-IP-PUBLICA
```

**3. Instalar la Aplicación**

```bash
# Descargar e instalar (10-15 minutos)
wget https://raw.githubusercontent.com/AlejandroMedina-Ar/Alura-Challenge-Agente-AI/main/aws/install.sh
chmod +x install.sh
bash install.sh

# Durante la instalación ingresa:
# - Gemini API Key
# - Cohere API Key (opcional)
# - Admin Password
```

El script instalará automáticamente:
- ✅ Python 3.11 y todas las dependencias
- ✅ Aplicación completa desde GitHub
- ✅ Nginx como reverse proxy
- ✅ Servicio systemd (auto-inicio)
- ✅ Firewall UFW configurado
- ✅ Swap memory de 2GB (previene OOM)

**4. Acceder a la Aplicación**

Abre tu navegador:
```
http://TU-IP-PUBLICA
```

¡Listo! Tu aplicación está en producción 🎉

---

#### 🔧 Comandos Útiles de Mantenimiento

```bash
# Ver estado del servicio
sudo systemctl status techflow-rag

# Ver logs en tiempo real
sudo journalctl -u techflow-rag -f

# Reiniciar aplicación
sudo systemctl restart techflow-rag

# Actualizar app (cuando haya cambios en GitHub)
cd ~/techflow-rag-agent
git pull origin main
sudo systemctl restart techflow-rag

# Ver uso de memoria y disco
free -h
df -h

# Editar variables de entorno (API keys, password)
nano ~/techflow-rag-agent/.env
sudo systemctl restart techflow-rag
```

---

#### 🛡️ Seguridad Adicional (Recomendado)

```bash
# Ejecutar script de hardening de seguridad
cd ~/techflow-rag-agent/aws
sudo bash security-setup.sh

# Esto configura:
# ✅ Fail2ban (protección contra ataques SSH)
# ✅ SSH hardening (deshabilita root login y password auth)
# ✅ Actualizaciones automáticas de seguridad
# ✅ Log rotation para logs de la app
```

---

#### 💰 Costos

**Free Tier (12 meses):** $0/mes
- 750 horas/mes de t3.micro
- 30GB almacenamiento EBS
- 15GB tráfico de salida

**Después del Free Tier:** ~$8-10/mes
- t3.micro 24/7: ~$7.50/mes
- 20GB EBS gp3: ~$1.60/mes
- **Total:** ~$9/mes (muy económico)

**Si necesitas más recursos:**
- t3.small (2GB RAM): ~$15/mes
- t3.medium (4GB RAM): ~$30/mes

---

#### 📚 Documentación Completa de AWS

| Guía | Descripción |
|------|-------------|
| [CLI-DEPLOYMENT-GUIDE.md](aws/CLI-DEPLOYMENT-GUIDE.md) | Deploy automatizado con AWS CLI y PowerShell |
| [DEPLOYMENT-GUIDE.md](aws/DEPLOYMENT-GUIDE.md) | Deploy manual paso a paso con screenshots |

---

#### ⚠️ Notas Importantes del Deploy en AWS

1. **Región us-east-1:** Usa `t3.micro`, NO `t2.micro` (cambio reciente de AWS)
2. **Swap memory:** El script instala 2GB de swap automáticamente para prevenir crashes por OOM
3. **Versiones de dependencias:**
   - `torch==2.2.2` (versión estable)
   - `transformers==4.40.2` (compatible)
   - `sentence-transformers==2.7.0` (probado y estable)
   - `numpy<2.0.0` (numpy 2.x rompe compatibilidad)
4. **Batch size optimizado:** Reducido a 8 (en lugar de 32) para mejor uso de RAM en t3.micro
5. **PDFs grandes:** Indexar de uno en uno, evitar múltiples a la vez

---

#### 🆘 Troubleshooting AWS

**502 Bad Gateway:**
```bash
# El servicio crasheó, reiniciar:
sudo systemctl restart techflow-rag
sudo journalctl -u techflow-rag -n 50
```

**Out of Memory (OOM):**
```bash
# Verificar swap está activo:
free -h
# Si Swap: 0B, agregar swap:
sudo fallocate -l 2G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
```

**Error "Numpy is not available":**
```bash
cd ~/techflow-rag-agent
source venv/bin/activate
pip uninstall numpy -y
pip install "numpy<2.0.0"
sudo systemctl restart techflow-rag
```

---

## 🏗️ Arquitectura del Sistema

### Flujo de una Consulta (Query Flow)

```
Usuario → Chat
    ↓
EmbeddingService (multilingual-e5-base)
    ↓
ChromaDB (búsqueda por similitud)
    ↓
Retriever (top 5 fragmentos)
    ↓
PromptBuilder (construcción de contexto)
    ↓
LLM (Gemini 3.6 Flash → Cohere fallback)
    ↓
Respuesta + Fuentes
```

### Flujo de Indexación

```
Admin → Upload documento
    ↓
FileManager (guardar en data/knowledge_library/)
    ↓
DocumentRepository (checksum SHA-256)
    ↓
TextChunker (chunk_size=1000, overlap=200)
    ↓
EmbeddingService (768 dimensiones, batch_size=8)
    ↓
ChromaDB (almacenar chunks + embeddings)
    ↓
MetadataRepository (metadata JSON)
```

### Diagrama de Componentes

```
┌──────────────────────────────────────────────────────┐
│           Interfaz Web (Streamlit)                    │
│  ┌─────────┐  ┌─────────┐  ┌──────────────────────┐ │
│  │  Chat   │  │  Admin  │  │  Configuración       │ │
│  └────┬────┘  └────┬────┘  └─────────┬────────────┘ │
└───────┼────────────┼──────────────────┼──────────────┘
        │            │                  │
┌───────┼────────────┼──────────────────┼──────────────┐
│       ▼            ▼                  ▼              │
│  ChatService  IndexingService  ConfigService        │
└───────┼────────────┼──────────────────┼──────────────┘
        │            │                  │
┌───────┼────────────┼──────────────────┼──────────────┐
│       ▼            ▼                  ▼              │
│  LLM Layer    RAG Pipeline    Storage Layer         │
│  • Gemini     • Retriever     • Documents           │
│  • Cohere     • Chunker       • Metadata            │
│               • Embeddings    • Config              │
└───────┼────────────┼──────────────────┼──────────────┘
        │            ▼                  │
        │    ┌──────────────┐           │
        └───▶│  ChromaDB    │◀──────────┘
             └──────────────┘
```

Para más detalles, ver [Architecture.md](architecture/Architecture.md)

---

## 📂 Estructura del Proyecto

```
techflow-rag-agent/
├── src/
│   ├── app.py                  # Entry point Streamlit
│   ├── config/                 # Configuración
│   ├── utils/                  # Utilidades
│   ├── storage/                # Persistencia
│   ├── auth/                   # Autenticación
│   ├── llm/                    # Proveedores LLM
│   ├── rag/                    # Pipeline RAG
│   ├── services/               # Lógica de negocio
│   └── ui/                     # Interfaz Streamlit
├── data/
│   ├── chromadb/               # Vector store
│   ├── knowledge_library/      # Documentos
│   ├── logs/                   # Logs
│   └── config.json             # Config runtime
├── aws/                        # Scripts de deploy AWS
│   ├── deploy-aws.ps1          # Deploy automatizado PowerShell
│   ├── install.sh              # Instalación en EC2
│   ├── update.sh               # Script de actualización
│   ├── security-setup.sh       # Hardening de seguridad
│   ├── CLI-DEPLOYMENT-GUIDE.md # Guía AWS CLI
│   └── DEPLOYMENT-GUIDE.md     # Guía manual paso a paso
├── architecture/               # Docs arquitectura
├── specs/                      # Especificaciones
├── docs/                       # Documentación
├── .env                        # Variables entorno
├── requirements.txt            # Dependencias
├── setup.py                    # Setup inicial
├── run.py                      # Inicializador
└── test_integration.py         # Tests
```

Ver [Source-Code-Structure.md](architecture/Source-Code-Structure.md) para detalles completos.

---

## 🛠️ Tecnologías

| Componente | Tecnología | Versión | Propósito |
|------------|-----------|---------|-----------|
| **Framework Web** | Streamlit | 1.47.1 | Interfaz interactiva |
| **LLM Principal** | Google Gemini | 3.6 Flash | Generación de respuestas |
| **LLM Fallback** | Cohere Command-R | command-r7b-12-2024 | Backup |
| **Embeddings** | Sentence Transformers | 2.7.0 | Embeddings (768d) |
| **Vector Store** | ChromaDB | 1.0.16 | Base de datos vectorial |
| **Framework RAG** | LangChain | 0.3.27 | Orquestación RAG |
| **PDF Parser** | PyMuPDF | 1.23+ | Extracción de texto |
| **Auth** | bcrypt | 5.0+ | Hash de contraseñas |
| **Lenguaje** | Python | 3.11+ | Base del proyecto |
| **PyTorch** | torch | 2.2.2 | Base para embeddings |
| **Transformers** | transformers | 4.40.2 | Modelos de lenguaje |

---

## 👥 Modos de Acceso

### Modo Guest (Usuario Común)

**Acceso:** Automático cuando hay documentos indexados

**Permisos:**
- ✅ Usar chat para consultar documentos
- ✅ Ver biblioteca de conocimiento
- ✅ Ver configuración (read-only)
- ✅ Cambiar tema (claro/oscuro)
- ❌ Subir o eliminar documentos
- ❌ Modificar configuración
- ❌ Acceder a Panel de Administración

**Interfaz:**
- Sidebar: "👤 Usuario: Invitado"
- Botón: "🔐 Login como Admin" disponible

### Modo Admin (Administrador)

**Acceso:** Login con contraseña de admin

**Permisos:**
- ✅ Todas las funciones de Guest
- ✅ Gestión completa de documentos
- ✅ Modificar configuración del sistema
- ✅ Panel de Administración completo
- ✅ Métricas y estadísticas
- ✅ Cambiar a vista Guest sin cerrar sesión

**Interfaz:**
- Sidebar: "👤 Usuario: admin" + "🔑 Rol: Admin"
- Botones: "👥 Modo Usuario" y "🚪 Cerrar Sesión"

---

## 💡 Ejemplos de Uso

### Preguntas Técnicas
- ¿Cómo solicito una notebook nueva en la empresa?
- ¿Cuál es el horario de atención de la Mesa de Ayuda?
- ¿Cómo me conecto a la VPN corporativa?
- ¿Qué hago si olvido mi contraseña corporativa?

### Preguntas Corporativas
- ¿Cuál es la misión de TechFlow Solutions?
- ¿Qué modalidad de trabajo aplica en la empresa?
- ¿Cuál es el código de vestimenta?
- ¿Cómo es el proceso de onboarding?

### Ejemplo de Respuesta

**Pregunta:** ¿Cómo solicito una notebook nueva?

**Respuesta:**
> Para solicitar una notebook nueva en TechFlow Solutions:
>
> 1. Ingresa al Portal de Tickets
> 2. Categoría: "Hardware / Equipamiento"
> 3. Completa el formulario indicando el motivo
> 4. Si es equipamiento adicional, necesitas aprobación de tu responsable
>
> **Tiempo de entrega:** 1-2 días hábiles en oficina, hasta 5 días para remotos
>
> **Fuente:** Manual de TI - Capítulo 4

---

## 🔧 Configuración Avanzada

### Parámetros RAG

| Parámetro | Default | Descripción |
|-----------|---------|-------------|
| `chunk_size` | 1000 | Tamaño de cada fragmento |
| `chunk_overlap` | 200 | Solapamiento entre fragmentos |
| `top_k` | 5 | Fragmentos recuperados |
| `temperature` | 0.7 | Creatividad del LLM |
| `embedding_dim` | 768 | Dimensión del embedding |
| `batch_size` | 8 | Lote de chunks para embeddings (optimizado para 1GB RAM) |

### Variables de Entorno (.env)

```bash
# LLM API Keys
GEMINI_API_KEY=tu-gemini-api-key
COHERE_API_KEY=tu-cohere-api-key

# Modelos (configuración por defecto)
GEMINI_MODEL=gemini-3.6-flash
COHERE_MODEL=command-r7b-12-2024

# Autenticación
ADMIN_PASSWORD=tu-password-segura

# RAG Parameters (opcional)
CHUNK_SIZE=1000
CHUNK_OVERLAP=200
TOP_K=5
TEMPERATURE=0.7

# Embeddings
EMBEDDING_MODEL=intfloat/multilingual-e5-base
```

---

## 📚 Documentación Adicional

| Documento | Descripción |
|-----------|-------------|
| [Architecture.md](architecture/Architecture.md) | Arquitectura general del sistema |
| [Source-Code-Structure.md](architecture/Source-Code-Structure.md) | Estructura del código fuente |
| [USER-GUIDE.md](docs/USER-GUIDE.md) | Guía de usuario completa |
| [TECHNICAL-DOCS.md](docs/TECHNICAL-DOCS.md) | Documentación técnica detallada |
| [TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md) | Solución de problemas |
| [FAQ.md](docs/FAQ.md) | Preguntas frecuentes |
| [SECURITY-NOTES.md](docs/SECURITY-NOTES.md) | Consideraciones de seguridad |
| [aws/CLI-DEPLOYMENT-GUIDE.md](aws/CLI-DEPLOYMENT-GUIDE.md) | Deploy automatizado con AWS CLI |
| [aws/DEPLOYMENT-GUIDE.md](aws/DEPLOYMENT-GUIDE.md) | Deploy manual en AWS EC2 |

---

## 🐛 Solución de Problemas

### Error: "ModuleNotFoundError: No module named 'X'"
```bash
pip install -r requirements.txt
```

### Error: "API Key inválida"
Verifica que `.env` tenga las API keys correctas:
```bash
GEMINI_API_KEY=tu-api-key-aqui
```

### ChromaDB no persiste datos
Verifica que `data/chromadb/` existe y tiene permisos de escritura:
```bash
ls -la data/chromadb/
```

### App no abre automáticamente
Abre manualmente: `http://localhost:8501`

### Error "Numpy is not available"
```bash
pip uninstall numpy -y
pip install "numpy<2.0.0"
```

### 502 Bad Gateway en AWS
```bash
sudo systemctl restart techflow-rag
sudo journalctl -u techflow-rag -f
```

Ver [TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md) para más detalles.

---

## 🆕 Historial de Actualizaciones

### Julio 2026 - v1.0.0

#### Migración a AWS EC2
- ✅ **Deploy en AWS EC2 Free Tier** (t3.micro, 1GB RAM)
- ✅ Scripts automatizados de instalación
- ✅ Deploy con AWS CLI + PowerShell para Windows
- ✅ Documentación completa de despliegue
- ✅ Optimizaciones para 1GB RAM (batch_size=8, swap memory)

#### Correcciones Críticas
- ✅ Fix de versiones de dependencias (numpy<2.0, torch 2.2.2, transformers 4.40.2)
- ✅ Resolución de conflictos de compatibilidad
- ✅ Optimización de uso de memoria (garbage collection)
- ✅ Prevención de OOM con swap memory

#### Migración a Gemini 3.6 Flash
- ✅ Actualizado a **Gemini 3.6 Flash** (última versión)
- ✅ Modelos Gemini 1.5 deprecados
- ✅ Mejor rendimiento y reducción de costos

#### Sistema de Autenticación Mejorado
- ✅ **Acceso automático como Guest** cuando hay documentos
- ✅ Login solo necesario para funciones de administración
- ✅ Alternancia entre modos sin cerrar sesión
- ✅ Flujo de onboarding optimizado

#### Embeddings Locales
- ✅ Migración a **Sentence Transformers** (multilingual-e5-base)
- ✅ Embeddings sin dependencia de APIs externas
- ✅ 768 dimensiones optimizadas
- ✅ Soporte multilingüe mejorado
- ✅ Lazy loading para reducir uso de RAM al inicio

#### UI y UX
- ✅ Tema claro por defecto
- ✅ Sidebar siempre visible
- ✅ Gestión de documentos mejorada
- ✅ Panel de administración completo
- ✅ Operaciones por lotes

#### Correcciones y Optimizaciones
- ✅ Corrección de duplicate keys en componentes
- ✅ Validación defensiva de datos
- ✅ CSS completo para temas claro/oscuro
- ✅ Logging mejorado para troubleshooting
- ✅ Manejo robusto de errores

---

## 📄 Licencia

Este proyecto está licenciado bajo la **Licencia MIT** - ver el archivo [LICENSE](LICENSE) para más detalles.

Libre para usar, modificar y distribuir para uso personal, comercial o interno de **TechFlow Solutions**.

---

## 👤 Créditos

**Proyecto:** Alura Challenge - Agente RAG con IA  
**Empresa:** TechFlow Solutions  
**Desarrollado por:** [Oscar Alejandro Medina](https://github.com/AlejandroMedina-Ar)

---

## 🌟 Stack de Tecnologías

Construido con las mejores herramientas del ecosistema de IA:

- [Streamlit](https://streamlit.io) - Framework web para IA/ML
- [LangChain](https://langchain.com) - Framework RAG y orquestación LLM
- [ChromaDB](https://www.trychroma.com) - Base de datos vectorial
- [Google Gemini](https://deepmind.google/technologies/gemini/) - LLM de última generación
- [Cohere](https://cohere.com) - LLM enterprise
- [HuggingFace](https://huggingface.co) - Modelos open-source (Sentence Transformers)
- [PyTorch](https://pytorch.org) - Framework de deep learning

---

**⭐ TechFlow Solutions - Transformación Digital con Inteligencia Artificial**
