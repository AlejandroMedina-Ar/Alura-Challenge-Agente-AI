# Contributing to TechFlow AI RAG Agent

Thank you for your interest in contributing to TechFlow AI! This document provides guidelines and instructions for contributing.

---

## Table of Contents

1. [Code of Conduct](#code-of-conduct)
2. [Getting Started](#getting-started)
3. [Development Setup](#development-setup)
4. [How to Contribute](#how-to-contribute)
5. [Coding Standards](#coding-standards)
6. [Testing](#testing)
7. [Documentation](#documentation)
8. [Pull Request Process](#pull-request-process)

---

## Code of Conduct

### Our Pledge

We are committed to providing a welcoming and inspiring community for all. Please be respectful and constructive in your interactions.

### Expected Behavior

- Be respectful and inclusive
- Welcome newcomers
- Be patient and helpful
- Focus on what's best for the community
- Show empathy towards others

### Unacceptable Behavior

- Harassment or discriminatory language
- Personal attacks
- Trolling or insulting comments
- Publishing others' private information
- Any conduct that could reasonably be considered inappropriate

---

## Getting Started

### Prerequisites

- Python 3.9 or higher
- Git
- Basic knowledge of Python, Streamlit, and RAG concepts
- Familiarity with the project architecture (see [Architecture](architecture/Architecture.md))

### First Contributions

Good first issues are labeled with `good first issue` on GitHub. These are typically:
- Documentation improvements
- Bug fixes
- Small feature additions
- Test coverage improvements

---

## Development Setup

### 1. Fork and Clone

```bash
# Fork the repository on GitHub
# Then clone your fork
git clone https://github.com/YOUR-USERNAME/Alura-Challenge-Agente-AI.git
cd Alura-Challenge-Agente-AI

# Add upstream remote
git remote add upstream https://github.com/AlejandroMedina-Ar/Alura-Challenge-Agente-AI.git
```

### 2. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate  # Windows
```

### 3. Install Dependencies

```bash
# Install requirements
pip install -r requirements.txt

# Install development dependencies (optional)
pip install black flake8 isort pytest pytest-cov
```

### 4. Configure Environment

```bash
cp .env.example .env
# Edit .env with your API keys
```

### 5. Run Setup

```bash
python setup.py
```

### 6. Run Tests

```bash
python test_integration.py
```

---

## How to Contribute

### Reporting Bugs

**Before submitting a bug report:**
1. Check existing issues to avoid duplicates
2. Test with the latest version
3. Verify it's not a configuration issue

**Bug report should include:**
- Clear, descriptive title
- Steps to reproduce
- Expected vs actual behavior
- Screenshots (if applicable)
- Environment info (OS, Python version)
- Relevant logs (remove sensitive data)

**Example:**
```markdown
**Bug:** Chat doesn't respond when no documents indexed

**Steps to reproduce:**
1. Fresh install
2. Login
3. Go to Chat page
4. Type a question

**Expected:** Error message or empty state
**Actual:** Application crashes

**Environment:**
- OS: Ubuntu 22.04
- Python: 3.11.2
- Browser: Chrome 120

**Logs:**
```
[ERROR] RAGPipeline query failed: vector store is empty
```
```

### Suggesting Features

**Feature requests should include:**
- Clear description of the feature
- Use cases and benefits
- Potential implementation approach
- Any alternatives considered

**Example:**
```markdown
**Feature:** Document versioning

**Description:**
Allow multiple versions of the same document to coexist in the knowledge library.

**Use case:**
- Track document changes over time
- Compare different versions
- Rollback to previous versions

**Implementation ideas:**
- Add version field to metadata
- Store versions as separate docs with naming convention
- Add UI to manage versions

**Alternatives:**
- Manual renaming (current workaround)
- External version control
```

### Contributing Code

1. **Create a branch:**
   ```bash
   git checkout -b feature/your-feature-name
   # or
   git checkout -b bugfix/issue-number
   ```

2. **Make changes:**
   - Follow coding standards (see below)
   - Add/update tests
   - Update documentation

3. **Test your changes:**
   ```bash
   python test_integration.py
   ```

4. **Commit:**
   ```bash
   git add .
   git commit -m "Description of changes"
   ```

5. **Push:**
   ```bash
   git push origin feature/your-feature-name
   ```

6. **Create Pull Request:**
   - Go to GitHub
   - Click "New Pull Request"
   - Fill in the template
   - Link related issues

---

## Coding Standards

### Python Style Guide

Follow **PEP 8** with these specifics:

**Formatting:**
- 4 spaces for indentation (no tabs)
- Max line length: 100 characters
- Use trailing commas in multi-line structures

**Example:**
```python
def process_document(
    file_path: str,
    chunk_size: int = 512,
    chunk_overlap: int = 50
) -> dict:
    """
    Process a document for indexing.
    
    Args:
        file_path: Path to document
        chunk_size: Size of chunks
        chunk_overlap: Overlap between chunks
    
    Returns:
        dict: Processing results
    """
    # Implementation
    pass
```

### Type Hints

**Always use type hints:**
```python
# Good
def add_numbers(a: int, b: int) -> int:
    return a + b

# Bad
def add_numbers(a, b):
    return a + b
```

### Docstrings

**Use Google-style docstrings:**
```python
def function_name(param1: str, param2: int) -> bool:
    """
    Brief description of function.
    
    Longer description if needed, explaining what the
    function does in more detail.
    
    Args:
        param1: Description of param1
        param2: Description of param2
    
    Returns:
        Description of return value
    
    Raises:
        ValueError: When param1 is empty
    
    Example:
        >>> function_name("test", 42)
        True
    """
    pass
```

### Naming Conventions

- **Functions/Variables:** `snake_case`
- **Classes:** `PascalCase`
- **Constants:** `UPPER_SNAKE_CASE`
- **Private:** `_leading_underscore`

```python
# Good
class DocumentProcessor:
    MAX_FILE_SIZE = 10_000_000
    
    def __init__(self):
        self._cache = {}
    
    def process_file(self, file_path: str) -> dict:
        pass
```

### Code Organization

**Import order:**
1. Standard library
2. Third-party packages
3. Local modules

```python
# Standard library
import os
from pathlib import Path

# Third-party
import streamlit as st
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Local
from src.config import DATA_DIR
from src.utils import get_logger
```

### Error Handling

**Use specific exceptions:**
```python
# Good
try:
    result = process_document(path)
except FileNotFoundError:
    logger.error(f"File not found: {path}")
    raise DocumentNotFoundError(path)
except PermissionError:
    logger.error(f"Permission denied: {path}")
    raise

# Bad
try:
    result = process_document(path)
except Exception as e:
    print(f"Error: {e}")
```

### Logging

**Use appropriate log levels:**
```python
logger.debug(f"Processing document", filename=filename)
logger.info(f"Document indexed", doc_id=doc_id, chunks=42)
logger.warning(f"Large document", size_mb=size/1024/1024)
logger.error(f"Indexing failed", error=str(e), exc_info=True)
```

---

## Testing

### Running Tests

```bash
# Run all integration tests
python test_integration.py

# Run specific test
python -m pytest tests/test_specific.py

# Run with coverage
pytest --cov=src --cov-report=html
```

### Writing Tests

**Test structure:**
```python
def test_function_name():
    """Test description."""
    # Arrange
    input_data = "test"
    expected = "result"
    
    # Act
    result = function_to_test(input_data)
    
    # Assert
    assert result == expected
```

**Test naming:**
- `test_<function>_<scenario>_<expected>`
- Example: `test_upload_document_duplicate_raises_error`

---

## Documentation

### When to Update Documentation

- Adding new features
- Changing existing functionality
- Fixing bugs that affect usage
- Adding configuration options

### What to Document

1. **User Guide** (`docs/USER-GUIDE.md`)
   - How to use new features
   - Configuration changes
   - New workflows

2. **Technical Docs** (`docs/TECHNICAL-DOCS.md`)
   - API changes
   - Architecture updates
   - New modules

3. **FAQ** (`docs/FAQ.md`)
   - Common issues
   - New troubleshooting steps

4. **README** (`README.md`)
   - Major changes
   - New features (high-level)

5. **Changelog** (`CHANGELOG.md`)
   - All changes
   - Follow Keep a Changelog format

---

## Pull Request Process

### Before Submitting

**Checklist:**
- [ ] Code follows style guide
- [ ] Tests pass locally
- [ ] Added/updated tests for changes
- [ ] Updated relevant documentation
- [ ] Commits are clean and descriptive
- [ ] Branch is up-to-date with main

### PR Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Integration tests pass
- [ ] Manual testing completed
- [ ] Added new tests

## Checklist
- [ ] Code follows style guide
- [ ] Documentation updated
- [ ] No new warnings
- [ ] Commits are clean

## Related Issues
Fixes #123
Related to #456

## Screenshots (if applicable)
[Add screenshots here]
```

### Review Process

1. **Automated checks:**
   - CI/CD pipeline runs tests
   - Linting checks
   - Build verification

2. **Code review:**
   - Maintainer reviews code
   - Requests changes if needed
   - Approves when ready

3. **Merge:**
   - Squash and merge (default)
   - Maintain clean history

### After Merge

- Delete your branch
- Update your local repo:
  ```bash
  git checkout main
  git pull upstream main
  ```

---

## Questions?

- Check [FAQ](docs/FAQ.md)
- Read [Technical Docs](docs/TECHNICAL-DOCS.md)
- Ask in GitHub Discussions
- Open an issue for bugs

---

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

**Thank you for contributing to TechFlow AI!** 🎉

**Version:** 1.0.0-beta  
**Last Updated:** 2026-07-25
