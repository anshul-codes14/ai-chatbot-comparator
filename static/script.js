document.getElementById('promptForm').addEventListener('submit', async (e) => {
    e.preventDefault();

    const prompt = document.getElementById('prompt').value.trim();
    const useMock = document.getElementById('mockToggle').checked;

    if (!prompt) {
        alert("Please enter a prompt.");
        return;
    }

    // Show loading messages
    document.getElementById('openai-answer').textContent = "Loading...";
    document.getElementById('gemini-answer').textContent = "Loading...";
    document.getElementById('mock-answer').textContent = "Loading...";

    try {
        const response = await fetch('/api/compare', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({ prompt: prompt, use_mock: useMock })
        });

        if (!response.ok) {
            const errorData = await response.json();
            const errMsg = errorData.error || "Unknown error";
            document.getElementById('openai-answer').textContent = "Error: " + errMsg;
            document.getElementById('gemini-answer').textContent = "Error: " + errMsg;
            document.getElementById('mock-answer').textContent = "Error: " + errMsg;
            return;
        }

        const data = await response.json();

        document.getElementById('openai-answer').textContent = data.openai || "No answer";
        document.getElementById('gemini-answer').textContent = data.gemini || "No answer";
        document.getElementById('mock-answer').textContent = data.mock || "No answer";

    } catch (err) {
        const msg = "Fetch error: " + err.message;
        document.getElementById('openai-answer').textContent = msg;
        document.getElementById('gemini-answer').textContent = msg;
        document.getElementById('mock-answer').textContent = msg;
    }
});
