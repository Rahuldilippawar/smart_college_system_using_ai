const userInput = document.getElementById('user-msg');
const suggestionsDiv = document.getElementById("suggestions");
const messagesDiv = document.getElementById('messages');
const autoRepliesDiv = document.getElementById("auto-replies");
const typingIndicator = document.getElementById('typing-indicator');
const chatBox = document.getElementById('chat-box');
let selectedIndex = -1;
let chatHistory = [];
let userPoints = 0;
let conversationState = "initial"; // ✅ Track current conversation state

// Function to show live query suggestions
userInput.addEventListener("input", async function () {
    const query = this.value.trim();
    if (query.length < 1) {
        suggestionsDiv.innerHTML = "";
        selectedIndex = -1;
        return;
    }
    const response = await fetch(`/suggest?query=${encodeURIComponent(query)}`);
    const suggestions = await response.json();
    if (suggestions.length === 0) {
        suggestionsDiv.innerHTML = "";
        return;
    }
    suggestionsDiv.innerHTML = suggestions.map((suggestion, index) => 
        `<div class="suggestion ${index === selectedIndex ? 'highlight' : ''}" 
             data-index="${index}" 
             onclick="selectAndSend('${suggestion}')">${suggestion}</div>`
    ).join("");
    selectedIndex = -1;
});

// Function to set input and send message when suggestion is clicked
function selectAndSend(text) {
    userInput.value = text;
    suggestionsDiv.innerHTML = "";
    sendMessage();
}

// Handle keyboard navigation (Up, Down, Enter)
userInput.addEventListener("keydown", function (event) {
    const suggestions = document.querySelectorAll(".suggestion");
    if (suggestions.length === 0) {
        if (event.key === "Enter") {
            event.preventDefault();
            sendMessage();
        }
        return;
    }
    if (event.key === "ArrowDown") {
        event.preventDefault();
        selectedIndex = (selectedIndex < suggestions.length - 1) ? selectedIndex + 1 : 0;
    } else if (event.key === "ArrowUp") {
        event.preventDefault();
        selectedIndex = (selectedIndex > 0) ? selectedIndex - 1 : suggestions.length - 1;
    } else if (event.key === "Enter") {
        event.preventDefault();
        if (selectedIndex >= 0 && suggestions[selectedIndex]) {
            userInput.value = suggestions[selectedIndex].textContent;
            suggestionsDiv.innerHTML = "";
            sendMessage();
        }
    }
    suggestions.forEach((s, index) => s.classList.toggle("highlight", index === selectedIndex));
});

// Function to show auto-suggested replies
async function showAutoReplies(userMessage) {
    const response = await fetch(`/auto-replies?query=${encodeURIComponent(userMessage)}`);
    const autoReplies = await response.json();
    autoRepliesDiv.innerHTML = autoReplies.map(reply =>
        `<button class="auto-reply" onclick="selectAndSend('${reply}')">${reply}</button>`
    ).join("");
}

// Function to send message
async function sendMessage() {
    const userMessage = userInput.value.trim();
    if (!userMessage) return;

    messagesDiv.innerHTML += `
        <div class="message user-message">
            <div class="message-content">${userMessage}</div>
            <div class="message-meta">You</div>
        </div>
    `;

    userInput.value = '';
    typingIndicator.style.display = 'block';  
    typingIndicator.innerText = "ChatGPT is typing..."; 

    try {
        const response = await fetch('/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message: userMessage }),
        });

        const data = await response.json();

        setTimeout(() => {
            typingIndicator.style.display = 'none';
            typeWriterEffect(data.message);  
            showAutoReplies(userMessage);
            scrollToBottom();  // 📌 Auto-scroll to latest message
        }, 1000); 
         

    } catch (error) {
        messagesDiv.innerHTML += `
            <div class="message bot-message error-message">
                <div class="message-content">Error: Unable to fetch response.</div>
            </div>
        `;
        typingIndicator.style.display = 'none';
    }
}

// ✨ Typewriter Effect Function ✨
function typeWriterEffect(text) {
    let index = 0;
    const botMessageDiv = document.createElement("div");
    botMessageDiv.classList.add("message", "bot-message");
    const messageContent = document.createElement("div");
    messageContent.classList.add("message-content");
    botMessageDiv.appendChild(messageContent);
    messagesDiv.appendChild(botMessageDiv);

    function type() {
        if (index < text.length) {
            messageContent.innerHTML += text.charAt(index);
            index++;
            setTimeout(type, 40);
        } else {
            scrollToBottom();  // 📌 Auto-scroll after message completes
        }
    }
    type();
}





// Function to scroll chat to bottom
function scrollToBottom() {
    setTimeout(() => {
        chatBox.scrollTop = chatBox.scrollHeight;
    }, 100); // Small delay to ensure smooth scrolling
}


// Function to handle quick emoji reactions
function addReactions(messageElement) {
    const emojiReactions = ['👍', '😊', '❓'];
    const reactionDiv = document.createElement("div");
    reactionDiv.classList.add("reaction-container");
    emojiReactions.forEach(emoji => {
        const button = document.createElement("button");
        button.textContent = emoji;
        button.classList.add("emoji-reaction");
        button.onclick = () => messageElement.append(emoji);
        reactionDiv.appendChild(button);
    });
    messageElement.appendChild(reactionDiv);
}


