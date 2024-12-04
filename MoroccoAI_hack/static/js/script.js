// static/js/script.js
document.addEventListener('DOMContentLoaded', function() {
    const messageInput = document.getElementById('message-input');
    const sendButton = document.getElementById('send-button');
    const chatMessages = document.getElementById('chat-messages');
    const fileUpload = document.getElementById('file-upload');
    const imagePreview = document.getElementById('image-preview');
    const agentRadios = document.querySelectorAll('input[name="agent"]');

    let currentFile = null;

    function addMessage(text, isUser, timestamp, imageUrl = null) {
        const messageContainer = document.createElement('div');
        messageContainer.className = `message-container ${isUser ? 'user' : 'bot'}`;
        
        const profileImg = document.createElement('img');
        profileImg.className = 'profile-image';
        profileImg.src = isUser ? '/static/images/user-profile.png' : '/static/images/bot-profile.png';
        profileImg.alt = isUser ? 'User' : 'Bot';
        
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${isUser ? 'user' : 'bot'}`;
        
        // If there's an image, add it first
        if (imageUrl) {
            const messageImage = document.createElement('img');
            messageImage.className = 'message-image';
            messageImage.src = imageUrl;
            messageImage.alt = 'Sent image';
            messageDiv.appendChild(messageImage);
        }
        
        // Add text if present
        if (text) {
            const messageText = document.createElement('div');
            messageText.className = 'message-text';
            messageText.textContent = text;
            messageDiv.appendChild(messageText);
        }
        
        const timestampDiv = document.createElement('div');
        timestampDiv.className = 'timestamp';
        timestampDiv.textContent = timestamp;
        messageDiv.appendChild(timestampDiv);
        
        messageContainer.appendChild(profileImg);
        messageContainer.appendChild(messageDiv);
        
        chatMessages.appendChild(messageContainer);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    function handleFileSelect(event) {
        const file = event.target.files[0];
        if (file) {
            currentFile = file;
            const reader = new FileReader();
            reader.onload = function(e) {
                const img = document.createElement('img');
                img.src = e.target.result;
                imagePreview.innerHTML = '';
                imagePreview.appendChild(img);
            };
            reader.readAsDataURL(file);
        }
    }

    async function sendMessage() {
        const message = messageInput.value.trim();
        const currentAgent = document.querySelector('input[name="agent"]:checked').value;

        if (!message && !currentFile) return;

        const formData = new FormData();
        formData.append('message', message);
        formData.append('agent_type', currentAgent);
        
        let imageUrl = null;
        if (currentFile) {
            formData.append('image', currentFile);
            imageUrl = URL.createObjectURL(currentFile);
        }

        // Add user message immediately
        addMessage(message, true, new Date().toLocaleTimeString('en-US', { 
            hour: 'numeric', 
            minute: 'numeric', 
            hour12: true 
        }), imageUrl);
        
        // Clear input and image preview
        messageInput.value = '';
        imagePreview.innerHTML = '';
        currentFile = null;

        try {
            const response = await fetch('/send_message', {
                method: 'POST',
                body: formData
            });
            
            const data = await response.json();
            if (data.status === 'success') {
                addMessage(data.response, false, data.timestamp);
            } else {
                addMessage('Error: ' + data.message, false, new Date().toLocaleTimeString());
            }
        } catch (error) {
            console.error('Error:', error);
            addMessage('Error sending message', false, new Date().toLocaleTimeString());
        }
    }

    // Event Listeners
    if (messageInput) {
        messageInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                sendMessage();
            }
        });
    }

    if (sendButton) {
        sendButton.addEventListener('click', () => {
            sendMessage();
        });
    }

    if (fileUpload) {
        fileUpload.addEventListener('change', handleFileSelect);
    }

    // Clear chat when changing agents
    agentRadios.forEach(radio => {
        radio.addEventListener('change', () => {
            chatMessages.innerHTML = '';
        });
    });
});