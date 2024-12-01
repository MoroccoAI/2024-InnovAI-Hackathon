import { jsPDF } from "jspdf";

const API_URL = import.meta.env.VITE_API_URL_LOCALHOST;


let chatHistory = [];

export function initChat() {
    const sendButton = document.getElementById('send-message');
    const chatMessages = document.getElementById('chat-messages');
    const userInput = document.getElementById('user-input');
    const fileUpload = document.getElementById('file-upload');

    // Check backend health on initialization
    checkBackendHealth();

    sendButton.addEventListener('click', handleMessage);
    userInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            handleMessage();
        }
    });

    async function checkBackendHealth() {
        try {
            const response = await fetch(`${API_URL}/health`);
            if (!response.ok) {
                appendMessage('system', 'Warning: AI service is currently unavailable. Please try again later.');
            }
        } catch (error) {
            appendMessage('system', 'Warning: Unable to connect to AI service. Please ensure the backend server is running.');
        }
    }

    async function handleMessage() {
        const message = userInput.value.trim();
        const files = fileUpload.files;

        if (message || files.length > 0) {
            // Disable send button and user input
            sendButton.disabled = true;
            userInput.disabled = true;

            appendMessage('user', message);

            let classificationMessage = null;

            if (files.length > 0) {
                const imageFile = files[0];
                appendImage(imageFile);

                // Wait for the classification result
                classificationMessage = await handleFileUpload(imageFile);
            }

            // Add user message to chatHistory
            chatHistory.push({ role: 'user', content: message });

            // Combine user message with classification result for the current query
            const currentQuery = [];
            if (classificationMessage) {
                currentQuery.push({ role: 'system', content: classificationMessage });
            }
            if (message) {
                currentQuery.push({ role: 'user', content: message });
            }

            console.log('Current query sent to backend:', currentQuery);
            console.log('Full chat history:', chatHistory);

            userInput.value = '';
            fileUpload.value = '';

            const loadingMessage = appendMessage('system', 'Processing your request...');

            try {
                const response = await fetch(`${API_URL}/chat`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        chatHistory, // Send full conversation history
                        messages: currentQuery, // Send the current query separately
                    }),
                });

                if (!response.ok) throw new Error('Network response was not ok');

                const reader = response.body.getReader();
                const decoder = new TextDecoder();
                let assistantMessage = '';
                let messageDiv = appendMessage('assistant', '');

                while (true) {
                    const { value, done } = await reader.read();
                    if (done) break;
                    const chunk = decoder.decode(value, { stream: true });
                    assistantMessage += chunk;

                    const renderedMarkdown = marked.parse(assistantMessage);
                    messageDiv.querySelector('p').innerHTML = renderedMarkdown;
                    chatMessages.scrollTop = chatMessages.scrollHeight;
                }

                // Add assistant's message to chatHistory
                chatHistory.push({ role: 'assistant', content: assistantMessage });
                loadingMessage.remove();

                // Re-enable send button and user input
                sendButton.disabled = false;
                userInput.disabled = false;
            } catch (error) {
                console.error('Error:', error);
                loadingMessage.remove();
                appendMessage('system', `Error: ${error.message || 'Unable to process your request.'}`);

                // Re-enable send button and user input in case of an error
                sendButton.disabled = false;
                userInput.disabled = false;
            }
        }
    }

    async function handleFileUpload(file) {
        const classificationResult = await classifyImage(file);
        if (classificationResult) {
            const classificationMessage = `Image Classification: ${classificationResult.label} (Score: ${classificationResult.score})`;

            // Append classification result to chat interface
            const lastUserMessage = chatMessages.querySelectorAll('.message.user');
            const appendedFileMessage = lastUserMessage[lastUserMessage.length - 1];

            if (appendedFileMessage) {
                appendedFileMessage.querySelector('.message-content').innerHTML += `
                    <p>${classificationMessage}</p>
                `;
            } else {
                appendMessage('system', classificationMessage);
            }

            // Return classification result for inclusion in the current query
            return classificationMessage;
        }
        return null;
    }

    async function classifyImage(image) {
        try {
            const formData = new FormData();
            formData.append('image', image);

            const response = await fetch(`${API_URL}/classify-image`, {
                method: 'POST',
                body: formData,
            });

            if (response.ok) {
                const result = await response.json();
                return { label: result.label, score: result.score };
            } else {
                throw new Error('Image classification failed');
            }
        } catch (error) {
            console.error('Error classifying image:', error);
            return null;
        }
    }

    function appendMessage(role, content) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${role}`;

        let displayName = role === 'user' ? 'User' :
                         role === 'assistant' ? 'MediBot:' :
                         'System';

        messageDiv.innerHTML = `
            <div class="message-content">
                <strong>${displayName}:</strong>
                <p>${content}</p>
            </div>
        `;
        chatMessages.appendChild(messageDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
        return messageDiv;
    }

    function appendImage(file) {
        const reader = new FileReader();
        reader.onload = function(event) {
            const messageDiv = document.createElement('div');
            messageDiv.className = 'message user';

            const displayName = 'User';
            messageDiv.innerHTML = `
                <div class="message-content">
                    <strong>${displayName}:</strong>
                    <p><img src="${event.target.result}" alt="${file.name}" class="uploaded-image"></p>
                </div>
            `;

            chatMessages.appendChild(messageDiv);
            chatMessages.scrollTop = chatMessages.scrollHeight;
        };
        reader.readAsDataURL(file);
    }

    // Toggle button to show the notification
    document.getElementById('toggle-instructions').addEventListener('click', () => {
        const overlay = document.getElementById('overlay');
        const isVisible = overlay.style.display === 'block';
        overlay.style.display = isVisible ? 'none' : 'block';
        document.getElementById('toggle-instructions').textContent = isVisible ? 'Show Instructions' : 'Hide Instructions';
    });

    // Close button inside the notification
    document.getElementById('close-instructions').addEventListener('click', () => {
        const overlay = document.getElementById('overlay');
        overlay.style.display = 'none';
        document.getElementById('toggle-instructions').textContent = 'Show Instructions';
    });

    document.getElementById('download-pdf').addEventListener('click', async () => {
    const doc = new jsPDF();
    let y = 20; // Initial y position for text
    const lineHeight = 6;
    const pageHeight = doc.internal.pageSize.height;
    const logo = 'data:image/jpeg;base64,...'; // Replace with your base64 encoded JPG logo

    // Adding a title
    doc.setFontSize(16);
    doc.text(10, y, 'Chat History');
    y += 10; // Adding some space after the title

    // Setting font size for the chat content
    doc.setFontSize(12);

    for (const entry of chatHistory) {
        // Adding logo to the top right corner of each page
        const currentPage = doc.internal.getCurrentPageInfo().pageNumber;
        if (currentPage > 1) {
            doc.addImage(logo, 'JPEG', doc.internal.pageSize.width - 60, 10, 50, 20);
        }

        if (entry.role === 'user' && entry.content.includes('data:image')) {
            // Handle image entries
            const img = entry.content.match(/data:image\/[a-zA-Z]+;base64,[^\s]+/)[0];
            const imgProps = doc.getImageProperties(img);
            const imgHeight = (imgProps.height * 50) / imgProps.width;

            if (y + imgHeight > pageHeight - 10) { // Check if image fits on current page
                doc.addPage();
                y = 10;
                doc.addImage(logo, 'JPEG', doc.internal.pageSize.width - 60, 10, 50, 20); // Adding logo to new page
            }

            doc.addImage(img, 'PNG', 10, y, 50, imgHeight); // Add image to the PDF
            y += imgHeight + 10; // Move y position down to accommodate the image
        } else {
            // Handle text entries
            doc.setFont("helvetica", entry.role === 'user' ? "bold" : "normal");
            const lines = doc.splitTextToSize(entry.content.replace(/[\*\_\`]/g, ''), 180); // Splitting text into multiple lines if it's too long

            lines.forEach(line => {
                if (y + lineHeight > pageHeight - 10) { // Check if text fits on current page
                    doc.addPage();
                    y = 10;
                    doc.addImage(logo, 'JPEG', doc.internal.pageSize.width - 60, 10, 50, 20); // Adding logo to new page
                }
                doc.text(10, y, line);
                y += lineHeight;
            });

            y += 4; // Adding some space between entries
        }

        if (entry.classificationResult) {
            // Add classification result
            doc.setFont("helvetica", "italic");
            const classificationText = `Classification: ${entry.classificationResult.label}, Score: ${entry.classificationResult.score}`;

            if (y + lineHeight > pageHeight - 10) { // Check if text fits on current page
                doc.addPage();
                y = 10;
                doc.addImage(logo, 'JPEG', doc.internal.pageSize.width - 60, 10, 50, 20); // Adding logo to new page
            }

            doc.text(10, y, classificationText);
            y += 10;
        }
    }

    doc.save('chat-history.pdf');
});

    
    
    
    // Function to set a static assistant message
    function setStaticAssistantMessage() {
        const messageContent = "Hi! I'm MediBot an AI Assistant tasked to help healthcare professionals make informed decisions. Do you have a medical question, case you'd like to discuss, or a project you need help with? Let me know and I'll do my best to provide you with accurate and informative responses.";

        const messageDiv = document.createElement('div');
        messageDiv.className = 'message assistant';

        messageDiv.innerHTML = `
            <div class="message-content">
                <strong>MediBot:</strong>
                <p>${messageContent}</p>
            </div>
        `;

        const chatMessages = document.getElementById('chat-messages');
        chatMessages.appendChild(messageDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    // Call the function to set the static message
    setStaticAssistantMessage();


    
}
