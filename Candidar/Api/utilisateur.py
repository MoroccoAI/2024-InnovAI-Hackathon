import json
from datetime import datetime
from typing import List, Dict


path_file = "infos_user.json"


class CandidateData:
    def __init__(self, role="olanda", interviewer="farya"):
        self.interview_log = []
        self.data = {
            "candidat": {"role": role, "interviewer": interviewer},
            "job": {"titre": "", "description": "", "campagne": ""},
            "test_quiz": {
                "questions": [],
                "temps_fin_test": "",
                "evaluations": []  # Évaluations liées au test/quiz
            },
            "interview": {
                "questions": [],
                "temps_fin_interview": "",
                "evaluations": []
            },
        }
        self.initialize_file(path_file)

    def initialize_file(self, filename):
        """Initialiser le fichier JSON si nécessaire."""
        try:
            with open(filename, "r", encoding="utf-8") as f:
                json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            self.save_to_file(filename)

    def add_question_interview(self, question, response):
        """Ajouter une question et une réponse à l'interview."""
        self.data["interview"]["questions"].append({
            "question": question,
            "reponse_candidat": response
        })
        self.save_to_file(path_file)

    def saveinterview(self):
        """Sauvegarder les questions de l'interview loggées."""
        for item in self.interview_log:
            self.add_question_interview(item["question"], item["response"])
        self.interview_log.clear()

    def add_job_info(self, titre, description, campagne):
        """Ajouter des informations sur le job."""
        self.data["job"].update({"titre": titre, "description": description, "campagne": campagne})
        self.save_to_file(path_file)

    def add_quiz_answer(self, question, reponse_candidat, bonne_reponse):
        """Ajouter une réponse au quiz."""
        self.data["test_quiz"]["questions"].append({
            "question": question,
            "reponse_candidat": reponse_candidat,
            "bonne_reponse": bonne_reponse
        })
        self.save_to_file(path_file)

    def set_test_completion_time(self, temps_fin=None):
        """Ajouter le temps de fin du test."""
        self.data["test_quiz"]["temps_fin_test"] = temps_fin or datetime.utcnow().isoformat()
        self.save_to_file(path_file)

    def set_interview_completion_time(self, temps_fin=None):
        """Ajouter le temps de fin de l'interview."""
        self.data["interview"]["temps_fin_interview"] = temps_fin or datetime.utcnow().isoformat()
        self.save_to_file(path_file)

    def add_evaluation(self, context, score, feedback, improvements):
        """Ajouter une évaluation au test ou à l'interview."""
        if context not in ["test_quiz", "interview"]:
            raise ValueError("Le contexte doit être 'test_quiz' ou 'interview'.")
        self.data[context]["evaluations"].append({
            "Score": score,
            "Feedback": feedback,
            "Key Improvements": improvements
        })
        self.save_to_file(path_file)

    def calculer_et_stocker_score(self):
        """Calculer le score du quiz et le stocker."""
        questions = self.data["test_quiz"]["questions"]
        bonnes_reponses = sum(1 for q in questions if q["reponse_candidat"] == q["bonne_reponse"])
        total_questions = len(questions)
        pourcentage = (bonnes_reponses / total_questions) * 100 if total_questions else 0
        self.data["test_quiz"]["evaluations"] = {
            "score": bonnes_reponses,
            "pourcentage": round(pourcentage, 2)
        }
        self.save_to_file(path_file)

    def save_to_file(self, filename):
        """Sauvegarder les données dans un fichier JSON."""
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(self.data, f, indent=4, ensure_ascii=False)

     

    def update_interview_time(self, update_time: str) -> bool:
        """
        Met à jour la valeur de 'temps_fin_interview' dans le fichier JSON.

        Args:
            update_time (str): La nouvelle valeur pour 'temps_fin_interview'.

        Returns:
            bool: True si la mise à jour a réussi, False sinon.
        """
        return self._update_json_field("interview", "temps_fin_interview", update_time)

    def update_interview_evaluations(self, evaluations: list) -> bool:
        """
        Met à jour les évaluations de l'interview dans le fichier JSON.

        Args:
            evaluations (list): La liste des évaluations à mettre à jour.

        Returns:
            bool: True si la mise à jour a réussi, False sinon.
        """
        return self._update_json_field("interview", "evaluations", evaluations)

    def _update_json_field(self, section: str, field: str, value) -> bool:
        """
        Méthode générique pour mettre à jour un champ dans une section donnée du fichier JSON.

        Args:
            section (str): La section à modifier (ex: 'interview').
            field (str): Le champ à mettre à jour (ex: 'temps_fin_interview').
            value: La nouvelle valeur à attribuer au champ.

        Returns:
            bool: True si la mise à jour a réussi, False sinon.
        """
        try:
            # Lire le fichier JSON
            with open(path_file, "r", encoding="utf-8") as f:
                data = json.load(f)

            # Vérifier si la section et le champ existent
            if section not in data:
                print(f"Erreur : La section '{section}' est manquante dans le fichier '{path_file}'.")
                return False

            # Mettre à jour le champ
            data[section][field] = value

            # Sauvegarder les modifications dans le fichier JSON
            with open(path_file, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4, ensure_ascii=False)

            print(f"{field} mis à jour avec succès dans la section '{section}'.")
            return True

        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Erreur : {str(e)}")
            return False
        
 
    def update_role(self,role):
        path =path_file
        """
        Met à jour le rôle dans la structure de données pour le chemin donné.

        :param path: Chemin d'accès dans le dictionnaire (ex: "candidat")
        :param role: Le rôle à assigner
        """
        if path in self.data:
            self.data[path]["role"] = role
            print(f"Le rôle a été mis à jour pour {path} avec la valeur '{role}'.")
        else:
            print("Le chemin spécifié n'existe pas dans les données.")

    def update_interviewer(self, interviewer):
        path =path_file
        """
        Met à jour l'intervieweur dans la structure de données pour le chemin donné.

        :param path: Chemin d'accès dans le dictionnaire (ex: "candidat")
        :param interviewer: Le nom de l'intervieweur
        """
        if path in self.data:
            self.data[path]["interviewer"] = interviewer
            print(f"L'intervieweur a été mis à jour pour {path} avec la valeur '{interviewer}'.")
        else:
            print("Le chemin spécifié n'existe pas dans les données.")
            
            
    

    def get_quiz_percentage(self):
        data=self.load_json()
        """
        Récupère le pourcentage du quiz à partir des données JSON.
        """
        try:
            return data['test_quiz']['evaluations']['pourcentage']
        except KeyError:
            return "Pourcentage non disponible"
    
    def get_quiz_questions(self):
        data=self.load_json()
        try:
            return data['test_quiz']['questions']
        except KeyError:
            return "questions non trouvé"

    
    def load_json(self,file_path=path_file):
        """
        Charge un fichier JSON depuis le chemin spécifié et retourne son contenu.
        """
        try:
            with open(file_path, 'r') as file:
                data = json.load(file)
            return data
        except FileNotFoundError:
            print(f"Le fichier à l'emplacement {file_path} n'a pas été trouvé.")
            return None
        except json.JSONDecodeError:
            print("Erreur lors de la lecture du fichier JSON.")
            return None

    def get_evaluations(self):
        input_data=self.load_json()
        evaluations = []
        
        # Extraire les questions et évaluations de l'entretien
        interview_questions = input_data["interview"]["questions"]
        evaluations_data = input_data["interview"]["evaluations"]
        
        # Itération sur les questions et évaluations
        for idx, (question_data, evaluation_data) in enumerate(zip(interview_questions, evaluations_data)):
            evaluation = {
                "id": idx + 1,  # ID basé sur l'index
                "question": question_data["question"],  # La question posée
                "reponse_candidat": question_data["reponse_candidat"],  # La réponse du candidat
                "Score": evaluation_data[0]["Score"],  # Le score
                "Feedback": evaluation_data[0]["Feedback"],  # Le feedback
                "KeyImprovements": evaluation_data[0]["Key Improvements"]  # Les améliorations suggérées
            }
            evaluations.append(evaluation)
        return evaluations
            
    def calculer_scores(self):
        input_data=self.load_json()
        # Récupération des scores de l'entretien et du quiz
        scores_entretien = input_data['interview']['evaluations']
        score_quiz = input_data['test_quiz']['evaluations']['pourcentage']
        
        # Calcul de la moyenne des scores d'entretien
        total_scores_entretien = 0
        total_questions_entretien = len(scores_entretien)
        
        for evaluation in scores_entretien:
            score = int(evaluation[0]["Score"].split("/")[0])  # On récupère la première partie du score (avant le '/')
            total_scores_entretien += score
        
        # Calcul de la moyenne des scores de l'entretien en pourcentage
        moyenne_entretien = (total_scores_entretien / (total_questions_entretien * 10)) * 100  # Total maximum de 10 points par question
        
        # Calcul de la moyenne générale entre le quiz et l'entretien
        moyenne_generale = (moyenne_entretien + score_quiz) / 2
        
        # Création du dictionnaire de résultat
        resultats = {
            "general_pourcentage": int(moyenne_generale),
            "quiz_pourcentage": score_quiz,
            "evaluation_pourcentage": moyenne_entretien
        }
        
        return resultats
        




    def __repr__(self):
        """Affichage des données pour debug."""
        return json.dumps(self.data, indent=4, ensure_ascii=False)
    