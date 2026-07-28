# 🚀 TechFlow Solutions - Guía de Despliegue

**Guía completa para desplegar TechFlow Solutions RAG Agent**

---

## Tabla de Contenidos

1. [Opciones de Despliegue](#opciones-de-despliegue)
2. [Despliegue Local](#despliegue-local)
3. [Despliegue en Fly.io](#despliegue-en-flyio) ⭐ **RECOMENDADO**
4. [Despliegue en VPS/Cloud](#despliegue-en-vpscloud)
5. [Consideraciones de Producción](#consideraciones-de-producción)
6. [Monitoreo](#monitoreo)
7. [Respaldo y Recuperación](#respaldo-y-recuperación)

---

## Opciones de Despliegue

### Opción 1: Despliegue Local
- **Pros:** Simple, sin Docker necesario, acceso directo
- **Cons:** Configuración manual, dependiente del SO
- **Mejor para:** Desarrollo, pruebas, usuario único

### Opción 2: Fly.io ⭐ RECOMENDADO
- **Pros:** Persistencia de datos, free tier generoso, HTTPS automático, global CDN, fácil escalabilidad
- **Cons:** Requiere tarjeta de crédito (no cobra en free tier)
- **Mejor para:** Producción, proyectos corporativos, aplicaciones que necesitan persistencia

### Opción 3: VPS/Cloud (AWS, GCP, Azure, DigitalOcean)
- **Pros:** Control total, escalable, seguro, IP dedicada
- **Cons:** Cuesta dinero, requiere conocimiento DevOps
- **Mejor para:** Empresas grandes, alta disponibilidad, requisitos de compliance específicos

---

## Despliegue Local

### Requisitos Previos

- Python 3.9 o superior
- pip package manager
- 2GB RAM mínimo
- 1GB espacio libre en disco

### Paso a Paso

```bash
# 1. Clonar repositorio
git clone https://github.com/AlejandroMedina-Ar/Alura-Challenge-Agente-AI.git
cd Alura-Challenge-Agente-AI

# 2. Crear entorno virtual
python -m venv venv

# Activar (Linux/Mac)
source venv/bin/activate

# Activar (Windows)
venv\Scripts\activate

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Configurar entorno
cp .env.example .env
# Editar .env con tus claves API

# 5. Ejecutar setup
python setup.py

# 6. Iniciar aplicación
python run.py
# o: streamlit run src/app.py
```

### Acceso

Abre el navegador en: **http://localhost:8501**

### Detener

Presiona `Ctrl+C` en la terminal

---

## Despliegue en Fly.io

**Plataforma recomendada para despliegue en producción de TechFlow RAG Agent**

### ¿Por qué Fly.io?

Fly.io es la mejor opción para desplegar esta aplicación porque:

✅ **Persistencia de Datos**
- Volúmenes persistentes que mantienen ChromaDB y documentos entre despliegues
- No pierdes documentos indexados al actualizar la aplicación

✅ **Free Tier Generoso**
- 3 máquinas virtuales compartidas incluidas
- 3GB de almacenamiento persistente gratis
- 160GB de tráfico de salida mensual
- Suficiente para proyectos pequeños/medianos

✅ **Despliegue Global**
- Data centers en 30+ regiones mundiales
- Despliega cerca de tus usuarios para baja latencia
- Anycast IPv4 y IPv6

✅ **HTTPS Automático**
- Certificados SSL gratuitos y automáticos
- Soporte para dominios personalizados

✅ **Developer Experience**
- CLI potente y fácil de usar
- Logs en tiempo real
- SSH a las máquinas para debugging
- Health checks automáticos

### Requisitos Previos

1. **Crear cuenta en Fly.io**
   - Ir a [fly.io/app/sign-up](https://fly.io/app/sign-up)
   - Se requiere tarjeta de crédito para verificación
   - No se cobra nada en el free tier

2. **Instalar flyctl CLI**

   **Windows (PowerShell como administrador):**
   ```powershell
   iwr https://fly.io/install.ps1 -useb | iex
   ```

   **macOS (Homebrew):**
   ```bash
   brew install flyctl
   ```

   **Linux:**
   ```bash
   curl -L https://fly.io/install.sh | sh
   ```

   **Verificar instalación:**
   ```bash
   flyctl version
   ```

3. **Autenticarse**
   ```bash
   flyctl auth login
   ```
   Esto abrirá tu navegador para completar la autenticación.

### Guía Paso a Paso

#### Paso 1: Preparar el Proyecto

El repositorio ya incluye los archivos necesarios:

```
techflow-rag-agent/
├── fly.toml              # Configuración de Fly.io
├── Dockerfile            # Imagen Docker optimizada
└── .dockerignore         # Archivos a excluir del build
```

Verifica que estás en el directorio del proyecto:
```bash
cd techflow-rag-agent
```

#### Paso 2: Lanzar la Aplicación

```bash
# Crear la aplicación sin desplegar aún
flyctl launch --no-deploy
```

**Responde las preguntas interactivas:**

- **Choose an app name:** `techflow-rag-agent` (o el nombre que prefieras)
- **Choose a region for deployment:** Selecciona la más cercana a tus usuarios
  - `mia` - Miami, Florida (Recomendado para Latinoamérica)
  - `iad` - Ashburn, Virginia (USA Este)
  - `lax` - Los Angeles (USA Oeste)
  - `gru` - São Paulo, Brasil
  - `mad` - Madrid, España
- **Would you like to set up a PostgreSQL database?** → **NO**
- **Would you like to set up an Upstash Redis database?** → **NO**
- **Would you like to deploy now?** → **NO**

El comando creará la aplicación en Fly.io pero no la desplegará aún.

#### Paso 3: Crear Volumen Persistente

Crea un volumen para almacenar datos de forma persistente:

```bash
# Crear volumen de 3GB (incluido en free tier)
flyctl volumes create techflow_data --region mia --size 3

# Verificar que se creó correctamente
flyctl volumes list
```

**Salida esperada:**
```
ID          NAME            SIZE    REGION  ATTACHED VM
vol_xxxxx   techflow_data   3 GB    mia     
```

**Notas importantes:**
- El volumen se crea en la misma región que elegiste para tu app
- Los datos en el volumen persisten entre despliegues
- Puedes aumentar el tamaño más adelante si es necesario

#### Paso 4: Configurar Secrets (Variables de Entorno)

Configura las API keys y contraseña de administrador como secrets:

```bash
# API Key de Google Gemini (obligatorio)
flyctl secrets set GEMINI_API_KEY="tu-gemini-api-key-aqui"

# API Key de Cohere (opcional, para fallback)
flyctl secrets set COHERE_API_KEY="tu-cohere-api-key-aqui"

# Contraseña de administrador (obligatorio)
flyctl secrets set ADMIN_PASSWORD="tu-password-segura-aqui"

# Opcional: Configurar modelos específicos
flyctl secrets set GEMINI_MODEL="gemini-3.6-flash"
flyctl secrets set COHERE_MODEL="command-r7b-12-2024"

# Opcional: Configuración de logging
flyctl secrets set LOG_LEVEL="INFO"
```

**Verificar secrets configurados:**
```bash
flyctl secrets list
```

**Notas de seguridad:**
- Los valores de los secrets nunca se muestran en texto plano
- Los secrets se inyectan como variables de entorno en tiempo de ejecución
- Cambiar un secret reinicia automáticamente la aplicación

#### Paso 5: Desplegar la Aplicación

```bash
# Primera vez (puede tomar 5-10 minutos)
flyctl deploy
```

**Qué sucede durante el despliegue:**

1. **Build de la imagen Docker:**
   - Fly.io construye la imagen desde el Dockerfile
   - Instala dependencias de Python
   - Copia el código de la aplicación
   
2. **Push al registro:**
   - La imagen se sube al registro de Fly.io
   
3. **Despliegue:**
   - Se crea una máquina virtual
   - Se monta el volumen persistente
   - Se inyectan los secrets
   - Se inicia la aplicación
   
4. **Health checks:**
   - Fly.io verifica que la app está saludable
   - Espera a que `/health` responda correctamente

**Salida esperada al finalizar:**
```
--> Pushing image done
==> Creating release
--> Release v1 created
--> Deploying release

Monitoring Deployment
  1 desired, 1 placed, 1 healthy, 0 unhealthy

--> v1 deployed successfully
```

#### Paso 6: Verificar el Despliegue

```bash
# Abrir la aplicación en el navegador
flyctl open

# Ver estado de la aplicación
flyctl status

# Ver información de las máquinas
flyctl machine list

# Ver logs en tiempo real
flyctl logs
```

**Tu aplicación estará disponible en:**
```
https://techflow-rag-agent.fly.dev
```

O en tu dominio personalizado si lo configuraste.

### Configuración Adicional

#### Cambiar Región de Despliegue

```bash
# Listar regiones disponibles
flyctl platform regions

# Agregar una nueva región
flyctl regions add gru  # São Paulo

# Remover una región
flyctl regions remove mia

# Ver regiones actuales
flyctl regions list
```

#### Escalar Recursos

**Cambiar tamaño de VM:**

```bash
# Ver configuración actual
flyctl scale show

# Cambiar a máquina con más memoria (costo adicional)
flyctl scale vm shared-cpu-2x --memory 512

# Cambiar a máquina dedicada (mejor rendimiento)
flyctl scale vm dedicated-cpu-1x --memory 2048
```

**Precios de referencia:**
- `shared-cpu-1x` (256MB): Incluido en free tier
- `shared-cpu-2x` (512MB): ~$5-7/mes
- `shared-cpu-4x` (1GB): ~$10-12/mes
- `dedicated-cpu-1x` (2GB): ~$15-20/mes

**Aumentar número de instancias (escalado horizontal):**

```bash
# Agregar más instancias para alta disponibilidad
flyctl scale count 2

# Volver a una instancia
flyctl scale count 1
```

#### Gestionar Volumen

**Ver información del volumen:**
```bash
flyctl volumes list
```

**Crear snapshot (backup):**
```bash
flyctl volumes snapshots create techflow_data
```

**Listar snapshots:**
```bash
flyctl volumes snapshots list techflow_data
```

**Aumentar tamaño del volumen:**
```bash
# Aumentar a 5GB (requiere reinicio)
flyctl volumes extend vol_xxxxx --size 5
```

#### Configurar Dominio Personalizado

```bash
# Agregar certificado SSL para tu dominio
flyctl certs create tudominio.com

# Verificar certificado
flyctl certs show tudominio.com

# Obtener la IP de Fly.io
flyctl ips list
```

Luego, en tu DNS:
```
A     tudominio.com        -> IPv4 de Fly.io
AAAA  tudominio.com        -> IPv6 de Fly.io
```

### Actualizaciones y Mantenimiento

#### Actualizar la Aplicación

```bash
# Después de hacer cambios en el código local
git add .
git commit -m "Descripción de cambios"

# Re-desplegar (sin push a GitHub)
flyctl deploy

# Fly.io construirá y desplegará automáticamente
```

**Estrategia de despliegue:**
- Por defecto usa "rolling" (zero-downtime)
- La nueva versión se despliega gradualmente
- Si hay errores, se revierte automáticamente

#### Ver Logs

```bash
# Logs en tiempo real (útil durante el despliegue)
flyctl logs

# Últimas 100 líneas
flyctl logs --lines 100

# Filtrar por nivel de log
flyctl logs --level error
flyctl logs --level warn

# Buscar en logs
flyctl logs | grep "ERROR"
```

#### Debugging Avanzado

**SSH a la máquina:**
```bash
# Abrir una consola SSH
flyctl ssh console

# Una vez dentro, puedes:
# - Ver archivos: ls /app
# - Ver logs: cat /app/data/logs/application.log
# - Verificar procesos: ps aux
# - Ver uso de recursos: df -h, free -h
```

**Ejecutar comandos remotos:**
```bash
# Ejecutar comando sin abrir consola interactiva
flyctl ssh console -C "ls -la /app/data"
```

#### Gestionar Secrets

**Actualizar un secret:**
```bash
flyctl secrets set ADMIN_PASSWORD="nueva-password-segura"
# La app se reinicia automáticamente
```

**Eliminar un secret:**
```bash
flyctl secrets unset COHERE_API_KEY
```

**Importar múltiples secrets desde archivo:**
```bash
# Crear archivo .env.production (no commitearlo)
# GEMINI_API_KEY=xxx
# COHERE_API_KEY=yyy
# ADMIN_PASSWORD=zzz

flyctl secrets import < .env.production
```

### Monitoreo

#### Dashboard Web

Accede al dashboard en: [fly.io/apps/techflow-rag-agent](https://fly.io/apps/techflow-rag-agent)

**Métricas disponibles:**
- CPU usage
- Memory usage
- Network traffic
- Request rate
- Response times
- Health check status

#### CLI

```bash
# Ver estado general
flyctl status

# Ver checks de salud
flyctl checks list

# Ver métricas en tiempo real
flyctl dashboard
```

#### Configurar Alertas

En el dashboard web:
1. Ve a tu app → Monitoring
2. Configura alertas para:
   - CPU > 80%
   - Memory > 90%
   - Health checks fallando
   - Crashes de aplicación

### Troubleshooting

#### La aplicación no inicia

```bash
# Ver logs detallados
flyctl logs

# Buscar errores específicos
flyctl logs | grep -i error

# Verificar configuración
flyctl config display

# Verificar secrets
flyctl secrets list
```

**Problemas comunes:**
- Secret de API key mal configurado
- Volumen no montado correctamente
- Puerto incorrecto expuesto

#### Error de memoria (OOM - Out of Memory)

```bash
# Síntomas en logs:
# "Killed" o "OOM killed"

# Solución: Aumentar memoria
flyctl scale vm shared-cpu-2x --memory 512
```

#### Health checks fallando

```bash
# Ver estado de health checks
flyctl checks list

# Si fallan constantemente:
# 1. Verificar que Streamlit esté sirviendo en puerto 8501
# 2. Verificar que /_stcore/health responde
# 3. Aumentar grace period en fly.toml si la app tarda en iniciar
```

Edita `fly.toml`:
```toml
[[services.http_checks]]
  grace_period = "120s"  # Aumentar si la app tarda en iniciar
```

#### Volumen lleno

```bash
# Ver uso del volumen (desde SSH)
flyctl ssh console -C "df -h /app/data"

# Solución 1: Limpiar datos viejos
flyctl ssh console
# rm -rf /app/data/logs/*.log

# Solución 2: Aumentar tamaño del volumen
flyctl volumes list
flyctl volumes extend vol_xxxxx --size 5
```

#### App muy lenta

**Posibles causas:**
1. **CPU/RAM insuficiente** → Escalar VM
2. **Región lejana** → Mover a región más cercana
3. **Muchos documentos** → Optimizar chunk_size y top_k
4. **API de LLM lenta** → Verificar latencia de Gemini/Cohere

```bash
# Verificar uso de recursos
flyctl machine list
flyctl ssh console -C "top -b -n 1"
```

### Respaldo y Recuperación

#### Crear Backup Manual

```bash
# Crear snapshot del volumen
flyctl volumes snapshots create techflow_data --description "Backup antes de actualización"

# Listar snapshots
flyctl volumes snapshots list techflow_data
```

#### Backup Automatizado

Crear script `backup.sh`:

```bash
#!/bin/bash
# Script para backup automático

DATE=$(date +%Y%m%d-%H%M%S)
flyctl volumes snapshots create techflow_data --description "Backup automatico $DATE"

# Retener solo últimos 7 snapshots
# (limpiar manualmente viejos si es necesario)
```

Ejecutar desde tu máquina local con cron o Task Scheduler.

#### Restaurar desde Backup

1. **Crear nuevo volumen desde snapshot:**
   ```bash
   flyctl volumes create techflow_data_restored --snapshot-id snap_xxxxx --region mia
   ```

2. **Actualizar fly.toml para usar el nuevo volumen:**
   ```toml
   [[mounts]]
     source = "techflow_data_restored"
     destination = "/app/data"
   ```

3. **Re-desplegar:**
   ```bash
   flyctl deploy
   ```

### Costos y Facturación

#### Free Tier (Incluido)

- **3 VMs compartidas** (shared-cpu-1x con 256MB RAM)
- **3GB de volumen persistente**
- **160GB de tráfico de salida/mes**
- **Certificados SSL ilimitados**

**Suficiente para:**
- Proyectos personales
- Demos
- 5-10 usuarios concurrentes

#### Costos Adicionales

**Si excedes el free tier:**

- **VMs adicionales:** ~$2-3/VM/mes (shared-cpu-1x)
- **Memoria adicional:** 
  - 512MB: +$3-5/mes
  - 1GB: +$10-12/mes
  - 2GB: +$15-20/mes
- **Volumen adicional:** ~$0.15/GB/mes
- **Tráfico:** $0.02/GB después de 160GB

**Ver uso actual:**
```bash
# Ver facturación en el dashboard
flyctl dashboard

# O en: https://fly.io/dashboard/personal/billing
```

### Mejores Prácticas

✅ **Hacer:**
- Crear snapshots antes de actualizaciones grandes
- Monitorear logs regularmente
- Usar secrets para información sensible
- Configurar alertas de monitoreo
- Probar en local antes de desplegar
- Documentar cambios de configuración

❌ **No hacer:**
- Commitear secrets al repositorio
- Ignorar health checks fallidos
- Desplegar sin probar localmente
- Olvidar hacer backups
- Usar contraseñas débiles

---

## Despliegue en VPS/Cloud

**Para proyectos que requieren más control y persistencia de datos**

### Opción 1: DigitalOcean Droplet

**Crear Droplet:**

1. **Cuenta:** Regístrate en https://digitalocean.com
2. **Create Droplet:**
   - **Distribución:** Ubuntu 22.04 LTS
   - **Plan:** Basic ($6/mes) o Premium ($12/mes)
   - **CPU:** 1-2 vCPUs
   - **RAM:** 2-4GB
   - **Storage:** 50GB SSD
   - **Datacenter:** Más cercano a tus usuarios

3. **Agregar SSH Key** (recomendado) o usa contraseña

4. **Create Droplet**

**Configurar servidor:**

```bash
# 1. Conectar via SSH
ssh root@tu-droplet-ip

# 2. Actualizar sistema
apt update && apt upgrade -y

# 3. Instalar Python y dependencias
apt install python3 python3-pip python3-venv git -y

# 4. Crear usuario no-root (opcional pero recomendado)
adduser techflow
usermod -aG sudo techflow
su - techflow

# 5. Clonar repositorio
git clone https://github.com/AlejandroMedina-Ar/Alura-Challenge-Agente-AI.git
cd Alura-Challenge-Agente-AI

# 6. Crear entorno virtual
python3 -m venv venv
source venv/bin/activate

# 7. Instalar dependencias
pip install -r requirements.txt

# 8. Configurar variables de entorno
nano .env
# Agregar:
# GEMINI_API_KEY=tu_clave
# COHERE_API_KEY=tu_clave
# ADMIN_PASSWORD=tu_contraseña

# 9. Ejecutar setup
python setup.py

# 10. Probar aplicación
streamlit run src/app.py --server.port 8501
```

**Acceder:**
- Abre: `http://tu-droplet-ip:8501`

**Ejecutar como servicio (para que corra siempre):**

```bash
# Crear archivo de servicio systemd
sudo nano /etc/systemd/system/techflow.service
```

Contenido:

```ini
[Unit]
Description=TechFlow Solutions RAG Agent
After=network.target

[Service]
Type=simple
User=techflow
WorkingDirectory=/home/techflow/Alura-Challenge-Agente-AI
Environment="PATH=/home/techflow/Alura-Challenge-Agente-AI/venv/bin"
ExecStart=/home/techflow/Alura-Challenge-Agente-AI/venv/bin/streamlit run src/app.py --server.port 8501 --server.address 0.0.0.0
Restart=always

[Install]
WantedBy=multi-user.target
```

Activar servicio:

```bash
sudo systemctl daemon-reload
sudo systemctl enable techflow
sudo systemctl start techflow
sudo systemctl status techflow
```

### Opción 2: AWS EC2

**Lanzar instancia:**

```bash
# 1. Lanzar instancia EC2
# - Ubuntu 22.04 LTS
# - t2.small o t3.small (2GB RAM)
# - 20GB storage
# - Security Group: permitir puerto 22 (SSH), 8501 (Streamlit)

# 2. Conectar via SSH
ssh -i tu-key.pem ubuntu@tu-ec2-ip

# 3. Seguir mismos pasos que DigitalOcean
```

### Opción 3: Google Cloud Platform (GCP)

```bash
# 1. Crear VM instance
gcloud compute instances create techflow-vm \
  --zone=us-central1-a \
  --machine-type=e2-small \
  --image-family=ubuntu-2204-lts \
  --image-project=ubuntu-os-cloud \
  --boot-disk-size=20GB

# 2. Conectar
gcloud compute ssh techflow-vm --zone=us-central1-a

# 3. Seguir mismos pasos que DigitalOcean
```

### Configurar HTTPS (Opcional pero Recomendado)

**Usando Nginx como reverse proxy + Let's Encrypt:**

```bash
# 1. Instalar Nginx
sudo apt install nginx certbot python3-certbot-nginx -y

# 2. Configurar dominio (necesitas un dominio apuntando a tu IP)
sudo nano /etc/nginx/sites-available/techflow
```

Contenido:

```nginx
server {
    listen 80;
    server_name tu-dominio.com;

    location / {
        proxy_pass http://localhost:8501;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Activar y obtener SSL:

```bash
sudo ln -s /etc/nginx/sites-available/techflow /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx

# Obtener certificado SSL gratis
sudo certbot --nginx -d tu-dominio.com
```

Ahora accede via: `https://tu-dominio.com`

---

## Consideraciones de Producción

### Seguridad

#### 1. Contraseñas Fuertes

```bash
# Generar contraseña segura
openssl rand -base64 32

# Usar en .env
ADMIN_PASSWORD=contraseña_generada_fuerte
```

#### 2. Firewall

```bash
# Ubuntu/Debian (ufw)
sudo ufw allow 22/tcp    # SSH
sudo ufw allow 80/tcp    # HTTP
sudo ufw allow 443/tcp   # HTTPS
sudo ufw enable

# Si no usas Nginx, permitir Streamlit
sudo ufw allow 8501/tcp
```

#### 3. Actualizar Regularmente

```bash
# Actualizar sistema
sudo apt update && sudo apt upgrade -y

# Actualizar dependencias Python
pip install -r requirements.txt --upgrade
```

#### 4. Rotar Claves API

- Rotar cada 90 días
- Generar nuevas en dashboards de Google/Cohere
- Actualizar en `.env` o Secrets
- Reiniciar aplicación

### Rendimiento

#### Recursos Mínimos Recomendados:

- **2GB RAM** - Para operación básica
- **4GB RAM** - Para mejor rendimiento
- **2 CPU cores** - Mínimo
- **20GB storage** - Para app + datos

#### Optimización:

1. Reducir Top-K si respuestas son lentas
2. Usar SSD para almacenamiento
3. Aumentar RAM si procesas muchos documentos
4. Considerar CDN para assets estáticos

### Confiabilidad

#### Auto-reinicio en caso de falla:

Ya configurado en el servicio systemd con `Restart=always`.

#### Health checks:

```bash
# Crear script de monitoreo
nano /home/techflow/health_check.sh
```

```bash
#!/bin/bash
if ! curl -f http://localhost:8501/_stcore/health; then
    sudo systemctl restart techflow
    echo "$(date): TechFlow restarted" >> /var/log/techflow-health.log
fi
```

```bash
chmod +x /home/techflow/health_check.sh

# Agregar a crontab (cada 5 minutos)
crontab -e
*/5 * * * * /home/techflow/health_check.sh
```

---

## Monitoreo

### Logs de Aplicación

**Local/VPS:**
```bash
# Ver logs de aplicación
tail -f data/logs/application.log

# Ver logs de servicio systemd
sudo journalctl -u techflow -f
```

**Streamlit Cloud:**
- Ve a tu app en https://share.streamlit.io
- Click en "Logs"

### Monitoreo de Recursos

```bash
# Instalar htop
sudo apt install htop

# Monitorear recursos
htop

# Uso de disco
df -h

# Memoria
free -h
```

### Métricas de Aplicación

En el Panel de Administración:
- Total de documentos
- Documentos indexados
- Tamaño de vector store
- Almacenamiento usado

---

## Respaldo y Recuperación

### Qué Respaldar

1. **Base de datos vectorial:** `data/chromadb/`
2. **Documentos:** `data/knowledge_library/`
3. **Configuración:** `data/config.json`
4. **Variables de entorno:** `.env` (¡mantener seguro!)

### Script de Respaldo

```bash
#!/bin/bash
# backup.sh

BACKUP_DIR="/backup/techflow-$(date +%Y%m%d-%H%M%S)"
mkdir -p "$BACKUP_DIR"

# Respaldar data
cp -r data/chromadb "$BACKUP_DIR/"
cp -r data/knowledge_library "$BACKUP_DIR/"
cp data/config.json "$BACKUP_DIR/"

# Crear archivo comprimido
tar -czf "$BACKUP_DIR.tar.gz" "$BACKUP_DIR"
rm -rf "$BACKUP_DIR"

echo "Respaldo creado: $BACKUP_DIR.tar.gz"
```

### Respaldos Automáticos

```bash
# Editar crontab
crontab -e

# Agregar respaldo diario a las 2 AM
0 2 * * * /home/techflow/backup.sh
```

### Recuperación

```bash
# 1. Detener aplicación
sudo systemctl stop techflow

# 2. Extraer respaldo
tar -xzf backup-20260725-020000.tar.gz

# 3. Restaurar datos
cp -r backup-20260725-020000/chromadb data/
cp -r backup-20260725-020000/knowledge_library data/
cp backup-20260725-020000/config.json data/

# 4. Iniciar aplicación
sudo systemctl start techflow
```

---

## Estimación de Costos

### Fly.io

**Free Tier:** $0/mes
- 3 VMs compartidas (shared-cpu-1x, 256MB RAM cada una)
- 3GB volumen persistente
- 160GB tráfico de salida/mes
- Certificados SSL ilimitados
- **Ideal para:** Proyectos pequeños/medianos, 5-10 usuarios concurrentes

**Producción Básica:** ~$5-10/mes
- shared-cpu-2x con 512MB-1GB RAM
- 3-5GB volumen
- **Ideal para:** 10-50 usuarios concurrentes

**Producción Media:** ~$15-25/mes
- dedicated-cpu-1x con 2GB RAM
- 10GB volumen
- **Ideal para:** 50-200 usuarios concurrentes

### DigitalOcean Droplet
- **Basic (2GB RAM):** $12/mes
- **Premium (4GB RAM):** $24/mes

### AWS EC2
- **t3.small (2GB RAM):** ~$15-20/mes
- **t3.medium (4GB RAM):** ~$30-40/mes

### Google Cloud (GCP)
- **e2-small (2GB RAM):** ~$13-18/mes
- **e2-medium (4GB RAM):** ~$27-35/mes

### Costos Adicionales (Todos los Proveedores)
- **Dominio:** ~$10-15/año
- **Certificado SSL:** Gratuito (Let's Encrypt / Fly.io automático)
- **Almacenamiento respaldos:** ~$1-5/mes
- **Transferencia de datos:** Usualmente incluida (verificar límites)

---

## Mejores Prácticas

✅ **Hacer:**
- Usar HTTPS en producción (automático en Fly.io)
- Respaldar datos regularmente (snapshots en Fly.io)
- Monitorear logs frecuentemente
- Actualizar dependencias periódicamente
- Usar contraseñas fuertes
- Rotar claves API cada 90 días
- Configurar health checks
- Probar cambios localmente antes de desplegar

❌ **No hacer:**
- Exponer puerto 8501 directamente sin proxy (Fly.io lo maneja)
- Commitear secrets a git
- Usar contraseñas por defecto
- Ignorar actualizaciones de seguridad
- Saltear respaldos
- Desplegar sin verificar logs
- Ignorar alertas de monitoreo

---

## Troubleshooting

### La aplicación no inicia

```bash
# Verificar logs
sudo journalctl -u techflow -n 50

# Verificar puerto en uso
sudo lsof -i :8501

# Reiniciar servicio
sudo systemctl restart techflow
```

### Sin memoria

```bash
# Verificar uso de memoria
free -h

# Aumentar RAM del servidor
# O reducir Top-K y tamaño de chunk
```

### Rendimiento lento

- Reducir valor de Top-K
- Aumentar recursos del servidor
- Usar SSD para storage
- Verificar conexión a Internet
- Revisar logs para errores de API

---

**¿Necesitas ayuda con el despliegue?** Revisa [FAQ](FAQ.md) o abre un issue en GitHub.

**Versión:** 1.0.0  
**Última Actualización:** 2026-07-25
