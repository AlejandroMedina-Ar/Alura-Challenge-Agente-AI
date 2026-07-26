"""
Script de Traducción UI al Español

Este script traduce todos los textos de interfaz de usuario al español.
Mantiene el código y nombres de variables en inglés, solo traduce:
- Textos mostrados al usuario
- Mensajes de error/éxito
- Etiquetas y descripciones

Run: python translate_ui.py
"""

# Diccionario de traducciones comunes
TRANSLATIONS = {
    # UI Components
    "Upload": "Subir",
    "Upload Document": "Subir Documento",
    "Delete": "Eliminar",
    "Index": "Indexar",
    "Re-index": "Re-indexar",
    "Clear": "Limpiar",
    "Export": "Exportar",
    "Save": "Guardar",
    "Cancel": "Cancelar",
    "Submit": "Enviar",
    "Login": "Iniciar Sesión",
    "Logout": "Cerrar Sesión",
    "Settings": "Configuración",
    "Dashboard": "Panel de Control",
    "Documents": "Documentos",
    "Chat": "Chat",
    "Admin Panel": "Panel de Administración",
    "Knowledge Library": "Biblioteca de Conocimiento",
    
    # Status messages
    "Success": "Éxito",
    "Error": "Error",
    "Warning": "Advertencia",
    "Info": "Información",
    "Loading": "Cargando",
    "Processing": "Procesando",
    "Ready": "Listo",
    "Not Ready": "No Listo",
    "Failed": "Falló",
    "Completed": "Completado",
    
    # Common phrases
    "Click here": "Haz clic aquí",
    "Select": "Seleccionar",
    "Choose": "Elegir",
    "Enter": "Ingresar",
    "Please": "Por favor",
    "Yes": "Sí",
    "No": "No",
    "OK": "Aceptar",
    "Confirm": "Confirmar",
    
    # File operations
    "File": "Archivo",
    "Document": "Documento",
    "Upload successful": "Carga exitosa",
    "Upload failed": "Carga fallida",
    "Delete successful": "Eliminación exitosa",
    "Delete failed": "Eliminación fallida",
    
    # System
    "Configuration": "Configuración",
    "System": "Sistema",
    "Status": "Estado",
    "Statistics": "Estadísticas",
    "Options": "Opciones",
    "Advanced": "Avanzado",
}

print("=" * 60)
print("Script de Traducción UI al Español")
print("=" * 60)
print()
print("ℹ️  Este script es un helper manual.")
print("ℹ️  Las traducciones se están haciendo archivo por archivo.")
print()
print("📋 Archivos a traducir:")
print("   - src/app.py (parcialmente hecho)")
print("   - src/ui/chat.py")
print("   - src/ui/admin_panel.py")  
print("   - src/ui/settings_panel.py")
print("   - src/ui/sidebar.py")
print("   - src/ui/components.py")
print()
print("✅ Las traducciones se están aplicando manualmente")
print("   para mayor precisión y contexto.")
print()
print("=" * 60)
