import os
import requests
from flask import Flask, request, jsonify, send_from_directory

app = Flask(__name__)

# Your A4F API key (set this in Render or .env)
OPENAI_A4F_MODEL = "provider-6/gpt-4.1"   # Replace with actual OpenAI model ID
GEMINI_A4F_MODEL = "provider-1/gemma-3-12b-it"  # Replace with actual Gemini model ID

def ask_a4f(prompt, model_id):
    a4f_key = os.getenv("A4F_API_KEY", "").strip()
    if not a4f_key:
        return "A4F API key not configured."

    try:
        headers = {
            "Authorization": f"Bearer {a4f_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": model_id,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.7,
            "max_tokens": 200
        }
        url = "https://api.a4f.co/v1/chat/completions"
        res = requests.post(url, headers=headers, json=payload, timeout=20)
        res.raise_for_status()
        return res.json()["choices"][0]["message"]["content"]
    except Exception as e:
        return f"A4F error: {str(e)}"

def ask_mock(prompt):
    return f"MockBot: This is a simulated answer for '{prompt}'."

@app.route('/api/compare', methods=['POST'])
def compare():
    data = request.get_json()
    prompt = data.get("prompt", "")
    use_openai = data.get("use_openai", False)
    use_gemini = data.get("use_gemini", False)
    use_mock = data.get("use_mock", True)

    result = {}

    if use_openai:
        result["openai"] = ask_a4f(prompt, OPENAI_A4F_MODEL)
    else:
        result["openai"] = "OpenAI disabled."

    if use_gemini:
        result["gemini"] = ask_a4f(prompt, GEMINI_A4F_MODEL)
    else:
        result["gemini"] = "Gemini disabled."

    if use_mock:
        result["mock"] = ask_mock(prompt)
    else:
        result["mock"] = "MockBot disabled."

    return jsonify(result)

@app.route('/')
def serve_index():
    return send_from_directory('static', 'index.html')

@app.route('/static/<path:path>')
def serve_static(path):
    return send_from_directory('static', path)

if __name__ == '__main__':
    app.run(debug=True)
