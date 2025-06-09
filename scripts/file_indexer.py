import os
import fitz  # PyMuPDF
import chromadb
from sentence_transformers import SentenceTransformer
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction
import json
import shutil

chroma_client = chromadb.Client()
embedding_func = SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")
collection = chroma_client.get_or_create_collection(name="danus_index", embedding_function=embedding_func)

# Load LLM model (DeepSeek)
model_name = "deepseek-ai/deepseek-coder-1.3b-base"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    device_map="auto",
    torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
    use_safetensors=True
)


# Supported file readers
def extract_text(file_path):
    if file_path.endswith(".pdf"):
        try:
            doc = fitz.open(file_path)
            return "\n".join(page.get_text() for page in doc)
        except Exception:
            return ""
    elif file_path.endswith(".txt"):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return f.read()
        except Exception:
            return ""
    return ""

# Scans folder and indexes all documents
def scan_folder(path: str):
    added = 0
    for root, _, files in os.walk(path):
        for name in files:
            full_path = os.path.join(root, name)
            if name.lower().endswith((".pdf", ".txt")):
                text = extract_text(full_path)
                if text.strip():
                    collection.add(
                        documents=[text],
                        metadatas=[{"path": full_path}],
                        ids=[full_path]
                    )
                    added += 1
                    print(f"[+] Indexed: {full_path}")
    return added

# Semantic search for top-K relevant docs
def search_files(query: str, top_k: int = 5):
    results = collection.query(query_texts=[query], n_results=top_k)
    matches = []
    for doc, meta in zip(results["documents"][0], results["metadatas"][0]):
        preview = doc[:300].replace("\n", " ").strip() + "..."
        matches.append({
            "path": meta["path"],
            "preview": preview
        })
    return matches

# QA-style summarization response
def answer_question_human_like(query: str):
    matches = search_files(query)
    if not matches:
        return {"summary": "I couldn’t find anything relevant.", "matches": []}

    # Build context from top 2 matches
    context = ""
    for m in matches[:2]:
        context += f"Path: {m['path']}\nPreview: {m['preview']}\n\n"

    prompt = f"""User asked:
{query}

Files:
{context}
Reply like a helpful AI. Recommend the most relevant file and summarize it clearly with the exact file path."""

    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
    outputs = model.generate(**inputs, max_new_tokens=300)
    summary = tokenizer.decode(outputs[0], skip_special_tokens=True).strip()

    return {
        "summary": summary,
        "matches": matches
    }

# Opens file location in system explorer
def open_file_in_explorer(path):
    if os.name == 'nt':  # Windows
        os.system(f'explorer /select,"{path}"')
    elif os.name == 'posix':  # macOS or Linux
        os.system(f'open "{os.path.dirname(path)}"')

LOG_PATH = "danus_log.json"
BACKUP_DIR = "backups"


def _append_log(action: str, details: dict):
    """Append an entry to the JSON log used for simple memory."""
    log = []
    if os.path.exists(LOG_PATH):
        try:
            with open(LOG_PATH, "r", encoding="utf-8") as f:
                log = json.load(f)
        except Exception:
            log = []
    log.append({"action": action, "details": details})
    with open(LOG_PATH, "w", encoding="utf-8") as f:
        json.dump(log, f, indent=2)


def backup_and_rename(file_path: str) -> str:
    """Backup the file and rename it with underscores."""
    os.makedirs(BACKUP_DIR, exist_ok=True)
    base = os.path.basename(file_path)
    backup_path = os.path.join(BACKUP_DIR, base)
    shutil.copy2(file_path, backup_path)

    new_name = base.replace(" ", "_")
    new_path = os.path.join(os.path.dirname(file_path), new_name)
    os.rename(file_path, new_path)

    _append_log("backup_rename", {"src": file_path, "backup": backup_path, "new": new_path})
    return new_path


def _categorize(text: str) -> str:
    text_l = text.lower()
    if any(k in text_l for k in ["assignment", "homework"]):
        return "assignments"
    if any(k in text_l for k in ["contract", "agreement", "terms"]):
        return "contracts"
    if any(k in text_l for k in ["personal", "diary", "letter"]):
        return "personal"
    return "others"


def organize_folder(path: str):
    """Move files into folders based on simple keyword categories."""
    for root, _, files in os.walk(path):
        for name in files:
            if not name.lower().endswith((".pdf", ".txt")):
                continue
            full_path = os.path.join(root, name)
            text = extract_text(full_path)
            category = _categorize(text)
            target_dir = os.path.join(path, category)
            os.makedirs(target_dir, exist_ok=True)
            target_path = os.path.join(target_dir, name)
            shutil.move(full_path, target_path)
            _append_log("move", {"src": full_path, "dst": target_path})

