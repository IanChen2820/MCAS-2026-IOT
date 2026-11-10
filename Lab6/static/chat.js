const form = document.getElementById("chat-form");
const input = document.getElementById("message-input");
const sendButton = document.getElementById("send-button");
const resetButton = document.getElementById("reset-button");
const messages = document.getElementById("messages");


function addMessage(text, type) {
    const div = document.createElement("div");
    div.className = "message " + type;
    div.textContent = text;
    messages.appendChild(div);
    messages.scrollTop = messages.scrollHeight;
}


form.addEventListener("submit", async (event) => {
    event.preventDefault();

    const message = input.value.trim();
    if (!message) return;

    addMessage("You：" + message, "user-message");

    input.value = "";
    input.disabled = true;
    sendButton.disabled = true;

    try {
        const response = await fetch("/api/chat", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ message }),
        });

        const contentType = response.headers.get("content-type") || "";
        const raw = await response.text();

        console.log("Chat response:", {
            status: response.status,
            url: response.url,
            contentType,
            body: raw,
        });

        if (!contentType.includes("application/json")) {
            const ngrokCode = raw.match(/ERR_NGROK_\d+/);

            throw new Error(
                `HTTP ${response.status}：收到 HTML 或其他非 JSON 回應`
                + (ngrokCode ? `（${ngrokCode[0]}）` : "")
                + "，請查看 F12 → Console 的 Chat response"
            );
        }

        const data = JSON.parse(raw);

        if (!response.ok) {
            throw new Error(data.error || "伺服器發生錯誤");
        }

        addMessage("Gemini：" + data.reply, "ai");

    } catch (error) {
        addMessage("Error：" + error.message, "error-message");

    } finally {
        input.disabled = false;
        sendButton.disabled = false;
        input.focus();
    }
});


resetButton.addEventListener("click", async () => {
    const response = await fetch("/api/reset", {
        method: "POST",
    });

    if (response.ok) {
        messages.innerHTML = "";
        addMessage("Gemini：已開始新的對話。", "ai");
    }
});
