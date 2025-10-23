import os
import requests
from flask import Flask, request, jsonify, send_from_directory, render_template




app = Flask(__name__)

# Your A4F API key (set this in Render or .env)
OPENAI_A4F_MODEL = "provider-1/llama-3.2-1b-instruct-fp-16"   # Replace with actual OpenAI model ID
GEMINI_A4F_MODEL = "provider-5/grok-4-0709"  # Replace with actual Gemini model ID
QWEN_A4F_MODEL = "provider-3/qwen-2.5-72b"

def ask_a4f(prompt, model_id):
    key = os.getenv("A4F_API_KEY", "").strip()
    if not key:
        return "A4F key not configured."
    headers = {
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": model_id,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.5,
        "max_tokens": 100
    }
    resp = requests.post("https://api.a4f.co/v1/chat/completions", headers=headers, json=payload, timeout=20)
    try:
        resp.raise_for_status()
        return resp.json()["choices"][0]["message"]["content"]
    except Exception as e:
        return f"A4F error: {e}"


@app.route('/')
def index():
    return render_template("index.html")

@app.route('/api/compare', methods=['POST'])
def compare():
    data = request.get_json()
    prompt = data.get("prompt", "")
    use_openai = data.get("use_openai", False)
    use_gemini = data.get("use_gemini", False)
    use_qwen = data.get("use_qwen", False)

    results = {}
    if use_openai:
        results["openai"] = ask_a4f(prompt, OPENAI_A4F_MODEL)
    else:
        results["openai"] = "OpenAI disabled."
    if use_gemini:
        results["gemini"] = ask_a4f(prompt, GEMINI_A4F_MODEL)
    else:
        results["gemini"] = "Gemini disabled."
    if use_qwen:
        results["qwen"] = ask_a4f(prompt, QWEN_A4F_MODEL)
    else:
        results["qwen"] = "Qwen AI disabled."
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)
