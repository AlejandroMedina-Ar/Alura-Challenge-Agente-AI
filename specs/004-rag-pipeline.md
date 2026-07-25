# RAG Pipeline Specification

**Specification ID:** SPEC-004

**Module:** RAG Pipeline

**Version:** 1.0

**Status:** Draft

---

# 1. Purpose

This document defines how the Retrieval-Augmented Generation (RAG) pipeline operates within the TechFlow AI Corporate Knowledge Agent.

The RAG pipeline is responsible for transforming a user's question into a context-aware response using information stored in the Knowledge Base.

Its primary goal is to improve answer accuracy by retrieving relevant information before sending the prompt to the Large Language Model (LLM).

---

# 2. Scope

This specification covers:

- User query processing
- Query embedding generation
- Vector similarity search
- Context retrieval
- Prompt construction
- LLM invocation
- Response generation
- Source attribution

This specification does not cover:

- Knowledge Asset processing
- Authentication
- UI design
- Deployment
- Provider configuration

---

# 3. RAG Pipeline Overview

The application follows a standard Retrieval-Augmented Generation workflow.

```
User Question

↓

Generate Query Embedding

↓

Search ChromaDB

↓

Retrieve Relevant Chunks

↓

Build Prompt

↓

Send to LLM

↓

Generate Answer

↓

Display Sources
```

Each step should remain independent and modular.

---

# 4. Pipeline Principles

The RAG pipeline should follow these principles:

- Simplicity
- Modularity
- Maintainability
- Explainability
- Source transparency
- Fast response time

The pipeline should avoid unnecessary complexity while remaining easy to extend.

---

# 5. User Query Processing

When a user submits a question:

1. Validate the input.
2. Ignore empty questions.
3. Trim unnecessary whitespace.
4. Preserve the original wording.
5. Generate an embedding for the query.

The original question should always be included in the final prompt.

---

# 6. Query Embedding

The user question should be converted into an embedding using the same embedding model employed during indexing.

Default model:

```
BAAI/bge-small-en-v1.5
```

This ensures compatibility between stored vectors and query vectors.

---

# 7. Similarity Search

After generating the query embedding, perform a similarity search against ChromaDB.

Recommended default:

Top K = 4

The number of retrieved chunks should remain configurable.

Only the most relevant chunks should be returned.

---

# 8. Retrieved Context

Each retrieved chunk should include:

- Text
- Filename
- Page number (if available)
- Chunk identifier

Example

```
Employee_Handbook.pdf

Page 18

Chunk 42
```

This information will later be shown as references.

---

# 9. Prompt Construction

The prompt sent to the LLM should contain:

System Instructions

Retrieved Context

Conversation History (optional)

User Question

Example structure:

```
System Prompt

Context

Question

Answer
```

The LLM should answer only using the retrieved context whenever possible.

---

# 10. LLM Invocation

The RAG pipeline should remain independent of any specific LLM provider.

The pipeline simply sends:

- Prompt
- Temperature
- Max Tokens

The provider implementation is defined in SPEC-005.

---

# 11. Response Generation

The LLM returns a response based on:

- User question
- Retrieved context
- System prompt

The application displays the answer inside the chat interface.

---

# 12. Source Attribution

Every response should display the sources used.

Suggested format:

```
Sources

• Employee_Handbook.pdf (Page 18)

• Company_FAQ.pdf (Page 4)
```

Source attribution increases user confidence and transparency.

---

# 13. Conversation Memory

Version 1 includes lightweight conversation memory.

The current chat session should preserve previous messages using Streamlit session state.

Conversation history should not persist after the application is closed.

---

# 14. Error Handling

Possible errors include:

- No relevant documents found
- Empty Knowledge Base
- LLM unavailable
- Embedding generation failed
- ChromaDB unavailable

Friendly messages should be displayed instead of technical errors.

---

# 15. Performance Guidelines

Recommended objectives:

- Query embedding generation under 1 second.
- Vector search under 500 milliseconds.
- Overall response time under 10 seconds (depending on the LLM).

The interface should display a loading indicator while processing.

---

# 16. Acceptance Criteria

This specification is complete when:

- User questions are embedded successfully.
- ChromaDB returns relevant chunks.
- Prompts include retrieved context.
- The LLM generates contextual answers.
- Sources are displayed.
- Errors are handled gracefully.

---

# 17. Notes for AI Development Agents

Implementation Guidelines

Architecture

- Keep each pipeline stage independent.
- Avoid mixing UI logic with backend logic.
- Keep provider logic separate from retrieval logic.

Performance

- Minimize unnecessary database calls.
- Cache reusable resources when appropriate.

Maintainability

- Use descriptive service names.
- Keep functions small and focused.

Future Compatibility

The architecture should support:

- Hybrid Search
- Metadata Filtering
- Reranking
- Multiple Vector Databases
- Streaming Responses

These enhancements are outside the scope of Version 1.

---

# 18. Final Notes

The RAG Pipeline is the core of the application.

It connects the Knowledge Base with the selected LLM, enabling accurate and context-aware answers while maintaining a simple, modular and maintainable architecture suitable for Version 1 of the TechFlow AI Corporate Knowledge Agent.
