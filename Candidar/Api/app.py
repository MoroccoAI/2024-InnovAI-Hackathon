from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from typing import List
from crud import *
from schemas import *
from database import get_db
import uvicorn
import hashlib
from db_models import *
from crud import *
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from rapidfuzz import process, fuzz
import google.generativeai as genai
from utilisateur import CandidateData
from model import Modele

# Fonction pour hacher le mot de passe
def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

# Initialisation de l'application FastAPI
app = FastAPI()

# Chemin relatif pour atteindre le dossier App/static depuis le fichier main.py
static_dir = Path(__file__).resolve().parent.parent / "App" / "static"

# Monter le dossier 'App/static' comme serveur de fichiers statiques
app.mount("/static", StaticFiles(directory=static_dir), name="static")

# Configuration CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

chat = Modele()
Candidat = CandidateData()

# Modèle pour la requête
class CommandRequest(BaseModel):
    query: str  # La réponse ou question du candidat

# Variable globale pour suivre la dernière question posée
last_question = None
# Endpoint pour gérer les requêtes
@app.post("/endpoint")
async def process_command(request: CommandRequest):
    global last_question

    query = request.query
    if query == "None":
        query = None
    
    # # Obtenir la réponse et la prochaine question
    response, question = chat.interview(query)

    # # Si une dernière question existe, on l'associe à la réponse actuelle
    if last_question:
        Candidat.add_question_interview(last_question, query)
    
    # # Met à jour la dernière question pour la prochaine réponse
    last_question = question
    print(Candidat.interview_log)
    Candidat.saveinterview()

    return {"response": response, "next_question": question}


class Evaluation(BaseModel):
    id: int
    question: str
    reponse_candidat: str
    Score: str
    Feedback: str
    KeyImprovements: List[str]

# Endpoint pour récupérer les évaluations
@app.get("/api/evaluation/endpoint/interview", response_model=List[Evaluation])
async def get_evaluations_interview():
    evaluations=Candidat.get_evaluations()
    print(evaluations)
    if not evaluations:
        raise HTTPException(status_code=404, detail="Aucune évaluation disponible.")
    return evaluations



class CalculerScoresResponse(BaseModel):
    general_pourcentage: int
    quiz_pourcentage: float
    evaluation_pourcentage: float
    

# Route GET pour renvoyer les résultats
@app.get("/api/calculer-scores", response_model=CalculerScoresResponse)
async def obtenir_scores():
    try:
        resultats = Candidat.calculer_scores()  # Retourne le bon format
        print(resultats)
        return resultats
    except Exception as e:
        print(f"Erreur lors de l'obtention des scores : {e}")
        raise HTTPException(status_code=500, detail=f"Erreur interne : {str(e)}")
    
    


class InfoInter(BaseModel):
    role_job: str
    interviewer: str
   

# Route GET pour renvoyer les résultats
@app.get("/api/InfoInter", response_model=InfoInter)
async def obtenir_InfoInter():
    try:
        resultats = chat.get_job_info()  # Retourne le bon format
        print(resultats)
        return resultats
    except Exception as e:
        print(f"Erreur lors de l'obtention des scores : {e}")
        raise HTTPException(status_code=500, detail=f"Erreur interne : {str(e)}")




class Question(BaseModel):
    question: str
    reponse_candidat: str
    bonne_reponse: str
    
@app.get("/api/evaluation/quiz/feed/endpoint", response_model=List[Question])
async def get_evaluations_quiz():
    eval = Candidat.get_quiz_questions()
    if not eval:
        raise HTTPException(status_code=404, detail="Aucune évaluation disponible.")
    return eval


class scoreendpoind(BaseModel):
    candidat: dict
    job: dict
    test_quiz: dict
    interview: dict
    
@app.get("/api/evaluation/score/endpoint",response_model=scoreendpoind)
async def get_evaluationsscore():
    score = {
        "jobrole": "Manager",
        "interviewer": "Farya",
        "quiz_mod": "10.0",
    }

    # Vérifier si le score contient les informations nécessaires
    if not score.get("jobrole") or not score.get("interviewer") or not score.get("quiz_mod"):
        raise HTTPException(status_code=404, detail="Aucune évaluation disponible.")
    
    return score


# Modèle pour valider les données entrantes
class InterviewerChoice(BaseModel):
    interviewer_number: str # Numéro de l'intervieweur

# Route pour accepter le choix de l'intervieweur
@app.post("/api/interview/choose-interviewer")
async def choose_interviewer(choice: InterviewerChoice):
    chat.add_interviewer(choice.interviewer_number)
    print(choice.interviewer_number)
    Candidat.update_interviewer(choice.interviewer_number)
    print(f"intervieweur choisi : {choice.interviewer_number}")

    return {
        "message": "Numéro d'intervieweur enregistré avec succès",
        "interviewer": choice.interviewer_number
    }


class TimeData(BaseModel):
    remaining_time: int

@app.post("/api/quiz/save-end-time")
async def save_end_time(data: TimeData):
    """
    Enregistrer le temps restant ou initial à la fin du quiz.
    """
    remaining_time = data.remaining_time
    Candidat.set_test_completion_time(remaining_time)
    # Ajoutez votre logique pour sauvegarder ces données
    # Exemple : enregistrez dans une base de données ou un fichier
    print(f"Temps restant reçu : {remaining_time} secondes")
    
    # Réponse API
    return {"message": "Temps enregistré avec succès", "remaining_time": remaining_time}


class TimeData2(BaseModel):
    remaining_time: str

@app.post("/api/quiz/save-end-time_interview")
async def save_end_time_interview(data: TimeData2):
    """
    Enregistrer le temps de l'interview .
    """
    remaining_time = data.remaining_time
    Candidat.update_interview_time(remaining_time)
    # Ajoutez votre logique pour sauvegarder ces données
    # Exemple : enregistrez dans une base de données ou un fichier
    print(f"Temps restant reçu : {remaining_time} secondes")
    
    # Réponse API
    return {"message": "Temps enregistré avec succès", "remaining_time": remaining_time}

# Modèle Pydantic pour valider les données reçues
class QuizAnswer(BaseModel):
    question: str
    reponse_candidat: str
    bonne_reponse: str


@app.post("/api/quiz/save-answer")
async def save_quiz_answer(answer: QuizAnswer):
    # Validation automatique grâce à Pydantic
    try:
        Candidat.add_quiz_answer(
            question=answer.question,
            reponse_candidat=answer.reponse_candidat,
            bonne_reponse=answer.bonne_reponse
        )
        return {"message": "Answer saved successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
    

# Modèle de la requête pour recevoir les données
class JobQuery(BaseModel):
    title: str
    description: str
    name_company: str
    


@app.post("/api/quiz/endpoint")
async def receive_job_query(query: JobQuery):
    try:
        print("request give qcm")
        chat.add_infos_job(query.title, query.description, query.name_company)
        Candidat.update_role(query.title)
        # Générer les questions
        questions = chat.generate_qcm_question()# exampleQuestions #chat.generate_qcm_question()#
        Candidat.add_job_info(query.title, query.description, query.name_company)
        if not questions:
            return {"message": "Aucune question générée", "data": []}

        # Retourner les questions
        return {"message": "Questions générées avec succès!", "data": questions}

    except Exception as e:
        # Gérer les erreurs imprévues
        raise HTTPException(status_code=500, detail=f"Erreur interne du serveur : {str(e)}")


# Candidats
@app.post("/candidats/", response_model=CandidatResponse)
def create_candidat_endpoint(candidat: CandidatCreate, db: Session = Depends(get_db)): # type: ignore
    created_candidat = create_candidat(db, candidat.nom, candidat.email, candidat.competences, candidat.objectif)
    if not created_candidat:
        raise HTTPException(status_code=400, detail="Erreur lors de la création du candidat")
    return created_candidat

@app.get("/candidats/", response_model=List[CandidatResponse])
def get_candidats_endpoint(db: Session = Depends(get_db)): # type: ignore
    return get_candidats(db)

@app.delete("/candidats/{candidat_id}")
def delete_candidat_endpoint(candidat_id: int, db: Session = Depends(get_db)): # type: ignore
    delete_candidat(db, candidat_id)
    return {"message": "Candidat supprimé"}

# Recruteurs IA
@app.post("/recruteurs/", response_model=RecruteurIAResponse)
def create_recruteur_endpoint(recruteur: RecruteurIACreate, db: Session = Depends(get_db)): # type: ignore
    created_recruteur = create_recruteur_ia(db, recruteur.nom)
    if not created_recruteur:
        raise HTTPException(status_code=400, detail="Erreur lors de la création du recruteur")
    return created_recruteur

@app.get("/recruteurs/", response_model=List[RecruteurIAResponse])
def get_recruteurs_endpoint(db: Session = Depends(get_db)): # type: ignore
    return get_recruteurs_ia(db)

# Entretiens
@app.post("/entretiens/", response_model=EntretienResponse)
def create_entretien_endpoint(entretien: EntretienCreate, db: Session = Depends(get_db)): # type: ignore
    created_entretien = create_entretien(db, entretien.candidat_id, entretien.recruteur_ia_id, entretien.score_final, entretien.commentaires_generaux)
    if not created_entretien:
        raise HTTPException(status_code=400, detail="Erreur lors de la création de l'entretien")
    return created_entretien

@app.get("/entretiens/{entretien_id}", response_model=EntretienResponse)
def get_entretien_endpoint(entretien_id: int, db: Session = Depends(get_db)): # type: ignore
    entretien = get_entretien_by_id(db, entretien_id)
    if not entretien:
        raise HTTPException(status_code=404, detail="Entretien non trouvé")
    return entretien

@app.patch("/entretiens/{entretien_id}/score")
def update_entretien_score_endpoint(entretien_id: int, score: float, db: Session = Depends(get_db)): # type: ignore
    updated_entretien = update_entretien_score(db, entretien_id, score)
    if not updated_entretien:
        raise HTTPException(status_code=404, detail="Erreur lors de la mise à jour du score")
    return {"message": "Score mis à jour"}

@app.delete("/entretiens/{entretien_id}")
def delete_entretien_endpoint(entretien_id: int, db: Session = Depends(get_db)): # type: ignore
    delete_entretien(db, entretien_id)
    return {"message": "Entretien supprimé"}

# Questions
@app.post("/questions/", response_model=QuestionResponse)
def create_question_endpoint(question: QuestionCreate, db: Session = Depends(get_db)): # type: ignore
    created_question = create_question(db, question.texte, question.type)
    if not created_question:
        raise HTTPException(status_code=400, detail="Erreur lors de la création de la question")
    return created_question

@app.delete("/questions/{question_id}")
def delete_question_endpoint(question_id: int, db: Session = Depends(get_db)): # type: ignore
    delete_question(db, question_id)
    return {"message": "Question supprimée"}

# Réponses
@app.post("/reponses/", response_model=ReponseResponse)
def create_reponse_endpoint(reponse: ReponseCreate, db: Session = Depends(get_db)): # type: ignore
    created_reponse = create_reponse(db, reponse.entretien_id, reponse.question_id, reponse.texte, reponse.evaluation, reponse.commentaires)
    if not created_reponse:
        raise HTTPException(status_code=400, detail="Erreur lors de la création de la réponse")
    return created_reponse

@app.patch("/reponses/{reponse_id}")
def update_reponse_endpoint(reponse_id: int, update_data: ReponseCreate, db: Session = Depends(get_db)): # type: ignore
    updated_reponse = update_reponse(db, reponse_id, update_data.texte, update_data.evaluation, update_data.commentaires)
    if not updated_reponse:
        raise HTTPException(status_code=404, detail="Réponse non trouvée ou erreur lors de la mise à jour")
    return {"message": "Réponse mise à jour"}


# Route pour servir le fichier HTML
@app.get("/", response_class=HTMLResponse)
async def read_index():
    # Chemin vers le fichier index.html
    html_path = Path("App\\static\\templates\\home.html")
    if html_path.exists():
        html_content = html_path.read_text(encoding="utf-8")
        return HTMLResponse(content=html_content)
    return HTMLResponse(content="<h1>Fichier non trouvé</h1>", status_code=404)


# Route pour servir le fichier HTML
@app.get("/about", response_class=HTMLResponse)
async def read_index():
    # Chemin vers le fichier index.html
    html_path = Path("App\\static\\templates\\about.html")
    if html_path.exists():
        html_content = html_path.read_text(encoding="utf-8")
        return HTMLResponse(content=html_content)
    return HTMLResponse(content="<h1>Fichier non trouvé</h1>", status_code=404)


# Route pour servir le fichier HTML
@app.get("/how", response_class=HTMLResponse)
async def read_index():
    # Chemin vers le fichier index.html
    html_path = Path("App\\static\\templates\\how.html")
    if html_path.exists():
        html_content = html_path.read_text(encoding="utf-8")
        return HTMLResponse(content=html_content)
    return HTMLResponse(content="<h1>Fichier non trouvé</h1>", status_code=404)


# Route pour servir le fichier HTML
@app.get("/next", response_class=HTMLResponse)
async def read_index():
    # Chemin vers le fichier index.html
    html_path = Path("App\\static\\templates\\next.html")
    if html_path.exists():
        html_content = html_path.read_text(encoding="utf-8")
        return HTMLResponse(content=html_content)
    return HTMLResponse(content="<h1>Fichier non trouvé</h1>", status_code=404)

# Route pour servir le fichier HTML
@app.get("/start", response_class=HTMLResponse)
async def read_index():
    # Chemin vers le fichier index.html
    html_path = Path("App\\static\\templates\\start.html")
    if html_path.exists():
        html_content = html_path.read_text(encoding="utf-8")
        return HTMLResponse(content=html_content)
    return HTMLResponse(content="<h1>Fichier non trouvé</h1>", status_code=404)


# Route pour servir le fichier HTML
@app.get("/interviwers", response_class=HTMLResponse)
async def read_index():
    Candidat.calculer_et_stocker_score()
    # Chemin vers le fichier index.html
    html_path = Path("App\\static\\templates\\interviwer.html")
    if html_path.exists():
        html_content = html_path.read_text(encoding="utf-8")
        return HTMLResponse(content=html_content)
    return HTMLResponse(content="<h1>Fichier non trouvé</h1>", status_code=404)

# Route pour servir le fichier HTML
@app.get("/congrate", response_class=HTMLResponse)
async def read_index():
    Candidat.update_interview_evaluations(chat.evaluate())
    # Chemin vers le fichier index.html
    html_path = Path("App\\static\\templates\\congrate_page.html")
    if html_path.exists():
        html_content = html_path.read_text(encoding="utf-8")
        return HTMLResponse(content=html_content)
    return HTMLResponse(content="<h1>Fichier non trouvé</h1>", status_code=404)


@app.get("/interview_page", response_class=HTMLResponse)
async def read_index():
   
    html_path = Path("App\\static\\templates\\interview_page.html")
    if html_path.exists():
        html_content = html_path.read_text(encoding="utf-8")
        return HTMLResponse(content=html_content)
    return HTMLResponse(content="<h1>Fichier non trouvé</h1>", status_code=404)



if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)

