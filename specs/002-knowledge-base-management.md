# Knowledge Base Management Specification

**Specification ID:** SPEC-002

**Module:** Knowledge Base Management

**Version:** 1.0

**Status:** Draft

---

# 1. Purpose

This document defines the architecture, workflow and management rules for the Knowledge Base used by the TechFlow AI Corporate Knowledge Agent.

The Knowledge Base is responsible for transforming uploaded knowledge assets into searchable vector representations that can be used by the Retrieval-Augmented Generation (RAG) pipeline.

This specification defines:

- Knowledge Library
- Knowledge Assets
- Upload workflow
- File validation
- Metadata model
- Storage strategy
- Document lifecycle

Business logic related to embeddings and retrieval is described in the RAG Engine specification.

---

# 2. Scope

This specification covers every operation performed before a document becomes searchable by the AI Assistant.

It includes:

- Uploading documents
- Validating files
- Organizing the Knowledge Library
- Metadata generation
- File management
- Duplicate prevention
- Storage organization
- Administration tools

It does not describe:

- Retrieval algorithms
- Prompt generation
- LLM communication
- Response generation

Those topics belong to other specifications.

---

# 3. Knowledge Base Concept

The Knowledge Base is the central repository of information used by the AI Assistant.

Rather than storing raw files only, the system stores structured knowledge extracted from uploaded assets.

Conceptually:

```
Knowledge Base

│

├── Knowledge Library

│

├── Metadata

│

├── Chunks

│

├── Embeddings

│

└── Vector Database
```

The Knowledge Base should always represent the latest indexed version of all approved knowledge assets.

---

# 4. Knowledge Library

The Knowledge Library represents the administrator-managed collection of knowledge assets.

Users never interact directly with the library.

Only authenticated administrators can:

- Add assets
- Remove assets
- Browse assets
- Update assets
- Reindex assets

The library acts as the source of truth for the RAG pipeline.

---

# 5. Knowledge Assets

A Knowledge Asset represents any file containing useful information that should become searchable by the assistant.

Examples

- Employee Handbook
- Product Documentation
- API Reference
- Company Policies
- FAQ
- User Manual
- Pricing Guide
- Internal Procedures

Each uploaded asset becomes an independent entity inside the Knowledge Library.

---

# 6. Supported Asset Types

Version 1 supports:

| Type           | Extension |
| -------------- | --------- |
| PDF            | .pdf      |
| Microsoft Word | .docx     |
| Plain Text     | .txt      |
| Markdown       | .md       |
| CSV            | .csv      |
| JSON           | .json     |
| HTML           | .html     |

The architecture should allow future support for additional formats.

Potential future formats:

- XLSX
- PPTX
- XML
- EPUB
- Images (OCR)
- Audio Transcripts

---

# 7. Knowledge Asset Lifecycle

Every knowledge asset follows the same lifecycle.

```
Upload

↓

Validation

↓

Storage

↓

Text Extraction

↓

Metadata Generation

↓

Chunking

↓

Embedding Generation

↓

Vector Storage

↓

Knowledge Base Updated

↓

Available for AI Queries
```

The administrator should not need to manually execute intermediate steps.

---

# 8. Upload Workflow

Uploading one or multiple assets should be straightforward.

Workflow

```
Administrator

↓

Select Files

↓

Drag & Drop or File Picker

↓

Validation

↓

Accepted Files

↓

Processing Queue

↓

Knowledge Base Update

↓

Success Notification
```

Uploads should support multiple files simultaneously.

---

# 9. Upload Interface

The upload interface should support:

- Drag and Drop
- Multiple File Selection
- Progress Display
- Cancel Upload (optional)
- Success Notification
- Error Notification

The upload process should require as few user interactions as possible.

---

# 10. File Validation

Every uploaded file must be validated before processing.

Validation Rules

File Exists

Supported Extension

Readable Format

Non-empty Content (reject files with 0 bytes or only whitespace)

Maximum Size

No Corruption Detected

Rejected files should never reach the indexing pipeline.

**Empty Document Policy:** Files with 0 bytes or containing only whitespace characters must be rejected during validation. The administrator should receive a clear error message: "Document '{filename}' is empty and cannot be indexed. Please upload a document with actual content."

---

# 10.1 Duplicate Detection

When a file with the same name already exists in the Knowledge Library, the system should detect it during validation.

**Duplicate Handling Strategy: SKIP**

The upload should be rejected with a clear message:

```
Document '{filename}' already exists in the Knowledge Library. 
Please delete the existing document first or rename the new file before uploading.
```

**Implementation:**

1. During file validation (before processing), check if `filename` exists in `data/knowledge_library/metadata/`
2. If exists, raise `DuplicateDocumentError` with the message above
3. Do NOT process, chunk, or index the duplicate file
4. Log the skipped upload: `logger.info(f"Upload skipped: duplicate filename '{filename}'")`

**Rationale:** SKIP strategy prevents accidental overwrites and maintains explicit control over document versions. Administrators must manually delete old versions before uploading new ones.

---

# 11. File Size Limits

Each file type should enforce a maximum size to prevent resource exhaustion and ensure reasonable processing times.

**Configuration:** File size limits are stored in `data/config.json` (not `.env`), allowing runtime adjustments without redeployment.

**Default limits (in MB):**

```json
{
  "document_processing": {
    "max_file_size_mb": {
      "pdf": 50,
      "docx": 25,
      "txt": 10,
      "md": 10,
      "csv": 25,
      "json": 10,
      "html": 10
    }
  }
}
```

**Validation:**

Files exceeding these limits should be rejected during validation with a clear error message:

```
Document '{filename}' exceeds maximum size for {file_type} files ({actual_size}MB > {limit}MB).
Please upload a smaller file or contact administrator to adjust limits.
```

**Implementation:** Read limits from `config.json` via `storage/config_repository.py` during file validation.

---

# 11. Maximum File Size

Version 1 recommends the following limits.

PDF

50 MB

DOCX

30 MB

TXT

10 MB

Markdown

10 MB

CSV

20 MB

JSON

20 MB

HTML

20 MB

These limits may be configured through environment variables.

---

# 12. Duplicate Detection

The system should attempt to detect duplicate assets before indexing.

Duplicate detection should be based on:

- SHA-256 checksum
- Filename
- File size
- Upload timestamp (secondary)

If an identical asset already exists, the administrator should be notified.

Possible actions:

- Skip
- Replace Existing
- Upload Anyway

---

# 13. Metadata Model

Each knowledge asset should maintain structured metadata.

Suggested model

```yaml
asset_id: UUID

filename: employee_handbook.pdf

file_type: PDF

file_size: 2.4 MB

uploaded_at: 2026-07-24 18:42

uploaded_by: Administrator

pages: 58

language: English

checksum: SHA256

indexed: true

chunk_count: 214

embedding_model: intfloat/multilingual-e5-base

last_indexed: 2026-07-24 18:43
```

Metadata should remain synchronized with the Knowledge Base.

---

# 14. Asset Storage Strategy

Uploaded assets should be stored independently from vector data.

Suggested directory structure

```
data/

    knowledge_library/

        documents/

        metadata/

    chromadb/

    logs/

    config.json
```

Responsibilities

documents/

Original uploaded files (document_repository.py).

metadata/

Structured asset metadata (metadata_repository.py).

chromadb/

Persistent vector database.

logs/

Upload and indexing logs.

config.json

Runtime configuration (config_repository.py).

---

# 15. Directory Organization

The application should avoid mixing responsibilities.

Recommended structure

```
techflow-rag-agent/

├── src/

│   ├── app.py

│   ├── ui/

│   ├── services/

│   ├── rag/

│   ├── llm/

│   ├── storage/

│   ├── auth/

│   ├── config/

│   └── utils/

├── assets/

├── data/

│   ├── knowledge_library/

│   │   ├── documents/

│   │   └── metadata/

│   ├── chromadb/

│   ├── logs/

│   └── config.json

├── specs/

├── architecture/

├── prompts/

└── requirements.txt
```

The project should remain easy to navigate and maintain.

---

# 16. Knowledge Library Principles

The Knowledge Library should follow these principles.

Single Source of Truth

Every indexed asset must exist inside the library.

Consistency

Metadata and vector data must remain synchronized.

Traceability

Every asset should be uniquely identifiable.

Scalability

The architecture should support growth within defined limits. v1 enforces a hard limit of 5000 knowledge assets.

Simplicity

The administrator should never need to understand embeddings or vector databases.

The application should hide technical complexity whenever possible.

**Document Limit Policy:** The Knowledge Library enforces a maximum of 5000 knowledge assets. When this limit is reached, new uploads will be rejected with the following message: "Maximum document limit reached (5000). Please delete existing documents before uploading new ones." This limit ensures optimal performance and manageable resource usage in v1.

---

# 17. Text Extraction

The first processing stage consists of extracting readable text from each uploaded Knowledge Asset.

The extraction process should preserve as much useful information as possible while removing unnecessary formatting.

The extraction service must operate automatically after successful file validation.

Supported extraction methods:

| File Type | Extraction Method |
| --------- | ----------------- |
| PDF       | PyMuPDF (fitz)    |
| DOCX      | python-docx       |
| TXT       | Native Python     |
| Markdown  | Native Python     |
| CSV       | pandas            |
| JSON      | Native Python     |
| HTML      | BeautifulSoup     |

The extraction process should return plain UTF-8 encoded text.

If extraction fails, the asset should not continue through the processing pipeline.

---

# 18. Text Normalization

After extraction, the text should be normalized before any additional processing.

Normalization should include:

- UTF-8 encoding
- Remove duplicated spaces
- Normalize line endings
- Remove invisible characters
- Remove empty lines
- Trim leading and trailing whitespace

The objective is to generate clean and predictable input for the chunking process.

---

# 19. Document Cleaning

Some documents contain information that should not become part of the semantic index.

Whenever possible, remove:

- Repeated headers
- Repeated footers
- Empty tables
- Decorative separators
- Multiple blank lines

Do not modify the original uploaded document.

Only the extracted text should be cleaned.

---

# 20. Language Detection

The processing pipeline should attempt to detect the document language.

Supported languages:

- English
- Spanish
- Portuguese

The detected language should be stored as metadata.

Example

```yaml
language: English
```

Future versions may use this information to select different embedding models.

---

# 21. Chunking Strategy

After normalization, the document should be divided into semantic chunks.

The objective is to maximize retrieval quality while preserving context.

Recommended strategy:

Recursive Character Text Splitter

Configuration:

Chunk Size

1000 characters

Chunk Overlap

200 characters

These values should be configurable.

---

# 22. Chunk Metadata

Each generated chunk should receive its own metadata.

Suggested structure:

```yaml
chunk_id: UUID

asset_id: UUID

chunk_number: 17

page: 6

language: English

source: employee_handbook.pdf
```

Chunk metadata allows precise source attribution during retrieval.

---

# 23. Chunk Quality

Chunks should satisfy the following rules:

- Preserve complete ideas whenever possible.
- Avoid splitting paragraphs unnecessarily.
- Preserve lists.
- Preserve tables when practical.
- Preserve section titles.

Very small chunks should be avoided.

Very large chunks should also be avoided.

---

# 24. Embedding Generation

Once chunking is complete, embeddings should be generated.

Version 1 uses local embedding generation.

Recommended default model:

```
intfloat/multilingual-e5-base
```

Advantages:

- Free
- Fast
- High quality
- Excellent retrieval performance
- Multilingual support (100+ languages including Spanish)
- No API cost

The embedding model should be configurable.

---

# 25. Embedding Pipeline

Each chunk follows the same embedding workflow.

```
Chunk

↓

Embedding Model

↓

Vector

↓

Metadata

↓

Store in ChromaDB
```

Every chunk produces exactly one embedding vector.

---

# 26. ChromaDB Integration

ChromaDB acts as the persistent vector database.

Responsibilities:

- Store embeddings
- Store metadata
- Execute similarity search
- Return relevant chunks

The UI should never access ChromaDB directly.

All communication must occur through service classes.

---

# 27. Collection Structure

A single collection is sufficient for Version 1.

Example

```
Collection

techflow_knowledge_base
```

Future versions may support multiple collections.

---

# 28. Metadata Stored in ChromaDB

Each stored vector should include metadata similar to:

```yaml
asset_id: UUID

filename: employee_handbook.pdf

page: 6

chunk: 17

language: English

embedding_model: intfloat/multilingual-e5-base
```

Metadata enables source attribution during answer generation.

---

# 29. Duplicate Prevention

Before generating embeddings, the system should verify whether the asset already exists.

Preferred validation order:

1. SHA-256 checksum
2. Asset ID
3. Filename
4. File Size

If an identical asset exists, the administrator should be notified.

---

# 30. Incremental Updates

Uploading a new document should not require rebuilding the entire Knowledge Base.

Only the new asset should be processed.

Workflow:

```
Upload

↓

Extract

↓

Chunk

↓

Generate Embeddings

↓

Store

↓

Update Statistics

↓

Ready
```

This minimizes processing time.

---

# 31. Reindex Workflow

Reindexing should regenerate embeddings for selected assets.

Typical scenarios:

- Embedding model updated
- Chunk size changed
- Metadata corrected

Workflow

```
Select Asset

↓

Delete Old Embeddings

↓

Generate New Embeddings

↓

Update Metadata

↓

Refresh Statistics
```

---

# 32. Full Knowledge Base Rebuild

The administrator may rebuild the entire Knowledge Base.

Workflow:

```
Delete Collection

↓

Read All Assets

↓

Extract

↓

Chunk

↓

Generate Embeddings

↓

Create New Collection

↓

Ready
```

This operation should require confirmation.

---

# 33. Logging

Every processing step should be logged.

Suggested events:

- Upload Started
- Upload Completed
- Extraction Failed
- Chunking Completed
- Embeddings Generated
- Chroma Updated
- Asset Deleted
- Reindex Completed

Logs simplify debugging and maintenance.

---

# 34. Performance Objectives

Recommended targets:

Document Upload

< 5 seconds (small documents)

Embedding Generation

As fast as hardware permits

Knowledge Base Update

Automatic

Memory Usage

Reasonable for consumer hardware

The application should remain responsive throughout processing.

---

# 35. Knowledge Library Dashboard

The Knowledge Library Dashboard provides administrators with a real-time overview of the current state of the Knowledge Base.

The dashboard should be displayed within the Administrator Panel.

Displayed information should include:

- Total Knowledge Assets
- Total Indexed Chunks
- Active Embedding Model
- Vector Database Status
- Total Storage Used
- Last Update Date
- Index Status

Example

```
Knowledge Library

────────────────────────────

📄 Assets

42

🧩 Chunks

5,842

🧠 Embedding Model

intfloat/multilingual-e5-base

💾 Vector Database

ChromaDB

📦 Storage

186 MB

📅 Last Update

2026-07-25

🟢 Status

Ready
```

The dashboard should refresh automatically after any operation.

---

# 36. Browse Knowledge Assets

Administrators should be able to browse all indexed assets.

Display each asset using a compact table.

Suggested columns:

| Asset | Type | Size | Pages | Chunks | Indexed | Uploaded |
| ----- | ---- | ---- | ----- | ------ | ------- | -------- |

Additional actions:

- View Metadata
- Reindex
- Delete

Future versions may include pagination and search.

---

# 37. Asset Details

Selecting an asset should display additional information.

Suggested information:

Filename

Original Path

Upload Date

File Size

Document Language

Number of Pages

Chunk Count

Embedding Model

Checksum

Index Status

Last Indexed

The administrator should be able to verify the complete processing history.

---

# 38. Search Knowledge Assets

The Knowledge Library should provide a search function for administrators.

Searchable fields:

- Filename
- File Type
- Language
- Upload Date
- Status

The objective is to simplify administration as the library grows.

---

# 39. Delete Knowledge Assets

Administrators may permanently remove assets from the Knowledge Base.

Workflow

```
Select Asset

↓

Confirmation Dialog

↓

Delete Metadata

↓

Delete Embeddings

↓

Delete Asset File

↓

Refresh Statistics

↓

Success Notification
```

Deletion must require explicit confirmation.

Example

```
Delete Knowledge Asset?

Employee_Handbook.pdf

This action cannot be undone.

[Cancel]

[Delete]
```

---

# 40. Reindex Individual Assets

Administrators may regenerate embeddings for a specific asset.

Typical reasons:

- Updated document
- New embedding model
- Improved chunking strategy

Workflow

```
Select Asset

↓

Delete Previous Embeddings

↓

Generate New Embeddings

↓

Update Metadata

↓

Refresh Statistics
```

Only the selected asset should be processed.

---

# 41. Rebuild Entire Knowledge Base

Administrators may rebuild the complete vector database.

Typical scenarios:

- Major architecture changes
- Embedding model migration
- Corrupted vector database

Workflow

```
Confirmation

↓

Delete Collection

↓

Reload Assets

↓

Extract Text

↓

Chunk Documents

↓

Generate Embeddings

↓

Store in ChromaDB

↓

Refresh Dashboard
```

The operation should display continuous progress.

---

# 42. Statistics

The system should maintain useful statistics.

Suggested metrics:

- Total Assets
- Total Pages
- Total Chunks
- Average Chunks per Asset
- Largest Asset
- Smallest Asset
- Storage Used
- Index Size
- Last Upload
- Last Reindex

Statistics improve transparency and maintenance.

---

# 43. Error Handling

Common processing errors should be handled gracefully.

Possible errors:

Unsupported File Type

Corrupted File

Empty Document

Extraction Failure

Embedding Failure

Database Failure

Duplicate Asset

Every error should generate:

- Friendly notification
- Log entry
- Suggested corrective action

The application should never expose Python stack traces to the user.

---

# 44. Logging Strategy

All administrative actions should be recorded.

Suggested events:

Upload Started

Upload Completed

Upload Failed

Asset Deleted

Asset Reindexed

Knowledge Base Rebuilt

Duplicate Detected

Extraction Failed

Embedding Failed

Database Updated

Logs should support troubleshooting and future auditing.

---

# 45. Performance Guidelines

The Knowledge Base should remain responsive.

Recommended objectives:

Small Documents

Processing under 5 seconds

Medium Documents

Processing under 20 seconds

Large Documents

Progress indicator required

Memory consumption should remain reasonable on consumer hardware.

---

# 46. Security Considerations

Only authenticated administrators may:

- Upload assets
- Delete assets
- Reindex assets
- Rebuild the Knowledge Base

Regular users must never access administrative functionality.

Uploaded assets should never be executable.

Only supported file types should be accepted.

---

# 47. Data Integrity

The Knowledge Base should guarantee consistency between:

- Original Assets
- Metadata
- Embeddings
- ChromaDB Collection

If any processing step fails, partial data should be rolled back whenever possible.

The system should never leave orphaned metadata or embeddings.

---

# 48. Scalability

The architecture should support future expansion.

Potential enhancements include:

- Multiple Knowledge Libraries
- Department-specific collections
- User-level permissions
- Scheduled indexing
- Automatic synchronization
- OCR support
- Image processing
- Audio transcription
- Cloud object storage

Version 1 intentionally focuses on a single local Knowledge Base.

---

# 49. Acceptance Criteria

This specification is considered complete when:

- Administrators can upload supported assets.
- Assets are validated before processing.
- Metadata is generated automatically.
- Embeddings are stored in ChromaDB.
- Duplicate assets are detected.
- Individual assets can be reindexed.
- Assets can be deleted safely.
- The entire Knowledge Base can be rebuilt.
- Statistics remain accurate.
- Dashboard information updates automatically.
- Processing errors are handled gracefully.

---

# 50. Notes for AI Development Agents

Implementation Guidelines

Architecture

- Respect Architecture.md.
- Respect all specifications.
- Keep responsibilities separated.

Backend

- One service per responsibility.
- Avoid duplicated logic.
- Keep services independent.

Storage

- Never mix uploaded files with vector data.
- Keep metadata synchronized.

Performance

- Process only modified assets.
- Avoid unnecessary reindexing.
- Cache expensive operations when appropriate.

Maintainability

- Use descriptive names.
- Document public methods.
- Follow Python best practices.

Future Compatibility

- Avoid hardcoded providers.
- Allow embedding model replacement.
- Keep the pipeline modular.

---

# 51. Final Notes

The Knowledge Base Management module is responsible for transforming uploaded knowledge assets into searchable semantic information.

It provides the administrative foundation required by the RAG Engine while hiding all technical complexity from end users.

This specification establishes the complete lifecycle of Knowledge Assets and ensures a consistent, maintainable and scalable architecture for Version 1 of the TechFlow AI Corporate Knowledge Agent.
