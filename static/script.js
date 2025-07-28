document.getElementById('promptForm').addEventListener('submit', async (e) => {
  e.preventDefault();
  const prompt = document.getElementById('prompt').value.trim();
  const useOpenAI = document.getElementById('mockToggle').checked ? false : true;
  const useGemini = useOpenAI;
  const useMock = document.getElementById('mockToggle').checked;

  if (!prompt) return alert('Please enter a prompt.');

  ['openai-answer','gemini-answer','mock-answer'].forEach(id => {
    document.getElementById(id).textContent = 'Loading...';
  });

  try {
    const resp = await fetch('/api/compare', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({ prompt, use_openai: useOpenAI, use_gemini: useGemini, use_mock: useMock })
    });
    const data = await resp.json();
    document.getElementById('openai-answer').textContent = data.openai;
    document.getElementById('gemini-answer').textContent = data.gemini;
    document.getElementById('mock-answer').textContent = data.mock;
  } catch (err) {
    ['openai-answer','gemini-answer','mock-answer'].forEach(id => {
      document.getElementById(id).textContent = `Error: ${err.message}`;
    });
  }
});
