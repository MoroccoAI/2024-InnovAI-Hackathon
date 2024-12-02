from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import relationship
from database import Base

class Candidat(Base):
    __tablename__ = "candidats"
    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    competences = Column(Text, nullable=True)
    objectif = Column(Text, nullable=True)

    entretiens = relationship("Entretien", back_populates="candidat")

class RecruteurIA(Base):
    __tablename__ = "recruteurs_ia"
    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String, index=True)

    entretiens = relationship("Entretien", back_populates="recruteur_ia")

class Question(Base):
    __tablename__ = "questions"
    id = Column(Integer, primary_key=True, index=True)
    texte = Column(Text, nullable=False)
    type = Column(String, nullable=False)

    reponses = relationship("Reponse", back_populates="question")

class Entretien(Base):
    __tablename__ = "entretiens"
    id = Column(Integer, primary_key=True, index=True)
    score_final = Column(Integer, default=0)
    commentaires_generaux = Column(Text, nullable=True)
    candidat_id = Column(Integer, ForeignKey("candidats.id"))
    recruteur_ia_id = Column(Integer, ForeignKey("recruteurs_ia.id"))

    candidat = relationship("Candidat", back_populates="entretiens")
    recruteur_ia = relationship("RecruteurIA", back_populates="entretiens")
    reponses = relationship("Reponse", back_populates="entretien")

class Reponse(Base):
    __tablename__ = "reponses"
    id = Column(Integer, primary_key=True, index=True)
    entretien_id = Column(Integer, ForeignKey("entretiens.id"))
    question_id = Column(Integer, ForeignKey("questions.id"))
    texte = Column(Text, nullable=False)
    evaluation = Column(Integer, nullable=False)
    commentaires = Column(Text, nullable=True)

    entretien = relationship("Entretien", back_populates="reponses")
    question = relationship("Question", back_populates="reponses")


