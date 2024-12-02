const discussions = document.querySelector("#discussions");

// Vérification de la prise en charge de la reconnaissance vocale
window.SpeechRecognition =
    window.SpeechRecognition || window.webkitSpeechRecognition;

function open_site() {
    window.open("https://www.youtube.com/@AryadAcademie");
    return "Ouverture de la chaîne YouTube";
}

function scrollToBottom() {
    discussions.scrollTop = discussions.scrollHeight;
}

if (!window.SpeechRecognition) {
    discussions.innerHTML = "<p>Votre navigateur ne supporte pas la reconnaissance vocale.</p>";
} else {
    const recognition = new SpeechRecognition();
    recognition.interimResults = true;
    recognition.lang = "fr-FR"; // Définit la langue en français

    recognition.addEventListener("result", async (e) => {
        // Traite le texte reconnu
        const text = Array.from(e.results)
            .map((result) => result[0])
            .map((result) => result.transcript)
            .join("");

        

        // Si le résultat est final, appelle l'API
        if (e.results[0].isFinal) {
            try {
                // Ajoute le texte reconnu à un nouvel élément
                const discussion = document.createElement("div");
                discussion.className = "discussion";

                const words = document.createElement("p");
                words.className = "words";
                words.innerText = text;

                discussion.appendChild(words);
                discussions.appendChild(discussion);
                scrollToBottom();

                const response = await fetch("http://127.0.0.1:8000/endpoint", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                    },
                    body: JSON.stringify({ query: text }),
                });

                if (!response.ok) {
                    throw new Error(`Erreur serveur : ${response.status}`);
                }

                const data = await response.json();
                const reply = data.response || "Aucune réponse disponible.";

                // Affiche la réponse
                const replyElement = document.createElement("p");
                replyElement.classList.add("reply");
                replyElement.innerText = reply;

                const replyDiv = document.createElement("div");
                replyDiv.className = "discussion";
                replyDiv.appendChild(replyElement);

                discussions.appendChild(replyDiv);

                // Joue la réponse avec la synthèse vocale
                const utterance = new SpeechSynthesisUtterance(reply);
                utterance.lang = "fr-FR";
                speechSynthesis.speak(utterance);
            } catch (error) {
                console.error("Erreur lors de l'appel à l'API :", error);
                const errorElement = document.createElement("p");
                errorElement.classList.add("error");
                errorElement.innerText =
                    "Une erreur est survenue lors de l'appel à l'API.";
                discussions.appendChild(errorElement);
            }
        }
    });const texts = document.querySelector(".texts");

    window.SpeechRecognition =
        window.SpeechRecognition || window.webkitSpeechRecognition;
    
    function open_site() {
        window.open("https://www.youtube.com/@AryadAcademie");
        return "Ouverture de la chaîne YouTube";
    }
    
    if (!window.SpeechRecognition) {
        texts.innerHTML = "<p>Votre navigateur ne supporte pas la reconnaissance vocale.</p>";
    } else {
        const recognition = new SpeechRecognition();
        recognition.interimResults = true;
        recognition.lang = "fr-FR"; // Définit la langue sur le français
    
        let p = document.createElement("p");
    
        recognition.addEventListener("result", async (e) => {
            // Ajoute un nouveau paragraphe si nécessaire
            if (!texts.lastChild || texts.lastChild.tagName !== "P") {
                p = document.createElement("p");
                texts.appendChild(p);
            }
    
            // Traite le texte reconnu
            const text = Array.from(e.results)
                .map((result) => result[0])
                .map((result) => result.transcript)
                .join("");
    
            p.innerText = text;
            texts.appendChild(p);
    
            // Si le résultat est final, envoie la requête à l'API
            if (e.results[0].isFinal) {
                try {
                    // Envoie la requête à l'API
                    const response = await fetch("http://127.0.0.1:8000/endpoint", {
                        method: "POST",
                        headers: {
                            "Content-Type": "application/json",
                        },
                        body: JSON.stringify({ query: text }),
                    });
    
                    // Vérifie si la requête a réussi
                    if (!response.ok) {
                        throw new Error(`Erreur serveur : ${response.status}`);
                    }
    
                    const data = await response.json();
                    const reply = data.response || "Aucune réponse disponible.";
    
                    // Affiche la réponse
                    const replyElement = document.createElement("p");
                    replyElement.classList.add("reply");
                    replyElement.innerText = reply;
                    texts.appendChild(replyElement);
    
                    // Joue la réponse avec la synthèse vocale
                    const utterance = new SpeechSynthesisUtterance(reply);
                    utterance.lang = "fr-FR"; // Définit la langue de la synthèse vocale
                    speechSynthesis.speak(utterance);
                } catch (error) {
                    console.error("Erreur lors de l'appel à l'API :", error);
                    const errorElement = document.createElement("p");
                    errorElement.classList.add("error");
                    errorElement.innerText = "Une erreur est survenue lors de l'appel à l'API.";
                    texts.appendChild(errorElement);
                }
    
                // Réinitialise pour la prochaine reconnaissance
                p = document.createElement("p");
            }
        });
    
        recognition.addEventListener("end", () => {
            recognition.start(); // Redémarre la reconnaissance
        });
    
        recognition.addEventListener("error", (e) => {
            console.error("Speech recognition error:", e.error);
            const errorElement = document.createElement("p");
            errorElement.classList.add("error");
            errorElement.innerText = `Une erreur est survenue : ${e.error}`;
            texts.appendChild(errorElement);
        });
    
        recognition.start();
    }
    

    recognition.addEventListener("end", () => {
        recognition.start(); // Redémarre la reconnaissance
    });

    recognition.addEventListener("error", (e) => {
        console.error("Speech recognition error:", e.error);
        const errorElement = document.createElement("p");
        errorElement.classList.add("error");
        errorElement.innerText = `Une erreur est survenue : ${e.error}`;
        discussions.appendChild(errorElement);
    });
    scrollToBottom();
    recognition.start();
}




const texts = document.querySelector(".texts");

window.SpeechRecognition =
    window.SpeechRecognition || window.webkitSpeechRecognition;

function open_site() {
    window.open("https://www.youtube.com/@AryadAcademie");
    return "Ouverture de la chaîne YouTube";
}

if (!window.SpeechRecognition) {
    texts.innerHTML = "<p>Votre navigateur ne supporte pas la reconnaissance vocale.</p>";
} else {
    const recognition = new SpeechRecognition();
    recognition.interimResults = true;
    recognition.lang = "fr-FR"; // Définit la langue sur le français

    let p = document.createElement("p");

    recognition.addEventListener("result", async (e) => {
        // Ajoute un nouveau paragraphe si nécessaire
        if (!texts.lastChild || texts.lastChild.tagName !== "P") {
            p = document.createElement("p");
            texts.appendChild(p);
        }

        // Traite le texte reconnu
        const text = Array.from(e.results)
            .map((result) => result[0])
            .map((result) => result.transcript)
            .join("");

        p.innerText = text;
        texts.appendChild(p);

        // Si le résultat est final, envoie la requête à l'API
        if (e.results[0].isFinal) {
            try {
                // Envoie la requête à l'API
                const response = await fetch("http://127.0.0.1:8000/endpoint", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                    },
                    body: JSON.stringify({ query: text }),
                });

                // Vérifie si la requête a réussi
                if (!response.ok) {
                    throw new Error(`Erreur serveur : ${response.status}`);
                }

                const data = await response.json();
                const reply = data.response || "Aucune réponse disponible.";

                // Affiche la réponse
                const replyElement = document.createElement("p");
                replyElement.classList.add("reply");
                replyElement.innerText = reply;
                texts.appendChild(replyElement);

                // Joue la réponse avec la synthèse vocale
                const utterance = new SpeechSynthesisUtterance(reply);
                utterance.lang = "fr-FR"; // Définit la langue de la synthèse vocale
                speechSynthesis.speak(utterance);
            } catch (error) {
                console.error("Erreur lors de l'appel à l'API :", error);
                const errorElement = document.createElement("p");
                errorElement.classList.add("error");
                errorElement.innerText = "Une erreur est survenue lors de l'appel à l'API.";
                texts.appendChild(errorElement);
            }

            // Réinitialise pour la prochaine reconnaissance
            p = document.createElement("p");
        }
    });

    recognition.addEventListener("end", () => {
        recognition.start(); // Redémarre la reconnaissance
    });

    recognition.addEventListener("error", (e) => {
        console.error("Speech recognition error:", e.error);
        const errorElement = document.createElement("p");
        errorElement.classList.add("error");
        errorElement.innerText = `Une erreur est survenue : ${e.error}`;
        texts.appendChild(errorElement);
    });

    recognition.start();
}
