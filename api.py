from flask import Flask, request, jsonify
from scripts.file_indexer import scan_folder, answer_question_human_like, open_file_in_explorer

app = Flask(__name__)

@app.route("/scan", methods=["POST"])
def scan():
    folder = request.json.get("path")
    scan_folder(folder)
    return jsonify({"status": "ok", "message": f"Scanned {folder}"}), 200

@app.route("/ask", methods=["POST"])
def ask():
    question = request.json.get("question")
    result = answer_question_human_like(question)
    return jsonify(result), 200

@app.route("/open", methods=["POST"])
def open_file():
    path = request.json.get("path")
    open_file_in_explorer(path)
    return jsonify({"status": "ok", "message": f"Opened {path}"}), 200

if __name__ == "__main__":
    app.run(port=5000, debug=True)
c