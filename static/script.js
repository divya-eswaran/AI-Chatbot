function handleKey(event) {
    if (event.key === "Enter") {
        sendMessage();
    }
}

function appendMessage(message, sender) {
    let chatBox = document.getElementById("chat-box");

    let msgDiv = document.createElement("div");
    msgDiv.classList.add("message", sender);
    msgDiv.innerText = message;

    chatBox.appendChild(msgDiv);
    chatBox.scrollTop = chatBox.scrollHeight;

    // ✅ Save chat history
    localStorage.setItem("chat", chatBox.innerHTML);
}

function showTyping() {
    let chatBox = document.getElementById("chat-box");

    let typing = document.createElement("div");
    typing.classList.add("message", "bot");
    typing.id = "typing";
    typing.innerText = "Typing...";

    chatBox.appendChild(typing);
    chatBox.scrollTop = chatBox.scrollHeight;
}

function removeTyping() {
    let typing = document.getElementById("typing");
    if (typing) typing.remove();
}

async function sendMessage() {
    let input = document.getElementById("user-input");
    let message = input.value.trim();

    if (message === "") return;

    appendMessage(message, "user");
    input.value = "";

    showTyping();

    let response = await fetch("/chat", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ message: message })
    });

    let data = await response.json();

    removeTyping();

    appendMessage(data.response, "bot");
}

function clearChat() {
    document.getElementById("chat-box").innerHTML = "";
    localStorage.removeItem("chat");  // ✅ clear saved chat
}
window.onload = function () {
    document.getElementById("chat-box").innerHTML = "";
};
// ✅ Load chat history when page loads
