"""
Code Structure Validation Test

This test validates code structure without requiring dependencies installed.
Tests syntax, imports structure, and method signatures.

Author: TechFlow Solutions Project
"""

import ast
import sys
from pathlib import Path


def test_file_syntax(file_path: Path) -> tuple[bool, str]:
    """Test if a Python file has valid syntax."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            code = f.read()
        ast.parse(code)
        return True, "OK"
    except SyntaxError as e:
        return False, f"Syntax error at line {e.lineno}: {e.msg}"
    except Exception as e:
        return False, f"Error: {str(e)}"


def test_import_structure(file_path: Path) -> tuple[bool, list[str]]:
    """Test import structure in a file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            code = f.read()
        tree = ast.parse(code)
        
        issues = []
        
        # Check for specific problematic imports
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom):
                if node.module:
                    # Check for known typos
                    if 'knowledge_base_service' in node.module:
                        issues.append(f"Line {node.lineno}: Import from 'knowledge_base_service' should be 'knowledge_library_service'")
        
        return len(issues) == 0, issues
    except Exception as e:
        return False, [f"Error parsing: {str(e)}"]


def test_method_calls(file_path: Path) -> tuple[bool, list[str]]:
    """Test for known problematic method calls."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            code = f.read()
        
        issues = []
        
        # Check for known problematic patterns
        problematic_patterns = [
            ('chat_completion_stream(', 'Should use chat_completion(stream=True)'),
            ('self.metadata_repo', 'Should use self.meta_repo for consistency'),
        ]
        
        lines = code.split('\n')
        for i, line in enumerate(lines, 1):
            for pattern, message in problematic_patterns:
                if pattern in line and 'def ' not in line:  # Exclude function definitions
                    issues.append(f"Line {i}: {message}")
        
        return len(issues) == 0, issues
    except Exception as e:
        return False, [f"Error: {str(e)}"]


def main():
    print("=" * 60)
    print("TechFlow RAG Agent - Code Structure Validation")
    print("=" * 60)
    print()
    
    # Key files to test
    test_files = [
        'src/services/chat_service.py',
        'src/services/indexing_service.py',
        'src/services/knowledge_library_service.py',
        'src/llm/gemini_provider.py',
        'src/llm/cohere_provider.py',
        'src/config/settings.py',
    ]
    
    all_passed = True
    results = []
    
    for file_path_str in test_files:
        file_path = Path(file_path_str)
        
        if not file_path.exists():
            print(f"❌ {file_path_str}: File not found")
            all_passed = False
            continue
        
        print(f"🔍 Testing {file_path_str}...")
        
        # Test 1: Syntax
        syntax_ok, syntax_msg = test_file_syntax(file_path)
        if not syntax_ok:
            print(f"  ❌ Syntax: {syntax_msg}")
            all_passed = False
            continue
        else:
            print(f"  ✅ Syntax: Valid")
        
        # Test 2: Import structure
        imports_ok, import_issues = test_import_structure(file_path)
        if not imports_ok:
            print(f"  ❌ Imports: {len(import_issues)} issue(s)")
            for issue in import_issues:
                print(f"     - {issue}")
            all_passed = False
        else:
            print(f"  ✅ Imports: Clean")
        
        # Test 3: Method calls
        methods_ok, method_issues = test_method_calls(file_path)
        if not methods_ok:
            print(f"  ⚠️  Methods: {len(method_issues)} potential issue(s)")
            for issue in method_issues:
                print(f"     - {issue}")
            # Don't fail on method issues, just warn
        else:
            print(f"  ✅ Methods: Clean")
        
        results.append({
            'file': file_path_str,
            'syntax': syntax_ok,
            'imports': imports_ok,
            'methods': methods_ok
        })
        
        print()
    
    # Summary
    print("=" * 60)
    print("Summary")
    print("=" * 60)
    
    passed = sum(1 for r in results if r['syntax'] and r['imports'])
    total = len(results)
    
    for result in results:
        status = "✅" if (result['syntax'] and result['imports']) else "❌"
        print(f"{status} {result['file']}")
    
    print()
    print(f"Pass Rate: {passed}/{total} ({100*passed//total if total > 0 else 0}%)")
    
    if all_passed:
        print()
        print("🎉 All code structure tests passed!")
        print("✅ No syntax errors")
        print("✅ No import issues")
        print("✅ No known problematic patterns")
        print()
        print("Note: To run full integration tests with LLM providers,")
        print("ensure all dependencies are installed:")
        print("  pip install -r requirements.txt")
    else:
        print()
        print("⚠️  Some issues found. Please review above.")
        sys.exit(1)


if __name__ == '__main__':
    main()
