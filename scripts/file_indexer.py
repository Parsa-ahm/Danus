import os
from typing import List, Dict
from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.utils import embedding_functions
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
import fitz  # PyMuPDF for PDF
from docx import Document


model = SentenceTransformer("all-MiniLM-L6-v2")  # small, fast, meaningful

client = chromadb.Client()
collection = client.create_collection(name="file_index")

def read_text_file(path):
    try:
        with open(path, 'r', encoding='utf-8', errors='ignore') as f:
            return f.read()
    except:
        return ""

def read_pdf_file(path):
    try:
        doc = fitz.open(path)
        return "\n".join([page.get_text() for page in doc])
    except:
        return ""

def read_docx_file(path):
    try:
        doc = Document(path)
        return "\n".join([para.text for para in doc.paragraphs])
    except:
        return ""

def scan_folder(root_path: str):
    supported = [".txt", ".md", ".pdf", ".docx", ".py", ".json", ".html"]
    for dirpath, _, filenames in os.walk(root_path):
        for file in filenames:
            ext = os.path.splitext(file)[1].lower()
            full_path = os.path.join(dirpath, file)
            if ext not in supported or file.startswith("~"):
                continue

            text = ""
            if ext in [".txt", ".md", ".py", ".json", ".html"]:
                text = read_text_file(full_path)
            elif ext == ".pdf":
                text = read_pdf_file(full_path)
            elif ext == ".docx":
                text = read_docx_file(full_path)

            if not text.strip():
                continue

            emb = model.encode(text[:1000], convert_to_tensor=False).tolist()
            collection.add(
                documents=[text[:1000]],
                metadatas=[{"path": full_path}],
                ids=[full_path]
            )

            print(f"[+] Indexed: {full_path}")

def search_files(query: str, top_k: int = 5):
    query_emb = model.encode(query, convert_to_tensor=False).tolist()
    results = collection.query(query_embeddings=[query_emb], n_results=top_k)

    print(f"\n🔍 Search Results for: '{query}'")
    for doc, meta in zip(results["documents"][0], results["metadatas"][0]):
        print(f"- {meta['path']}")
        print(f"  Preview: {doc[:200].strip()}...\n")


llm_model_name = "deepseek-ai/deepseek-coder-1.3b-base"
llm_tokenizer = AutoTokenizer.from_pretrained(llm_model_name)
llm_model = AutoModelForCausalLM.from_pretrained(
    llm_model_name,
    device_map="auto",
    torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
    trust_remote_code=True,
    use_safetensors=True
)

def open_file_in_explorer(path: str):
    if os.name == "nt":  # Windows
        os.startfile(path)
    elif os.name == "posix":
        os.system(f'open "{os.path.dirname(path)}"')  # macOS
    else:
        os.system(f'xdg-open "{os.path.dirname(path)}"')  # Linux

def answer_question_human_like(query: str, top_k: int = 5) -> dict:
    query_emb = model.encode(query, convert_to_tensor=False).tolist()
    results = collection.query(query_embeddings=[query_emb], n_results=top_k)

    summaries = []
    for doc, meta in zip(results["documents"][0], results["metadatas"][0]):
        summaries.append({
            "path": meta['path'],
            "preview": doc[:300].strip()
        })

    # LLM input formatting
    context_str = "\n".join([f"Path: {s['path']}\nPreview: {s['preview']}" for s in summaries])
    prompt = f"""You are a friendly assistant helping the user understand their files.

User asked:
{query}

Files:
{context_str}

Reply like a helpful AI. Recommend the most relevant file and summarize it clearly with the exact file path.
"""

    inputs = llm_tokenizer(prompt, return_tensors="pt").to(llm_model.device)
    outputs = llm_model.generate(**inputs, max_new_tokens=300)
    response = llm_tokenizer.decode(outputs[0], skip_special_tokens=True)

    return {
        "query": query,
        "summary": response[len(prompt):].strip(),
        "matches": summaries
    }


