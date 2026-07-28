# 🚀 Guía Completa de Despliegue en AWS EC2 Free Tier

Esta guía te llevará paso a paso para desplegar TechFlow RAG Agent en AWS EC2 usando el Free Tier (12 meses gratis).

---

## 📋 Tabla de Contenidos

1. [Requisitos Previos](#requisitos-previos)
2. [Crear Instancia EC2](#crear-instancia-ec2)
3. [Conectarse a la Instancia](#conectarse-a-la-instancia)
4. [Instalar la Aplicación](#instalar-la-aplicación)
5. [Verificar el Despliegue](#verificar-el-despliegue)
6. [Configuración de Seguridad](#configuración-de-seguridad)
7. [Mantenimiento y Actualizaciones](#mantenimiento-y-actualizaciones)
8. [Troubleshooting](#troubleshooting)

---

## 1. Requisitos Previos

### ✅ Cuenta AWS
- Crear cuenta en [aws.amazon.com](https://aws.amazon.com)
- Verificar con tarjeta de crédito (no se cobra en Free Tier)
- Free Tier incluye:
  - **750 horas/mes** de t2.micro (1GB RAM, 1 vCPU)
  - **30GB** de almacenamiento EBS
  - **15GB** de tráfico de salida
  - **Válido por 12 meses**

### ✅ API Keys
- **Gemini API Key**: [Google AI Studio](https://makersuite.google.com/app/apikey) - Gratuito
- **Cohere API Key**: [Cohere Dashboard](https://dashboard.cohere.com/api-keys) - Gratuito (opcional)

### ✅ SSH Client
- **Windows**: PuTTY o PowerShell con OpenSSH
- **macOS/Linux**: Terminal (ssh ya incluido)

---

## 2. Crear Instancia EC2

### Paso 2.1: Acceder a la Consola EC2

1. Inicia sesión en [console.aws.amazon.com](https://console.aws.amazon.com)
2. Busca "EC2" en la barra de búsqueda
3. Click en **"Launch Instance"** (Lanzar instancia)

### Paso 2.2: Configurar la Instancia

#### **Name and tags**
```
Name: techflow-rag-agent
```

#### **Application and OS Images (Amazon Machine Image)**
- **Quick Start**: Ubuntu
- **AMI**: Ubuntu Server 22.04 LTS (HVM), SSD Volume Type
- **Architecture**: 64-bit (x86)
- ✅ **Free tier eligible**

#### **Instance type**
- **Type**: `t2.micro`
- **Specs**: 1 vCPU, 1 GiB RAM
- ✅ **Free tier eligible**

#### **Key pair (login)**
- Click **"Create new key pair"**
  - **Name**: `techflow-key`
  - **Type**: RSA
  - **Format**: 
    - `.pem` para macOS/Linux
    - `.ppk` para Windows (PuTTY)
- Click **"Create key pair"**
- ⚠️ **IMPORTANTE**: Guarda el archivo `.pem` o `.ppk` en lugar seguro. No podrás descargarlo después.

#### **Network settings**
Click en **"Edit"** y configura:

- ✅ **Auto-assign public IP**: Enable
- **Firewall (security groups)**: Create security group
  - **Security group name**: `techflow-rag-sg`
  - **Description**: Security group for TechFlow RAG Agent

**Inbound rules** (agregar 3 reglas):

| Type | Protocol | Port Range | Source | Description |
|------|----------|------------|--------|-------------|
| SSH | TCP | 22 | My IP | SSH access |
| HTTP | TCP | 80 | Anywhere (0.0.0.0/0) | Web access |
| HTTPS | TCP | 443 | Anywhere (0.0.0.0/0) | Secure web access |

⚠️ **Importante**: Usar "My IP" para SSH es más seguro. Solo tu IP puede conectarse.

#### **Configure storage**
- **Size**: `20 GiB` (Free tier incluye hasta 30GB)
- **Volume Type**: `gp3` (General Purpose SSD)
- **Delete on Termination**: ✅ Marcado

#### **Advanced details** (Opcional - puedes dejarlo por defecto)

### Paso 2.3: Lanzar la Instancia

1. Revisa el resumen en el panel derecho
2. Verifica que diga **"Free tier eligible"**
3. Click en **"Launch instance"**
4. Espera 2-3 minutos mientras se inicializa

### Paso 2.4: Obtener IP Pública

1. Ve a **EC2 Dashboard** → **Instances**
2. Selecciona tu instancia `techflow-rag-agent`
3. Copia la **Public IPv4 address** (ejemplo: `54.123.45.67`)
4. Guarda esta IP, la necesitarás para conectarte

---

## 3. Conectarse a la Instancia

### Opción A: Windows (PowerShell)

```powershell
# Navegar a la carpeta donde guardaste la key
cd C:\Users\TuUsuario\Downloads

# Cambiar permisos (solo primera vez)
icacls techflow-key.pem /inheritance:r
icacls techflow-key.pem /grant:r "$($env:USERNAME):(R)"

# Conectar
ssh -i techflow-key.pem ubuntu@54.123.45.67
# (Reemplaza con tu IP pública)
```

### Opción B: macOS/Linux

```bash
# Cambiar permisos (solo primera vez)
chmod 400 ~/Downloads/techflow-key.pem

# Conectar
ssh -i ~/Downloads/techflow-key.pem ubuntu@54.123.45.67
# (Reemplaza con tu IP pública)
```

### Opción C: Windows (PuTTY)

1. Abrir PuTTY
2. **Host Name**: `ubuntu@54.123.45.67`
3. **Connection → SSH → Auth**: Browse y seleccionar `techflow-key.ppk`
4. Click **Open**

**Primera conexión**: Te preguntará si confías en el host, escribe `yes` y Enter.

---

## 4. Instalar la Aplicación

Una vez conectado a tu instancia EC2:

### Paso 4.1: Descargar el Script de Instalación

```bash
# Descargar el script
wget https://raw.githubusercontent.com/AlejandroMedina-Ar/Alura-Challenge-Agente-AI/main/aws/install.sh

# Dar permisos de ejecución
chmod +x install.sh

# Ejecutar (tomará 10-15 minutos)
bash install.sh
```

### Paso 4.2: Configurar API Keys

Durante la instalación, se te pedirá:

```
Enter your Gemini API Key: AIzaSy...  [pega tu key]
Enter your Cohere API Key (optional): [pega o presiona Enter]
Enter Admin Password: ********  [contraseña segura]
```

### Paso 4.3: Esperar la Instalación

El script instalará automáticamente:
- ✅ Python 3.11 y dependencias del sistema
- ✅ Clonación del repositorio desde GitHub
- ✅ Virtual environment de Python
- ✅ Todas las dependencias de Python
- ✅ Configuración del servicio systemd
- ✅ Firewall (UFW)
- ✅ Nginx como reverse proxy
- ✅ Inicio automático de la aplicación

**Tiempo estimado**: 10-15 minutos en t2.micro

---

## 5. Verificar el Despliegue

### Paso 5.1: Verificar el Servicio

```bash
# Ver estado del servicio
sudo systemctl status techflow-rag

# Debería mostrar: "Active: active (running)"
```

### Paso 5.2: Ver Logs

```bash
# Logs en tiempo real
sudo journalctl -u techflow-rag -f

# Últimas 50 líneas
sudo journalctl -u techflow-rag -n 50
```

### Paso 5.3: Acceder a la Aplicación

Abre tu navegador y ve a:
```
http://TU-IP-PUBLICA
```

Por ejemplo: `http://54.123.45.67`

**✅ Deberías ver la interfaz de TechFlow RAG Agent**

---

## 6. Configuración de Seguridad

### Paso 6.1: Ejecutar Script de Seguridad (RECOMENDADO)

```bash
cd /home/ubuntu/techflow-rag-agent/aws

# Ejecutar con sudo
sudo bash security-setup.sh
```

Este script configura:
- ✅ Fail2Ban (protección contra fuerza bruta)
- ✅ SSH hardening (deshabilita login con password)
- ✅ Actualizaciones automáticas de seguridad
- ✅ Rotación de logs
- ✅ Permisos seguros de archivos

⚠️ **IMPORTANTE**: Después de ejecutar este script, solo podrás conectarte por SSH usando tu key (no con password).

### Paso 6.2: Verificar Fail2Ban

```bash
# Estado de fail2ban
sudo fail2ban-client status

# Ver IPs baneadas
sudo fail2ban-client status sshd
```

---

## 7. Mantenimiento y Actualizaciones

### Actualizar la Aplicación

Cuando haya nuevas versiones en GitHub:

```bash
cd /home/ubuntu/techflow-rag-agent/aws
bash update.sh
```

Este script:
1. Detiene el servicio
2. Hace backup de `.env`
3. Hace pull de GitHub
4. Actualiza dependencias
5. Restaura `.env`
6. Reinicia el servicio

### Comandos Útiles

```bash
# Ver estado
sudo systemctl status techflow-rag

# Reiniciar servicio
sudo systemctl restart techflow-rag

# Detener servicio
sudo systemctl stop techflow-rag

# Iniciar servicio
sudo systemctl start techflow-rag

# Ver logs
sudo journalctl -u techflow-rag -f

# Ver uso de recursos
htop
free -h
df -h
```

### Backups

```bash
# Backup de datos
cd /home/ubuntu
tar -czf techflow-backup-$(date +%Y%m%d).tar.gz \
    techflow-rag-agent/data \
    techflow-rag-agent/.env

# Listar backups
ls -lh techflow-backup-*.tar.gz

# Descargar backup a tu máquina local
# (Desde tu máquina local, no desde EC2)
scp -i techflow-key.pem ubuntu@54.123.45.67:~/techflow-backup-*.tar.gz ~/Desktop/
```

---

## 8. Troubleshooting

### Problema: La aplicación no inicia

```bash
# Ver logs detallados
sudo journalctl -u techflow-rag -n 100 --no-pager

# Verificar que el puerto 8501 está escuchando
sudo netstat -tulpn | grep 8501

# Verificar procesos
ps aux | grep streamlit
```

### Problema: No puedo acceder desde el navegador

1. **Verificar Security Group en AWS Console**:
   - EC2 → Security Groups → techflow-rag-sg
   - Debe tener regla de entrada para puerto 80 desde 0.0.0.0/0

2. **Verificar firewall local**:
   ```bash
   sudo ufw status
   # Debe mostrar: 80/tcp ALLOW Anywhere
   ```

3. **Verificar nginx**:
   ```bash
   sudo systemctl status nginx
   sudo nginx -t
   ```

### Problema: Out of Memory (OOM)

```bash
# Ver uso de memoria
free -h

# Ver procesos por memoria
ps aux --sort=-%mem | head -10

# Si hay OOM, considera:
# 1. Escalar a t3.small (2GB RAM - no free tier)
# 2. Agregar swap
sudo fallocate -l 2G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab
```

### Problema: SSH no funciona después de security-setup.sh

- El script deshabilita autenticación por password
- Solo puedes conectarte con tu SSH key
- Si perdiste tu key, necesitarás:
  1. Detener la instancia
  2. Crear snapshot del volumen
  3. Crear nueva instancia desde snapshot
  4. Asignar nueva key pair

### Problema: Error al clonar repositorio

```bash
# Si el repo es privado, configura credenciales:
git config --global credential.helper store
git clone https://github.com/AlejandroMedina-Ar/Alura-Challenge-Agente-AI.git
```

---

## 📊 Costos Estimados

### Free Tier (12 meses)
- **Costo**: $0/mes
- **Incluye**: 750 horas/mes t2.micro
- **Suficiente para**: 1 instancia 24/7

### Después del Free Tier
- **t2.micro**: ~$8.50/mes (1GB RAM)
- **t3.small**: ~$15/mes (2GB RAM, mejor rendimiento)
- **t3.medium**: ~$30/mes (4GB RAM, producción)

### Costos Adicionales
- **EBS Storage**: $0.10/GB/mes (después de 30GB gratis)
- **Transfer OUT**: $0.09/GB (después de 15GB gratis/mes)
- **Elastic IP**: Gratis si está asociada a instancia activa

**Consejo**: Detén la instancia cuando no la uses para ahorrar horas del free tier.

---

## 🎯 Checklist de Despliegue

- [ ] Cuenta AWS creada y verificada
- [ ] Instancia EC2 t2.micro lanzada
- [ ] Security Group configurado (puertos 22, 80, 443)
- [ ] SSH key descargada y guardada
- [ ] Conexión SSH exitosa
- [ ] Script install.sh ejecutado
- [ ] API keys configuradas
- [ ] Aplicación accesible desde navegador
- [ ] Security-setup.sh ejecutado (opcional pero recomendado)
- [ ] Primer backup creado

---

## 🆘 Soporte

**Problemas con el despliegue?**
- Revisa los logs: `sudo journalctl -u techflow-rag -n 100`
- Consulta el [README principal](../README.md)
- Abre un issue en [GitHub](https://github.com/AlejandroMedina-Ar/Alura-Challenge-Agente-AI/issues)

---

## 📚 Recursos Adicionales

- [AWS Free Tier](https://aws.amazon.com/free/)
- [EC2 Documentation](https://docs.aws.amazon.com/ec2/)
- [Ubuntu Server Guide](https://ubuntu.com/server/docs)
- [Streamlit Documentation](https://docs.streamlit.io/)

---

**¡Listo!** Tu aplicación TechFlow RAG Agent está desplegada en AWS EC2 Free Tier 🎉
