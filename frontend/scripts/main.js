const API_BASE_URL = "";

async function sendMessage(message) {
    try {
        // Sistem otomatis menentukan model (Auto-Pilot)

        const response = await fetch(`${API_BASE_URL}/consult`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                question: message,
                user_id: "guest",
                preferred_model: "auto"
            })
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        return data.response; // Backend returns { response: "..." }
    } catch (error) {
        console.error("Error communicating with AI:", error);
        return "Maaf, terjadi kesalahan saat menghubungkan ke server AI.";
    }
}

// Chat UI Logic
document.addEventListener("DOMContentLoaded", () => {
    const sendBtn = document.getElementById("send-btn");
    const userInput = document.getElementById("user-input");
    const chatBox = document.getElementById("chat-box");

    if (sendBtn && userInput && chatBox) {
        sendBtn.addEventListener("click", async () => {
            const message = userInput.value.trim();
            if (!message) return;

            // Display user message
            chatBox.innerHTML += `<div class="message user-msg">${message}</div>`;
            userInput.value = "";
            chatBox.scrollTop = chatBox.scrollHeight;

            // Show loading state
            const loadingDiv = document.createElement("div");
            loadingDiv.className = "message ai-msg";
            loadingDiv.textContent = "AI sedang mengetik...";
            chatBox.appendChild(loadingDiv);

            // Fetch response
            const aiResponse = await sendMessage(message);

            // Display AI response
            // Display AI response with Markdown rendering
            const rawResponse = aiResponse;
            // Check if marked is available, otherwise fallback to plain text
            if (typeof marked !== 'undefined') {
                loadingDiv.innerHTML = marked.parse(rawResponse);
            } else {
                loadingDiv.textContent = rawResponse;
            }

            chatBox.scrollTop = chatBox.scrollHeight;
        });
    }
});
