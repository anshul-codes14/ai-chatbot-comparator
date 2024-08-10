# AI Chatbot Comparator Dashboard

A simple dashboard where you can enter a prompt and instantly see responses from multiple AI chatbots side-by-side. Perfect for research, fact-checking, or comparing chatbot outputs.

## Features

- Enter your research question or prompt
- Get answers from 3 chatbots (OpenAI ChatGPT, Google Gemini, and a mock/third bot)
- Easy web interface, no login required

## Setup & Run

### 1. Clone the repo

```bash
git clone https://github.com/<your-username>/ai-chatbot-comparator.git
cd ai-chatbot-comparator
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Set your API keys

Set your OpenAI and Gemini API keys in environment variables:

**Linux/macOS:**
```bash
export OPENAI_API_KEY='your-openai-key'
export GEMINI_API_KEY='your-gemini-key'
```
**Windows:**
```cmd
set OPENAI_API_KEY=your-openai-key
set GEMINI_API_KEY=your-gemini-key
```

Or paste them directly in `app.py`.

### 4. Run the app

```bash
python app.py
```
Then open [http://localhost:5000](http://localhost:5000) in your browser.

---


**Extra:**  
You can add more chatbots (Claude, Bing, etc.) by extending the backend with their API calls.

---

## Customization

- Change UI theme in `style.css`
- Add more chatbots in `app.py`
- Deploy for free using PythonAnywhere, Render, or Heroku

---