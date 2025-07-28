document.getElementById("chat-form").addEventListener("submit", async function (e) {
  e.preventDefault();

  const prompt = document.getElementById("prompt").value;
  const useOpenAI = document.getElementById("use_openai").checked;
  const useGemini = document.getElementById("use_gemini").checked;
  const useQwen = document.getElementById("use_qwen").checked;

  // Show loading indicators
  if (useOpenAI) document.getElementById("openai-answer").textContent = "Loading...";
  if (useGemini) document.getElementById("gemini-answer").textContent = "Loading...";
  if (useQwen) document.getElementById("qwen-answer").textContent = "Loading...";

  try {
    const response = await fetch("/api/compare", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        prompt,
        use_openai: useOpenAI,
        use_gemini: useGemini,
        use_qwen: useQwen
      }),
    });

    const data = await response.json();
    document.getElementById("openai-answer").textContent = data.openai || "Disabled.";
    document.getElementById("gemini-answer").textContent = data.gemini || "Disabled.";
    document.getElementById("qwen-answer").textContent = data.qwen || "Disabled.";
  } catch (err) {
    document.getElementById("openai-answer").textContent = "Error fetching response.";
    document.getElementById("gemini-answer").textContent = "Error fetching response.";
    document.getElementById("qwen-answer").textContent = "Error fetching response.";
  }
});
