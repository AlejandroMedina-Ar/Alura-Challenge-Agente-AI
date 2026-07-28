# Scripts de Despliegue Fly.io

Este directorio contiene scripts helper para facilitar el despliegue y gestión de TechFlow RAG Agent en Fly.io.

## 📄 Archivos

- `deploy.sh` - Script automatizado para gestión completa de Fly.io

## 🚀 Uso Rápido

### Primera vez (Setup completo)

```bash
# 1. Configuración inicial
./.fly/deploy.sh setup

# 2. Configurar secrets
./.fly/deploy.sh secrets

# 3. Desplegar
./.fly/deploy.sh deploy
```

### Actualizaciones

```bash
# Desplegar nuevos cambios
./.fly/deploy.sh deploy
```

### Monitoreo

```bash
# Ver estado
./.fly/deploy.sh status

# Ver logs en tiempo real
./.fly/deploy.sh logs

# Abrir en navegador
./.fly/deploy.sh open
```

## 📋 Comandos Disponibles

| Comando | Descripción |
|---------|-------------|
| `setup` | Configuración inicial (crear app y volumen) |
| `secrets` | Configurar secrets interactivamente |
| `deploy` | Desplegar la aplicación |
| `status` | Ver estado completo de la app |
| `logs` | Ver logs en tiempo real |
| `open` | Abrir aplicación en navegador |
| `ssh` | Conectar via SSH a la máquina |
| `backup` | Crear snapshot del volumen |
| `scale` | Escalar recursos (CPU/RAM) |
| `restart` | Reiniciar la aplicación |
| `destroy` | Eliminar aplicación (⚠️ destructivo) |
| `help` | Mostrar ayuda completa |

## 🔧 Requisitos

- `flyctl` CLI instalado ([Guía de instalación](https://fly.io/docs/hands-on/install-flyctl/))
- Autenticado en Fly.io: `flyctl auth login`

## 💡 Ejemplos

### Despliegue inicial completo

```bash
# Paso 1: Setup
./.fly/deploy.sh setup

# Paso 2: Configurar secrets
./.fly/deploy.sh secrets
# Se te pedirá:
# - Gemini API Key
# - Cohere API Key (opcional)
# - Admin Password

# Paso 3: Desplegar
./.fly/deploy.sh deploy
```

### Monitoreo regular

```bash
# Ver estado general
./.fly/deploy.sh status

# Ver logs mientras la app corre
./.fly/deploy.sh logs

# Abrir en navegador para probar
./.fly/deploy.sh open
```

### Crear backup antes de actualización

```bash
# Crear snapshot del volumen
./.fly/deploy.sh backup

# Luego desplegar
./.fly/deploy.sh deploy
```

### Escalar recursos

```bash
# Menú interactivo para cambiar VM size
./.fly/deploy.sh scale

# Opciones:
# - shared-cpu-1x (256MB) - Free tier
# - shared-cpu-2x (512MB) - ~$5-7/mes
# - shared-cpu-4x (1GB)   - ~$10-12/mes
```

## 🔐 Gestión de Secrets

### Configurar secrets manualmente

```bash
flyctl secrets set GEMINI_API_KEY="tu-key" -a techflow-rag-agent
flyctl secrets set COHERE_API_KEY="tu-key" -a techflow-rag-agent
flyctl secrets set ADMIN_PASSWORD="tu-password" -a techflow-rag-agent
```

### Listar secrets configurados

```bash
flyctl secrets list -a techflow-rag-agent
```

### Actualizar un secret

```bash
flyctl secrets set ADMIN_PASSWORD="nueva-password" -a techflow-rag-agent
```

## 🐛 Troubleshooting

### El script no tiene permisos de ejecución

```bash
# Linux/Mac
chmod +x .fly/deploy.sh
```

### flyctl no encontrado

```bash
# Instalar flyctl
curl -L https://fly.io/install.sh | sh

# O en macOS con Homebrew
brew install flyctl
```

### No autenticado en Fly.io

```bash
flyctl auth login
```

### Comando falla con error

```bash
# Ver logs detallados
./.fly/deploy.sh logs

# Ver estado
./.fly/deploy.sh status

# Conectar via SSH para debugging
./.fly/deploy.sh ssh
```

## 📚 Documentación

Para guía completa de despliegue, ver:
- [docs/DEPLOYMENT.md](../docs/DEPLOYMENT.md)
- [Documentación oficial de Fly.io](https://fly.io/docs/)

## ⚠️ Advertencias

- **destroy**: Elimina la aplicación y TODOS los datos permanentemente
- **backup**: Crear snapshots regularmente antes de actualizaciones importantes
- **secrets**: Nunca commitear secrets al repositorio

## 🆘 Soporte

¿Problemas con el despliegue?
- Ver [docs/TROUBLESHOOTING.md](../docs/TROUBLESHOOTING.md)
- Abrir issue en [GitHub](https://github.com/AlejandroMedina-Ar/Alura-Challenge-Agente-AI/issues)
