function sendQuery() {
    const query = document.getElementById('queryInput').value;
    showQuery(query);
    document.getElementById('queryInput').value = ""; 

    
    const typingIndicator = document.createElement('div');
    typingIndicator.className = "typingIndicator";
    typingIndicator.textContent = '.';
    responseDiv.appendChild(typingIndicator);
    
    const typingInterval = setInterval(() => {
        typingIndicator.textContent += '.';
        if (typingIndicator.textContent.length > 3) typingIndicator.textContent = '.';
    }, 500)
    
    fetch(`http://127.0.0.1:8000/query?query=${query}`)
        .then(response => response.json())
        .then(data => {
            console.log("Data:", data);
        
            clearInterval(typingInterval);
            responseDiv.removeChild(typingIndicator);

            showResponse(data.response)}) 
        .catch(error => console.error('An error occurred:', error));
}

function showQuery(query) {
    const responseDiv = document.getElementById('responseDiv');
    const queryDiv = document.createElement('div');
    queryDiv.className = 'userMessage';
    queryDiv.textContent = query;
    responseDiv.appendChild(queryDiv);
    responseDiv.scrollTop = responseDiv.scrollHeight;
  }

function showResponse(response) {
    const responseDiv = document.getElementById('responseDiv');
    const responseDivMessage = document.createElement('div');
    responseDivMessage.className = 'botMessage';
    responseDivMessage.textContent = response.result;
    responseDiv.appendChild(responseDivMessage);

    
    const followUpDiv = document.createElement('div');
    followUpDiv.className = "botMessage";
    followUpDiv.textContent = "I hope I answered your question. Do you need any more help?";
    responseDiv.appendChild(followUpDiv);

    responseDiv.scrollTop = responseDiv.scrollHeight; 
}
