#!/bin/bash

################################################################################
# Script de Despliegue Automatizado para Fly.io
# TechFlow RAG Agent
#
# Este script facilita el despliegue y gestión de la aplicación en Fly.io
################################################################################

set -e  # Salir si hay error

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Variables
APP_NAME="techflow-rag-agent"
REGION="mia"
VOLUME_NAME="techflow_data"
VOLUME_SIZE=3

################################################################################
# Funciones Helper
################################################################################

print_header() {
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${BLUE}  $1${NC}"
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo ""
}

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ $1${NC}"
}

check_flyctl() {
    if ! command -v flyctl &> /dev/null; then
        print_error "flyctl no está instalado"
        echo ""
        echo "Instala flyctl desde: https://fly.io/docs/hands-on/install-flyctl/"
        echo ""
        echo "  macOS/Linux: curl -L https://fly.io/install.sh | sh"
        echo "  Windows:     iwr https://fly.io/install.ps1 -useb | iex"
        echo ""
        exit 1
    fi
    print_success "flyctl está instalado"
}

check_auth() {
    if ! flyctl auth whoami &> /dev/null; then
        print_error "No estás autenticado en Fly.io"
        echo ""
        echo "Ejecuta: flyctl auth login"
        echo ""
        exit 1
    fi
    print_success "Autenticado en Fly.io"
}

################################################################################
# Comandos Principales
################################################################################

cmd_setup() {
    print_header "Configuración Inicial de Fly.io"
    
    check_flyctl
    check_auth
    
    echo ""
    print_info "Creando aplicación en Fly.io..."
    
    if flyctl apps list | grep -q "$APP_NAME"; then
        print_warning "La aplicación '$APP_NAME' ya existe"
        read -p "¿Deseas continuar con la configuración? (y/n): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            exit 0
        fi
    else
        flyctl launch --no-deploy --name "$APP_NAME" --region "$REGION"
        print_success "Aplicación creada"
    fi
    
    echo ""
    print_info "Verificando volumen persistente..."
    
    if flyctl volumes list -a "$APP_NAME" | grep -q "$VOLUME_NAME"; then
        print_warning "El volumen '$VOLUME_NAME' ya existe"
    else
        print_info "Creando volumen de ${VOLUME_SIZE}GB..."
        flyctl volumes create "$VOLUME_NAME" --region "$REGION" --size "$VOLUME_SIZE" -a "$APP_NAME"
        print_success "Volumen creado"
    fi
    
    echo ""
    print_warning "Configuración de secrets necesaria"
    echo ""
    echo "Ejecuta los siguientes comandos para configurar tus secrets:"
    echo ""
    echo "  flyctl secrets set GEMINI_API_KEY=\"tu-gemini-api-key\" -a $APP_NAME"
    echo "  flyctl secrets set COHERE_API_KEY=\"tu-cohere-api-key\" -a $APP_NAME"
    echo "  flyctl secrets set ADMIN_PASSWORD=\"tu-password-segura\" -a $APP_NAME"
    echo ""
    echo "O usa el comando: $0 secrets"
    echo ""
    print_success "Configuración inicial completada"
}

cmd_secrets() {
    print_header "Configurar Secrets"
    
    check_flyctl
    check_auth
    
    echo ""
    print_info "Configurando secrets para $APP_NAME"
    echo ""
    
    # GEMINI_API_KEY
    read -p "Gemini API Key: " GEMINI_KEY
    if [ -n "$GEMINI_KEY" ]; then
        flyctl secrets set GEMINI_API_KEY="$GEMINI_KEY" -a "$APP_NAME"
        print_success "GEMINI_API_KEY configurado"
    fi
    
    echo ""
    
    # COHERE_API_KEY
    read -p "Cohere API Key (opcional, Enter para omitir): " COHERE_KEY
    if [ -n "$COHERE_KEY" ]; then
        flyctl secrets set COHERE_API_KEY="$COHERE_KEY" -a "$APP_NAME"
        print_success "COHERE_API_KEY configurado"
    fi
    
    echo ""
    
    # ADMIN_PASSWORD
    read -sp "Admin Password: " ADMIN_PASS
    echo ""
    if [ -n "$ADMIN_PASS" ]; then
        flyctl secrets set ADMIN_PASSWORD="$ADMIN_PASS" -a "$APP_NAME"
        print_success "ADMIN_PASSWORD configurado"
    fi
    
    echo ""
    print_success "Secrets configurados exitosamente"
}

cmd_deploy() {
    print_header "Desplegando en Fly.io"
    
    check_flyctl
    check_auth
    
    echo ""
    print_info "Desplegando $APP_NAME..."
    echo ""
    
    flyctl deploy -a "$APP_NAME"
    
    echo ""
    print_success "Despliegue completado"
    echo ""
    print_info "Tu aplicación está disponible en:"
    flyctl status -a "$APP_NAME" | grep "Hostname"
}

cmd_logs() {
    print_header "Logs de la Aplicación"
    
    check_flyctl
    
    echo ""
    print_info "Mostrando logs en tiempo real (Ctrl+C para salir)..."
    echo ""
    
    flyctl logs -a "$APP_NAME"
}

cmd_status() {
    print_header "Estado de la Aplicación"
    
    check_flyctl
    check_auth
    
    echo ""
    flyctl status -a "$APP_NAME"
    
    echo ""
    print_header "Máquinas"
    flyctl machine list -a "$APP_NAME"
    
    echo ""
    print_header "Volúmenes"
    flyctl volumes list -a "$APP_NAME"
    
    echo ""
    print_header "Secrets Configurados"
    flyctl secrets list -a "$APP_NAME"
}

cmd_open() {
    print_header "Abrir Aplicación"
    
    check_flyctl
    
    flyctl open -a "$APP_NAME"
    print_success "Aplicación abierta en el navegador"
}

cmd_ssh() {
    print_header "Conectar via SSH"
    
    check_flyctl
    check_auth
    
    echo ""
    print_info "Abriendo consola SSH..."
    echo ""
    
    flyctl ssh console -a "$APP_NAME"
}

cmd_backup() {
    print_header "Crear Backup del Volumen"
    
    check_flyctl
    check_auth
    
    TIMESTAMP=$(date +%Y%m%d-%H%M%S)
    DESCRIPTION="Backup manual $TIMESTAMP"
    
    echo ""
    print_info "Creando snapshot del volumen..."
    echo ""
    
    flyctl volumes snapshots create "$VOLUME_NAME" --description "$DESCRIPTION" -a "$APP_NAME"
    
    print_success "Snapshot creado exitosamente"
    
    echo ""
    print_info "Snapshots disponibles:"
    flyctl volumes snapshots list "$VOLUME_NAME" -a "$APP_NAME"
}

cmd_scale() {
    print_header "Escalar Recursos"
    
    check_flyctl
    check_auth
    
    echo ""
    print_info "Configuración actual:"
    flyctl scale show -a "$APP_NAME"
    
    echo ""
    echo "Opciones disponibles:"
    echo "  1) shared-cpu-1x  (256MB)  - Free tier"
    echo "  2) shared-cpu-2x  (512MB)  - ~\$5-7/mes"
    echo "  3) shared-cpu-4x  (1GB)    - ~\$10-12/mes"
    echo "  4) Cancelar"
    echo ""
    
    read -p "Selecciona una opción (1-4): " -n 1 -r
    echo ""
    echo ""
    
    case $REPLY in
        1)
            flyctl scale vm shared-cpu-1x --memory 256 -a "$APP_NAME"
            print_success "Escalado a shared-cpu-1x (256MB)"
            ;;
        2)
            flyctl scale vm shared-cpu-2x --memory 512 -a "$APP_NAME"
            print_success "Escalado a shared-cpu-2x (512MB)"
            ;;
        3)
            flyctl scale vm shared-cpu-4x --memory 1024 -a "$APP_NAME"
            print_success "Escalado a shared-cpu-4x (1GB)"
            ;;
        4)
            print_info "Cancelado"
            exit 0
            ;;
        *)
            print_error "Opción inválida"
            exit 1
            ;;
    esac
}

cmd_restart() {
    print_header "Reiniciar Aplicación"
    
    check_flyctl
    check_auth
    
    echo ""
    print_info "Reiniciando $APP_NAME..."
    
    flyctl apps restart "$APP_NAME"
    
    print_success "Aplicación reiniciada"
}

cmd_destroy() {
    print_header "Eliminar Aplicación"
    
    check_flyctl
    check_auth
    
    echo ""
    print_warning "⚠️  ADVERTENCIA: Esto eliminará la aplicación y TODOS los datos"
    print_warning "Esta acción NO se puede deshacer"
    echo ""
    
    read -p "¿Estás SEGURO que deseas eliminar '$APP_NAME'? (escribe 'DELETE' para confirmar): " CONFIRM
    
    if [ "$CONFIRM" != "DELETE" ]; then
        print_info "Cancelado"
        exit 0
    fi
    
    echo ""
    print_info "Eliminando aplicación..."
    
    flyctl apps destroy "$APP_NAME" --yes
    
    print_success "Aplicación eliminada"
}

cmd_help() {
    cat << EOF
${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}
${BLUE}  TechFlow RAG Agent - Script de Despliegue Fly.io${NC}
${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}

${GREEN}Uso:${NC}
  $0 <comando>

${GREEN}Comandos de Configuración:${NC}
  ${YELLOW}setup${NC}      Configuración inicial (crear app y volumen)
  ${YELLOW}secrets${NC}    Configurar secrets (API keys, passwords)

${GREEN}Comandos de Despliegue:${NC}
  ${YELLOW}deploy${NC}     Desplegar la aplicación
  ${YELLOW}restart${NC}    Reiniciar la aplicación

${GREEN}Comandos de Monitoreo:${NC}
  ${YELLOW}status${NC}     Ver estado de la aplicación
  ${YELLOW}logs${NC}       Ver logs en tiempo real
  ${YELLOW}open${NC}       Abrir aplicación en navegador

${GREEN}Comandos de Gestión:${NC}
  ${YELLOW}ssh${NC}        Conectar via SSH a la máquina
  ${YELLOW}backup${NC}     Crear snapshot del volumen
  ${YELLOW}scale${NC}      Escalar recursos (CPU/RAM)
  ${YELLOW}destroy${NC}    Eliminar aplicación (⚠️  destructivo)

${GREEN}Ayuda:${NC}
  ${YELLOW}help${NC}       Mostrar esta ayuda

${GREEN}Ejemplos:${NC}
  # Primera vez
  $0 setup
  $0 secrets
  $0 deploy

  # Actualización
  $0 deploy

  # Monitoreo
  $0 status
  $0 logs

${GREEN}Más información:${NC}
  Ver docs/DEPLOYMENT.md para guía completa

EOF
}

################################################################################
# Main
################################################################################

# Si no hay argumentos, mostrar ayuda
if [ $# -eq 0 ]; then
    cmd_help
    exit 0
fi

# Ejecutar comando
case "$1" in
    setup)
        cmd_setup
        ;;
    secrets)
        cmd_secrets
        ;;
    deploy)
        cmd_deploy
        ;;
    logs)
        cmd_logs
        ;;
    status)
        cmd_status
        ;;
    open)
        cmd_open
        ;;
    ssh)
        cmd_ssh
        ;;
    backup)
        cmd_backup
        ;;
    scale)
        cmd_scale
        ;;
    restart)
        cmd_restart
        ;;
    destroy)
        cmd_destroy
        ;;
    help|--help|-h)
        cmd_help
        ;;
    *)
        print_error "Comando desconocido: $1"
        echo ""
        echo "Ejecuta '$0 help' para ver comandos disponibles"
        exit 1
        ;;
esac
