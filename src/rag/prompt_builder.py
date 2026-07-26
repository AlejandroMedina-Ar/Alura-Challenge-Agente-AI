"""
Prompt Builder Module

This module constructs RAG prompts by combining retrieved context
with user queries and system instructions.

Author: TechFlow AI Project
License: MIT
"""

from typing import Optional

from src.utils import get_logger


logger = get_logger()


class PromptBuilder:
    """
    Builder for RAG prompts.
    
    Features:
    - Combine query + retrieved context
    - System instruction formatting
    - Context citation formatting
    - Token-aware context truncation
    
    Constructs prompts in OpenAI message format for LLM providers.
    """
    
    # Default system instruction for RAG
    DEFAULT_SYSTEM_INSTRUCTION = """Eres un asistente corporativo de conocimiento especializado en responder preguntas basándote en documentación interna.

INSTRUCCIONES:
1. Responde ÚNICAMENTE usando la información del contexto proporcionado
2. Si la información no está en el contexto, indica claramente que no tienes esa información
3. Sé preciso y conciso en tus respuestas
4. Si el contexto contiene información relevante de múltiples fuentes, cítalas
5. Usa un tono profesional pero amigable
6. Responde en el mismo idioma que la pregunta

IMPORTANTE: No inventes información que no esté en el contexto."""
    
    def __init__(
        self,
        system_instruction: Optional[str] = None,
        include_sources: bool = True
    ):
        """
        Initialize prompt builder.
        
        Args:
            system_instruction: Custom system instruction (uses default if None)
            include_sources: Whether to include source citations in context
        
        Example:
            >>> builder = PromptBuilder()
            >>> messages = builder.build_prompt("What is RAG?", retrieved_docs)
        """
        self.system_instruction = system_instruction or self.DEFAULT_SYSTEM_INSTRUCTION
        self.include_sources = include_sources
        
        logger.info(
            f"PromptBuilder initialized",
            has_custom_instruction=bool(system_instruction),
            include_sources=include_sources
        )
    
    def build_prompt(
        self,
        query: str,
        retrieved_documents: list[dict],
        conversation_history: Optional[list[dict]] = None
    ) -> list[dict]:
        """
        Build complete RAG prompt in OpenAI message format.
        
        Args:
            query: User query
            retrieved_documents: List of retrieved docs (from Retriever)
            conversation_history: Optional previous messages
        
        Returns:
            list[dict]: Messages in OpenAI format
                [
                    {'role': 'system', 'content': '...'},
                    {'role': 'user', 'content': '...'}, (history)
                    {'role': 'assistant', 'content': '...'}, (history)
                    {'role': 'user', 'content': 'query + context'}
                ]
        
        Example:
            >>> builder = PromptBuilder()
            >>> messages = builder.build_prompt(
            ...     query="What is RAG?",
            ...     retrieved_documents=results
            ... )
            >>> print(messages[0]['role'])  # system
            >>> print(messages[-1]['role'])  # user
        """
        messages = []
        
        # Add system instruction
        messages.append({
            'role': 'system',
            'content': self.system_instruction
        })
        
        # Add conversation history if provided
        if conversation_history:
            messages.extend(conversation_history)
        
        # Build context from retrieved documents
        context = self._format_context(retrieved_documents)
        
        # Build user message with query + context
        user_message = self._build_user_message(query, context)
        
        messages.append({
            'role': 'user',
            'content': user_message
        })
        
        logger.debug(
            f"Prompt built",
            num_messages=len(messages),
            context_length=len(context),
            query_length=len(query)
        )
        
        return messages
    
    def _format_context(self, retrieved_documents: list[dict]) -> str:
        """
        Format retrieved documents into context string.
        
        Args:
            retrieved_documents: List of retrieved docs with text and metadata
        
        Returns:
            str: Formatted context string
        """
        if not retrieved_documents:
            return ""
        
        context_parts = []
        
        for i, doc in enumerate(retrieved_documents, 1):
            text = doc.get('text', '')
            metadata = doc.get('metadata', {})
            
            if self.include_sources:
                # Include source in citation
                source = metadata.get('source', 'Unknown')
                chunk_idx = metadata.get('chunk_index', '')
                
                if chunk_idx != '':
                    citation = f"[Fuente: {source}, Sección {chunk_idx + 1}]"
                else:
                    citation = f"[Fuente: {source}]"
                
                context_parts.append(f"--- Documento {i} {citation} ---\n{text}")
            else:
                context_parts.append(f"--- Documento {i} ---\n{text}")
        
        return "\n\n".join(context_parts)
    
    def _build_user_message(self, query: str, context: str) -> str:
        """
        Build user message combining query and context.
        
        Args:
            query: User query
            context: Formatted context string
        
        Returns:
            str: Complete user message
        """
        if not context:
            # No context available
            return f"""No se encontró información relevante en la base de conocimiento.

Pregunta: {query}

Por favor indica que no tienes información suficiente para responder esta pregunta."""
        
        return f"""Contexto (información recuperada de la base de conocimiento):

{context}

---

Pregunta: {query}

Responde basándote únicamente en el contexto proporcionado arriba."""
    
    def build_simple_prompt(
        self,
        query: str,
        context_texts: list[str]
    ) -> list[dict]:
        """
        Build simple prompt from query and context texts.
        
        Simpler version that takes just text strings instead of full document dicts.
        
        Args:
            query: User query
            context_texts: List of context text strings
        
        Returns:
            list[dict]: Messages in OpenAI format
        
        Example:
            >>> builder = PromptBuilder()
            >>> texts = ["Context 1...", "Context 2..."]
            >>> messages = builder.build_simple_prompt("query", texts)
        """
        # Convert texts to document format
        documents = [
            {'text': text, 'metadata': {}}
            for text in context_texts
        ]
        
        return self.build_prompt(query, documents)
    
    def estimate_token_count(
        self,
        messages: list[dict],
        chars_per_token: float = 4.0
    ) -> int:
        """
        Estimate token count for messages.
        
        Uses simple heuristic: ~4 characters per token.
        
        Args:
            messages: Messages list
            chars_per_token: Characters per token estimate
        
        Returns:
            int: Estimated token count
        
        Example:
            >>> builder = PromptBuilder()
            >>> messages = builder.build_prompt(query, docs)
            >>> tokens = builder.estimate_token_count(messages)
            >>> print(f"Estimated tokens: {tokens}")
        """
        total_chars = sum(len(msg['content']) for msg in messages)
        estimated_tokens = int(total_chars / chars_per_token)
        
        return estimated_tokens
    
    def truncate_context(
        self,
        retrieved_documents: list[dict],
        max_context_tokens: int,
        chars_per_token: float = 4.0
    ) -> list[dict]:
        """
        Truncate retrieved documents to fit token budget.
        
        Keeps most relevant documents (assuming they're sorted by relevance).
        
        Args:
            retrieved_documents: List of retrieved docs
            max_context_tokens: Maximum tokens for context
            chars_per_token: Characters per token estimate
        
        Returns:
            list[dict]: Truncated document list
        
        Example:
            >>> builder = PromptBuilder()
            >>> # Limit context to 2000 tokens
            >>> truncated = builder.truncate_context(docs, max_context_tokens=2000)
            >>> print(f"Kept {len(truncated)} of {len(docs)} documents")
        """
        max_chars = int(max_context_tokens * chars_per_token)
        
        truncated = []
        total_chars = 0
        
        for doc in retrieved_documents:
            text = doc.get('text', '')
            doc_chars = len(text)
            
            # Include overhead for formatting (citations, separators)
            doc_chars_with_overhead = doc_chars + 100
            
            if total_chars + doc_chars_with_overhead <= max_chars:
                truncated.append(doc)
                total_chars += doc_chars_with_overhead
            else:
                # Budget exceeded, stop adding
                break
        
        if len(truncated) < len(retrieved_documents):
            logger.warning(
                f"Context truncated to fit token budget",
                original_count=len(retrieved_documents),
                truncated_count=len(truncated),
                max_tokens=max_context_tokens
            )
        
        return truncated
    
    def update_system_instruction(self, new_instruction: str) -> None:
        """
        Update system instruction.
        
        Args:
            new_instruction: New system instruction text
        
        Example:
            >>> builder = PromptBuilder()
            >>> builder.update_system_instruction("Custom instruction...")
        """
        self.system_instruction = new_instruction
        logger.info("System instruction updated")
    
    def get_system_instruction(self) -> str:
        """
        Get current system instruction.
        
        Returns:
            str: Current system instruction
        
        Example:
            >>> builder = PromptBuilder()
            >>> instruction = builder.get_system_instruction()
            >>> print(instruction[:50])
        """
        return self.system_instruction


# Convenience: Allow direct import
__all__ = [
    'PromptBuilder',
]
