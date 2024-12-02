// Fonction pour récupérer les données du quiz
async function fetchQuizData(apiUrl) {
    try {
        const response = await fetch(apiUrl, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            },
        });

        if (!response.ok) {
            throw new Error(`Erreur lors de la récupération des questions : ${response.statusText}`);
        }

        const responseData = await response.json();

        if (!responseData || !Array.isArray(responseData)) {
            throw new Error('Le format de réponse de l’API est invalide.');
        }

        return responseData;
    } catch (error) {
        console.error('Une erreur est survenue lors de la récupération des données :', error.message);
        return null;
    }
}




// Fonction pour afficher chaque question avec un bouton pour les détails
function renderQuestions(questions) {
    const quizContainer = document.getElementById('quiz-container');

    questions.forEach((question, index) => {
        // Conteneur de la question
        const questionDiv = document.createElement('div');
        questionDiv.className = 'question-container';

        // Question principale
        const questionContent = `
            <div style="display: flex; align-items: center; justify-content: space-between; gap: 10px;">
                <p><strong>Question ${question.id}:</strong> ${question.question}</p>
                <button class="details-btn" data-id="${index}">Afficher les détails</button>
            </div>
            <div class="question-details" id="details-${index}" style="display: none; flex-direction: column; margin-top: 10px; gap: 5px;">
                <p><strong>Your Answer:</strong> ${question.reponse_candidat || 'No answer provided'}</p>
                <p><strong>Score:</strong> ${question.Score || 'No score available'}</p>
                <p><strong>Feedback:</strong> ${question.Feedback || 'No feedback provided'}</p>
                <p><strong>Key Improvements:</strong></p>
                <ul>
                    ${(question['KeyImprovements'] && question['KeyImprovements'].length > 0) ?
                        question['KeyImprovements'].map(improvement => improvement ? `<li>${improvement}</li>` : '').join('') :
                        '<li>No key improvements provided</li>'}
                </ul>
            </div>
        `;
        questionDiv.innerHTML = questionContent;

        // Ajouter l'écouteur sur le bouton "Détails"
        const detailsBtn = questionDiv.querySelector('.details-btn');
        const detailsDiv = questionDiv.querySelector(`#details-${index}`);

        detailsBtn.addEventListener('click', () => {
            // Basculer l'affichage des détails
            if (detailsDiv.style.display === 'none' || detailsDiv.style.display === '') {
                detailsDiv.style.display = 'flex';
                detailsBtn.textContent = 'hide details';
            } else {
                detailsDiv.style.display = 'none';
                detailsBtn.textContent = 'view details ';
            }
        });

        // Ajouter la question au conteneur principal
        quizContainer.appendChild(questionDiv);
    });
}

// URL de l'API
const apiUrl_interview = 'http://127.0.0.1:8000/api/evaluation/endpoint/interview';

// Récupérer les données et les afficher
fetchQuizData(apiUrl_interview).then(questions => {
    if (questions) {
        renderQuestions(questions);
    } else {
        const quizContainer = document.getElementById('quiz-container');
        quizContainer.innerHTML = '<p>Aucune question n’a été récupérée.</p>';
    }
});
















async function fetchQuizData2(apiUrl) {
    try {
        const response = await fetch(apiUrl, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            },
        });

        if (!response.ok) {
            throw new Error(`Erreur lors de la récupération des scores : ${response.statusText}`);
        }

        const responseData = await response.json();

        // Vérifier si la réponse contient les clés attendues
        if (
            !responseData.hasOwnProperty("general_pourcentage") ||
            !responseData.hasOwnProperty("quiz_pourcentage") ||
            !responseData.hasOwnProperty("evaluation_pourcentage")
        ) {
            throw new Error("La réponse de l'API ne contient pas les données nécessaires.");
        }

        return responseData; // Renvoyer l'objet JSON
    } catch (error) {
        console.error('Une erreur est survenue lors de la récupération des données :', error.message);
        return null;
    }
}

function renderCalculerScore(scores) {
    console.log("Scores reçus :", scores); // Debug

    if (scores.quiz_pourcentage != null && scores.evaluation_pourcentage != null && scores.general_pourcentage != null) {
        document.getElementById('testnote').innerHTML = `${scores.quiz_pourcentage}`;
        document.getElementById('interviewnote').innerHTML = `${scores.evaluation_pourcentage}`;
        document.getElementById('testnote2').innerHTML = `${scores.quiz_pourcentage}`;
        document.getElementById('interviewnote2').innerHTML = `${scores.evaluation_pourcentage}`;
        startTimer(scores.general_pourcentage);
    } else {
        console.error("Certaines données nécessaires sont manquantes dans 'scores'.");
    }
}


// URL de l'API
const url_calculer_scores = 'http://127.0.0.1:8000/api/calculer-scores';

// Récupérer les données et les afficher
document.addEventListener("DOMContentLoaded", function () {
    fetchQuizData2(url_calculer_scores).then(scores => {
        if (scores) {
            renderCalculerScore(scores);
        } else {
            alert("Les scores sont introuvables.");
        }
    });
});


// Fonction pour démarrer le timer et mettre à jour le cercle de progression
function startTimer(maxValue) {
    const progressCircle = document.getElementById("progress");
    const timerText = document.getElementById("timer");

    const circumference = 2 * Math.PI * 45; // Circonférence du cercle
    progressCircle.style.strokeDasharray = circumference;

    // Calcul du pourcentage de remplissage en fonction de la valeur maximale
    const offset = circumference - (maxValue / 100) * circumference;

    // Mise à jour immédiate du cercle de progression
    progressCircle.style.strokeDashoffset = offset;

    // Mise à jour de la valeur du timer
    timerText.textContent = `${maxValue}`;
}




const url_InfoInter = 'http://127.0.0.1:8000/api/InfoInter';
// Récupérer les données et les afficher
document.addEventListener("DOMContentLoaded", function () {
    fetchQuizData3(url_InfoInter ).then(scores => {
        if (scores) {
            renderurl_InfoInter(scores);
        } else {
            alert("Les InfoInter sont introuvables.");
        }
    });
});


function renderurl_InfoInter(scores) {
    console.log("Scores reçus :", scores); // Debug

    if (scores.role_job != null && scores.interviewer != null) {
        document.getElementById('namerole').innerHTML = `${scores.interviewer}`;
        document.getElementById('jobrole').innerHTML = `${scores.role_job}`;
    } else {
        console.error("Certaines données nécessaires sont manquantes dans 'scores'.");
    }
}


async function fetchQuizData3(apiUrl) {
    try {
        const response = await fetch(apiUrl, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            },
        });

        if (!response.ok) {
            throw new Error(`Erreur lors de la récupération des scores : ${response.statusText}`);
        }

        const responseData = await response.json();
        
        // Vérifier si la réponse contient les clés attendues
        if (
            !responseData.hasOwnProperty("role_job") ||
            !responseData.hasOwnProperty("interviewer")
        ) {
            throw new Error("La réponse de l'API ne contient pas les données nécessaires.");
        }

        return responseData; // Renvoyer l'objet JSON
    } catch (error) {
        console.error('Une erreur est survenue lors de la récupération des données :', error.message);
        return null;
    }
}













const apiUrl3 = 'http://127.0.0.1:8000/api/evaluation/quiz/feed/endpoint';

// Récupérer les données et les afficher
fetchQuizData(apiUrl3).then(questions => {
    if (questions) {
        renderQuestions3(questions);
    } else {
        const quizContainer = document.getElementById('quiz_main-container');
        quizContainer.innerHTML = '<p>Aucune question n’a été récupérée.</p>';
    }
});

// Fonction pour afficher les questions du quiz
function renderQuestions3(questions) {
    const quizContainer = document.getElementById('quiz_main-container');

    questions.forEach((question, index) => {
        // Conteneur de la question
        const questionDiv = document.createElement('div');
        questionDiv.className = 'question-container';

        // Question principale
        const questionContent = `
            <div style="display: flex; align-items: center; justify-content: space-between; gap: 10px;">
                <p><strong>Question:</strong> ${question.question}</p>
                <button class="details-btn" data-id="${index}">Afficher les détails</button>
            </div>
            <div class="question-details" id="details-${index}" style="display: none; flex-direction: column; margin-top: 10px; gap: 5px;">
                <p><strong>Your Answer:</strong> ${question.reponse_candidat || 'No answer provided'}</p>
                <p><strong>Correct Answer:</strong> ${question.bonne_reponse}</p>
            </div>
        `;
        questionDiv.innerHTML = questionContent;

        // Ajouter l'écouteur sur le bouton "Détails"
        const detailsBtn = questionDiv.querySelector('.details-btn');
        const detailsDiv = questionDiv.querySelector(`#details-${index}`);

        detailsBtn.addEventListener('click', () => {
            // Basculer l'affichage des détails
            if (detailsDiv.style.display === 'none' || detailsDiv.style.display === '') {
                detailsDiv.style.display = 'flex';
                detailsBtn.textContent = 'hide details';
            } else {
                detailsDiv.style.display = 'none';
                detailsBtn.textContent = 'view details ';
            }
        });

        // Ajouter la question au conteneur principal
        quizContainer.appendChild(questionDiv);
    });
}
