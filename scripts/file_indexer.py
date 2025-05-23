import os
import fitz  # PyMuPDF
import chromadb
from sentence_transformers import SentenceTransformer
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction

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
