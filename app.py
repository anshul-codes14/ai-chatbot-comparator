import os
import requests
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "").strip()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "").strip()

def ask_openai(prompt):
    if not OPENAI_API_KEY:
        return "OpenAI API key not configured."

    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "user", "content": prompt}]
    }

    try:
        response = requests.post(url, headers=headers, json=data, timeout=20)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
    except Exception as e:
        return f"OpenAI API error: {str(e)}"

def ask_gemini(prompt):
    if not GEMINI_API_KEY:
        return "Gemini API key not configured."

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-pro-latest:generateContent?key={GEMINI_API_KEY}"
    headers = {"Content-Type": "application/json"}
    data = {"contents": [{"parts": [{"text": prompt}]}]}

    try:
        response = requests.post(url, headers=headers, json=data, timeout=20)
        response.raise_for_status()
        return response.json()["candidates"][0]["content"]["parts"][0]["text"]
    except Exception as e:
        return f"Gemini API error: {str(e)}"

def ask_mock(prompt):
    return f"MockBot: This is a simulated answer for your prompt: '{prompt}'"

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/api/compare', methods=['POST'])
def compare():
    data = request.get_json()
    prompt = data.get("prompt", "").strip()
    use_mock = data.get("use_mock", False)

    if not prompt:
        return jsonify({"error": "Prompt is empty."}), 400

    result = {}

    if use_mock:
        # MockBot only
        result["mock"] = ask_mock(prompt)
        result["openai"] = "OpenAI disabled."
        result["gemini"] = "Gemini disabled."
    else:
        # Real APIs only
        result["mock"] = "MockBot disabled."
        result["openai"] = ask_openai(prompt)
        result["gemini"] = ask_gemini(prompt)

    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
