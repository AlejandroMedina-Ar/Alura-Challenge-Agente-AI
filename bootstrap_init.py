"""
=============================================================
 TechFlow AI Package Initializer
=============================================================

Creates missing __init__.py files inside Python packages.

Features
--------

✓ Safe to execute multiple times
✓ Never overwrites existing files
✓ Only creates missing __init__.py files
✓ Prints a summary

Author:
Alejandro Medina + ChatGPT

Version:
1.0
=============================================================
"""

from pathlib import Path

PROJECT_ROOT = Path.cwd()

PACKAGES = [

    "src",
    "src/ui",
    "src/services",
    "src/rag",
    "src/llm",
    "src/storage",
    "src/auth",
    "src/config",
    "src/utils",

]

INIT_CONTENT = '''"""
TechFlow AI Package
"""
'''

created = 0
skipped = 0


def main():

    global created
    global skipped

    print("\n==============================================")
    print(" TechFlow AI Package Initializer")
    print("==============================================\n")

    for package in PACKAGES:

        package_path = PROJECT_ROOT / package

        if not package_path.exists():

            print(f"[SKIP] Directory not found: {package}")
            skipped += 1
            continue

        init_file = package_path / "__init__.py"

        if init_file.exists():

            print(f"[SKIP] {init_file}")
            skipped += 1
            continue

        init_file.write_text(INIT_CONTENT, encoding="utf-8")

        print(f"[CREATE] {init_file}")

        created += 1

    print("\n==============================================")
    print(" Summary")
    print("==============================================")
    print(f"Created : {created}")
    print(f"Skipped : {skipped}")
    print("==============================================\n")


if __name__ == "__main__":
    main()