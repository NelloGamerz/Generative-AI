// Event listener for the Send button click
document.getElementById('sendButton').addEventListener('click', sendMessage);

// Event listener for the Enter key press
document.getElementById('questionInput').addEventListener('keydown', function (e) {
    if (e.key === 'Enter') {
        e.preventDefault();  // Prevent default action (like form submission)
        sendMessage();
    }
});

function sendMessage() {
    const userInput = document.getElementById('questionInput').value;

    if (userInput.trim() !== '') {
        addUserMessage(userInput);
        document.getElementById('questionInput').value = '';  // Clear the input after sending

        // Send the user input to the backend API
        fetch('/api', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ text: userInput })
        })
            .then(response => response.json())
            .then(data => {
                if (data.response) {
                    addResponseMessage(data.response);
                }
            })
            .catch(error => {
                console.error('Error:', error);
            });
    }
}

function addUserMessage(message) {
    const chatContainer = document.getElementById('chatContainer');
    const userBubble = document.createElement('div');
    userBubble.classList.add('chat-bubble', 'user-bubble');
    userBubble.textContent = message;
    chatContainer.appendChild(userBubble);
    chatContainer.scrollTop = chatContainer.scrollHeight;  // Scroll to bottom
}

function addResponseMessage(message) {
    const chatContainer = document.getElementById('chatContainer');
    const responseBubble = document.createElement('div');
    responseBubble.classList.add('chat-bubble', 'response-bubble');
    
    // Check if the message contains code by looking for the "```" flag
    if (message.includes('```')) {
        const codeContent = message.match(/```(\w+)?\n([\s\S]*?)```/);
        const language = codeContent[1] || 'javascript';  // Default to JavaScript if no language is specified
        const codeText = codeContent[2];

        // Create a <pre><code> block with syntax highlighting
        responseBubble.innerHTML = `
            <pre><code class="language-${language}">${codeText}</code></pre>
        `;
    } else {
        // For regular text responses
        responseBubble.textContent = message;
    }

    chatContainer.appendChild(responseBubble);
    chatContainer.scrollTop = chatContainer.scrollHeight;  // Scroll to bottom

    // Trigger Prism.js to highlight the newly added code block
    Prism.highlightAllUnder(chatContainer);
}

// Function to add a chat bubble (user or response)
function addChatBubble(message, isUser) {
    const chatBubble = document.createElement('div');
    chatBubble.classList.add('chat-bubble');

    // If it's a user message, apply the user-bubble style
    if (isUser) {
        chatBubble.classList.add('user-bubble');
    } else {
        chatBubble.classList.add('response-bubble');
    }

    // Format the message to support bullet points and highlights
    const formattedMessage = formatMessage(message);
    
    chatBubble.innerHTML = formattedMessage; // Use innerHTML to set formatted content
    chatContainer.appendChild(chatBubble);
    chatContainer.scrollTop = chatContainer.scrollHeight; // Scroll to bottom
}

// Function to format the message
function formatMessage(message) {
    // Replace **text** with <strong>text</strong>
    message = message.replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>'); // Bold
    // Replace *text* with <em>text</em>
    message = message.replace(/\*(.+?)\*/g, '<em>$1</em>'); // Italics
    // Replace line breaks
    message = message.replace(/\n/g, '<br>'); // Line breaks
    // Replace bullet points
    message = message.replace(/• (.+?)(?=\n|$)/g, '<li>$1</li>'); // Bullet points

    // Wrap unordered lists in <ul> tags
    message = message.replace(/<li>(.*?)<\/li>/g, '<ul><li>$1</li></ul>');
    message = message.replace(/<\/ul><ul>/g, ''); // Remove extra wrapping

    // Remove any asterisks left
    message = message.replace(/\*/g, ''); // Remove any stray asterisks

    return message;
}
