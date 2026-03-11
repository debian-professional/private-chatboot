# Multi-LLM Chat Client – OpenAI, DeepSeek, Google Gemini, Hugging Face & GroqCloud

**Multi-LLM Chat Client** ist ein vollständig eigenständiger, lokal gehosteter Chat-Client mit Unterstützung für mehrere KI-Anbieter: OpenAI, DeepSeek, Google Gemini, Hugging Face und GroqCloud. Entwickelt mit Fokus auf **Sicherheit, Einfachheit und professionelle Nutzbarkeit**. Die Architektur kommt ohne exotische Frameworks aus und verwendet ausschliesslich bewährte Technologien: Apache als Webserver, Python CGI für serverseitige Logik und reines HTML/JavaScript/CSS auf der Client-Seite.

Wichtigste Highlights:
- **Multi-LLM-Unterstützung** – Wechsel zwischen OpenAI, DeepSeek, Google Gemini, Hugging Face und GroqCloud über einen Anbieter-Toggle im LLM-Einstellungs-Panel.
- **Multi-Datei-Upload** – Mehrere Dateien gleichzeitig auswählen und senden. Inhalte werden kombiniert und gemeinsam als Kontext gesendet.
- **Audio-Aufnahme via Mikrofon** – Audio direkt im Browser aufnehmen und an die KI senden. Unterstützt von Google Gemini (alle Modelle) und OpenAI (gpt-4o, gpt-4.1). Der Aufnahme-Button erscheint automatisch nur bei audio-fähigen Modellen.
- **Einzigartiges Kontextmanagement** – Einzelne Nachrichten zusammen mit allen nachfolgenden löschen. Der Chat bleibt konsistent, die Token-Nutzung wird dynamisch aktualisiert.
- **Maximale Sicherheit** – Der API-Key ist clientseitig nie sichtbar, Uploads werden via Magic-Byte-Prüfung gegen ausführbare Dateien geschützt, Sessions werden mit restriktiven Dateiberechtigungen gespeichert.
- **Keine exotischen Frameworks** – Alles basiert auf Apache, Python, Bash und reinem HTML/JS.
- **Professionelle Exportfunktionen** – PDF, Markdown, TXT, RTF für den gesamten Chat oder einzelne Nachrichten.
- **Mehrsprachige Unterstützung** – Vollständige UI-Übersetzung via externer `language.xml` (Englisch, Deutsch, Spanisch, erweiterbar).
- **Audio recording** – Built-in microphone button (MediaRecorder API) for direct voice input. Automatically visible only when an audio-capable model is active (all Gemini models, OpenAI gpt-4o and gpt-4.1). Audio is transmitted as base64 WebM/MP4 — no transcription, the model processes speech natively.
- **Zwischenablage-Integration** – Ctrl+V-Handler mit Dialog für Text, Bilder und Schutz gegen versehentliches Einfügen von Dateipfaden.
- **Streaming-Antworten** – KI-Antworten erscheinen Token für Token, genau wie bei ChatGPT oder Claude.
- **429-Rate-Limit-Handling** – Automatischer Wiederholungsversuch mit Countdown-Anzeige für Google Gemini Free Tier Limits.
- **Enthaltenes Tool** – Das Skript `repo2text.sh` exportiert das gesamte Repository als Textdatei, ideal für die Arbeit mit KI-Assistenten (wie diesem).

---

## Inhaltsverzeichnis

- [Übersicht](#übersicht)
- [Architektur](#architektur)
- [Einzigartiges Kontextmanagement](#einzigartiges-kontextmanagement)
- [Features im Detail](#features-im-detail)
  - [Chat-Interface](#chat-interface)
  - [Streaming-Antworten](#streaming-antworten)
  - [Zwischenablage-Handler (Ctrl+V)](#zwischenablage-handler-ctrlv)
  - [Datei-Upload mit Sicherheitsprüfung](#datei-upload-mit-sicherheitsprüfung)
  - [Umlaut-Platzhalter-System](#umlaut-platzhalter-system)
  - [DeepThink-Modus](#deepthink-modus)
  - [Modellerkennung & Fähigkeiten](#modellerkennung--fähigkeiten)
  - [Mehrsprachiges System](#mehrsprachiges-system)
  - [Einstellungen (Toggles statt Radio-Buttons)](#einstellungen-toggles-statt-radio-buttons)
  - [Session-Management](#session-management)
  - [Exportfunktionen](#exportfunktionen)
  - [Feedback-Buttons & Logging](#feedback-buttons--logging)
  - [Dynamische Kontext-Anzeige](#dynamische-kontext-anzeige)
  - [Datei-Card-Anzeige](#datei-card-anzeige)
  - [Audio-Aufnahme](#audio-aufnahme)
- [Das Hilfsskript `repo2text.sh`](#das-hilfsskript-repo2textsh)
- [Sicherheitsarchitektur im Detail](#sicherheitsarchitektur-im-detail)
- [Deployment & Verwendung](#deployment--verwendung)
  - [Voraussetzungen](#voraussetzungen)
  - [Installation](#installation)
  - [Konfiguration](#konfiguration)
  - [Deploy-Skripte](#deploy-skripte)
- [Projektstruktur](#projektstruktur)
- [Modell-Konfiguration](#modell-konfiguration)
- [Design-Manifest](#design-manifest)
- [Bekannte Einschränkungen & technische Hinweise](#bekannte-einschränkungen--technische-hinweise)
- [Abhängigkeiten](#abhängigkeiten)
- [Fazit / Warum dieses Projekt heraussticht](#fazit--warum-dieses-projekt-heraussticht)

---

## Übersicht

DeepSeek Chat is a **local web application** that communicates via the DeepSeek API (models `deepseek-chat` and `deepseek-reasoner`). Developed for a private server environment (Debian), it can run on any system with Apache and Python 3. The goal was to create a **secure, extensible, and user-friendly** chat client that operates without cloud dependencies and offers full control over data.

The project has grown continuously over several weeks of active development, adding features like streaming, session management, export functions, multilingual support, clipboard integration, and robust security measures — all without ever introducing external JavaScript frameworks.

---

## Architektur

The architecture is intentionally simple but well thought out:

### 1. Client
- Pure HTML/JavaScript/CSS, served via Apache.
- No build tools, no Node.js, no external libraries (except PDF.js for in-browser PDF text extraction).
- The entire client logic (message processing, UI updates, streaming reception, language switching, clipboard handling) is encapsulated in a single `index.html`.
- All UI texts are loaded from an external `language.xml` at startup — no hardcoded strings in the HTML.

### 2. Server
- **Apache** with CGI support (`mod_cgi`).
- **Python CGI scripts** under `/cgi-bin/` handle:
  - Communication with the OpenAI API (`openai-api.py`) — native OpenAI endpoint with streaming (Server-Sent Events)
  - Communication with the DeepSeek API (`deepseek-api.py`) — with streaming (Server-Sent Events)
  - Communication with the Google Gemini API (`google-api.py`) — converts OpenAI format to Gemini format
  - Communication with the Hugging Face Inference API (`hugging-api.py`) — OpenAI-compatible router endpoint
  - Communication with the GroqCloud API (`groq-api.py`) — OpenAI-compatible endpoint, hardware-accelerated inference (LPU)
  - Model discovery (`deepseek-models.py`) — queries `/v1/models` at startup
  - Session storage and retrieval (`save-session.py`, `load-session.py`, `delete-session.py`)
  - Exports in various formats (`export-pdf.py`, `export-markdown.py`, `export-txt.py`, `export-rtf.py`)
  - Feedback logging (`feedback-log.py`)
  - Log display (`get-log.py`)
- API keys are provided exclusively via Apache environment variables (`OPENAI_API_KEY`, `DEEPSEEK_API_KEY`, `GOOGLE_API_KEY`, `HF_API_KEY`, `GRQ_API_KEY` in `/etc/apache2/envvars`) — **never in client code**.
- A single `ScriptAlias /cgi-bin/ /var/www/deepseek-chat/cgi-bin/` covers all scripts — no Apache changes needed when adding new scripts.

### 3. Data Storage
- **Sessions** are stored as JSON files in `/var/www/deepseek-chat/sessions/` with `chmod 700`.
- **Logs** are written to `/var/www/deepseek-chat/cgi-bin/deepseek-chat.log` (without API key or session contents).
- **Settings** remain locally in the browser (`localStorage`) with version control.
- **Language data** is loaded from `language.xml` at page load via `fetch()`.

### 4. Helper Scripts
- `deploy.sh`, `sync-back.sh`, `install.sh`, `tag-release.sh` facilitate deployment between development and production directories.
- `repo2text.sh` exports the entire repository as a text file for AI assistants.

---

## Einzigartiges Kontextmanagement

One of the standout features is the ability to **delete individual messages along with all subsequent ones**. This goes far beyond the typical "delete last message" and allows flexible correction of the conversation history.

**Implementation**:
- Each message (user & AI) receives a unique `id` (format: `msg_N`) and is stored in an array `contextHistory.messages`.
- The `deleteMessage(msgId)` function determines the index of the message, truncates the array from `index` onwards, and removes all following elements from the DOM (including dividers).
- The token estimate (`updateContextEstimation()`) is immediately recalculated, as is the percentage context utilization in the header.
- The modified session is then automatically saved (`saveSession()`).

**Why is this unique?**
Many chat clients only allow deletion of the last message or no history manipulation at all. Here, the user can **define any point in the conversation as a new starting point** — perfect for testing, corrections, or cleaning up the context window without losing the entire chat.

**Regenerate function**: In addition to deletion, each AI response has a "Regenerate" button that deletes the old response and automatically generates a new one based on the same user message — using the full conversation context up to that point.

---

## Features im Detail

### Chat-Interface

- **Dark Mode** (fixed, no option) — easy on the eyes, professional appearance.
  - Background: `#121212`, text: `#f0f0f0`, accent: `#0056b3`
- **Server header** shows server name, internal IP address, dynamic context utilization, and detected model names.
- **Message containers** with hover buttons (feedback, export, delete).
- **Textarea** expands on focus from 40px to 120px with smooth CSS animation — Enter sends, Shift+Enter creates a new line.
- All buttons follow a strict **pill-style** design (border-radius: 20px, height: 36px) — no square buttons anywhere.
- User messages appear in blue (`#4dabf7`), AI responses in white on dark background.
- Automatic line break preservation (`white-space: pre-wrap`) for all message content.
- Automatic scrolling to the latest message during and after streaming.

### Streaming-Antworten

AI responses are received and displayed **token by token** using Server-Sent Events (SSE):

- `deepseek-api.py` sends requests to DeepSeek with `stream: True` and forwards the event stream directly.
- `index.html` reads the stream via `ReadableStream` API and `TextDecoder`.
- Each received token is appended to the message element in real time.
- The psychological effect is significant: the first tokens appear within ~0.3 seconds instead of waiting 8+ seconds for a complete response.
- Both `sendMessage()` and `handleRegenerate()` use identical streaming logic.
- Auto-scroll remains active during streaming.

**Technical headers** set by `deepseek-api.py` for correct streaming:
```
Content-Type: text/event-stream
X-Accel-Buffering: no
Cache-Control: no-cache
```

### OpenAI-Integration

The client supports OpenAI as the first AI provider (shown at the top of the LLM selection) via `openai-api.py`:

- **Architecture**: Uses the native OpenAI Chat Completions endpoint — no format conversion required. The SSE stream is forwarded directly.
- **Endpoint**: `https://api.openai.com/v1/chat/completions`
- **API key**: `OPENAI_API_KEY` in `/etc/apache2/envvars` — never exposed to the client.
- **Free Tier**: `gpt-4o-mini`, `gpt-5-mini`.
- **Paid Tier**: `gpt-5.4`, `gpt-5.2-chat-latest`, `gpt-4o`, `gpt-4.1`, `gpt-4o-mini`.
- The model dropdown in LLM Settings updates automatically based on the selected tier.
- **Audio input**: `gpt-4o` and `gpt-4.1` support direct microphone recordings. When either model is active, the audio recording button becomes visible. Audio is sent as `input_audio` in OpenAI format.
- The DeepThink button and DeepThink indicator are hidden when OpenAI is active.
- System prompt identifies the active model: *"You are [model], an AI assistant made by OpenAI."*

### Google Gemini-Integration

The client supports Google Gemini as a second AI provider via `google-api.py`:

- **Architecture**: The CGI script converts the OpenAI-compatible message format used internally into the Gemini-specific `contents` format, sends the request to the Gemini `streamGenerateContent` endpoint, and converts the response back into the OpenAI SSE format expected by `index.html`.
- **API key**: `GOOGLE_API_KEY` in `/etc/apache2/envvars` — never exposed to the client.
- **Free Tier** (default): `gemini-2.5-flash` — 5 requests per minute, 20 requests per day.
- **Paid Tier**: `gemini-2.5-flash`, `gemini-2.5-pro`, `gemini-1.5-pro`, `gemini-2.0-flash`.
- The model dropdown in LLM Settings updates automatically based on the selected tier.
- **Audio input**: All Gemini models support direct microphone recordings. The audio recording button is always visible when Google Gemini is the active provider. Audio is sent as `inline_data` in Gemini's native format.
- The DeepThink button and DeepThink indicator are hidden when Google Gemini is active.

### Hugging Face-Integration

The client supports Hugging Face Inference Providers as a third AI provider via `hugging-api.py`:

- **Architecture**: Uses the OpenAI-compatible Hugging Face router endpoint — no format conversion required. The SSE stream is forwarded directly.
- **Endpoint**: `https://router.huggingface.co/v1/chat/completions` — the router selects the fastest available provider automatically.
- **API key**: `HF_API_KEY` in `/etc/apache2/envvars` — a Write token from huggingface.co/settings/tokens with "Make calls to Inference Providers" permission.
- **Free Tier**: `Qwen/Qwen2.5-72B-Instruct`, `mistralai/Mistral-7B-Instruct-v0.3`, `microsoft/Phi-3.5-mini-instruct`.
- **Paid Tier**: `meta-llama/Meta-Llama-3.1-70B-Instruct`, `meta-llama/Meta-Llama-3.1-405B-Instruct`, `Qwen/Qwen2.5-72B-Instruct`, `mistralai/Mixtral-8x7B-Instruct-v0.1`.
- The model dropdown updates automatically based on the selected tier.
- The DeepThink button and DeepThink indicator are hidden when Hugging Face is active.


### GroqCloud-Integration

The client supports GroqCloud as a fourth AI provider via `groq-api.py`:

- **Architecture**: Uses the OpenAI-compatible GroqCloud endpoint — no format conversion required. The SSE stream is forwarded directly.
- **Endpoint**: `https://api.groq.com/openai/v1/chat/completions`
- **API key**: `GRQ_API_KEY` in `/etc/apache2/envvars`.
- **Note**: A `User-Agent` header is required to bypass Cloudflare protection (error code 1010 without it).
- **Free & Paid Tier**: `llama-3.3-70b-versatile`, `llama-3.1-8b-instant`, `mixtral-8x7b-32768`, `gemma2-9b-it`.
- The model dropdown updates automatically based on the selected tier.
- The DeepThink button and DeepThink indicator are hidden when GroqCloud is active.
- All models run on GroqCloud's LPU (Language Processing Unit) hardware for very low latency.

### LLM-Einstellungs-Panel

A dedicated **LLM Settings** panel (separate from the main Settings panel) keeps provider-specific options out of the main UI:

- **Provider selection**: Toggle between OpenAI, DeepSeek, Google Gemini, Hugging Face, and GroqCloud — only one active at a time.
- **OpenAI options**: Free / Paid plan selection with automatic model list update.
- **DeepSeek options**: Default mode (Normal Chat / DeepThink), Privacy toggle (X-No-Training header).
- **Google options**: Free / Paid plan selection with automatic model list update.
- **Hugging Face options**: Free / Paid plan selection with automatic model list update.
- **GroqCloud options**: Free / Paid plan selection with automatic model list update.
- **Model dropdown**: Always visible, content updates automatically based on the active provider and plan.
- All settings are saved to `localStorage` and persist after page reload.

### 429-Rate-Limit-Handling

The Google Gemini Free Tier enforces strict rate limits (5 RPM, 20 RPD). The client handles these gracefully:

- On a 429 response, the client automatically retries up to **3 times** with **15-second intervals**.
- During the wait, a countdown is displayed directly in the chat: *"Rate limit reached – waiting 15 seconds and retrying... (Attempt 1/3)"*
- After 3 failed attempts, a final error message is shown.
- Verbose error details are written to the server log for diagnosis.
- The retry logic distinguishes between temporary RPM limits (retryable) and exhausted daily quota (not retryable).

### Zwischenablage-Handler (Ctrl+V)

A sophisticated clipboard handler intercepts paste events and responds intelligently based on content type:

**Text content** → Paste dialog appears with two options:
- "Insert at cursor position" — inserts the text directly into the input field at the cursor
- "Attach as file" — treats the clipboard text as `clipboard.txt` and attaches it as a file to the next message

**Image content** → A thumbnail preview box appears above the input field with the image, its size in KB, and a remove button. The image is ready to be sent with the next message (if the model supports images).

**File paths from file manager (XFCE/Thunar, KDE/Dolphin)** → These are blocked and an alert is shown:
> "Files copied in the file manager cannot be read by the browser. Please use the Upload button instead."

**Technical background**: On Linux/X11/Firefox, `e.preventDefault()` does not reliably block paste events. The solution is to allow the paste, then immediately check the input field content via `setTimeout(0)` and clear it if file paths are detected. Detection logic: 2 or more lines where every line starts with `/` or `file://`. A `requestAnimationFrame` call ensures the input field is visually cleared before the alert dialog appears.

### Datei-Upload mit Sicherheitsprüfung

- Accepted formats: `.txt`, `.pdf`, `.doc`, `.docx`, `.jpg`, `.jpeg`, `.png`, `.csv`, `.xlsx`, `.pptx`
- Processable formats (content extraction): `.txt`, `.pdf`
- Other accepted formats: attached as binary context (without text extraction)
- Maximum file size: **10 MB**
- Maximum extracted content: **250,000 characters** (enough for large text files and repository exports)

**Magic byte inspection** (first 20 bytes) detects and blocks executable files regardless of their filename extension:

| Platform | Format | Signature |
|----------|--------|-----------|
| Windows 32/64 bit | PE/MZ Executable | `4D 5A` |
| Linux 32 bit | ELF32 | `7F 45 4C 46 01` |
| Linux 64 bit | ELF64 | `7F 45 4C 46 02` |
| ARM 32 bit | ELF32 ARM | `7F 45 4C 46 01 01 01 00 ... 02 00 28 00` |
| ARM 64 bit | ELF64 AArch64 | `7F 45 4C 46 02 01 01 00 ... 02 00 B7 00` |
| macOS 32 bit | Mach-O | `CE FA ED FE` |
| macOS 64 bit | Mach-O | `CF FA ED FE` |
| macOS Universal | Fat Binary | `CA FE BA BE` |
| macOS/iOS ARM 32 | Big Endian | `FE ED FA CE` |
| macOS/iOS ARM 64 | Big Endian | `FE ED FA CF` |
| Linux/macOS | Shell Script | `23 21` (#!) |
| Python | Bytecode (.pyc) | `55 0D 0D 0A` |

**PDF extraction**: Uses PDF.js 3.11.174 loaded from CDN with automatic fallback to a secondary CDN. Progress is displayed page by page. Extraction timeout: 30 seconds.

**Uploaded files are displayed as file cards** in the user message (see [File Card Display](#file-card-display)).

### Umlaut-Platzhalter-System

A unique solution for a fundamental problem with the DeepSeek API and German text:

**Problem**: DeepSeek internally replaces German umlauts in file content with ASCII equivalents (e.g. `Ä → AeNDERUNG`, `Ü → MUeSSEN`). This behavior cannot be suppressed via system prompts or API parameters.

**Solution**: Before sending file content to DeepSeek, umlauts are replaced with unique placeholders. DeepSeek returns these placeholders unchanged. JavaScript then replaces them back to real umlauts after receiving the response.

| Original | Placeholder |
|----------|-------------|
| `ä` | `[[AE]]` |
| `ö` | `[[OE]]` |
| `ü` | `[[UE]]` |
| `ß` | `[[SS]]` |
| `Ä` | `[[CAE]]` |
| `Ö` | `[[COE]]` |
| `Ü` | `[[CUE]]` |

**Important implementation detail**: The functions `encodeUmlautsForAI()` and `decodeUmlautsFromAI()` use **exclusively Unicode escape sequences** (`\u00e4` instead of `ä`) and `split/join` instead of regex — this is critical to avoid corruption when files are transferred via Git.

The decode runs **both during streaming** (token by token) and after the complete response is received.

This system is **only applied to file content**, not to regular user messages or system prompts.

### DeepThink-Modus

- Switchable via a dedicated button (pill-mode style) in the second button row.
- In DeepThink mode, the `deepseek-reasoner` model is used (real chain-of-thought reasoning).
- The button visually changes: dark/inactive (`#2d2d2d`) → active blue (`#1e3a5f` background, `#4dabf7` border and text).
- An indicator bar appears below the buttons showing "DeepThink Mode active: In-depth analysis in progress".
- Context limits and output token limits are automatically adjusted (see [Model Configuration](#model-configuration)).
- The mode is recorded with each message and displayed in exports.
- The default mode (Chat or DeepThink) can be set in Settings and is persisted in `localStorage`.

### Modellerkennung & Fähigkeiten

At startup, the client queries `/cgi-bin/deepseek-models.py` which in turn calls the DeepSeek `/v1/models` endpoint:

- Detected model IDs are displayed in the server header: `Model: deepseek-chat, deepseek-reasoner`
- A `MODEL_CAPABILITIES` map defines which models support images:
  ```javascript
  const MODEL_CAPABILITIES = {
      'deepseek-chat':     { images: false, text: true },
      'deepseek-reasoner': { images: false, text: true },
      'deepseek-v4':       { images: true,  text: true },  // ready for future models
      'default':           { images: false, text: true },
  };
  ```
- If an image is pasted via clipboard or a `.jpg`/`.png` file is uploaded, and the current model does not support images, an alert blocks the operation.
- This architecture is **forward-compatible**: when DeepSeek V4 with image support is released, it will automatically work without code changes.

### Mehrsprachiges System

The UI supports multiple languages loaded from an external `language.xml` file:

**Currently included languages**:
- English (`en`) — default
- German (`de`) — with formal/informal address form (Sie/Du)
- Spanish (`es`) — with formal/informal address form (Usted/Tú)
- Custom slot (`custom`) — can be activated via `visible="true"` in `language.xml`

**How it works**:
- All UI texts are referenced by numeric IDs (e.g. `t(205)` = Send button label).
- `loadLanguage()` fetches and parses `language.xml` at page load.
- `t(id)` returns the text for the current language, falling back to English if not found.
- `tf(id, ...args)` supports placeholder substitution (`{0}`, `{1}`, ...).
- `tform(idFormal, idInformal)` returns the appropriate text based on the selected address form.
- Language switching is immediate without page reload.
- The selected language is persisted in `localStorage`.

**Address form system (German/Spanish)**:
- Languages can declare `has_address_form="true"` in `language.xml`.
- For such languages, the Settings panel shows an "Address Form" group (Formal/Informal).
- The selected form affects: system prompt (forces consistent AI responses), input placeholder, all settings descriptions.
- English has no address form distinction.

**System prompt** is built dynamically based on language, address form, and mode:
- Base prompt (text IDs 29/30 for formal/informal)
- DeepThink addition (text IDs 31/32)
- A strict instruction for file display is always appended in English to ensure consistent behavior regardless of UI language.

### Einstellungen (Toggles statt Radio-Buttons)

All settings use **toggle switches** (sliding left-to-right), never radio buttons or checkboxes:

| Group | Setting | Toggle Color |
|-------|---------|-------------|
| Language | EN / DE / ES / Custom | Green (personal preference) |
| Address Form | Formal / Informal | Green (personal preference) |
| Default Mode | Normal Chat / DeepThink | Blue (technical mode) |
| Privacy | Do not use data for training | Green |

**Toggle behavior**:
- Within a group, toggles behave like radio buttons: activating one deactivates the others.
- Clicking anywhere on the `setting-item` row activates that toggle (not just the toggle element itself).
- Visual feedback: active items get a colored background (`#1a2e1a` green or `#1e3a5f` blue).

**Privacy toggle**: Sets the header `X-No-Training: true` in API requests (supported by DeepSeek's opt-out mechanism).

**Settings persistence**: All settings are stored in `localStorage` under key `deepseekSettings`. Current `SETTINGS_VERSION: 1.3`. The `migrateSettings()` function provides backward compatibility with older stored settings (e.g. the removed "search" mode is automatically migrated to "chat").

### Session-Management

Each conversation is automatically managed as a named session:

- **Session ID format**: `YYYY-MM-DD_HHMMSS_random` (e.g. `2026-02-16_143045_abc123`) — generated client-side, validated server-side.
- **Automatic saving**: After every message pair (user + AI), the complete `contextHistory.messages` array is saved to the server as a JSON file.
- **Session file format**: `{sessionId}.json` in `/var/www/deepseek-chat/sessions/`, `chmod 600`.
- **Load chat history modal**: Shows all saved sessions with ID, date, message preview, and message count. Each session has [Load] (green) and [Delete] (red) buttons.
- **Loading behavior**: When loading a session, the current chat is automatically saved first, then the selected session is restored with full message history and UI reconstruction.
- **Session deletion**: The JSON file is deleted from the server immediately.

**CGI scripts**:
- `save-session.py` — POST: receives `{sessionId, messages}`, validates ID format, writes JSON
- `load-session.py` — GET: returns list with previews; GET with `?id=`: returns full session data
- `delete-session.py` — DELETE: removes session file

### Exportfunktionen

**Global export** (dropdown button in main row):

| Format | Generation | Contains |
|--------|-----------|---------|
| PDF | Server-side (ReportLab) | Header, statistics, table of contents, full chat |
| Markdown | Server-side | Identical structure to PDF, with Markdown anchors |
| TXT | Server-side | Plain text with separators |
| RTF | Server-side | RTF format, umlauts as RTF codes (no external library) |

**Per-message export** (hover button on each message):

| Format | Generation |
|--------|-----------|
| TXT | Client-side (JavaScript Blob, no server roundtrip) |
| Markdown | Client-side |
| RTF | Client-side |
| PDF | Server-side (single message sent to `export-pdf.py`) |

**Export content** (PDF/Markdown):
- Header with server name, IP, export date, language/address form settings
- Statistics section: message count, modes used, files attached, estimated tokens, duration
- Table of contents with all messages
- Full chat history with timestamps and mode indicators
- Color coding by message role and mode

**PDF technical note**: Binary PDF data is written exclusively via `sys.stdout.buffer` with HTTP headers encoded as bytes — avoiding the "Bad header" error that occurs when mixing `print()` (text mode) with binary output.

### Feedback-Buttons & Logging

Four buttons appear on hover for each AI response (left side, bottom):

- **Copy** — Copies message text to clipboard; shows "Copied!" for 2 seconds, then resets.
- **Like** — Marks the response positively (blue highlight); sends a LIKE entry to the server log. Clicking again removes the like.
- **Dislike** — Marks the response negatively (red highlight); sends a DISLIKE entry. Like and Dislike are mutually exclusive.
- **Regenerate** — Removes the current AI response from context and DOM, then calls the API again with the same user message and full preceding history.

**Server-side log format** (`deepseek-chat.log`):
```
2026-02-17 17:30:00 | 192.168.1.x | FEEDBACK | LIKE | msg_5 | "First 60 chars of message..."
2026-02-17 17:30:00 | 192.168.1.x | POST | /cgi-bin/deepseek-api.py | 200
```
**Never logged**: API keys, session contents, or message text beyond the 60-character feedback preview.

### Dynamische Kontext-Anzeige

The server header shows four lines of information:
1. Server name (in blue, `#4dabf7`)
2. `IP: xxx.xxx.xxx.xxx`
3. `Context: XX% (model-name)`
4. `Model: deepseek-chat, deepseek-reasoner`

**Context utilization calculation**:
- Estimated tokens = total characters in recent messages × `TOKENS_PER_CHAR` (0.25)
- Only the last N messages are counted (N = `maxContextMessages` from `MODEL_CONFIG`)
- System prompt tokens are added separately
- Percentage = estimated tokens / `maxContextTokens` × 100

**Warning system**: Above 90%, the context line turns red and blinks (CSS animation, opacity 0 → 1, 1 second cycle) — a highly visible warning that the context window is nearly full.

The display updates automatically with: every sent message, every deleted message, every model switch.

### Datei-Card-Anzeige

When a file is uploaded or clipboard text is attached, the user message displays a **file card** — a compact visual element similar to Claude or ChatGPT:

```
┌─────────────────────────────────────┐
│  [PDF]  │  filename.pdf             │
│  icon   │  PDF Document             │
└─────────────────────────────────────┘
```

- Shows file type badge (PDF, TXT, XLSX, etc.) derived from the file extension
- Shows truncated filename (max 30 characters with `...`)
- Applies to: real file uploads via the Upload button, clipboard text attached as file (`clipboard.txt`), all other accepted formats, and audio recordings
- Audio-Aufnahmen zeigen das Badge `AUDIO` mit dem lokalisierten Label (z.B. „Audioaufnahme")

### Multi-Datei-Upload

Der Upload-Button unterstützt die Auswahl von **mehreren Dateien gleichzeitig**:

- Alle ausgewählten Dateien werden einzeln validiert (Formatprüfung, Magic-Byte-Prüfung, Bild-Fähigkeitsprüfung).
- Textextrahierbare Dateien (`.txt`, `.pdf`) werden der Reihe nach verarbeitet; ihre Inhalte werden mit einem `---`-Trennzeichen und einem `[dateiname]`-Header kombiniert.
- Die Datei-Info-Leiste zeigt alle Dateien mit ` | ` getrennt in einer einzigen Zeile.
- Eine Datei-Card wird pro Datei in der Benutzernachricht angezeigt.
- Accepted formats: `.txt`, `.pdf`, `.doc`, `.docx`, `.jpg`, `.jpeg`, `.png`, `.csv`, `.xlsx`, `.pptx`

### Audio-Aufnahme

The client includes a built-in **microphone recording button** that enables direct voice input to audio-capable models:

- **Button**: `audioButton` — pill-mode style, positioned in button row 2 next to the DeepThink button.
- **Visibility**: The button is only shown when the currently selected model supports audio input. It is hidden automatically when a non-audio model is active. This is controlled by `updateAudioButtonVisibility()` which is called on every model change.
- **Audio-capable models** (`AUDIO_CAPABLE_MODELS` constant):
  - **Google Gemini**: `gemini-2.5-flash`, `gemini-2.5-pro`, `gemini-1.5-pro`, `gemini-2.0-flash`
  - **OpenAI**: `gpt-4o`, `gpt-4.1`
- **Recording flow**: `getUserMedia()` → `MediaRecorder` API → chunked recording → `Blob` assembled on stop → base64-encoded.
- **MIME type**: `audio/webm` (Chrome/Firefox) or `audio/mp4` (Safari) — auto-detected at runtime.
- **After recording**: The audio data is shown in the `fileInfo` box with an AUDIO badge card. The label is pulled from `language.xml` (`t(250)` — "Audio recording" in all four languages).
- **Sending**: `audio_data` (base64 string) and `audio_mime_type` are included in the JSON request body alongside the text message. The `hasFile` flag is **not** set for audio — no file-processing system prompt is injected.
- **Mutual exclusivity**: File upload and audio recording are mutually exclusive. Starting a recording clears any pending file attachment and vice versa.
- **Backend — Google (`google-api.py`)**: Audio is appended to the last user message as an `inline_data` block in Gemini's native format. The model receives and processes the audio directly.
- **Backend — OpenAI (`openai-api.py`)**: Audio is appended to the last user message as an `input_audio` block in OpenAI's format (`format: webm` or `mp4`).
- **Maintenance rule** (documented in manifest): Whenever an integrated LLM provider adds or removes audio support for a model, `AUDIO_CAPABLE_MODELS` in `index.html` **must** be updated immediately.

**Language IDs added** (all four languages):

| ID | Content |
|----|---------|
| 247 | Record Audio / Audio aufnehmen / Grabar audio |
| 248 | Stop |
| 249 | Audio recorded / Audio aufgenommen / Audio grabado |
| 250 | Audio recording / Audioaufnahme / Grabación de audio |


---


### API-Proxy-Infoblock (ab 08.03.2026)

Each of the five CGI proxy scripts (`openai-api.py`, `deepseek-api.py`, `google-api.py`, `hugging-api.py`, `groq-api.py`) contains a structured documentation header directly after the encoding declaration:

- **Import date** — when the file was last updated
- **Model version** — version of each supported model/sub-model
- **Context window** — input and output token limits per model
- **Capabilities** — Text only / Text + Images + Audio + Video
- **Free/Paid assignment** — for providers with tier distinction
- **Source link** — official API documentation

This ensures that model information is always traceable directly in the source code without consulting external documentation.

## Das Hilfsskript `repo2text.sh`

This Bash script was specifically developed to **export the entire source code of a GitHub repository as a single text file** — ideal for passing the complete project context to an AI assistant.

**How it works**:
- Clones the repository with `git clone --depth 1`.
- Analyzes all text files (MIME type + `grep -Iq .`) and writes them with separators into an output file.
- Explicitly respects `.gitignore` and `.gitattributes`.
- Supports TXT, JSON, and Markdown output formats.
- Creates a ZIP archive of the export file.
- Includes metadata: commit hash, branch, timestamp.

**Special options**:
- `--flat`: Use only filenames without paths.
- `-o, --only PATH`: Export only a specific subdirectory.
- `-md5, --md5`: Compute and include MD5 checksum for each file.
- Intelligent detection of the remote URL when run inside a Git repository.
- Both `md5sum` (Linux) and `md5` (macOS) are supported.

**Examples**:

```bash
# Simple export (interactive URL prompt)
./repo2text.sh

# Export with URL as Markdown
./repo2text.sh -f md https://github.com/debian-professional/private-chatboot.git

# Export only the 'shell-scipts' directory with flat structure
./repo2text.sh --flat -o shell-scipts https://github.com/debian-professional/private-chatboot.git

# Export with MD5 checksums
./repo2text.sh -md5 https://github.com/debian-professional/private-chatboot.git
```

**Why is this useful?**
- Enables complete project documentation in a single file.
- Perfect for inserting entire codebases into AI chats.
- The MD5 option helps verify file integrity after export.

> `repo2text` is also available as a standalone project: [github.com/debian-professional/repo2text](https://github.com/debian-professional/repo2text)

---

## Sicherheitsarchitektur im Detail

Security was the top priority throughout this project. Here are all key measures:

### 1. API-Key — Nie dem Client gegenüber exponiert
- The key is held **exclusively** in the Apache environment variable `DEEPSEEK_API_KEY` (set in `/etc/apache2/envvars`).
- `deepseek-api.py` retrieves it via `os.environ.get('DEEPSEEK_API_KEY')`.
- The client communicates only with `/cgi-bin/deepseek-api.py` (local proxy) — never directly with the DeepSeek API.
- Even in the event of an XSS attack, the key could not be read from the page.

### 2. Magic-Byte-Prüfung gegen ausführbare Dateien
- Before reading any uploaded file, the first 20 bytes are checked against a comprehensive signature database (see [File Upload with Security Check](#file-upload-with-security-check)).
- If a signature matches, the upload is blocked with a detailed error message showing the detected platform and format.
- This protection works even if malicious files are renamed (e.g. `virus.exe` → `invoice.pdf`).

### 3. Sichere Session-Speicherung
- Sessions directory: `/var/www/deepseek-chat/sessions/` — `chmod 700`
- Each session file: `chmod 600`
- Session ID format is validated server-side — no path traversal possible.

### 4. Logging ohne sensible Daten
- Log contains: timestamps, IP addresses, HTTP methods, paths, status codes, error messages.
- **Never logged**: API keys, session contents, message text (beyond 60-char feedback previews).
- OPTIONS requests are filtered out to prevent log flooding.

### 5. Keine direkte Client-API-Kommunikation
- All security-critical operations occur server-side via Python CGI.
- The client has no knowledge of API credentials, server paths, or session storage locations.

### 6. Input-Validierung
- File formats validated both by extension and by magic bytes.
- Session IDs validated against expected format regex server-side.
- Clipboard paste filtered to block file paths before they reach the API.

### 7. Transportsicherheit
- HTTPS enforced via Apache SSL configuration (`deepseek-chat-ssl.conf`).
- HTTP configuration (`deepseek-chat.conf`) is disabled via `a2dissite`.

---

## Deployment & Verwendung

### Voraussetzungen

- Debian-based system (or any Linux with Apache, Python 3, Bash)
- Apache with CGI module (`a2enmod cgi`) and SSL (`a2enmod ssl`)
- Python 3 with packages: `reportlab`
- For `repo2text.sh`: `jq`, `pv`, `zip`, `git`
- A valid DeepSeek API key from [platform.deepseek.com](https://platform.deepseek.com)

### Installation

**1. Clone the repository** (as user `source`):
```bash
git clone https://github.com/debian-professional/private-chatboot.git /home/source/private-chatboot
```

**2. Configure the API key**:
```bash
# Add to /etc/apache2/envvars:
export DEEPSEEK_API_KEY="your-deepseek-api-key-here"
```

**3. Enable Apache configuration**:
```bash
a2ensite deepseek-chat-ssl.conf
a2dissite deepseek-chat.conf   # disable plain HTTP config
systemctl restart apache2
```

**4. Create required directories**:
```bash
mkdir -p /var/www/deepseek-chat/sessions
chown www-data:www-data /var/www/deepseek-chat/sessions
chmod 700 /var/www/deepseek-chat/sessions
```

**5. Run the deploy script** (as root):
```bash
./deploy.sh source
```

**6. Install helper scripts**:
```bash
./install.sh   # as root — copies deploy.sh and sync-back.sh to production directory
```

### Konfiguration

**Model configuration** (`MODEL_CONFIG` in `index.html`):
```javascript
const MODEL_CONFIG = {
    'deepseek-chat':     { maxContextTokens: 100000,  maxOutputTokens: 8192,  maxContextMessages: 50  },
    'deepseek-reasoner': { maxContextTokens: 65000,   maxOutputTokens: 32768, maxContextMessages: 30  },
    'gemini-2.5-flash':  { maxContextTokens: 1048576, maxOutputTokens: 8192,  maxContextMessages: 100 },
    'gemini-2.5-pro':    { maxContextTokens: 1048576, maxOutputTokens: 65536, maxContextMessages: 100 },
    'gemini-1.5-pro':    { maxContextTokens: 2097152, maxOutputTokens: 8192,  maxContextMessages: 100 },
    'gemini-2.0-flash':  { maxContextTokens: 1048576, maxOutputTokens: 8192,  maxContextMessages: 100 },
    'Qwen/Qwen2.5-72B-Instruct':              { maxContextTokens: 128000, maxOutputTokens: 8192, maxContextMessages: 80 },
    'mistralai/Mistral-7B-Instruct-v0.3':     { maxContextTokens: 32768,  maxOutputTokens: 4096, maxContextMessages: 40 },
    'microsoft/Phi-3.5-mini-instruct':        { maxContextTokens: 128000, maxOutputTokens: 4096, maxContextMessages: 60 },
    'meta-llama/Meta-Llama-3.1-70B-Instruct': { maxContextTokens: 128000, maxOutputTokens: 8192, maxContextMessages: 80 },
    'meta-llama/Meta-Llama-3.1-405B-Instruct':{ maxContextTokens: 128000, maxOutputTokens: 8192, maxContextMessages: 80 },
    'mistralai/Mixtral-8x7B-Instruct-v0.1':   { maxContextTokens: 32768,  maxOutputTokens: 4096, maxContextMessages: 40 },
    // GroqCloud
    'llama-3.3-70b-versatile': { maxContextTokens: 128000, maxOutputTokens: 8192,  maxContextMessages: 80 },
    'llama-3.1-8b-instant':    { maxContextTokens: 131072, maxOutputTokens: 8192,  maxContextMessages: 80 },
    'mixtral-8x7b-32768':      { maxContextTokens: 32768,  maxOutputTokens: 32768, maxContextMessages: 40 },
    'gemma2-9b-it':            { maxContextTokens: 8192,   maxOutputTokens: 8192,  maxContextMessages: 50 }
};
const OPENAI_MODELS_FREE = ['gpt-4o-mini', 'gpt-5-mini'];
const OPENAI_MODELS_PAID = ['gpt-5.4', 'gpt-5.2-chat-latest', 'gpt-4o', 'gpt-4.1', 'gpt-4o-mini'];
const DEEPSEEK_MODELS    = ['deepseek-chat', 'deepseek-reasoner'];
const GOOGLE_MODELS_FREE = ['gemini-2.5-flash'];
const GOOGLE_MODELS_PAID = ['gemini-2.5-flash', 'gemini-2.5-pro', 'gemini-1.5-pro', 'gemini-2.0-flash'];
const HF_MODELS_FREE     = ['Qwen/Qwen2.5-72B-Instruct', 'mistralai/Mistral-7B-Instruct-v0.3', 'microsoft/Phi-3.5-mini-instruct'];
const HF_MODELS_PAID     = ['meta-llama/Meta-Llama-3.1-70B-Instruct', 'meta-llama/Meta-Llama-3.1-405B-Instruct', 'Qwen/Qwen2.5-72B-Instruct', 'mistralai/Mixtral-8x7B-Instruct-v0.1'];
const GROQ_MODELS_FREE   = ['llama-3.3-70b-versatile', 'llama-3.1-8b-instant', 'mixtral-8x7b-32768', 'gemma2-9b-it'];
const GROQ_MODELS_PAID   = ['llama-3.3-70b-versatile', 'llama-3.1-8b-instant', 'mixtral-8x7b-32768', 'gemma2-9b-it'];
// Models with native audio input support (microphone recording button)
const AUDIO_CAPABLE_MODELS = ['gemini-2.5-flash','gemini-2.5-pro','gemini-1.5-pro','gemini-2.0-flash','gpt-4o','gpt-4.1'];
```

**API key configuration** (`/etc/apache2/envvars`):
```bash
export OPENAI_API_KEY="sk-proj-..."
export DEEPSEEK_API_KEY="sk-..."
export GOOGLE_API_KEY="AIza..."
export HF_API_KEY="hf_..."
export GRQ_API_KEY="gsk_..."
```

**Language configuration** (`language.xml`):
- Add a new `<language id="custom" name="..." visible="true">` block to enable the custom language slot.
- Set `has_address_form="true"` for languages with formal/informal distinction.

### Deploy-Skripte

| Skript | Funktion |
|--------|----------|
| `deploy.sh <user>` | Copies files from `/home/<user>/private-chatboot/var/www/deepseek-chat/` to `/var/www/deepseek-chat/`, sets ownership/permissions, reloads Apache |
| `sync-back.sh <user>` | Copies changed files from production back to the source repo |
| `install.sh` | Installs `deploy.sh` and `sync-back.sh` in the production directory |
| `tag-release.sh` | Creates a new Git tag with auto-incremented version number (e.g. v0.80 → v0.81) and pushes it |

---

## Projektstruktur

```
/
├── etc/apache2/sites-available/
│   ├── deepseek-chat.conf              (disabled — HTTP only, redirects to HTTPS)
│   └── deepseek-chat-ssl.conf          (active — SSL, CGI, API key via envvars)
├── shell-scipts/
│   ├── repo2text.sh                    Export entire repo as single text file
│   ├── deploy.sh                       Copies source repo → production
│   ├── sync-back.sh                    Copies production → source repo
│   ├── install.sh                      Installs deploy/sync-back scripts
│   └── tag-release.sh                  Creates and pushes Git version tags
├── var/www/deepseek-chat/
│   ├── index.html                      Main application (all JS/CSS/HTML)
│   ├── language.xml                    All UI texts in all languages (EN, DE, ES, Custom)
│   ├── manifest                        Design manifest (all conventions, ~20KB)
│   ├── changelog                       Complete development history (68+ entries, ~44KB)
│   ├── files-directorys                File overview / directory listing
│   ├── cgi-bin/
│   │   ├── openai-api.py              Streaming proxy to OpenAI API
│   │   ├── deepseek-api.py            Streaming proxy to DeepSeek API
│   │   ├── google-api.py              Streaming proxy to Google Gemini API
│   │   ├── hugging-api.py             Streaming proxy to Hugging Face Inference API
│   │   ├── groq-api.py                Streaming proxy to GroqCloud API (LPU-accelerated)
│   │   ├── deepseek-models.py         Queries /v1/models endpoint
│   │   ├── save-session.py            Saves chat sessions (POST)
│   │   ├── load-session.py            Loads session list (GET) or session (GET ?id=)
│   │   ├── delete-session.py          Deletes session (DELETE)
│   │   ├── export-pdf.py              PDF export with ReportLab
│   │   ├── export-markdown.py         Markdown export
│   │   ├── export-txt.py              TXT export
│   │   ├── export-rtf.py              RTF export (no external library)
│   │   ├── feedback-log.py            Like/Dislike logging
│   │   ├── get-log.py                 Reads and returns log file
│   │   └── deepseek-chat.log          Server log file (auto-created)
│   └── sessions/                      Chat session JSON files (auto-created)

```

---

## Modell-Konfiguration

The `MODEL_CONFIG` object in `index.html` is the single point of truth for all model-specific limits. It covers all five providers:

```javascript
const MODEL_CONFIG = {
    // OpenAI
    'gpt-5.4':              { maxContextTokens: 1050000, maxOutputTokens: 16384, maxContextMessages: 100 },
    'gpt-5.2-chat-latest':  { maxContextTokens: 128000,  maxOutputTokens: 16384, maxContextMessages: 80  },
    'gpt-4o':               { maxContextTokens: 128000,  maxOutputTokens: 16384, maxContextMessages: 80  },
    'gpt-4.1':              { maxContextTokens: 1048576, maxOutputTokens: 32768, maxContextMessages: 100 },
    'gpt-4o-mini':          { maxContextTokens: 128000,  maxOutputTokens: 16384, maxContextMessages: 80  },
    'gpt-5-mini':           { maxContextTokens: 128000,  maxOutputTokens: 16384, maxContextMessages: 80  },
    // DeepSeek
    'deepseek-chat':     { maxContextTokens: 100000,  maxOutputTokens: 8192,  maxContextMessages: 50  },
    'deepseek-reasoner': { maxContextTokens: 65000,   maxOutputTokens: 32768, maxContextMessages: 30  },
    // Google Gemini
    'gemini-2.5-flash':  { maxContextTokens: 1048576, maxOutputTokens: 8192,  maxContextMessages: 100 },
    'gemini-2.5-pro':    { maxContextTokens: 1048576, maxOutputTokens: 65536, maxContextMessages: 100 },
    'gemini-1.5-pro':    { maxContextTokens: 2097152, maxOutputTokens: 8192,  maxContextMessages: 100 },
    'gemini-2.0-flash':  { maxContextTokens: 1048576, maxOutputTokens: 8192,  maxContextMessages: 100 },
    // Hugging Face
    'Qwen/Qwen2.5-72B-Instruct':               { maxContextTokens: 128000, maxOutputTokens: 8192, maxContextMessages: 80 },
    'mistralai/Mistral-7B-Instruct-v0.3':      { maxContextTokens: 32768,  maxOutputTokens: 4096, maxContextMessages: 40 },
    'microsoft/Phi-3.5-mini-instruct':         { maxContextTokens: 128000, maxOutputTokens: 4096, maxContextMessages: 60 },
    'meta-llama/Meta-Llama-3.1-70B-Instruct':  { maxContextTokens: 128000, maxOutputTokens: 8192, maxContextMessages: 80 },
    'meta-llama/Meta-Llama-3.1-405B-Instruct': { maxContextTokens: 128000, maxOutputTokens: 8192, maxContextMessages: 80 },
    'mistralai/Mixtral-8x7B-Instruct-v0.1':    { maxContextTokens: 32768,  maxOutputTokens: 4096, maxContextMessages: 40 },
    // GroqCloud
    'llama-3.3-70b-versatile': { maxContextTokens: 128000, maxOutputTokens: 8192,  maxContextMessages: 80 },
    'llama-3.1-8b-instant':    { maxContextTokens: 131072, maxOutputTokens: 8192,  maxContextMessages: 80 },
    'mixtral-8x7b-32768':      { maxContextTokens: 32768,  maxOutputTokens: 32768, maxContextMessages: 40 },
    'gemma2-9b-it':            { maxContextTokens: 8192,   maxOutputTokens: 8192,  maxContextMessages: 50 }
};
```

Sources: [OpenAI API Docs](https://platform.openai.com/docs), [DeepSeek API Docs](https://api-docs.deepseek.com), [Google Gemini Docs](https://ai.google.dev/gemini-api/docs), [Hugging Face Inference Providers](https://huggingface.co/docs/inference-providers), [GroqCloud Docs](https://console.groq.com/docs/models) (as of 10.03.2026).

---

## Design-Manifest

The project includes a **`manifest` file** that documents all design decisions and conventions. Every change to the project is documented there. Key rules:

- **All buttons**: Pill-style only (border-radius: 20px, height: 36px) — square buttons are forbidden.
- **Button colors**: Blue (`#0056b3`) for actions, dark/blue toggle for modes, red (`#dc3545`) for destructive, green (`#28a745`) for constructive.
- **Settings**: Toggle switches only — no radio buttons, no checkboxes.
- **No emojis** in buttons or labels (exception: the DeepThink icon ✦).
- **No PHP** — exclusively JavaScript and Python.
- **No external JS frameworks** — no Node, no React, no Vue.
- **Formatting preservation**: Existing indentation and formatting in `index.html` must never be changed.
- **`AUDIO_CAPABLE_MODELS` nachführen**: Sobald ein Modell Audio-Unterstützung erhält oder verliert, muss die Konstante sofort aktualisiert werden (Manifest-Regel E.1).
- The manifest is a **separate file** and must never be embedded in `index.html`.

---

## Bekannte Einschränkungen & technische Hinweise

### „Lost in the Middle" — Eine bekannte KI-Einschränkung
All current language models (including DeepSeek) tend to remember content at the **beginning and end** of a long context reliably, but content **in the middle** is sometimes overlooked or hallucinated. (Liu et al., 2023: "Lost in the Middle: How Language Models Use Long Contexts")

**Practical impact on this project**:
- A repository export of ~270,000 characters ≈ ~67,500 tokens.
- DeepSeek context window: 100,000 tokens → ~67% utilization → content in the middle may be unreliable.
- **Recommendation**: For specific tasks, upload only the relevant files individually rather than the entire repository export.

### GitHub Raw URL Caching
After a `git push`, the new version is **not immediately available** via `raw.githubusercontent.com` URLs — GitHub caches these for up to 10 minutes. This is normal and cannot be circumvented. The files are correctly stored on GitHub as soon as `git push` succeeds.

### Nano und Unicode — Kritische Warnung
**Never** edit files containing Unicode escape sequences (like the umlaut functions) using `nano` or by copy-pasting into a terminal. Nano corrupts `\u00e4` to `M-CM-$` which is binary garbage for JavaScript.

**The only safe workflow**:
1. Edit files locally (VS Code, gedit, kate, or any proper editor).
2. `git add` / `git commit` / `git push` from the local machine.
3. On the server: `git pull` (in the source repo as user `source`).
4. As root: `./deploy.sh source`.

### Linux/X11/Firefox Einfüge-Verhalten
On Linux with X11 and Firefox, `e.preventDefault()` in paste event handlers does not reliably block browser-native paste behavior for content coming from file managers. The solution implemented here (allow paste, check content in `setTimeout(0)`, clear if file paths detected) is the reliable workaround for this platform-specific limitation.

---

## Abhängigkeiten

| Komponente | Zweck | Installation |
|-----------|---------|-------------|
| Apache2 | Webserver, CGI-Unterstützung | `apt install apache2` |
| Python 3 | Serverseitige CGI-Skripte | `apt install python3` |
| reportlab | PDF-Export | `pip3 install reportlab` |
| pdf.js 3.11.174 | Clientseitige PDF-Extraktion | Via CDN geladen (automatischer Fallback) |
| jq | JSON-Verarbeitung in `repo2text.sh` | `apt install jq` |
| pv | Fortschrittsanzeige in `repo2text.sh` | `apt install pv` |
| git | Versionsverwaltung | `apt install git` |
| zip | Archiv-Erstellung in `repo2text.sh` | `apt install zip` |

**No exotic frameworks** — all dependencies are standard packages in a Debian environment or loaded from well-established CDNs.

---

## Fazit / Warum dieses Projekt heraussticht

This project demonstrates professional-level web development in a minimalist, security-first approach:

**Architecture**:
- Clean separation of client (pure HTML/JS) and server (Python CGI) with no blurring of responsibilities.
- API key never exposed — even a full XSS compromise cannot leak it.
- Single-file client (`index.html`) that is entirely self-contained yet highly modular internally.

**User experience**:
- Streaming responses with sub-second first-token latency.
- Unique flexible context management (delete any message + all subsequent).
- Intelligent clipboard handling for text, images, and file path protection.
- **Audio-Aufnahme** direkt im Browser — Mikrofon-Input für Google Gemini (alle Modelle) und OpenAI gpt-4o / gpt-4.1.
- Multi-language support with address form distinction, loaded from external XML.

**Engineering**:
- Magic byte inspection that detects malware regardless of filename extension.
- Umlaut placeholder system solving a fundamental DeepSeek API limitation.
- Forward-compatible model capability map ready for image-supporting models.
- Complete audit trail via Git and detailed changelog.

**Tooling**:
- `repo2text.sh` as a practical tool for AI-assisted development.
- Deployment scripts ensuring consistent, permission-correct deployments.
- Version tagging for clean release management.

**For a professional developer**, this project demonstrates:
- **Security awareness** — API key protection, malware detection, secure session storage.
- **Structured discipline** — manifest, version tags, strict design conventions, documented changelog.
- **Problem-solving depth** — X11 paste behavior, umlaut corruption, PDF binary output, "Lost in the Middle".
- **Complete documentation** — both inline and in dedicated files.

DeepSeek Chat is a **showcase for professional web development** — without unnecessary overhead, but with the highest standards for security, correctness, and user-friendliness.

---

*Zuletzt aktualisiert: 11.03.2026*





