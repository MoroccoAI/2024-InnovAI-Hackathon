from pydantic import BaseModel, EmailStr
from typing import List, Optional

# Modèles pour les candidats
class CandidatCreate(BaseModel):
    nom: str
    email: EmailStr
    competences: Optional[str] = None
    objectif: Optional[str] = None

class CandidatResponse(BaseModel):
    id: int
    nom: str
    email: EmailStr
    competences: Optional[str] = None
    objectif: Optional[str] = None

  

# Modèles pour les recruteurs IA
class RecruteurIACreate(BaseModel):
    nom: str

class RecruteurIAResponse(BaseModel):
    id: int
    nom: str

  

# Modèles pour les questions
class QuestionCreate(BaseModel):
    texte: str
    type: str

class QuestionResponse(BaseModel):
    id: int
    texte: str
    type: str


# Modèles pour les entretiens
class EntretienCreate(BaseModel):
    candidat_id: int
    recruteur_ia_id: int
    score_final: Optional[int] = 0
    commentaires_generaux: Optional[str] = None

class EntretienResponse(BaseModel):
    id: int
    candidat_id: int
    recruteur_ia_id: int
    score_final: int
    commentaires_generaux: Optional[str] = None
    questions: List[QuestionResponse] = []
    reponses: List[str] = []

 

# Modèles pour les réponses
class ReponseCreate(BaseModel):
    entretien_id: int
    question_id: int
    texte: str
    evaluation: int
    commentaires: Optional[str] = None

class ReponseResponse(BaseModel):
    id: int
    entretien_id: int
    question_id: int
    texte: str
    evaluation: int
    commentaires: Optional[str] = None
