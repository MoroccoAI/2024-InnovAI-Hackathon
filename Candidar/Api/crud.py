from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from db_models import Candidat, RecruteurIA, Entretien, Question, Reponse  # Modèles à importer
from database import engine

Session = sessionmaker(bind=engine)

# Création
def create_candidat(session, nom, email, competences, objectif):
    try:
        candidat = Candidat(nom=nom, email=email, competences=competences, objectif=objectif)
        session.add(candidat)
        session.commit()
        return candidat
    except IntegrityError:
        session.rollback()
        print("Erreur: Un candidat avec cet email existe déjà.")
        return None
    except SQLAlchemyError as e:
        session.rollback()
        print(f"Erreur SQL: {e}")
        return None

def create_recruteur_ia(session, nom):
    try:
        recruteur_ia = RecruteurIA(nom=nom)
        session.add(recruteur_ia)
        session.commit()
        return recruteur_ia
    except SQLAlchemyError as e:
        session.rollback()
        print(f"Erreur SQL: {e}")
        return None

def create_entretien(session, candidat_id, recruteur_id, score_final=0, commentaires=""):
    try:
        entretien = Entretien(
            candidat_id=candidat_id, recruteur_ia_id=recruteur_id, 
            score_final=score_final, commentaires_generaux=commentaires
        )
        session.add(entretien)
        session.commit()
        return entretien
    except SQLAlchemyError as e:
        session.rollback()
        print(f"Erreur SQL: {e}")
        return None

def create_question(session, texte, type_question):
    try:
        question = Question(texte=texte, type=type_question)
        session.add(question)
        session.commit()
        return question
    except SQLAlchemyError as e:
        session.rollback()
        print(f"Erreur SQL: {e}")
        return None

def create_reponse(session, entretien_id, question_id, texte, evaluation, commentaires):
    try:
        reponse = Reponse(
            entretien_id=entretien_id, question_id=question_id, 
            texte=texte, evaluation=evaluation, commentaires=commentaires
        )
        session.add(reponse)
        session.commit()
        return reponse
    except SQLAlchemyError as e:
        session.rollback()
        print(f"Erreur SQL: {e}")
        return None

# Lecture
def get_candidats(session):
    try:
        return session.query(Candidat).all()
    except SQLAlchemyError as e:
        print(f"Erreur SQL: {e}")
        return []

def get_recruteurs_ia(session):
    try:
        return session.query(RecruteurIA).all()
    except SQLAlchemyError as e:
        print(f"Erreur SQL: {e}")
        return []

def get_entretien_by_id(session, entretien_id):
    try:
        return session.query(Entretien).filter_by(id=entretien_id).first()
    except SQLAlchemyError as e:
        print(f"Erreur SQL: {e}")
        return None

def get_questions_by_entretien(session, entretien_id):
    try:
        entretien = session.query(Entretien).filter_by(id=entretien_id).first()
        return entretien.questions if entretien else []
    except SQLAlchemyError as e:
        print(f"Erreur SQL: {e}")
        return []

def get_reponses_by_entretien(session, entretien_id):
    try:
        entretien = session.query(Entretien).filter_by(id=entretien_id).first()
        return entretien.reponses if entretien else []
    except SQLAlchemyError as e:
        print(f"Erreur SQL: {e}")
        return []

# Mise à jour
def update_entretien_score(session, entretien_id, new_score):
    try:
        entretien = session.query(Entretien).filter_by(id=entretien_id).first()
        if entretien:
            entretien.score_final = new_score
            session.commit()
        return entretien
    except SQLAlchemyError as e:
        session.rollback()
        print(f"Erreur SQL: {e}")
        return None

def update_reponse(session, reponse_id, texte, evaluation, commentaires):
    try:
        reponse = session.query(Reponse).filter_by(id=reponse_id).first()
        if reponse:
            reponse.texte = texte
            reponse.evaluation = evaluation
            reponse.commentaires = commentaires
            session.commit()
        return reponse
    except SQLAlchemyError as e:
        session.rollback()
        print(f"Erreur SQL: {e}")
        return None

# Suppression
def delete_candidat(session, candidat_id):
    try:
        candidat = session.query(Candidat).filter_by(id=candidat_id).first()
        if candidat:
            session.delete(candidat)
            session.commit()
    except SQLAlchemyError as e:
        session.rollback()
        print(f"Erreur SQL: {e}")

def delete_entretien(session, entretien_id):
    try:
        entretien = session.query(Entretien).filter_by(id=entretien_id).first()
        if entretien:
            session.delete(entretien)
            session.commit()
    except SQLAlchemyError as e:
        session.rollback()
        print(f"Erreur SQL: {e}")

def delete_question(session, question_id):
    try:
        question = session.query(Question).filter_by(id=question_id).first()
        if question:
            session.delete(question)
            session.commit()
    except SQLAlchemyError as e:
        session.rollback()
        print(f"Erreur SQL: {e}")
