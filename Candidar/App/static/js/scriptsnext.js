let questions = [];
let currentIndex = 0;
let remainingTime = 45; // Temps total en secondes, ajustez selon vos besoins
let timerInterval; // Déclarez la variable du timer globalement

async function loadQuestions() {
    // **Afficher le loader pendant le chargement des questions**
    document.getElementById("loader").style.display = "block";

    // Récupération des données depuis le localStorage
    const title = localStorage.getItem("title");
    const description = localStorage.getItem("description");
    const name_company = localStorage.getItem("name_company");

    // URL de l'API
    const apiUrl = 'http://127.0.0.1:8000/api/quiz/endpoint';

    // Vérification si les données nécessaires existent
    if (!title || !description || !name_company) {
        console.error('Certains champs requis manquent dans le localStorage.');
        return;
    }

    // Préparer les données pour la requête
    const requestData = {
        title: title,
        description: description,
        name_company: name_company
    };

    try {
        // Envoyer la requête POST
        const response = await fetch(apiUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(requestData) // Convertir l'objet en JSON
        });

        // Vérifier si la réponse est correcte
        if (!response.ok) {
            throw new Error(`Erreur lors de la récupération des questions : ${response.statusText}`);
        }

        // Parser la réponse en JSON
        const responseData = await response.json();

        // Vérifier que les données renvoyées par l'API sont valides
        if (!responseData || !Array.isArray(responseData.data)) {
            throw new Error('Le format de réponse de l’API est invalide.');
        }

        questions = responseData.data; // Assurez-vous que l'API retourne les questions dans `data`

        // Charger la première question si disponible
        if (questions.length > 0) {
            loadQuestion(currentIndex); // Appeler une fonction pour afficher la première question

            // **Une fois les questions chargées, démarrer le quiz**
            startQuiz();
        } else {
            console.warn('Aucune question reçue de l’API.');
        }
    } catch (error) {
        // Gérer les erreurs
        console.error('Erreur lors du chargement des questions:', error);
    } finally {
        // **Masquer le loader une fois les questions chargées**
        document.getElementById("loader").style.display = "none";
    }
}

function loadQuestion(index) {
    const questionBox = document.getElementById("questionBox");
    questionBox.innerHTML = ""; // Efface les précédentes questions

    const currentQuestion = questions[index];

    const questionText = document.createElement("h3");
    questionText.textContent = currentQuestion.question;
    questionBox.appendChild(questionText);

    currentQuestion.options.forEach(option => {
        const optionContainer = document.createElement("div");
        optionContainer.className = "in_put";
        optionContainer.innerHTML = ` 
            <div>${option}</div>
            <div class="circle-in">
                <img src="/static/icons/Website flowchart -chek.svg" alt="Check" height="70%" width="70%">
            </div>
        `;
        optionContainer.addEventListener("click", () => selectOption(optionContainer));
        questionBox.appendChild(optionContainer);
    });
}

function selectOption(optionElement) {
    const allOptions = document.querySelectorAll(".in_put");
    allOptions.forEach(opt => opt.classList.remove("selected"));
    optionElement.classList.add("selected");

    // Capture de la réponse sélectionnée
    const selectedAnswer = optionElement.querySelector("div:first-child").textContent; // Texte de la réponse
    const currentQuestion = questions[currentIndex]; // Question actuelle

    // Appel pour sauvegarder la réponse
    saveCandidateAnswer(
        currentQuestion.question,
        selectedAnswer,
        currentQuestion.correct_answer
    );
}

document.getElementById("nextQuestionBtn").addEventListener("click", () => {
    const selectedOption = document.querySelector(".in_put.selected");
    if (!selectedOption) {
        alert("Please select an answer before proceeding.");
        return;
    }

    if (currentIndex < questions.length - 1) {
        currentIndex++;
        loadQuestion(currentIndex);
    } else {
        // Lorsque toutes les questions sont terminées
        sendEndTime(remainingTime); 
        disabled_btn();
        alert("You have completed the quiz. Thank you!");
        clearInterval(timerInterval); // Arrêter le timer   
        remainingTime = 0; // Optionnel: Si vous voulez aussi réinitialiser le timer à 0
    }
});

function disabled_btn() {
    const btnchangenext = document.querySelector("#btnchangenext");
    if (btnchangenext) {
        btnchangenext.disabled = true;
        btnchangenext.style.opacity = "0.5";
    }

    const btn_next = document.querySelector("#nextQuestionBtn");
    if (btn_next) {
        btn_next.disabled = true;
        btn_next.style.opacity = "0.5";
    }
}

// Initialisation du quiz et du timer
function startQuiz() {
    const timerElement = document.getElementById('timer');
    const progressCircle = document.getElementById('progress');

    // Temps total en secondes
    let totalTime = remainingTime;

    // Calcul de la circonférence
    const radius = 45;
    const circumference = 2 * Math.PI * radius;

    // Initialisation de la progression
    progressCircle.style.strokeDasharray = `${circumference}`;
    progressCircle.style.strokeDashoffset = `${circumference}`;

    function updateTimer() {
        const offset = (remainingTime / totalTime) * circumference;
        progressCircle.style.strokeDashoffset = `${offset}`;
        timerElement.textContent = remainingTime;
        remainingTime--;

        if (remainingTime == 0) {
            sendEndTime(remainingTime); 
            disabled_btn();
            clearInterval(timerInterval); // Arrêter le timer
            timerElement.textContent = "Fini!"; // Afficher le message
        }
    }

    // Mise à jour toutes les secondes
    timerInterval = setInterval(updateTimer, 1000); // Affectez l'intervalle globalement pour pouvoir l'arrêter plus tard
}

function saveCandidateAnswer(question, candidateAnswer, correctAnswer) {
    // Préparer les données à envoyer
    const answerData = {
        question: question,
        reponse_candidat: candidateAnswer,
        bonne_reponse: correctAnswer
    };

    console.log("Réponse sauvegardée :", answerData); // Pour vérifier dans la console

    // Si vous voulez envoyer à une API
    const apiUrl = "http://127.0.0.1:8000/api/quiz/save-answer"; // URL de l'API pour enregistrer les réponses

    fetch(apiUrl, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(answerData) // Convertir l'objet en JSON
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`Erreur lors de l'enregistrement de la réponse : ${response.statusText}`);
        }
        return response.json();
    })
    .then(data => {
        console.log("Réponse enregistrée avec succès :", data);
    })
    .catch(error => {
        console.error("Erreur lors de l'enregistrement de la réponse :", error);
    });
}





async function sendEndTime(time) {
    // Préparer les données à envoyer
    const endTimeData = {
        remaining_time: time // Temps restant ou initial
    };

    console.log("Temps restant envoyé :", endTimeData); // Debug

    // URL de l'API pour enregistrer le temps de fin
    const apiUrl = "http://127.0.0.1:8000/api/quiz/save-end-time";

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

// Charger les questions au démarrage
loadQuestions();


