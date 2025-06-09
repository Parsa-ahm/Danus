# 🧠 Danus: A Local AI Assistant

> **Danus** is a local-first, fully private AI assistant that understands, organizes, and automates everything on your computer. Powered by semantic search, chunked document QA, file automation, and full system memory — Danus runs offline with no cloud or tracking.

---

## ⚡ Quick Start

### 🧰 Prerequisites

- Python 3.10 or higher
- pip
- Git

---

### 🖥️ Windows

```bash
git clone https://github.com/your-username/danus.git
cd danus
bash setup_env.sh   # creates venv and installs deps
./start.sh
```

---

### 💻 macOS / Linux

```bash
git clone https://github.com/your-username/danus.git
cd danus
./setup_env.sh    # one-time venv setup
./start.sh
```

You can also read the project overview at `website/index.html` for a friendly introduction.

---

### 🧪 Test the API

```bash
curl -X POST http://localhost:5000/scan \
  -H "Content-Type: application/json" \
  -d '{"path": "/Users/yourname/Documents"}'

curl -X POST http://localhost:5000/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "What are the terms in my rental agreement?"}'
```

---

## 🧠 What Danus Can Do

- Semantic document understanding (even scanned contracts)
- AI chat that gives **real answers** from your files
- One-click open of relevant results
- Organizes files by meaning (assignments, personal, contracts)
- Automates file renaming, backups, and format conversion
- Maintains memory of what you've done
- Uses your **own GPU or CPU**, all local, no cloud

---

## 🗂️ Project Structure

```plaintext
danus/
├── api.py                 # Flask REST API
├── main.py                # Local testing CLI
├── scripts/
│   ├── file_indexer.py    # Core logic: scanning, search, answers, file ops
│   ├── task_scheduler.py  # Lightweight task runner for deferred jobs
│   └── live_editor.py     # Diff-based editing helper
├── ui/                    # React + Tauri desktop frontend
├── setup_env.sh           # Virtual environment bootstrap
├── venv/                  # Local Python environment (gitignored)
├── models/                # Downloaded LLMs (safetensors format)
├── backups/               # Backups of original files
├── danus_log.json         # Full audit trail of file changes
├── danus_memory/          # Conversations, generated code, etc.
├── requirements.txt       # Python dependencies
└── README.md              # You’re here
```

---

## 💬 API Endpoints

| Endpoint | Method | Description                                               |
| -------- | ------ | --------------------------------------------------------- |
| `/scan`  | POST   | `{ "path": "folder" }` – Indexes all documents in folder  |
| `/ask`   | POST   | `{ "question": "..." }` – Answers using top relevant file |
| `/open`  | POST   | `{ "path": "file" }` – Opens folder in file explorer      |

---

## 🔮 Feature Roadmap

- ✅ Chunked RAG QA — Extract & summarize exact paragraphs
- 🔜 Contextual Memory — Retain conversations for 7–30 days
- 🔜 Intent-Aware Actions — “Organize folder” → suggest structure
- 🔜 Inline Snippet Linking — Highlight source quote from files
- 🔜 AI File Automation — Rename, move, zip, or convert files via natural language
- 🔜 Auto-Classify (temp folders) — Safe reorganization with preview
- 🔜 Private Model Picker — DeepSeek, Mistral, Phi-3, etc.
- 🔜 Undo Log System — Rollback file ops
- 🔜 Self-Updating Memory — Detect changed/added files

### 🆕 Additional Modules

- `TaskScheduler` — schedule long running or overnight jobs and execute them
  later.
- `live_editor` — propose edits to files using diffs so you can accept or reject
  changes before they are applied.
- `memory` — lightweight SQLite store for recent conversations.
- `gpu_ops` — optional CUDA kernels for accelerated math.

To build the CUDA extension, see `cpp/README.md`.

---

## 👩‍💻 How to Modify the Code

All logic lives in `scripts/file_indexer.py`. You can modify:

- `scan_folder()` → to support more file types
- `answer_question_human_like()` → to change how answers are generated
- `open_file_in_explorer()` → to tweak OS integration

- The backend runs independently of the UI. You can connect it to:

- A Tauri + React GUI
- A CLI terminal assistant

### Running the Optional UI

```bash
cd ui
npm install
npm run dev
```

This launches a React interface with theme toggle, model picker and a basic text editor.
- A chatbot plugin

---

## 🔒 Privacy First

Danus:

- Runs 100% locally
- Never sends data to the cloud
- Can use fully offline LLMs (no Hugging Face APIs required)
- Encrypts or prunes memory on schedule (coming soon)

---

## 📦 Setup for Private Repo

1. Create repo on GitHub (`danus`)
2. Set as private
3. Push your code:

```bash
git remote add origin https://github.com/your-username/danus.git
git add .
git commit -m "Initial private upload of Danus"
git push -u origin main
```

---

For a live demo site, open `website/index.html` in your browser.
