# ============================================================================
# Script de Despliegue Automatizado AWS EC2 - TechFlow RAG Agent
# Para Windows PowerShell
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
Write-Host ""
