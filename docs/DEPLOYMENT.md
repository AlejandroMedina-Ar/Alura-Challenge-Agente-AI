# 🚀 TechFlow Solutions - Guía de Despliegue

**Guía completa para desplegar TechFlow Solutions RAG Agent**

---

## Tabla de Contenidos

1. [Opciones de Despliegue](#opciones-de-despliegue)
2. [Despliegue Local](#despliegue-local)
3. [Despliegue en Streamlit Community Cloud](#despliegue-en-streamlit-community-cloud)
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

### Opción 2: Streamlit Community Cloud ⭐ RECOMENDADO
- **Pros:** Hosting gratuito, despliegue automático, HTTPS, sin servidor
- **Cons:** Repositorio público requerido (o plan pagado), recursos limitados
- **Mejor para:** Demos, proyectos públicos, despliegue rápido sin servidor propio

### Opción 3: VPS/Cloud (AWS, GCP, Azure, DigitalOcean)
- **Pros:** Control total, escalable, seguro, IP dedicada
- **Cons:** Cuesta dinero, requiere conocimiento DevOps
- **Mejor para:** Empresas, producción, alta disponibilidad

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

## Despliegue en Streamlit Community Cloud

**Hosting gratuito para aplicaciones Streamlit - RECOMENDADO para despliegue rápido**

### Requisitos Previos
- Cuenta GitHub
- Repositorio GitHub (público o plan pagado de Streamlit)
- Claves API de Gemini y Cohere

### Paso 1: Preparar el Repositorio

**1.1. Asegúrate que tu código esté en GitHub:**

```bash
# Si aún no has subido el código
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/tu-usuario/tu-repo.git
git push -u origin main
```

**1.2. Verifica que tengas estos archivos:**

- ✅ `requirements.txt` - Dependencias Python
- ✅ `src/app.py` - Aplicación principal Streamlit
- ✅ `.gitignore` - Para excluir `.env` y `data/`
- ✅ `.env.example` - Template de variables de entorno

**Nota:** NO subas `.env` con tus claves reales a GitHub.

### Paso 2: Crear Cuenta en Streamlit Cloud

1. **Visita:** https://share.streamlit.io
2. **Inicia sesión** con tu cuenta GitHub
3. Streamlit pedirá permisos para acceder a tus repositorios (acepta)

### Paso 3: Desplegar la Aplicación

**3.1. Click en "New app"**

**3.2. Configurar el despliegue:**

- **Repository:** Selecciona `tu-usuario/tu-repo`
- **Branch:** `main` (o la rama que uses)
- **Main file path:** `src/app.py`
- **App URL (opcional):** Personaliza tu URL: `tu-app.streamlit.app`

**3.3. Click en "Advanced settings"**

### Paso 4: Configurar Secrets (Variables de Entorno)

En la sección "Secrets", agrega tus claves API en formato TOML:

```toml
# Secrets de Streamlit Cloud
GEMINI_API_KEY = "tu_clave_gemini_real"
COHERE_API_KEY = "tu_clave_cohere_real"
ADMIN_PASSWORD = "tu_contraseña_segura"
```

**⚠️ IMPORTANTE:**
- Usa claves de **producción**, no las de desarrollo
- Usa contraseña **fuerte** (no "admin123")
- Estas claves son privadas (no aparecen en el código público)

### Paso 5: Desplegar

1. Click en **"Deploy!"**
2. Streamlit comenzará a construir la aplicación (3-5 minutos)
3. Verás logs del proceso de construcción
4. Cuando termine, tu app estará en: `https://tu-app.streamlit.app`

### Paso 6: Verificar el Despliegue

**6.1. Accede a tu URL:** `https://tu-app.streamlit.app`

**6.2. Prueba la aplicación:**
- ✅ Modo Guest funciona (sin login)
- ✅ Modo Admin funciona (con contraseña correcta)
- ✅ Gemini 3.6 Flash responde
- ✅ Fallback a Cohere funciona si Gemini falla

**6.3. Si hay errores:**
- Revisa los logs en el panel de Streamlit Cloud
- Verifica que las claves API sean correctas
- Verifica que `requirements.txt` tenga todas las dependencias

### Actualizar la Aplicación Desplegada

**Streamlit re-despliega automáticamente cuando haces push:**

```bash
# Hacer cambios en el código
git add .
git commit -m "Actualizar funcionalidad X"
git push origin main

# Streamlit detecta el push y re-despliega automáticamente (2-3 minutos)
```

**Re-despliegue manual:**
1. Ve a https://share.streamlit.io
2. Click en tu app
3. Click en "Reboot" o "Redeploy"

### Actualizar Secrets

1. Ve a tu app en https://share.streamlit.io
2. Click en "Settings" → "Secrets"
3. Edita los valores
4. Click en "Save"
5. La app se reiniciará automáticamente

### Limitaciones de Streamlit Community Cloud

**Recursos:**
- **RAM:** 1GB (puede causar problemas con muchos documentos grandes)
- **CPU:** Compartida (puede ser lenta en horas pico)
- **Storage:** Temporal (se pierde al reiniciar)
- **Apps:** 3 apps gratuitas máximo

**Persistencia de Datos:**
- ⚠️ Los datos en `data/` se pierden al reiniciar la app
- ⚠️ ChromaDB se reinicia (vectores se pierden)
- ⚠️ Documentos cargados se pierden

**Solución para persistencia:**
- Usa almacenamiento externo (S3, Google Drive, etc.)
- O considera VPS si necesitas datos persistentes

**Otros límites:**
- Apps públicas por defecto (o plan pagado para privadas)
- Timeouts en operaciones largas
- Sin acceso a shell/terminal

### Costo

- **Plan Community:** Gratuito
  - 3 apps públicas
  - 1GB RAM por app
  - Storage temporal
  
- **Plan Team:** ~$20/mes por miembro
  - Apps privadas
  - Más recursos
  - Soporte prioritario

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

### Streamlit Community Cloud
- **Costo:** Gratuito (plan community)
- **Limitaciones:** 3 apps, 1GB RAM, público

### DigitalOcean Droplet
- **Basic (2GB RAM):** $12/mes
- **Premium (4GB RAM):** $24/mes

### AWS EC2
- **t3.small (2GB RAM):** ~$15-20/mes
- **t3.medium (4GB RAM):** ~$30-40/mes

### Google Cloud (GCP)
- **e2-small (2GB RAM):** ~$13-18/mes
- **e2-medium (4GB RAM):** ~$27-35/mes

### Costos Adicionales
- **Dominio:** ~$10-15/año
- **Certificado SSL:** Gratuito (Let's Encrypt)
- **Almacenamiento respaldos:** ~$1-5/mes
- **Transferencia de datos:** Usualmente incluida

---

## Mejores Prácticas

✅ **Hacer:**
- Usar HTTPS en producción
- Respaldar datos regularmente
- Monitorear logs
- Actualizar dependencias
- Usar contraseñas fuertes
- Rotar claves API
- Configurar health checks

❌ **No hacer:**
- Exponer puerto 8501 directamente (usar reverse proxy)
- Commitear secretos a git
- Usar contraseñas por defecto
- Ignorar actualizaciones de seguridad
- Saltear respaldos

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
