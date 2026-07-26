# 📖 TechFlow AI - User Guide

**Complete guide for using the TechFlow AI RAG Agent**

---

## Table of Contents

1. [Getting Started](#getting-started)
2. [Login](#login)
3. [Chat Interface](#chat-interface)
4. [Knowledge Library](#knowledge-library)
5. [Admin Panel](#admin-panel)
6. [Settings](#settings)
7. [Tips & Best Practices](#tips--best-practices)
8. [Troubleshooting](#troubleshooting)

---

## Getting Started

### First Time Setup

1. **Install the application** (if not already done):
   ```bash
   python setup.py
   ```

2. **Configure API keys** in `.env` file:
   ```bash
   GEMINI_API_KEY=your_gemini_key_here
   COHERE_API_KEY=your_cohere_key_here
   ADMIN_PASSWORD=your_secure_password
   ```

3. **Start the application**:
   ```bash
   python run.py
   ```

4. **Open browser** at: http://localhost:8501

---

## Login

### Admin Authentication

1. Navigate to the login page (default on first visit)
2. Enter your admin password (set in `.env` file)
3. Click **Login**

**Default Credentials:**
- Username: `admin` (fixed)
- Password: Check your `.env` file

**Security Notes:**
- Sessions expire after inactivity
- Always logout when done using public computers
- Change default password in production

---

## Chat Interface

### Starting a Conversation

1. Navigate to **💬 Chat** from the sidebar
2. Type your question in the chat input box
3. Press Enter or click Send
4. Wait for the streaming response

### Chat Features

#### **Streaming Responses**
- Responses appear word-by-word in real-time
- Can be interrupted by refreshing the page
- Shows thinking process

#### **Conversation History**
- Previous messages are maintained in session
- Context-aware: system remembers conversation
- Cleared when you click "Clear Chat" or reload

#### **Source Citations**
- Responses include source document references
- Format: `[Fuente: document.pdf, Sección 2]`
- Helps verify information accuracy

### Example Questions

**Good Questions:**
- "¿Cuál es el proceso de onboarding para nuevos empleados?"
- "Resume el documento de políticas de vacaciones"
- "¿Qué dice el manual sobre trabajo remoto?"

**Questions to Avoid:**
- Too vague: "Dime algo"
- Outside knowledge base: "¿Qué hora es?"
- Personal questions: System doesn't have personal context

### Chat Controls

**Clear Chat:**
- Clears conversation history
- Fresh start for new topic

**Export Chat:**
- Downloads conversation as text file
- Useful for documentation or sharing

---

## Knowledge Library

### Uploading Documents

1. Navigate to **📚 Knowledge Library**
2. Click **Choose a document** or drag & drop
3. Select file from your computer
4. Wait for upload confirmation

**Supported Formats:**
- PDF (.pdf) - Max 10MB
- Text (.txt) - Max 10MB
- Markdown (.md) - Max 10MB
- Word (.docx) - Max 10MB

**Upload Best Practices:**
- Use descriptive filenames
- Keep files under 10MB
- Remove sensitive information first
- Ensure text is readable (not scanned images)

### Managing Documents

**View Documents:**
- See list of all uploaded documents
- Check upload date and size
- View indexing status

**Delete Documents:**
- Click 🗑️ Delete button
- Confirm deletion
- Both file and index are removed

**Index Status:**
- ✅ Indexed - Ready for chat
- ⚠️ Not indexed - Needs indexing

---

## Admin Panel

### Dashboard Tab

**System Overview:**
- Total documents uploaded
- Indexed documents count
- Total chunks in vector store
- Storage used (MB)

**System Status:**
- RAG Pipeline status (Ready/Not Ready)
- Vector store count
- LLM configuration (Provider, Temperature)

### Documents Tab

**Upload Documents:**
- Same as Knowledge Library page
- More detailed upload interface
- Bulk operations available

**Manage Documents:**
- View all documents
- Delete individual documents
- Index/Re-index documents

**Document Actions:**
- 🗑️ **Delete** - Remove document permanently
- ⚡ **Index** - Index document for chat
- 🔄 **Re-index** - Re-process existing document

### Indexing Tab

**Indexing Operations:**
- View pending documents (not indexed)
- Index all pending at once
- Clear all indexes (warning: destructive!)

**Statistics:**
- Indexed documents
- Pending documents
- Total chunks

**Batch Operations:**
- ⚡ **Index All Pending** - Process all unindexed documents
- 🗑️ **Clear All Indexes** - Remove all from vector store

### Testing Tab

**LLM Provider Tests:**
- Test Gemini connectivity
- Test Cohere connectivity
- View response times
- Verify API keys

**Test Results:**
- ✅ Success - Provider working
- ❌ Failed - Check API key or connection

---

## Settings

### LLM Settings

**Provider Selection:**
- **Gemini** (Primary) - Fast, reliable
- **Cohere** (Fallback) - Automatic backup

**Model Selection:**
- Gemini: `gemini-1.5-flash` (recommended)
- Cohere: `command-r`

**API Key:**
- Enter your provider API key
- Stored securely in local config
- Hidden with asterisks for security

### RAG Settings

**Chunking Settings:**
- **Chunk Size** (128-2048 chars)
  - Smaller = More precise, more chunks
  - Larger = More context, fewer chunks
  - Default: 512 characters

- **Chunk Overlap** (0-512 chars)
  - Overlap between chunks
  - Prevents losing context at boundaries
  - Default: 50 characters

**Retrieval Settings:**
- **Top K** (1-20)
  - Number of chunks to retrieve
  - More = More context, slower
  - Less = Faster, less context
  - Default: 5 chunks

**Generation Settings:**
- **Temperature** (0.0-2.0)
  - 0.0-0.5: Focused, deterministic
  - 0.5-1.0: Balanced (default: 0.7)
  - 1.0-2.0: Creative, varied

### UI Settings

**Theme Selection:**
- **Light** - Bright, high contrast
- **Dark** - Easy on eyes, low light

**Theme Changes:**
- Applied immediately
- Saved for next session

### Configuration Management

**Validate Configuration:**
- Check if all settings are valid
- Shows errors if any

**Export Configuration:**
- Download config as JSON
- API keys are redacted
- Useful for backup

**Reset to Defaults:**
- Restore original settings
- Warning: Cannot be undone
- API keys are preserved

---

## Tips & Best Practices

### Document Preparation

**Before Uploading:**
1. Review content for sensitive information
2. Ensure text is machine-readable
3. Use clear, descriptive filenames
4. Remove unnecessary pages/sections

**Optimal Document Format:**
- Well-structured with headers
- Clear paragraphs
- Avoid overly long documents (split if needed)
- Include table of contents if possible

### Getting Better Responses

**Ask Specific Questions:**
- ❌ "Tell me about HR"
- ✅ "What is the vacation policy for full-time employees?"

**Reference Documents:**
- "According to the employee handbook..."
- "In the 2024 sales report..."

**Break Down Complex Questions:**
- Instead of one complex question
- Ask 2-3 simpler questions

**Use Context from History:**
- Follow-up questions work well
- "Can you elaborate on that?"
- "What about part-time employees?"

### Indexing Strategy

**When to Index:**
- Immediately after uploading new documents
- After updating existing documents
- If search results seem outdated

**Batch Indexing:**
- Upload multiple documents first
- Then index all at once
- More efficient than one-by-one

**Re-indexing:**
- If document was updated
- If search quality degrades
- After changing chunk settings

### Configuration Tuning

**For Precise Answers:**
- Smaller chunk size (256-384)
- Higher top-k (7-10)
- Lower temperature (0.3-0.5)

**For Creative Responses:**
- Larger chunk size (512-1024)
- Medium top-k (5)
- Higher temperature (0.7-1.0)

**For Fast Performance:**
- Medium chunk size (512)
- Lower top-k (3-5)
- Default temperature (0.7)

---

## Troubleshooting

### Common Issues

#### Cannot Login

**Problem:** Login fails with "Invalid credentials"

**Solutions:**
1. Check `.env` file for correct password
2. Ensure no extra spaces in password
3. Try resetting password in `.env`
4. Restart application after changing `.env`

#### No Response from Chat

**Problem:** Chat doesn't respond or shows error

**Solutions:**
1. Check if documents are indexed (Admin Panel)
2. Verify API keys in Settings
3. Test LLM providers in Admin Panel → Testing
4. Check internet connection
5. Review logs in `data/logs/application.log`

#### Upload Fails

**Problem:** Document upload fails

**Solutions:**
1. Check file size (max 10MB)
2. Verify file format (PDF, TXT, MD, DOCX)
3. Ensure filename has no special characters
4. Check disk space
5. Try different file

#### Indexing Fails

**Problem:** Document fails to index

**Solutions:**
1. Check if file is readable (not corrupted)
2. Verify file contains text (not just images)
3. Check logs for specific error
4. Try re-uploading document
5. Check disk space for ChromaDB

#### Poor Search Results

**Problem:** Responses don't use relevant documents

**Solutions:**
1. Re-index documents
2. Increase top-k (Settings → RAG)
3. Adjust chunk size
4. Rephrase question more specifically
5. Check if relevant documents are uploaded

#### Slow Performance

**Problem:** Application is slow or laggy

**Solutions:**
1. Reduce top-k value
2. Clear browser cache
3. Restart application
4. Check system resources
5. Reduce number of indexed documents

### Error Messages

**"Knowledge Library is Empty"**
- Upload and index at least one document
- Go to Knowledge Library → Upload

**"LLM Provider Failed"**
- Check API keys in Settings
- Test providers in Admin Panel
- Verify internet connection
- Check API quota/limits

**"Indexing Error"**
- Check file format is supported
- Verify file is not corrupted
- Review application logs
- Try smaller documents

**"Configuration Invalid"**
- Go to Settings → Configuration
- Click "Validate Configuration"
- Fix reported errors
- Or reset to defaults

### Getting Help

**Check Logs:**
```
data/logs/application.log
```

**Run Tests:**
```bash
python test_integration.py
```

**Report Issues:**
- GitHub Issues: [Repository Issues](https://github.com/AlejandroMedina-Ar/Alura-Challenge-Agente-AI/issues)
- Include error message
- Describe steps to reproduce
- Attach relevant logs (remove sensitive info)

---

## Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Enter` | Send chat message |
| `Ctrl+K` | Focus chat input |
| `Esc` | Clear chat input |
| `Ctrl+/` | Toggle sidebar |

---

## Best Practices Summary

✅ **Do:**
- Use specific, clear questions
- Upload well-formatted documents
- Index documents after uploading
- Test LLM providers regularly
- Keep API keys secure
- Logout when done

❌ **Don't:**
- Upload sensitive information without review
- Ask questions outside knowledge base
- Share admin credentials
- Delete documents without backup
- Change settings randomly
- Ignore error messages

---

**Need more help?** Check the [Technical Documentation](TECHNICAL-DOCS.md) or [API Reference](API-REFERENCE.md)

**Version:** 1.0.0-beta  
**Last Updated:** 2026-07-25
