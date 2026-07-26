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

Send to LLM (Gemini primary, Cohere fallback)

↓

Generate Answer

↓

Display Sources
```

Each step should remain independent and modular.

---

## 3.1 Pipeline Orchestration

The `rag/pipeline.py` module acts as the primary orchestrator of the RAG workflow. It receives a user question from `chat_service.py` and coordinates the following steps:

1. Call `embedding_service.generate_query_embedding(question)`
2. Call `retriever.search(embedding, top_k=MAX_CONTEXT_CHUNKS)`
3. Call `prompt_builder.build_rag_prompt(question, retrieved_chunks)`
4. Return the prompt to `chat_service.py`, which then calls `llm_service.generate_response(prompt)`

**Responsibility boundary:** `rag/pipeline.py` handles everything EXCEPT the final LLM invocation, which remains the responsibility of `chat_service.py` to allow future conversation management features and provider fallback logic.

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
intfloat/multilingual-e5-base
```

This ensures compatibility between stored vectors and query vectors.

---

# 7. Similarity Search

After generating the query embedding, perform a similarity search against ChromaDB.

Recommended default:

MAX_CONTEXT_CHUNKS = 4

The number of retrieved chunks should remain configurable via environment variables (see SPEC-005).

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

System Prompt

Retrieved Context

Conversation History (current session only, using Streamlit session state)

User Question

Example structure:

```
System Prompt

Context

Question

Answer
```

The LLM should answer only using the retrieved context whenever possible.

**Token Limit Handling:** If the constructed prompt exceeds the LLM's context window (checked via provider-specific token counter), the system should dynamically reduce `MAX_CONTEXT_CHUNKS` or truncate chunks to fit within limits.

---

# 10. LLM Invocation

The RAG pipeline should remain independent of any specific LLM provider.

The pipeline simply sends:

- Prompt
- Temperature
- Max Tokens

Provider implementation and fallback logic are defined in SPEC-005.

The LLM invocation is handled by `chat_service.py`, which uses `llm_service` to call the appropriate provider (Gemini primary, Cohere fallback).

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

v1 includes lightweight conversation memory during the current session only.

The current chat session should preserve previous messages using Streamlit session state.

Conversation history should not persist after the application is closed or the browser is refreshed.

**Scope Clarification:** "Session-based conversation memory" (temporary, current chat) is included in v1. "Persistent conversation history" (saved chats across sessions) is explicitly out of scope for v1.

---

# 13.1 LLM Provider Fallback Strategy

v1 implements a dual-provider architecture with automatic fallback for reliability and cost optimization.

## Primary Provider: Google Gemini (Free Tier)

Default model: `gemini-2.0-flash-exp` or equivalent free-tier model

Used for all requests under normal conditions.

## Fallback Provider: Cohere

Used automatically when Gemini encounters errors or limitations.

## Fallback Triggers

The system switches to Cohere when Gemini experiences:

1. **Rate Limit Errors** (429 status code or equivalent)
2. **Quota Exceeded** (free tier daily/monthly limits)
3. **API Timeout** (request exceeds 30 seconds)
4. **Service Unavailable** (503 status code)
5. **Authentication Errors** (invalid API key)
6. **Model Not Available** (model deprecation or unavailability)

## Retry Strategy

Before switching to fallback:

1. First request fails → Log error
2. Retry once with exponential backoff (2 seconds delay)
3. Second failure → Switch to Cohere fallback
4. Log fallback event with reason

**No retries** for authentication errors or invalid API keys (immediate fallback).

## User Notification

Fallback is **transparent and automatic**. Users are NOT notified during normal operation.

However, the system status indicator in the sidebar should reflect the active provider:

```
🟢 LLM: Gemini

or

🟡 LLM: Cohere (fallback active)
```

## Logging

All fallback events should be logged with:

- Timestamp
- Original error from Gemini
- Reason for fallback
- Active provider after fallback

Example log entry:

```
[2026-07-25 14:32:18] WARNING - Gemini rate limit exceeded (429). Switching to Cohere fallback.
[2026-07-25 14:32:19] INFO - LLM request successful using Cohere.
```

## Fallback Duration

Once triggered, the fallback provider remains active for:

- Current request only (request-level fallback), OR
- 5 minutes (session-level fallback if Gemini is experiencing ongoing issues)

After 5 minutes, the system automatically attempts to use Gemini again.

## Configuration

Both API keys must be configured in `.env`:

```
GEMINI_API_KEY=your_gemini_key
COHERE_API_KEY=your_cohere_key
```

If either key is missing, the application should warn during startup but continue with available provider(s).

## Error Handling if Both Fail

If both Gemini AND Cohere fail:

1. Log critical error
2. Display user-friendly message:
   ```
   ⚠ AI services temporarily unavailable.
   Please try again in a few moments.
   ```
3. Do NOT expose technical error details to users

---

# 14. Error Handling

Possible errors include:

- No relevant documents found
- Empty Knowledge Base
- LLM unavailable (both Gemini and Cohere)
- Embedding generation failed
- ChromaDB unavailable
- ChromaDB initialization failure
- ChromaDB collection corruption
- Disk full (ChromaDB persistence)

Friendly messages should be displayed instead of technical errors.

## Empty Knowledge Base

If a user submits a question but the Knowledge Library contains no indexed documents (count = 0), the system must NOT invoke the LLM.

Instead, display exactly this message:

```
Por favor agregar al menos 2 documentos para poder indexarlos
```

This validates that the Knowledge Base has sufficient content before attempting retrieval.

## ChromaDB Error Handling

Specific ChromaDB failure scenarios:

**Initialization Failure:**
Display: "Vector database initialization failed. Please check logs and restart the application."

**Collection Corruption:**
Display: "Knowledge Base index corrupted. Administrator should rebuild the index."

**Disk Full:**
Display: "Storage space exhausted. Please free disk space or contact administrator."

**Connection Lost:**
Display: "Knowledge Base temporarily unavailable. Retrying..."

All ChromaDB errors should be logged with full stack traces for debugging.

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
