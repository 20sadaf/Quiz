from flask import Flask, jsonify, send_from_directory
import json
import random
import os

app = Flask(__name__, static_folder="static")

def load_questions_from_file(filepath, num_questions=5):
    if not os.path.exists(filepath):
        print(f"[ERROR] File not found: {filepath}")
        return []
    try:
        with open(filepath, 'r') as file:
            all_questions = json.load(file)
            if not isinstance(all_questions, list):
                print("[ERROR] JSON format is invalid: expected a list of questions.")
                return []
            return random.sample(all_questions, min(num_questions, len(all_questions)))
    except json.JSONDecodeError as e:
        print(f"[ERROR] JSON decoding error: {e}")
        return []

@app.route("/")
def serve_index():
    return send_from_directory("static", "index.html")

@app.route("/api/questions")
def get_questions():
    selected_questions = load_questions_from_file("questions.json", num_questions=5)
    return jsonify(selected_questions)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Railway provides PORT automatically
    app.run(host="0.0.0.0", port=port)  # This is correct for Railway
