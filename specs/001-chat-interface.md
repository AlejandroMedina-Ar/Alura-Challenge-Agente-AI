# Chat Interface Specification

**Specification ID:** SPEC-001

**Module:** User Interface

**Version:** 1.0

**Status:** Draft

---

# 1. Purpose

This document defines the complete graphical user interface (GUI) specification for the TechFlow Solutions Corporate Knowledge Agent.

Its objective is to provide a modern, intuitive and professional user experience inspired by contemporary AI applications such as ChatGPT, Claude, and Perplexity, while maintaining the simplicity and rapid development offered by Streamlit.

This specification defines:

- User Interface
- User Experience
- Visual Design
- Navigation
- Theme System
- Screen Layout
- Component Behaviour

Business logic is intentionally excluded from this document and is defined in other specifications.

---

# 2. Design Philosophy

The interface should immediately communicate that the application is an AI-powered assistant.

The design philosophy follows five principles.

## Simplicity

Every screen should focus on a single primary task.

Avoid visual clutter.

Avoid unnecessary controls.

---

## Familiarity

Users should immediately recognize the interface.

The application should feel familiar to users of:

- ChatGPT
- Claude
- Perplexity
- GitHub Copilot

---

## Productivity

The interface should reduce clicks whenever possible.

Frequently used actions must remain easily accessible.

---

## Readability

Typography, spacing and colors should prioritize long reading sessions.

---

## Professional Appearance

Although this project is intended for educational purposes, the final result should resemble a production SaaS application rather than a classroom exercise.

---

# 3. User Experience Goals

The interface should make the user feel that:

- the application is intelligent
- the application is fast
- the application is reliable
- the application is easy to use
- the application is professionally designed

The learning curve should be practically zero.

---

# 4. General Layout

The application follows Streamlit's native two-zone layout without custom HTML.

```
┌────────────────────────────────────────────────────────────────┐
│  Streamlit Menu (⋮)                              [Settings]    │
├────────────────┬───────────────────────────────────────────────┤
│                │                                               │
│  Sidebar       │         Main Chat Area                        │
│                │                                               │
│  🤖 TechFlow   │    [Chat messages displayed here]            │
│                │                                               │
│  Status:       │                                               │
│  ✓ Ready       │                                               │
│                │                                               │
│  Admin Panel   │                                               │
│  Knowledge     │                                               │
│  Library       │                                               │
│                │                                               │
└────────────────┴───────────────────────────────────────────────┘
```

**Key principles:**
- **No custom top bar** - Uses Streamlit's native hamburger menu (⋮)
- **Python-only** - No custom HTML, minimal CSS (only for dark/light themes)
- **Streamlit native components** - Leverages built-in sidebar and menu
- **Clean and balanced** - Chat area occupies most screen space

---

# 5. Streamlit Menu (⋮)

The application uses Streamlit's native hamburger menu for global settings and information.

**Menu contents should include:**
- Application info (version, about)
- Theme selector (accessible via Streamlit settings)
- Documentation links
- Current LLM model display (read-only info)
- Administrator status indicator

**Implementation:** Use Streamlit's built-in menu system - no custom implementation needed.

**Note:** Some items (like theme) are automatically included by Streamlit. Additional custom menu items can be added via `st.sidebar` or displayed as info in the sidebar itself.

---

# 6. Sidebar

The sidebar is the primary navigation and information hub, positioned on the left side of the screen.

## Top Section: Branding

```
┌─────────────────────┐
│  🤖 TechFlow Solutions     │
│  Corporate Agent    │
└─────────────────────┘
```

**Components:**
- Company/Product logo (emoji or small image)
- Application name
- Optional tagline

**Purpose:** Brand identity and application context

---

## System Status Section

Display key system information:

```
┌─────────────────────┐
│  📊 System Status   │
│                     │
│  ✓ Ready            │
│  📚 42 Documents    │
│  🧠 Gemini 2.0      │
│  🔄 Cohere Ready    │
└─────────────────────┘
```

**Status indicators:**
- System health (✓ Ready / ⚠ Warning / ❌ Error)
- Document count in Knowledge Library
- Active LLM provider (Gemini / Cohere)
- Fallback status

**Implementation:** Use `st.sidebar.metric()` or `st.sidebar.info()` for clean display

---

## Admin Access Section

```
┌─────────────────────┐
│  👤 Administrator   │
│                     │
│  🔐 Login          │
│  or                 │
│  📚 Knowledge      │
│  ⚙️  Settings       │
└─────────────────────┘
```

**If NOT authenticated:**
- Show "Admin Login" button

**If authenticated:**
- Show "Knowledge Library" access
- Show "Settings" access
- Show "Logout" button

---

## Navigation (if applicable)

For future multi-page support (out of scope for v1):
- Home / Chat
- Knowledge Library (admin only)
- Settings (admin only)

---

# 7. Theme Manager

The application supports light and dark visual themes using Streamlit's native theme system enhanced with custom CSS.

## Theme Implementation Strategy

**Streamlit Native Themes:**
- Light mode: Streamlit's default light theme
- Dark mode: Streamlit's default dark theme

**Custom CSS Enhancement:**
Two CSS files provide theme-specific styling:
- `assets/css/light.css` - Light mode customizations
- `assets/css/dark.css` - Dark mode customizations

**CSS applies:**
- Tokyo Night color palette for dark mode
- Professional light mode colors
- Consistent spacing and typography
- Chat message styling
- Sidebar enhancements

**Theme Selection:**
Users change themes via Streamlit's hamburger menu (⋮) → Settings → Theme

**No custom theme selector needed** - Streamlit handles theme switching natively.

**Implementation:**
```python
# Load appropriate CSS based on Streamlit's theme
def load_theme_css():
    # Detect current theme from Streamlit
    theme = st.get_option("theme.base")  # "light" or "dark"
    
    if theme == "dark":
        with open("assets/css/dark.css") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    else:
        with open("assets/css/light.css") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
```

---

## Default Theme

The application starts with **Dark mode** by default (Tokyo Night color scheme via custom CSS).

Users can switch to Light mode via Streamlit's settings menu at any time.

---

## Primary Theme: Tokyo Night (Dark)

---

## Theme Selector

Location

Top Navigation Bar

Behaviour

Selecting a theme immediately updates the application appearance.

The preference remains active during the current session using Streamlit Session State.

Future versions may persist the preference between sessions.

---

## Theme Requirements

Dark mode must be the default.

The transition between themes should be immediate.

The user should never need to reload the application.

---

# 7. Visual Identity

The interface should adopt the visual language of modern developer tools.

Inspiration

- VS Code
- Claude
- ChatGPT
- Perplexity
- GitHub Copilot

The design should communicate:

- professionalism
- modernity
- simplicity

---

## Primary Theme

Tokyo Night (Dark)

Primary Background

#1a1b26

Secondary Background

#24283b

Surface

#292e42

Primary Accent

#7aa2f7

Secondary Accent

#7dcfff

Success

#9ece6a

Warning

#e0af68

Error

#f7768e

Primary Text

#c0caf5

Secondary Text

#a9b1d6

Muted Text

#565f89

---

## Light Theme

Background

#ffffff

Cards

#f5f7fa

Surface

#ffffff

Accent

#4f7cff

Primary Text

#1f2937

Secondary Text

#4b5563

Borders

#d1d5db

---

# 8. Typography

The interface should use Streamlit default fonts whenever possible.

Typography hierarchy

Title

Large

Bold

Section

Medium

Semi-Bold

Body

Regular

Captions

Small

Muted

Code

Monospace

---

# 9. Sidebar

The sidebar provides secondary functionality.

The sidebar remains visible at all times.

It contains navigation, system information and administrator tools.

The chat itself should never appear inside the sidebar.

---

## Sidebar Structure

```
📚 Navigation

────────────────────────

💬 New Conversation

📜 Chat History

────────────────────────

📊 Knowledge Base

────────────────────────

🔒 Administrator

────────────────────────

ℹ System Status

────────────────────────

Version

Developer

GitHub
```

---

# 10. Navigation Section

Purpose

Allow quick navigation through the application.

Available actions

- Start New Conversation
- View Current Session History

Future versions may include saved conversations.

---

# 11. Knowledge Base Card

The sidebar should display a compact dashboard showing the current knowledge base status.

Displayed information

- Number of Documents
- Number of Indexed Chunks
- Embedding Model
- Vector Database
- Last Index Date

Example

```
Knowledge Base

Documents

28

Chunks

1,246

Embedding

intfloat/multilingual-e5-base

Database

ChromaDB

Last Index

2026-07-24
```

This information is read-only for regular users.

---

# 12. Main Chat Area

The Main Chat Area is the central component of the application.

It occupies approximately 75% of the available horizontal space and represents the primary workspace for end users.

The interface should remain clean and distraction-free.

Only information relevant to the current conversation should appear in this area.

---

# 13. Chat Window

The chat window is responsible for displaying the entire conversation between the user and the AI assistant.

Requirements:

- Scrollable conversation
- Automatic scroll to latest message
- Markdown rendering
- Code block support
- Tables
- Lists
- Hyperlinks
- Blockquotes
- Inline code
- Responsive layout

The chat should resemble modern conversational AI interfaces.

---

# 14. Welcome Screen

When no conversation exists, the application should display a Welcome Screen instead of an empty chat.

Example:

```
🤖

Welcome to TechFlow Solutions

Your intelligent corporate knowledge assistant.

Ask anything about your company documentation.

```

The Welcome Screen disappears after the first user message.

---

# 15. Suggested Questions

Below the Welcome Screen, display several clickable example questions.

Purpose:

Help first-time users understand what the assistant can answer.

Examples:

• What features are included in the Pro Plan?

• How do I reset my password?

• Where is the API documentation?

• How do I request a refund?

• Explain our onboarding process.

Selecting a question automatically sends it to the chat.

---

# 16. Conversation Flow

Each conversation follows this sequence:

```
User Question

↓

Loading Indicator

↓

Retriever

↓

LLM Response

↓

Display Sources

↓

Ready for Next Question
```

The transition between states should feel smooth and immediate.

---

# 17. User Messages

User messages appear aligned to the right.

Characteristics:

- Rounded corners
- Accent color
- Maximum readability
- Timestamp (optional)

Example

```
How do I upgrade my subscription?
```

---

# 18. Assistant Messages

Assistant messages appear aligned to the left.

Characteristics:

- AI avatar
- Markdown support
- Code rendering
- Lists
- Tables
- Hyperlinks

Responses should feel conversational while remaining professional.

---

# 19. Markdown Rendering

The assistant must correctly render Markdown.

Supported elements:

- Headings
- Bold
- Italic
- Bullet Lists
- Numbered Lists
- Tables
- Code Blocks
- Horizontal Rules
- Hyperlinks
- Inline Code
- Blockquotes

---

# 20. Code Blocks

If the retrieved documentation contains code examples, they should be displayed using syntax highlighting.

Supported languages include:

- Python
- JavaScript
- Java
- SQL
- JSON
- YAML
- HTML
- CSS
- Bash

Horizontal scrolling should be available when necessary.

---

# 21. Tables

Tables should remain readable.

Requirements:

- Borders
- Alternating row colors
- Horizontal scrolling on small screens

---

# 22. Hyperlinks

Hyperlinks should:

- Open in a new tab.
- Use the application accent color.
- Display hover feedback.

---

# 23. Sources Panel

Every answer generated by the AI should display the documents used as context.

Purpose:

Increase transparency and user trust.

Example

```
Sources

✓ pricing.pdf (Page 3)

✓ onboarding.pdf (Page 7)

✓ faq.md
```

If page information is unavailable, only display the filename.

---

# 24. Confidence Information

When available, the application may display retrieval confidence.

Example

```
Confidence

92%
```

This information is optional and primarily intended for future versions.

---

# 25. Chat Input Area

The message input is permanently located at the bottom of the interface.

Placeholder

```
Ask a question about your company documentation...
```

Requirements:

- Multi-line support
- Automatic height adjustment
- Clear placeholder
- Keyboard friendly

---

# 26. Keyboard Shortcuts

Supported shortcuts

Enter

Send Message

Shift + Enter

Insert New Line

Escape

Clear current input (optional)

---

# 27. Send Button

A Send button should always be available.

Example

```
🚀 Send
```

Requirements

- Disabled while processing.
- Enabled when text exists.
- Loading animation during generation.

---

# 28. Loading State

While the assistant generates an answer, display:

Spinner

Status message

Animated progress indicator

Example

```
🤖 Thinking...

Searching documentation...

Generating response...
```

The user should always know that the system is working.

---

# 29. Empty State

When no messages exist:

Display

- Logo
- Welcome message
- Suggested questions
- Short application description

Avoid empty white space.

---

# 30. Error State

Unexpected errors should never expose Python exceptions.

Instead display friendly messages.

Example

```
⚠ Something went wrong.

Please try again.

If the problem persists, contact the administrator.
```

---

# 31. No Results State

If the retriever finds no relevant information:

Display

```
I couldn't find enough information in the available documentation to answer that question.

Try asking differently or upload additional documentation.
```

The assistant should never fabricate information.

---

# 32. Streaming Responses

Responses should appear progressively whenever supported by the selected LLM.

Benefits

- Faster perceived performance.
- More natural interaction.
- Better user experience.

---

# 33. Conversation Persistence

Conversation history exists only during the current Streamlit session (session-based conversation memory).

Refreshing the browser clears the conversation.

Persistent chat history (saved chats across sessions) is intentionally excluded from v1.

---

# 34. Streaming Responses

The chat interface should stream LLM responses in real-time for improved user experience.

**Implementation Status: v1 - REQUIRED**

Streaming is **implemented** for both LLM providers as it is critical for chat UX:

**Gemini Streaming:**
```python
# Use streaming API
response_stream = model.generate_content(prompt, stream=True)
for chunk in response_stream:
    yield chunk.text
```

**Cohere Streaming:**
```python
# Use chat_stream method
response_stream = client.chat_stream(message=prompt)
for event in response_stream:
    if event.event_type == "text-generation":
        yield event.text
```

**Streamlit Integration:**

Display streaming responses using `st.write_stream()`:

```python
with st.chat_message("assistant"):
    response = st.write_stream(stream_llm_response(prompt))
```

**Fallback Behavior:**

If streaming fails (network issues, API errors):
1. Log warning: `logger.warning("Streaming failed, using non-streaming mode")`
2. Generate complete response
3. Display full response at once

**Benefits:**
- Lower perceived latency
- Better UX for long responses
- Maintains user engagement

---

# 34. Scroll Behaviour

The interface should automatically scroll to the newest message.

Users should never need to manually scroll after sending a question.

---

# 35. Message Styling

Spacing should remain generous.

Recommended spacing

16–24 px between messages.

Rounded corners

12–16 px.

Maximum content width

Approximately 900 px.

---

# 36. Icons

Use lightweight emoji or Material Symbols consistently.

Suggested icons

🤖 Assistant

👤 User

📄 Sources

⚠ Warning

❌ Error

✅ Success

📂 Documents

📊 Statistics

---

# 37. Animations

Animations should remain subtle.

Allowed

- Fade In
- Progress Bars
- Loading Spinner

Avoid

- Bounce
- Flash
- Heavy transitions
- Complex animations

---

# 38. Accessibility

The interface should support

- Keyboard navigation
- Screen readers where possible
- High contrast
- Readable font sizes
- Visible focus states

Accessibility should not compromise visual simplicity.

---

# 39. Responsive Behaviour

The interface should adapt correctly to:

Desktop (Primary)

Laptop

Tablet

On narrow screens, the sidebar may collapse automatically.

Mobile support is considered optional.

---

# 40. Administrator Panel

The Administrator Panel provides secure access to all knowledge base management functions.

Regular users should never see administrator tools.

The administrator panel remains collapsed until successful authentication.

---

# 41. Administrator Authentication

The administrator section is protected using a password defined through environment variables.

Authentication is intentionally lightweight.

Requirements

- Password input field
- Login button
- Friendly error messages
- Session-based authentication
- Logout button

The password must never be hardcoded.

---

# 42. Administrator Dashboard

After authentication the sidebar expands to display administration tools.

Example

```
Administrator

✅ Logged In

────────────────────────

📂 Upload Documents

🗑 Delete Documents

🔄 Rebuild Index

📊 Database Status

⚙ AI Settings

🚪 Logout
```

The dashboard should remain simple and uncluttered.

---

# 43. Upload Manager

Administrators may upload one or multiple documents simultaneously.

Requirements

- Multi-file upload
- Drag & Drop support
- File validation
- Upload progress
- Success notification
- Error notification

Supported formats

- PDF
- DOCX
- TXT
- Markdown
- CSV
- JSON
- HTML

Future versions may support additional formats.

---

# 44. Upload Workflow

The upload process follows the sequence below.

```
Select Files

↓

Validate Files

↓

Extract Text

↓

Chunk Documents

↓

Generate Embeddings

↓

Store in ChromaDB

↓

Update Knowledge Base

↓

Display Success
```

The workflow should execute automatically.

No manual indexing steps should be required.

---

# 45. Upload Progress

While processing documents, the application should display a progress card.

Example

```
📂 Processing Documents

pricing.pdf

████████████░░░░░░░░

62%

Generating Embeddings

Current File

3 of 8

Estimated Time

00:16
```

The user should always know the current progress.

---

# 46. Upload Result

After indexing finishes, display a summary.

Example

```
✅ Upload Completed

Files

8

Chunks

1,348

Embedding Model

intfloat/multilingual-e5-base

Vector Database

ChromaDB

Elapsed Time

21 seconds
```

The user should clearly understand that the knowledge base has been updated.

---

# 47. Delete Documents

Administrators should be able to remove documents already indexed.

Workflow

```
Select Document

↓

Confirmation Dialog

↓

Delete Chunks

↓

Update ChromaDB

↓

Refresh Statistics
```

Deletion must require confirmation.

Example

```
Delete selected document?

This action cannot be undone.

[Cancel]

[Delete]
```

---

# 48. Rebuild Knowledge Base

The administrator may rebuild the complete vector database.

Typical use cases

- New embedding model
- Corrupted index
- Large document updates

Display progress throughout the operation.

---

# 49. Knowledge Base Dashboard

The sidebar should always display current knowledge base statistics.

Example

```
Knowledge Base

──────────────────

📄 Documents

28

🧩 Chunks

1,264

🧠 Embeddings

intfloat/multilingual-e5-base

🧠 LLM

Gemini 2.0 Flash

💾 Database

ChromaDB

📅 Last Update

2026-07-24

🟢 Status

Ready
```

This information should refresh automatically whenever the knowledge base changes.

---

# 50. System Status Card

Display current system status.

Example

```
System Status

🟢 LLM Connected

🟢 ChromaDB Ready

🟢 Embeddings Ready

🟢 API Available
```

Failures should be clearly indicated.

Example

```
🔴 OpenRouter Offline
```

---

# 51. Notifications

Display non-intrusive notifications.

Success

✅ Documents uploaded.

✅ Index rebuilt.

✅ Login successful.

Warning

⚠ Unsupported document ignored.

⚠ Empty document skipped.

Error

❌ Upload failed.

❌ API unavailable.

❌ Invalid password.

Messages should remain concise and informative.

---

# 52. Footer

The sidebar footer should contain project information.

Example

```
────────────────────

TechFlow Solutions

Version 1.0

Developer : Oscar Alejandro Medina

Current date in 2026
```

---

# 53. Custom Styling

Although Streamlit provides default styling, this project should include custom CSS to establish a unique visual identity.

CSS should remain modular and easy to maintain.

Recommended structure

```
assets/

css/

tokyo_night.css

light_theme.css

components.css

layout.css
```

Each stylesheet should focus on a single responsibility.

---

# 54. Design Rules

The interface should follow these principles.

- Rounded corners
- Comfortable spacing
- Flat modern design
- Minimal shadows
- High contrast
- Consistent icons
- Smooth scrolling
- Clean typography
- No visual clutter

The interface should feel modern and professional, similar to contemporary AI chat applications.

---

# 55. Performance Requirements

The interface should remain responsive.

Target objectives

- Initial page load under 3 seconds
- Theme switch under 300 ms
- Message rendering under 100 ms
- Smooth scrolling
- No unnecessary reruns

Heavy operations should provide visual feedback.

---

# 56. Accessibility

The application should support

- Keyboard navigation
- Focus indicators
- High-contrast themes
- Readable typography
- Consistent spacing

Accessibility should be considered during all UI development.

---

# 57. Future Improvements

The architecture should allow future implementation of

- Conversation history
- User profiles
- Multiple administrators
- Dark theme customization
- Additional color themes
- Multi-language interface
- Mobile optimization
- Voice interaction
- Conversation export
- Document preview

These features are outside the scope of Version 1.

---

# 58. Acceptance Criteria

The Chat Interface specification will be considered complete when

- Users can interact naturally with the assistant.
- Administrator functions remain protected.
- Documents can be uploaded without leaving the page.
- Upload progress is visible.
- Sources appear with every response.
- Theme switching works correctly.
- Tokyo Night is the default theme.
- The interface remains responsive.
- System status is always visible.
- The application maintains a professional appearance.

---

# 59. Notes for AI Development Agents

The following implementation guidelines must be respected.

General

- Respect Architecture.md.
- Respect all project specifications.
- Avoid unnecessary dependencies.
- Keep code modular.
- Separate UI from business logic.

Frontend

- Use native Streamlit widgets whenever possible.
- Use CSS only for visual improvements.
- Avoid JavaScript unless absolutely necessary.
- Keep components reusable.

Backend

- Never access ChromaDB directly from UI code.
- Use service modules for business logic.
- Keep state management centralized.

Configuration

- Store secrets in environment variables.
- Avoid hardcoded values.
- Support future provider replacement.

Performance

- Minimize Streamlit reruns.
- Cache expensive operations when appropriate.
- Keep memory usage low.

Maintainability

- Write readable code.
- Use meaningful function names.
- Document non-obvious logic.
- Follow Python best practices.

---

# 60. Final Notes

This specification defines the complete graphical interface for Version 1 of the TechFlow Solutions Corporate Knowledge Agent.

Its purpose is to ensure a consistent, maintainable and professional implementation while preserving the simplicity.

All future UI modifications should remain compatible with the principles established in this document.
