let selectedVoiceName = localStorage.getItem('selectedVoice');
document.getElementById("finish").disabled = true; 
let voices = [];
let selectedVoice = null;
let maleVoice = null;
let femaleVoice = null;

// Récupération des données depuis le localStorage
const title = localStorage.getItem("title");
const description = localStorage.getItem("description");
const name_company = localStorage.getItem("name_company");

// Charger les voix disponibles
function loadVoices() {
    voices = speechSynthesis.getVoices();

    // Sélectionner les voix spécifiées
    maleVoice = voices.find(voice => voice.name.includes("Microsoft Mark") && voice.lang === "en-US");
    femaleVoice = voices.find(voice => voice.name.includes("Google US") && voice.lang === "en-US");
    const dave = voices.find(voice => voice.name.includes("Microsoft David") && voice.lang === "en-US"); 

    // Appliquer la voix sélectionnée
    if (selectedVoiceName) {
        if (selectedVoiceName.includes("homme")) {
            selectedVoice = maleVoice;
        } else if (selectedVoiceName.includes("femme")) {
            selectedVoice = femaleVoice;
        } else {
            selectedVoice = dave;
        }
    }
}

// Vérifier si les voix sont chargées
speechSynthesis.onvoiceschanged = loadVoices;

// Charger immédiatement si les voix sont déjà disponibles
loadVoices();

const wave = document.querySelector("#wave-container");
const texts = document.querySelector(".texts");
wave.style.display = "none";

// Vérification de la compatibilité du navigateur
window.SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;

if (!window.SpeechRecognition) {
    texts.innerHTML = "<p>Votre navigateur ne supporte pas la reconnaissance vocale.</p>";
} else {
    let recognition;
    let isRecognizing = false;
    let currentQuestion = '';
    let isSpeaking = false;
    let silenceTimer;

    // Fonction pour la synthèse vocale
    function speakMessage(message, callback) {
        const utterance = new SpeechSynthesisUtterance(message);
        utterance.lang = "en-US";
        utterance.voice = selectedVoice; // Appliquer la voix sélectionnée
        wave.style.display = "block";

        utterance.onstart = () => {
            isSpeaking = true;
        };

        utterance.onend = () => {
            isSpeaking = false;
            wave.style.display = "none";
            if (callback) callback(); // Appeler le callback une fois la synthèse terminée
        };

        speechSynthesis.speak(utterance);
    }

    // Fonction pour démarrer la reconnaissance vocale
    function startRecognition() {
        if (isRecognizing || isSpeaking) return;

        recognition = new SpeechRecognition();
        recognition.interimResults = true;
        recognition.lang = "en-US";

        recognition.addEventListener("result", async (e) => {
            if (isSpeaking) return;

            let text = Array.from(e.results)
                .map(result => result[0].transcript)
                .join("");

            currentQuestion = text;

            if (e.results[0].isFinal) {
                const questionElement = document.createElement("p");
                questionElement.className = "question";
                questionElement.innerText = currentQuestion;
                texts.appendChild(questionElement);

                try {
                    const response = await fetch("http://127.0.0.1:8000/endpoint", {
                        method: "POST",
                        headers: { "Content-Type": "application/json" },
                        body: JSON.stringify({ query: currentQuestion }),
                    });

                    if (!response.ok) throw new Error(`Erreur serveur : ${response.status}`);

                    const data = await response.json();
                    const reply = data.response || "Aucune réponse disponible.";

                    const replyElement = document.createElement("p");
                    replyElement.classList.add("reply");
                    replyElement.innerText = reply;
                    texts.appendChild(replyElement);


                    if (reply.toLowerCase().includes("end interview")||reply.toLowerCase().includes("end the interview")) {
                        recognition.stop();
                        isRecognizing = false;
                        speechSynthesis.cancel();
                        stopCamera();
                        
                        sendEndTime2(document.getElementById("duration").value)

                        const finishElement = document.getElementById("finish");
                        if (finishElement) {
                            finishElement.style.background = "#957195";
                            finishElement.disabled = false;
                        }

                        const waveContainer = document.getElementById("wave-container");
                        if (waveContainer) {
                            waveContainer.style.display = "none";
                        }

                        const startCamera = document.getElementById("start-camera");
                        if (startCamera) {
                            startCamera.disabled = true;
                        }

                        return;
                    }

                    recognition.stop();
                    isRecognizing = false;


                    // Synthèse vocale de la réponse
                    speakMessage(reply, () => {
                        setTimeout(startRecognition, 3000);
                    });
                } catch (error) {
                    console.error("Erreur lors de l'appel à l'API :", error);
                    const errorElement = document.createElement("p");
                    errorElement.classList.add("error");
                    errorElement.innerText = "Une erreur est survenue lors de l'appel à l'API.";
                    texts.appendChild(errorElement);
                }

                currentQuestion = '';
            }

            // Clear the previous timer if it exists
    clearTimeout(silenceTimer);

    // Set a new timer for 30 seconds
    silenceTimer = setTimeout(() => {
        if (!isSpeaking) {

            recognition.stop();
            isRecognizing = false;
            speechSynthesis.cancel();
            stopCamera();
            sendEndTime2(document.getElementById("duration").value)
            
            document.getElementById("pressmidlle").innerHTML=""
            let p = document.createElement("p");
            p.innerHTML="END INTERVIEW";
            document.getElementById("pressmidlle").appendChild(p);
            document.getElementById("wave-container").style.display="None";
            document.getElementById("finish").disabled = false;
        }
    }, 30000);

        });

        recognition.addEventListener("end", () => {
            if (!isSpeaking && !isRecognizing) {
                recognition.start();
            }
        });

        recognition.addEventListener("error", (e) => {
            console.error("Speech recognition error:", e.error);
            const errorElement = document.createElement("p");
            errorElement.classList.add("error");
            errorElement.innerText = `Une erreur est survenue : ${e.error}`;
            texts.appendChild(errorElement);
        });

        recognition.start();
        isRecognizing = true;
    }

    async function startProcess() {
        try {
            const response = await fetch("http://127.0.0.1:8000/endpoint", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ query: "None" }),
            });

            if (!response.ok) throw new Error(`Erreur serveur : ${response.status}`);

            const data = await response.json();
            const reply = data.response || "Aucune réponse disponible.";

            if (reply.toLowerCase().includes("end interview")) {
                stopCamera();
                clearInterval(timerInterval);
                sendEndTime2(document.getElementById("duration").value);
                document.getElementById("finish").disabled = false;
                document.getElementById("finish").style.opacity = 1;
            }

            const replyElement = document.createElement("p");
            replyElement.classList.add("reply");
            replyElement.innerText = reply;
            texts.appendChild(replyElement);

            speakMessage(reply, startRecognition);
        } catch (error) {
            console.error("Erreur lors de l'appel à l'API :", error);
            const errorElement = document.createElement("p");
            errorElement.classList.add("error");
            errorElement.innerText = "Une erreur est survenue lors de l'appel à l'API.";
            texts.appendChild(errorElement);
        }
    }

    document.getElementById("startRecognitionBtn").addEventListener("click", startProcess);
}




function alarm() {
    const status = document.querySelector("#pressmidlle");
    const record = document.querySelector("#ondevoice");

    let text = "Recording ...";

    // Supprimer le contenu existant dans 'status'
    status.innerHTML = "";

    // Créer et insérer le nouveau paragraphe
    let message = document.createElement("p");
    message.innerHTML = text;
    status.appendChild(message);  // Remplace le contenu avec le nouveau texte
    // Commence le compteur dès le chargement
    startTimer();
    // Vérifie si la fonction startCamera est définie, sinon crée une fonction vide pour éviter des erreurs
    if (typeof startCamera === "function") {
        startCamera();  // Vérifie si cette fonction existe
    }
    record.style.display = "block";  // Affiche l'élément #ondevoice
}

let cameraStream = null; // Variable pour stocker le flux vidéo
function startCamera() {
    const video = document.getElementById("camera");

    // Vérifie si le navigateur supporte l'API getUserMedia
    if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
        navigator.mediaDevices.getUserMedia({ video: true }) // Accède à la caméra
            .then(function (stream) {
                cameraStream = stream; // Stocke le flux dans une variable globale
                video.srcObject = stream; // Associe le flux vidéo au <video>
            })
            .catch(function (error) {
                console.error("Erreur lors de l'accès à la caméra :", error);
                alert("Impossible d'accéder à la caméra. Vérifiez vos paramètres de confidentialité.");
            });
    } else {
        alert("Votre navigateur ne supporte pas l'accès à la caméra.");
    }
}

function stopCamera() {
    const video = document.getElementById("camera");

    if (cameraStream) {
        // Arrête toutes les pistes du flux vidéo
        cameraStream.getTracks().forEach((track) => track.stop());
        cameraStream = null; // Réinitialise la variable
    }

    // Retire la source vidéo pour libérer le <video>
    video.srcObject = null;
}



let durationElement = document.getElementById("duration");
let finishButton = document.getElementById("finish");

let seconds = 0;
let timerInterval;

// Fonction pour mettre à jour l'affichage de la durée
function updateDuration() {
    let minutes = Math.floor(seconds / 60);
    let remainingSeconds = seconds % 60;

    // Formate l'affichage des secondes avec un zéro initial si < 10
    durationElement.textContent = `${minutes}:${remainingSeconds.toString().padStart(2, "0")}`;
    seconds++;
}

// Démarre le compteur de temps
function startTimer() {
    timerInterval = setInterval(updateDuration, 1000); // Appelle `updateDuration` chaque seconde
}

// Fonction pour arrêter toutes les activités et rediriger
function finalizeProcess() {
    // Arrêter le timer si actif
    if (timerInterval) {
        clearInterval(timerInterval);
        timerInterval = null; // Réinitialiser pour éviter une double interruption
    }

    // Arrêter la caméra si en cours d'utilisation
    if (cameraStream) {
        stopCamera();
    }

    // Redirection vers la page de félicitations
    window.location.href = "http://127.0.0.1:8000/congrate";
}

// Associe le clic sur le bouton "Finish" à la fonction finalizeProcess
finishButton.addEventListener("click", finalizeProcess);




async function sendEndTime2(time) {
    // Préparer les données à envoyer
    const endTimeData = {
        remaining_time: time // Temps restant ou initial
    };

    console.log("Temps restant envoyé :", endTimeData); // Debug

    // URL de l'API pour enregistrer le temps de fin
    const apiUrl = "http://127.0.0.1:8000/api/quiz/save-end-time_interview";

    try {
        // Effectuer la requête POST
        const response = await fetch(apiUrl, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(endTimeData) // Convertir l'objet en JSON
        });

        // Vérifier si la réponse est OK
        if (!response.ok) {
            throw new Error(`Erreur lors de l'enregistrement du temps de fin : ${response.statusText}`);
        }

        // Essayer de récupérer les données JSON de la réponse
        const data = await response.json();
        console.log("Temps enregistré avec succès :", data);

    } catch (error) {
        console.error("Erreur lors de l'enregistrement du temps de fin :", error);
    }
}