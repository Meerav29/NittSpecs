function sendMessage() {
    const userInput = document.getElementById('userInput');
    const message = userInput.value.trim();
    if (!message) return;

    // Display user message
    appendMessage('user', message);
    userInput.value = '';

    // Show loading indicator
    appendMessage('loading', 'Thinking...');

    // Send to backend
    fetch('/chat', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message: message })
    })
    .then(response => response.json())
    .then(data => {
        // Remove loading message
        document.querySelector('.loading-message')?.remove();
        
        if (data.error) {
            appendMessage('error', 'Sorry, something went wrong: ' + data.error);
        } else {
            appendMessage('bot', data.response);
        }
    })
    .catch(error => {
        // Remove loading message
        document.querySelector('.loading-message')?.remove();
        appendMessage('error', 'Sorry, something went wrong. Please try again.');
        console.error('Error:', error);
    });
}

function appendMessage(sender, message) {
    const chatBox = document.getElementById('chatBox');
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${sender}-message`;
    messageDiv.textContent = message;
    chatBox.appendChild(messageDiv);
    chatBox.scrollTop = chatBox.scrollHeight;
}