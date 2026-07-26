#!/usr/bin/env python3
"""
Script para actualizar el nombre de la compañía de TechFlow Solutions a TechFlow Solutions
en todos los archivos del proyecto.
"""

import os
import sys
from pathlib import Path

def update_file(file_path: Path) -> bool:
    """Actualiza el nombre de la compañía en un archivo."""
    try:
        # Leer contenido
        content = file_path.read_text(encoding='utf-8')
        original_content = content
        
        # Reemplazar todas las variaciones
        content = content.replace('TechFlow Solutions', 'TechFlow Solutions')
        content = content.replace('techflow-solutions', 'techflow-solutions')
        content = content.replace('techflow_solutions', 'techflow_solutions')
        
        # Si hubo cambios, escribir
        if content != original_content:
            file_path.write_text(content, encoding='utf-8')
            print(f"✅ Actualizado: {file_path}")
            return True
        
        return False
    except Exception as e:
        print(f"❌ Error en {file_path}: {e}")
        return False

def main():
    """Función principal."""
    project_root = Path(__file__).parent
    
    # Archivos a actualizar (extensiones)
    extensions = ['.md', '.py', '.txt', '.json', '.html', '.css']
    
    # Directorios a excluir
    exclude_dirs = {'.git', 'venv', '__pycache__', '.pytest_cache', 'node_modules', 'data'}
    
    updated_files = []
    
    print("🔍 Buscando archivos para actualizar...")
    print()
    
    # Recorrer todos los archivos
    for file_path in project_root.rglob('*'):
        # Saltar directorios excluidos
        if any(excluded in file_path.parts for excluded in exclude_dirs):
            continue
        
        # Solo archivos con extensiones específicas
        if file_path.is_file() and file_path.suffix in extensions:
            if update_file(file_path):
                updated_files.append(file_path)
    
    print()
    print("=" * 60)
    print(f"✅ Actualización completada")
    print(f"📝 Archivos modificados: {len(updated_files)}")
    print("=" * 60)
    
    if updated_files:
        print("\nArchivos actualizados:")
        for f in updated_files:
            print(f"  - {f.relative_to(project_root)}")

if __name__ == "__main__":
    main()
