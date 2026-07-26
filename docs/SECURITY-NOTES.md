# 🔒 Security Notes - API Keys and Credentials

**Created:** 2026-07-25  
**Status:** Development Environment Setup

---

## ⚠️ IMPORTANT: API Keys Configuration

This document explains how API keys are managed in this project for **security** and **deployment** purposes.

---

## 📁 Files and Their Purposes

### `.env` (LOCAL ONLY - NOT IN GIT)
**Location:** `d:\techflow-rag-agent\.env`  
**Purpose:** Contains real API keys for local development and testing  
**Git Status:** ✅ Protected by `.gitignore` - NEVER committed to repository  
**Current Status:** ✅ Created with testing API keys

**Contents:**
```env
GEMINI_API_KEY=your_testing_gemini_api_key_here
COHERE_API_KEY=your_testing_cohere_api_key_here
ADMIN_PASSWORD=admin123
```

**⚠️ IMPORTANT:** Real API keys are configured in your local `.env` file (not in Git).

⚠️ **THESE ARE TESTING KEYS** - Will be replaced before production deployment.

---

### `.env.example` (PUBLIC - IN GIT)
**Location:** `d:\techflow-rag-agent\.env.example`  
**Purpose:** Template showing what variables are needed (without real values)  
**Git Status:** ✅ Committed to repository as reference  

**Contents:**
```env
GEMINI_API_KEY=your_gemini_api_key_here
COHERE_API_KEY=your_cohere_api_key_here
ADMIN_PASSWORD=admin123
```

---

## 🔐 Security Rules

### ❌ NEVER Do This
- Commit `.env` file to Git
- Share API keys in public channels
- Hardcode API keys in source code
- Push API keys to GitHub/GitLab
- Screenshot files containing API keys
- Email or message API keys in plain text

### ✅ ALWAYS Do This
- Keep API keys in `.env` (local) or Secrets (cloud)
- Use `.env.example` as template
- Verify `.env` is in `.gitignore`
- Rotate keys before production deployment
- Use different keys for dev/test/prod environments

---

## 🛠️ Current Development Setup

### Local Development (Cursor/Testing)
**File:** `.env` (already created)  
**Keys:** Testing keys provided by user  
**Status:** ✅ Ready for Cursor to use during implementation

### Testing Keys Information
- **Gemini Key:** Free tier, 15 req/min, 1M tokens/day
- **Cohere Key:** Free tier, 1000 req/month
- **Purpose:** Development and functional testing only
- **Replacement:** Required before production deployment

---

## 🚀 Deployment Configurations

### Streamlit Community Cloud
**Method:** Secrets Management (TOML format)

**Location:** Dashboard → App Settings → Secrets

**Format:**
```toml
# LLM Providers
GEMINI_API_KEY = "production_key_here"
COHERE_API_KEY = "production_key_here"

# Security
ADMIN_PASSWORD = "strong_password_here"

# Embeddings
EMBEDDING_MODEL = "intfloat/multilingual-e5-base"

# Vector Database
CHROMA_DB_PATH = "data/chromadb"
CHROMA_COLLECTION = "techflow_knowledge_base"

# Chunking
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200

# Chat
MAX_CONTEXT_CHUNKS = 4
TEMPERATURE = 0.2
MAX_OUTPUT_TOKENS = 1024

# Timeouts
LLM_REQUEST_TIMEOUT = 30
EMBEDDING_TIMEOUT = 120
CHROMADB_TIMEOUT = 10

# Logging
LOG_LEVEL = "INFO"
LOG_FILE = "data/logs/application.log"
```

⚠️ **BEFORE DEPLOYMENT:**
1. Generate new production API keys
2. Create strong admin password (not "admin123")
3. Never reuse development keys in production

---

### Render Deployment
**Method:** Environment Variables

**Location:** Dashboard → Environment → Environment Variables

Add each variable as Key-Value pair:
- `GEMINI_API_KEY` = `production_key_here`
- `COHERE_API_KEY` = `production_key_here`
- `ADMIN_PASSWORD` = `strong_password_here`
- (etc.)

---

## 🔄 Key Rotation Strategy

### When to Rotate Keys

**Immediately:**
- Before production deployment
- If keys are accidentally exposed
- If keys are committed to Git (even if removed later)
- If unauthorized access is suspected

**Periodically:**
- Every 90 days for production
- Every 6 months for development/testing

### How to Rotate

**Google Gemini:**
1. Go to: https://makersuite.google.com/app/apikey
2. Delete old key
3. Create new key
4. Update `.env` (local) or Secrets (cloud)

**Cohere:**
1. Go to: https://dashboard.cohere.com/api-keys
2. Revoke old key
3. Generate new key
4. Update `.env` (local) or Secrets (cloud)

---

## 📋 Pre-Deployment Checklist

Before deploying to production:

- [ ] Generate new Gemini API key (production)
- [ ] Generate new Cohere API key (production)
- [ ] Create strong admin password (12+ characters, mixed case, numbers, symbols)
- [ ] Verify `.env` is NOT in Git history
- [ ] Configure Secrets in deployment platform
- [ ] Test with production keys in staging environment
- [ ] Document key expiration dates
- [ ] Set calendar reminders for key rotation (90 days)

---

## 🚨 What to Do If Keys Are Exposed

If API keys are accidentally exposed (committed to Git, shared publicly, etc.):

1. **Immediately revoke** the exposed keys in provider dashboards
2. **Generate new keys** immediately
3. **Update** `.env` (local) or Secrets (cloud) with new keys
4. **Remove** exposed keys from Git history if committed:
   ```bash
   # Use git filter-repo or BFG Repo-Cleaner
   # Or contact repository admin to reset
   ```
5. **Notify** team members if applicable
6. **Review** access logs in provider dashboards for unauthorized usage

---

## 📊 Current Status Summary

| Item | Status | Notes |
|------|--------|-------|
| `.env` file created | ✅ Done | Contains testing keys |
| `.env` in `.gitignore` | ✅ Confirmed | Protected from Git |
| `.env.example` updated | ✅ Done | Template without real keys |
| Testing keys configured | ✅ Done | Gemini + Cohere |
| Production keys generated | ❌ Pending | Before deployment |
| Strong admin password | ❌ Pending | Before deployment |

---

## 👨‍💻 For Cursor (Development Phase)

The `.env` file is ready for use during implementation:

✅ **Available for testing:**
- Gemini API integration
- Cohere fallback mechanism
- Full RAG pipeline with real LLM responses
- Embedding generation and retrieval

⚠️ **Remember:**
- These are testing keys with free tier limits
- Gemini: 15 requests/minute
- Cohere: 1000 requests/month
- Monitor usage to avoid hitting limits during development

---

## 📞 Support Resources

**If you need help with:**

**Google Gemini:**
- Dashboard: https://makersuite.google.com/
- Documentation: https://ai.google.dev/docs
- Rate limits: https://ai.google.dev/pricing

**Cohere:**
- Dashboard: https://dashboard.cohere.com/
- Documentation: https://docs.cohere.com/
- Rate limits: https://cohere.com/pricing

---

**Document maintained by:** Project team  
**Last updated:** 2026-07-25  
**Next review:** Before production deployment
