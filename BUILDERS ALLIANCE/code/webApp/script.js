document.addEventListener('DOMContentLoaded', () => {
    const chatBody = document.querySelector('.chat-body');
    const chatInput = document.querySelector('.chat-footer input');
    const sendButton = document.querySelector('.chat-footer button');

    const addMessage = (message, type) => {
        const messageElement = document.createElement('div');
        messageElement.classList.add('chat-message', `${type}-message`);
        messageElement.textContent = message;
        chatBody.appendChild(messageElement);
        chatBody.scrollTop = chatBody.scrollHeight;
    };


    const fetchBotResponse = async (userInput) => {
        try {
            console.log('Sending request to API with payload:', { user_input: userInput });

            const response = await fetch('http://localhost:3000/api/generate-response', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ user_input: userInput }),
            });

            console.log('API Response Status:', response.status, response.statusText);

            if (!response.ok) {
                console.error('API error:', response.status, response.statusText);
                throw new Error('Failed to fetch response from the server');
            }

            const data = await response.json();
            console.log('Response received:', data);

            return data?.answer || 'The bot did not provide a response. Please try again.';
        } catch (error) {
            console.error('Error fetching bot response:', error);
            return 'Sorry, something went wrong. Please try again later.';
        }
    };

    sendButton.addEventListener('click', async () => {
        const message = chatInput.value.trim();
        if (message) {
            addMessage(message, 'user');
            chatInput.value = '';

            console.log('Calling fetchBotResponse...');
            const botResponse = await fetchBotResponse(message);
            console.log('Bot Response:', botResponse);
            addMessage(botResponse, 'bot');
        }
    });

    chatInput.addEventListener('keypress', (event) => {
        if (event.key === 'Enter') {
            sendButton.click();
        }
    });

    const changeBackground = () => {
        const photos = [
            'Logo/background2.jpg',
            'Logo/background3.jpg',
            'Logo/background1.jpg',
            'Logo/background4.jpg',
            'Logo/background5.jpg',
        ];
        let currentIndex = 0;

        setInterval(() => {
            document.body.style.backgroundImage = `url('${photos[currentIndex]}')`;
            currentIndex = (currentIndex + 1) % photos.length;
        }, 10000);
    };

    changeBackground();
});
