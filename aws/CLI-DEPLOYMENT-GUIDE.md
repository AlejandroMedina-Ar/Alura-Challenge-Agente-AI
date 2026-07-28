# 🚀 Despliegue en AWS EC2 usando AWS CLI (Windows)

Guía paso a paso para desplegar TechFlow RAG Agent en AWS EC2 Free Tier usando AWS CLI desde Windows 10.

---

## 📋 Prerequisitos

✅ **Ya tienes:**
- AWS CLI instalado
- Región configurada (us-east-1)

✅ **Verificar configuración:**

```powershell
# Verificar que AWS CLI funciona
aws --version

# Ver configuración actual
aws configure list

# Verificar credenciales
aws sts get-caller-identity
```

Si `get-caller-identity` funciona, ¡estás listo! 🎉

---

## 🔑 Paso 1: Crear Key Pair (SSH)

Esta key te permitirá conectarte a tu instancia:

```powershell
# Crear key pair
aws ec2 create-key-pair `
  --key-name techflow-key `
  --query 'KeyMaterial' `
  --output text `
  --region us-east-1 > techflow-key.pem

# Verificar que se creó
Get-Content techflow-key.pem
```

**Resultado esperado:** Archivo `techflow-key.pem` con contenido que empieza con `-----BEGIN RSA PRIVATE KEY-----`

⚠️ **MUY IMPORTANTE:** Guarda este archivo en lugar seguro. Si lo pierdes, no podrás acceder a tu instancia.

---

## 🔒 Paso 2: Crear Security Group

El Security Group controla qué puertos están abiertos:

```powershell
# Crear Security Group
$SG_ID = aws ec2 create-security-group `
  --group-name techflow-rag-sg `
  --description "Security group for TechFlow RAG Agent" `
  --region us-east-1 `
  --output text `
  --query 'GroupId'

Write-Host "Security Group creado: $SG_ID"

# Agregar regla SSH (puerto 22) - Solo desde tu IP
$MI_IP = (Invoke-WebRequest -Uri "https://api.ipify.org").Content
Write-Host "Tu IP pública: $MI_IP"

aws ec2 authorize-security-group-ingress `
  --group-id $SG_ID `
  --protocol tcp `
  --port 22 `
  --cidr "$MI_IP/32" `
  --region us-east-1

Write-Host "✓ SSH permitido desde tu IP"

# Agregar regla HTTP (puerto 80) - Desde cualquier lugar
aws ec2 authorize-security-group-ingress `
  --group-id $SG_ID `
  --protocol tcp `
  --port 80 `
  --cidr 0.0.0.0/0 `
  --region us-east-1

Write-Host "✓ HTTP permitido desde cualquier lugar"

# Agregar regla HTTPS (puerto 443) - Desde cualquier lugar
aws ec2 authorize-security-group-ingress `
  --group-id $SG_ID `
  --protocol tcp `
  --port 443 `
  --cidr 0.0.0.0/0 `
  --region us-east-1

Write-Host "✓ HTTPS permitido desde cualquier lugar"

# Verificar reglas creadas
aws ec2 describe-security-groups `
  --group-ids $SG_ID `
  --region us-east-1 `
  --query 'SecurityGroups[0].IpPermissions'
```

**Resultado esperado:** Verás las 3 reglas (SSH, HTTP, HTTPS) configuradas.

---

## 🖥️ Paso 3: Buscar AMI de Ubuntu 22.04

Necesitamos el ID de la imagen de Ubuntu 22.04 LTS:

```powershell
# Buscar AMI de Ubuntu 22.04 LTS (Free Tier eligible)
$AMI_ID = aws ec2 describe-images `
  --owners 099720109477 `
  --filters "Name=name,Values=ubuntu/images/hvm-ssd/ubuntu-jammy-22.04-amd64-server-*" `
            "Name=state,Values=available" `
  --query 'Images | sort_by(@, &CreationDate) | [-1].ImageId' `
  --output text `
  --region us-east-1

Write-Host "AMI ID de Ubuntu 22.04: $AMI_ID"
```

**Resultado esperado:** Un ID como `ami-0c55b159cbfafe1f0`

---

## 🚀 Paso 4: Lanzar Instancia EC2

Ahora lanzamos la instancia t2.micro (Free Tier):

```powershell
# Lanzar instancia
$INSTANCE_ID = aws ec2 run-instances `
  --image-id $AMI_ID `
  --instance-type t2.micro `
  --key-name techflow-key `
  --security-group-ids $SG_ID `
  --block-device-mappings "DeviceName=/dev/sda1,Ebs={VolumeSize=20,VolumeType=gp3,DeleteOnTermination=true}" `
  --tag-specifications "ResourceType=instance,Tags=[{Key=Name,Value=techflow-rag-agent}]" `
  --region us-east-1 `
  --query 'Instances[0].InstanceId' `
  --output text

Write-Host ""
Write-Host "================================================"
Write-Host "Instancia lanzada exitosamente!" -ForegroundColor Green
Write-Host "Instance ID: $INSTANCE_ID" -ForegroundColor Cyan
Write-Host "================================================"
Write-Host ""
Write-Host "Esperando a que la instancia esté lista..."
```

---

## ⏳ Paso 5: Esperar que la Instancia esté Lista

```powershell
# Esperar a que la instancia esté running
aws ec2 wait instance-running `
  --instance-ids $INSTANCE_ID `
  --region us-east-1

Write-Host "✓ Instancia está running" -ForegroundColor Green

# Esperar a que los checks pasen
Write-Host "Esperando a que los checks de sistema pasen (2-3 minutos)..."
aws ec2 wait instance-status-ok `
  --instance-ids $INSTANCE_ID `
  --region us-east-1

Write-Host "✓ Instancia lista para usar!" -ForegroundColor Green
```

---

## 🌐 Paso 6: Obtener IP Pública

```powershell
# Obtener IP pública
$PUBLIC_IP = aws ec2 describe-instances `
  --instance-ids $INSTANCE_ID `
  --query 'Reservations[0].Instances[0].PublicIpAddress' `
  --output text `
  --region us-east-1

Write-Host ""
Write-Host "================================================"
Write-Host "IP Pública de tu instancia:" -ForegroundColor Yellow
Write-Host $PUBLIC_IP -ForegroundColor Cyan
Write-Host "================================================"
Write-Host ""
Write-Host "Guarda esta IP, la necesitarás para conectarte"
```

---

## 🔗 Paso 7: Conectarse por SSH

### Opción A: OpenSSH (PowerShell con OpenSSH instalado)

```powershell
# Cambiar permisos de la key (solo primera vez)
icacls techflow-key.pem /inheritance:r
icacls techflow-key.pem /grant:r "$($env:USERNAME):(R)"

# Conectar
ssh -i techflow-key.pem ubuntu@$PUBLIC_IP
```

### Opción B: PuTTY

Si usas PuTTY, necesitas convertir la key:

```powershell
# 1. Instalar PuTTYgen si no lo tienes
# Descargar de: https://www.putty.org/

# 2. Convertir .pem a .ppk
# - Abrir PuTTYgen
# - Conversions → Import Key → Seleccionar techflow-key.pem
# - Save private key → Guardar como techflow-key.ppk

# 3. Conectar con PuTTY
# - Host: ubuntu@TU_IP_PUBLICA
# - Connection → SSH → Auth → Browse → Seleccionar techflow-key.ppk
# - Open
```

---

## 📥 Paso 8: Instalar la Aplicación (Desde SSH)

Una vez conectado a tu instancia por SSH:

```bash
# Descargar script de instalación
wget https://raw.githubusercontent.com/AlejandroMedina-Ar/Alura-Challenge-Agente-AI/main/aws/install.sh

# Dar permisos de ejecución
chmod +x install.sh

# Ejecutar instalación (10-15 minutos)
bash install.sh
```

Durante la instalación, se te pedirá:
```
Enter your Gemini API Key: [pegar aquí]
Enter your Cohere API Key (optional): [pegar o Enter]
Enter Admin Password: [tu password segura]
```

---

## ✅ Paso 9: Verificar el Despliegue

Desde SSH:

```bash
# Ver estado del servicio
sudo systemctl status techflow-rag

# Ver logs
sudo journalctl -u techflow-rag -n 50
```

Desde tu navegador:
```
http://TU_IP_PUBLICA
```

---

## 🛠️ Script Completo de PowerShell

Guarda este script completo en un archivo `deploy-aws.ps1`:

```powershell
# ============================================================================
# Script de Despliegue Automatizado AWS EC2 - TechFlow RAG Agent
# ============================================================================

Write-Host "================================================" -ForegroundColor Blue
Write-Host "  TechFlow RAG Agent - AWS EC2 Deployment" -ForegroundColor Blue
Write-Host "================================================" -ForegroundColor Blue
Write-Host ""

# Variables
$REGION = "us-east-1"
$KEY_NAME = "techflow-key"
$SG_NAME = "techflow-rag-sg"
$INSTANCE_NAME = "techflow-rag-agent"

# Paso 1: Crear Key Pair
Write-Host "[1/9] Creando Key Pair..." -ForegroundColor Yellow
try {
    aws ec2 create-key-pair `
      --key-name $KEY_NAME `
      --query 'KeyMaterial' `
      --output text `
      --region $REGION > "$KEY_NAME.pem"
    
    Write-Host "✓ Key Pair creado: $KEY_NAME.pem" -ForegroundColor Green
} catch {
    Write-Host "⚠ Key Pair ya existe o error al crear" -ForegroundColor Yellow
}

# Paso 2: Obtener tu IP pública
Write-Host ""
Write-Host "[2/9] Obteniendo tu IP pública..." -ForegroundColor Yellow
$MI_IP = (Invoke-WebRequest -Uri "https://api.ipify.org").Content
Write-Host "✓ Tu IP: $MI_IP" -ForegroundColor Green

# Paso 3: Crear Security Group
Write-Host ""
Write-Host "[3/9] Creando Security Group..." -ForegroundColor Yellow
try {
    $SG_ID = aws ec2 create-security-group `
      --group-name $SG_NAME `
      --description "Security group for TechFlow RAG Agent" `
      --region $REGION `
      --output text `
      --query 'GroupId'
    
    Write-Host "✓ Security Group creado: $SG_ID" -ForegroundColor Green
} catch {
    # Si ya existe, obtener su ID
    $SG_ID = aws ec2 describe-security-groups `
      --filters "Name=group-name,Values=$SG_NAME" `
      --query 'SecurityGroups[0].GroupId' `
      --output text `
      --region $REGION
    
    Write-Host "✓ Security Group existente: $SG_ID" -ForegroundColor Green
}

# Paso 4: Configurar reglas del Security Group
Write-Host ""
Write-Host "[4/9] Configurando reglas del Security Group..." -ForegroundColor Yellow

# SSH
try {
    aws ec2 authorize-security-group-ingress `
      --group-id $SG_ID `
      --protocol tcp `
      --port 22 `
      --cidr "$MI_IP/32" `
      --region $REGION 2>$null
    Write-Host "✓ Regla SSH agregada" -ForegroundColor Green
} catch {
    Write-Host "⚠ Regla SSH ya existe" -ForegroundColor Yellow
}

# HTTP
try {
    aws ec2 authorize-security-group-ingress `
      --group-id $SG_ID `
      --protocol tcp `
      --port 80 `
      --cidr 0.0.0.0/0 `
      --region $REGION 2>$null
    Write-Host "✓ Regla HTTP agregada" -ForegroundColor Green
} catch {
    Write-Host "⚠ Regla HTTP ya existe" -ForegroundColor Yellow
}

# HTTPS
try {
    aws ec2 authorize-security-group-ingress `
      --group-id $SG_ID `
      --protocol tcp `
      --port 443 `
      --cidr 0.0.0.0/0 `
      --region $REGION 2>$null
    Write-Host "✓ Regla HTTPS agregada" -ForegroundColor Green
} catch {
    Write-Host "⚠ Regla HTTPS ya existe" -ForegroundColor Yellow
}

# Paso 5: Buscar AMI de Ubuntu 22.04
Write-Host ""
Write-Host "[5/9] Buscando AMI de Ubuntu 22.04 LTS..." -ForegroundColor Yellow
$AMI_ID = aws ec2 describe-images `
  --owners 099720109477 `
  --filters "Name=name,Values=ubuntu/images/hvm-ssd/ubuntu-jammy-22.04-amd64-server-*" `
            "Name=state,Values=available" `
  --query 'Images | sort_by(@, &CreationDate) | [-1].ImageId' `
  --output text `
  --region $REGION

Write-Host "✓ AMI encontrado: $AMI_ID" -ForegroundColor Green

# Paso 6: Lanzar instancia
Write-Host ""
Write-Host "[6/9] Lanzando instancia EC2 t2.micro..." -ForegroundColor Yellow
$INSTANCE_ID = aws ec2 run-instances `
  --image-id $AMI_ID `
  --instance-type t2.micro `
  --key-name $KEY_NAME `
  --security-group-ids $SG_ID `
  --block-device-mappings "DeviceName=/dev/sda1,Ebs={VolumeSize=20,VolumeType=gp3,DeleteOnTermination=true}" `
  --tag-specifications "ResourceType=instance,Tags=[{Key=Name,Value=$INSTANCE_NAME}]" `
  --region $REGION `
  --query 'Instances[0].InstanceId' `
  --output text

Write-Host "✓ Instancia lanzada: $INSTANCE_ID" -ForegroundColor Green

# Paso 7: Esperar a que esté running
Write-Host ""
Write-Host "[7/9] Esperando a que la instancia esté running..." -ForegroundColor Yellow
aws ec2 wait instance-running --instance-ids $INSTANCE_ID --region $REGION
Write-Host "✓ Instancia running" -ForegroundColor Green

# Paso 8: Esperar status checks
Write-Host ""
Write-Host "[8/9] Esperando status checks (puede tomar 2-3 minutos)..." -ForegroundColor Yellow
aws ec2 wait instance-status-ok --instance-ids $INSTANCE_ID --region $REGION
Write-Host "✓ Status checks passed" -ForegroundColor Green

# Paso 9: Obtener IP pública
Write-Host ""
Write-Host "[9/9] Obteniendo IP pública..." -ForegroundColor Yellow
$PUBLIC_IP = aws ec2 describe-instances `
  --instance-ids $INSTANCE_ID `
  --query 'Reservations[0].Instances[0].PublicIpAddress' `
  --output text `
  --region $REGION

Write-Host "✓ IP pública obtenida" -ForegroundColor Green

# Resumen final
Write-Host ""
Write-Host "================================================" -ForegroundColor Green
Write-Host "  ¡Instancia EC2 creada exitosamente!" -ForegroundColor Green
Write-Host "================================================" -ForegroundColor Green
Write-Host ""
Write-Host "Información de la instancia:" -ForegroundColor Cyan
Write-Host "  Instance ID:  $INSTANCE_ID"
Write-Host "  IP Pública:   $PUBLIC_IP"
Write-Host "  Key Pair:     $KEY_NAME.pem"
Write-Host "  Region:       $REGION"
Write-Host ""
Write-Host "Próximos pasos:" -ForegroundColor Yellow
Write-Host ""
Write-Host "1. Configurar permisos de la key:" -ForegroundColor White
Write-Host "   icacls $KEY_NAME.pem /inheritance:r"
Write-Host "   icacls $KEY_NAME.pem /grant:r `"`$(`$env:USERNAME):(R)`""
Write-Host ""
Write-Host "2. Conectarte por SSH:" -ForegroundColor White
Write-Host "   ssh -i $KEY_NAME.pem ubuntu@$PUBLIC_IP"
Write-Host ""
Write-Host "3. Instalar la aplicación (desde SSH):" -ForegroundColor White
Write-Host "   wget https://raw.githubusercontent.com/AlejandroMedina-Ar/Alura-Challenge-Agente-AI/main/aws/install.sh"
Write-Host "   chmod +x install.sh"
Write-Host "   bash install.sh"
Write-Host ""
Write-Host "4. Acceder desde navegador:" -ForegroundColor White
Write-Host "   http://$PUBLIC_IP"
Write-Host ""
Write-Host "================================================" -ForegroundColor Green

# Guardar información en archivo
$INFO = @"
TechFlow RAG Agent - AWS EC2 Instance Info
==========================================

Instance ID: $INSTANCE_ID
Public IP:   $PUBLIC_IP
Region:      $REGION
Key Pair:    $KEY_NAME.pem

SSH Command:
ssh -i $KEY_NAME.pem ubuntu@$PUBLIC_IP

Web Access:
http://$PUBLIC_IP

Created: $(Get-Date -Format "yyyy-MM-dd HH:mm:ss")
"@

$INFO | Out-File -FilePath "instance-info.txt" -Encoding UTF8
Write-Host "ℹ Información guardada en: instance-info.txt" -ForegroundColor Cyan
```

---

## 🚀 Uso del Script Completo

```powershell
# Guardar el script como deploy-aws.ps1

# Ejecutar
.\deploy-aws.ps1

# El script hará TODO automáticamente:
# - Crear key pair
# - Crear security group
# - Configurar reglas de firewall
# - Buscar AMI de Ubuntu
# - Lanzar instancia
# - Esperar a que esté lista
# - Mostrar IP pública y próximos pasos
```

---

## 🗑️ Eliminar Todo (Cleanup)

Si quieres eliminar la instancia y recursos:

```powershell
# Obtener Instance ID
$INSTANCE_ID = aws ec2 describe-instances `
  --filters "Name=tag:Name,Values=techflow-rag-agent" `
            "Name=instance-state-name,Values=running" `
  --query 'Reservations[0].Instances[0].InstanceId' `
  --output text `
  --region us-east-1

# Terminar instancia
aws ec2 terminate-instances `
  --instance-ids $INSTANCE_ID `
  --region us-east-1

Write-Host "Instancia $INSTANCE_ID terminada"

# Eliminar Security Group (esperar a que la instancia termine)
Start-Sleep -Seconds 60

aws ec2 delete-security-group `
  --group-name techflow-rag-sg `
  --region us-east-1

Write-Host "Security Group eliminado"

# Eliminar Key Pair
aws ec2 delete-key-pair `
  --key-name techflow-key `
  --region us-east-1

Remove-Item techflow-key.pem
Write-Host "Key Pair eliminado"
```

---

## 📊 Verificar Uso del Free Tier

```powershell
# Ver instancias activas
aws ec2 describe-instances `
  --filters "Name=instance-state-name,Values=running" `
  --query 'Reservations[*].Instances[*].[InstanceId,InstanceType,LaunchTime,State.Name]' `
  --output table `
  --region us-east-1
```

**Recuerda:** 750 horas/mes de t2.micro es suficiente para 1 instancia 24/7 durante todo el mes.

---

## 🆘 Troubleshooting

### Error: "Unable to locate credentials"

```powershell
# Configurar AWS CLI
aws configure

# Ingresar:
# AWS Access Key ID: tu-access-key
# AWS Secret Access Key: tu-secret-key
# Default region: us-east-1
# Default output format: json
```

### Error: "Key pair already exists"

```powershell
# Eliminar key pair existente
aws ec2 delete-key-pair --key-name techflow-key --region us-east-1

# Volver a ejecutar el script
```

### No puedo conectarme por SSH

```powershell
# Verificar que la instancia está running
aws ec2 describe-instances `
  --instance-ids $INSTANCE_ID `
  --region us-east-1 `
  --query 'Reservations[0].Instances[0].State.Name'

# Verificar Security Group
aws ec2 describe-security-groups `
  --group-names techflow-rag-sg `
  --region us-east-1

# Asegurarte que tu IP está permitida
```

---

¡Listo! Con esta guía podrás desplegar en AWS EC2 usando solo la línea de comandos desde Windows 10 🚀
