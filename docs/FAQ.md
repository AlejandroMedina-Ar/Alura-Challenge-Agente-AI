# ❓ Frequently Asked Questions (FAQ)

**Common questions about TechFlow AI RAG Agent**

---

## General Questions

### What is TechFlow AI?

TechFlow AI is a RAG-powered (Retrieval-Augmented Generation) knowledge agent that allows you to chat with your document collection using natural language. It combines document search with AI language models to provide accurate, context-aware responses.

### What does RAG mean?

RAG stands for Retrieval-Augmented Generation. It's a technique that:
1. **Retrieves** relevant information from your documents
2. **Augments** the AI's knowledge with that information
3. **Generates** accurate responses based on your data

### Is it free to use?

Yes! The entire stack uses free-tier services:
- **Google Gemini 1.5 Flash** (free tier)
- **Cohere Command-R** (free tier)
- **Local ChromaDB** (free, open-source)
- **Local embeddings** (free, runs on your machine)

You only need free API keys from Google and Cohere.

### What languages does it support?

The system is optimized for **Spanish** but also works well with:
- English
- Portuguese
- Other major languages

The multilingual E5 embeddings support 100+ languages.

---

## Installation & Setup

### What are the system requirements?

**Minimum:**
- Python 3.9 or higher
- 2GB RAM
- 1GB free disk space
- Internet connection

**Recommended:**
- Python 3.11+
- 4GB RAM
- 5GB free disk space
- Stable internet

### How do I get API keys?

**Google Gemini:**
1. Go to https://makersuite.google.com/app/apikey
2. Sign in with Google account
3. Click "Create API Key"
4. Copy the key

**Cohere:**
1. Go to https://dashboard.cohere.com
2. Sign up for free account
3. Navigate to API Keys section
4. Copy your key

### Where do I put the API keys?

In the `.env` file in the project root:

```bash
GEMINI_API_KEY=your_gemini_key_here
COHERE_API_KEY=your_cohere_key_here
```

### Do I need both API keys?

**Recommended:** Yes, for automatic fallback.

**Minimum:** Just one (Gemini or Cohere) will work, but without fallback protection.

### How do I know if setup was successful?

Run the test suite:

```bash
python test_integration.py
```

If you see "Pass Rate: 80-100%", setup is successful.

---

## Usage Questions

### What file formats are supported?

**Supported:**
- PDF (.pdf)
- Text (.txt)
- Markdown (.md)
- Word (.docx)

**Maximum size:** 10MB per file

### Why can't I upload my file?

**Common reasons:**
1. File is too large (>10MB)
2. Unsupported format
3. File is corrupted
4. Filename has special characters

**Solution:** Try converting to PDF or splitting large documents.

### Do I need to index documents after uploading?

**Yes!** Uploading just stores the file. Indexing processes it for search:
1. Upload document
2. Click "Index" in Admin Panel
3. Wait for indexing to complete
4. Now you can chat about it

### How long does indexing take?

**Typical times:**
- 1MB document: 10-30 seconds
- 5MB document: 1-2 minutes
- 10MB document: 2-5 minutes

Depends on document complexity and system performance.

### Can I upload multiple documents at once?

**Upload:** One at a time currently.

**Index:** Yes! Use "Index All Pending" in Admin Panel to process multiple documents in batch.

### Why don't my responses reference my documents?

**Possible reasons:**
1. Documents not indexed yet
2. Question not specific enough
3. Relevant info not in documents
4. Top-K too low (increase in Settings)

**Try:**
- Re-index documents
- Ask more specific questions
- Increase Top-K to 7-10
- Check if documents uploaded successfully

---

## Technical Questions

### How does the RAG pipeline work?

**Step-by-step:**
1. **Upload:** You upload a document
2. **Chunking:** Document split into ~512 character chunks with overlap
3. **Embedding:** Each chunk converted to 768-dimensional vector
4. **Storage:** Vectors stored in ChromaDB
5. **Query:** Your question is also converted to a vector
6. **Search:** Similar vectors (chunks) are retrieved
7. **Prompt:** Retrieved chunks added as context
8. **Generate:** LLM generates answer using context

### What is chunk size and overlap?

**Chunk Size:**
- How many characters per chunk
- Default: 512 characters
- Smaller = more precise, more chunks
- Larger = more context, fewer chunks

**Overlap:**
- Characters shared between consecutive chunks
- Default: 50 characters
- Prevents losing context at boundaries

### What is Top-K?

**Top-K** is the number of most relevant chunks retrieved per query.

- **K=3:** Fast, less context
- **K=5:** Balanced (default)
- **K=10:** Slower, more context

Higher K = more context but slower responses.

### What does temperature control?

**Temperature** (0.0-2.0) controls response creativity:

- **0.0-0.5:** Deterministic, focused, consistent
- **0.5-1.0:** Balanced (default: 0.7)
- **1.0-2.0:** Creative, varied, less predictable

For factual Q&A, keep it low (0.3-0.7).

### How does automatic fallback work?

If Gemini fails (API error, quota, timeout):
1. System automatically tries Cohere
2. Response seamlessly continues
3. User doesn't notice the switch
4. Logged for monitoring

### Where is my data stored?

**Locally on your machine:**
- Documents: `data/knowledge_library/documents/`
- Metadata: `data/knowledge_library/metadata/`
- Vector DB: `data/chromadb/`
- Config: `data/config.json`
- Logs: `data/logs/`

**Not sent anywhere** except:
- Document chunks to embedding model (local)
- Prompts to LLM APIs (Gemini/Cohere)

---

## Troubleshooting

### "Module not found" error on startup

**Cause:** Missing dependencies

**Fix:**
```bash
pip install -r requirements.txt
```

### Chat doesn't respond

**Causes:**
1. No API keys configured
2. No documents indexed
3. Internet connection issue
4. API quota exceeded

**Fix:**
1. Check `.env` has valid API keys
2. Index at least one document
3. Check internet connection
4. Test providers in Admin Panel

### "LLM provider test failed"

**Causes:**
1. Invalid API key
2. No internet connection
3. API service down
4. Quota exceeded

**Fix:**
1. Verify API keys in `.env`
2. Test: `curl https://google.com`
3. Wait and retry
4. Check API dashboard for quota

### Indexing fails silently

**Check logs:**
```bash
cat data/logs/application.log | grep ERROR
```

**Common causes:**
1. File is corrupted
2. File has no extractable text
3. Out of disk space
4. ChromaDB connection issue

### Responses are slow

**Optimization:**
1. Reduce Top-K (Settings → RAG)
2. Use smaller chunk size
3. Clear browser cache
4. Check internet speed
5. Try different LLM provider

### Can't login

**Default password location:** `.env` file

**Reset steps:**
1. Open `.env` file
2. Change `ADMIN_PASSWORD=new_password`
3. Save file
4. Restart application

### Application crashes on startup

**Steps:**
1. Check Python version: `python --version` (need 3.9+)
2. Run setup: `python setup.py`
3. Check logs: `data/logs/application.log`
4. Reinstall dependencies: `pip install -r requirements.txt --force-reinstall`

---

## Performance Questions

### How many documents can I upload?

**Practical limits:**
- **100 documents:** Works smoothly
- **1000 documents:** Slower but functional
- **10,000+ documents:** May need optimization

**Factors:**
- Total size of documents
- Available RAM
- Disk space

### How much disk space do I need?

**Breakdown:**
- Application: ~50MB
- Documents: Depends on your files
- Vector DB: ~1KB per chunk
- Logs: ~10-50MB

**Example:** 100 documents (1MB each, ~200 chunks) = ~100MB + 200KB + logs

### Can I run this on a Raspberry Pi?

**Theoretically yes**, but not recommended:
- Indexing will be very slow
- Limited RAM may cause issues
- Better on a laptop/desktop

### Does it work offline?

**Partial:**
- ✅ Indexing works (with local embeddings)
- ❌ Chat requires internet (LLM APIs)

**Workaround:** Use local LLM (requires code modification)

---

## Privacy & Security

### Is my data private?

**Yes, mostly:**
- Documents stored **locally only**
- Vectors stored **locally only**
- Metadata stored **locally only**

**Sent to cloud:**
- Document chunks (during query) → LLM API
- Questions → LLM API

**Not sent:**
- Full documents
- User information
- Anything else

### Can I use it for sensitive documents?

**Considerations:**
1. Data sent to Gemini/Cohere during chat
2. Review their privacy policies
3. For highly sensitive data, consider self-hosted LLMs

**Recommendation:** Remove sensitive info before uploading.

### How are passwords stored?

- **Hashed** using bcrypt
- **Not reversible**
- **Stored** in session state (temporary)
- **Not logged**

### Can someone else access my documents?

**No**, if:
- You're the only user on your machine
- You logout when done
- You don't share admin password

**Yes**, if:
- Someone has physical access to your machine
- Someone knows your admin password
- Computer is compromised

---

## Customization Questions

### Can I change the system prompt?

**Yes!** In code:
```python
# src/rag/prompt_builder.py
DEFAULT_SYSTEM_INSTRUCTION = "Your custom prompt here..."
```

Or via Settings → RAG → System Instruction (if UI implemented).

### Can I add more LLM providers?

**Yes!** Follow the pattern:
1. Create `src/llm/new_provider.py`
2. Extend `BaseLLMProvider`
3. Implement required methods
4. Add to `src/llm/__init__.py`

### Can I change the theme colors?

**Yes!** Edit CSS files:
- Light: `assets/css/light.css`
- Dark: `assets/css/dark.css`

### Can I deploy this as a service?

**Yes!** See deployment options:
1. Streamlit Community Cloud (easiest)
2. Docker container
3. Cloud VM (AWS, GCP, Azure)
4. On-premises server

See `docs/DEPLOYMENT.md` for details.

---

## Comparison Questions

### vs. ChatGPT?

**TechFlow AI:**
- ✅ Uses YOUR documents
- ✅ Privacy (local storage)
- ✅ Free tier
- ✅ Customizable
- ❌ Smaller model
- ❌ Self-hosted

**ChatGPT:**
- ✅ Powerful model
- ✅ Cloud-hosted
- ✅ No setup
- ❌ Doesn't know your docs
- ❌ Data privacy concerns
- ❌ Paid for full features

### vs. Microsoft Copilot?

**TechFlow AI:**
- ✅ 100% free
- ✅ Full control
- ✅ Local data
- ❌ Manual setup

**Copilot:**
- ✅ Integrated in Office
- ✅ No setup
- ❌ Microsoft account needed
- ❌ Subscription required

### vs. Building from scratch?

**TechFlow AI:**
- ✅ Ready to use
- ✅ Tested and working
- ✅ Good architecture
- ✅ Documentation
- ❌ Less flexible

**From Scratch:**
- ✅ Full customization
- ✅ Learning experience
- ❌ Weeks of development
- ❌ More bugs

---

## Advanced Questions

### Can I use local LLMs?

**Yes**, but requires code changes:
1. Create new LLM provider for local model (Ollama, llama.cpp)
2. Point to local endpoint
3. Adjust prompts if needed

### Can I use different embedding models?

**Yes!** In code:
```python
# src/config/constants.py
DEFAULT_EMBEDDING_MODEL = "your-model-name"
```

Must be compatible with sentence-transformers.

### Can I export the vector database?

**Yes!** ChromaDB data is in:
```
data/chromadb/
```

Can be backed up/moved to another machine.

### Can I integrate with my existing app?

**Yes!** The services layer can be imported:
```python
from src.services import get_chat_service

chat_service = get_chat_service()
response = chat_service.chat("query", stream=False)
```

### Can I contribute to the project?

**Yes!** Contributions welcome:
1. Fork the repository
2. Create feature branch
3. Make changes
4. Submit pull request

See `CONTRIBUTING.md` for guidelines.

---

## Getting Help

### Where can I find more information?

**Documentation:**
- [User Guide](USER-GUIDE.md) - How to use
- [Technical Docs](TECHNICAL-DOCS.md) - Developer reference
- [Architecture](../architecture/Architecture.md) - System design

**Code:**
- [GitHub Repository](https://github.com/AlejandroMedina-Ar/Alura-Challenge-Agente-AI)
- [Issues](https://github.com/AlejandroMedina-Ar/Alura-Challenge-Agente-AI/issues)

### How do I report a bug?

1. Check if it's already reported: [Issues](https://github.com/AlejandroMedina-Ar/Alura-Challenge-Agente-AI/issues)
2. If not, create new issue with:
   - Steps to reproduce
   - Expected vs actual behavior
   - Error messages
   - System info (OS, Python version)
   - Relevant logs

### How do I request a feature?

1. Open GitHub issue
2. Tag with "enhancement"
3. Describe:
   - What you want
   - Why it's useful
   - How it might work

### Can I get commercial support?

**Currently:** Community support only (GitHub Issues)

**Future:** Commercial support may be available for enterprise users.

---

**Have a question not answered here?** Open an issue on GitHub!

**Version:** 1.0.0-beta  
**Last Updated:** 2026-07-25
