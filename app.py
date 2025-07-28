import os
import requests
from flask import Flask, request, jsonify, send_from_directory

app = Flask(__name__)

# Your A4F API key (set this in Render or .env)
OPENAI_A4F_MODEL = "provider-6/gpt-4.1"   # Replace with actual OpenAI model ID
GEMINI_A4F_MODEL = "provider-1/gemma-3-12b-it"  # Replace with actual Gemini model ID

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
        "temperature": 0.7,
        "max_tokens": 200
    }
    resp = requests.post("https://api.a4f.co/v1/chat/completions", headers=headers, json=payload, timeout=20)
    try:
        resp.raise_for_status()
        return resp.json()["choices"][0]["message"]["content"]
    except Exception as e:
        return f"A4F error: {e}"

def ask_mock(prompt):
    return f"MockBot: Simulated answer for '{prompt}'"

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/api/compare', methods=['POST'])
def compare():
    data = request.get_json()
    prompt = data.get("prompt", "")
    use_openai = data.get("use_openai", False)
    use_gemini = data.get("use_gemini", False)
    use_mock = data.get("use_mock", True)

    results = {}
    if use_openai:
        results["openai"] = ask_a4f(prompt, OPENAI_A4F_MODEL)
    else:
        results["openai"] = "OpenAI disabled."
    if use_gemini:
        results["gemini"] = ask_a4f(prompt, GEMINI_A4F_MODEL)
    else:
        results["gemini"] = "Gemini disabled."
    if use_mock:
        results["mock"] = ask_mock(prompt)
    else:
        results["mock"] = "MockBot disabled."
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)
