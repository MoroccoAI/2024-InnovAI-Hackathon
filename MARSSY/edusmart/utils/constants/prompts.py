PROMPT_QCM_GENERAL_SCI = """
Vous êtes une intelligence artificielle chargée de générer des questions à choix multiple (QCM) en format LaTeX basées sur le cours, le niveau scolaire et\
les exercices d'exemple que je vous fournirai. Ne suivez pas exactement ces exemples de questions car elles ne sont pas nécessairement des questions QCM. 
Toutes les questions doivent être au même niveau de difficulté, que je spécifierai. Les questions, les options\
et la réponse correcte doivent être structurées comme suit et renvoyées sous la forme JSON:
{{"data": [
{{"question": "Le texte de la question en LaTeX",
  "options": [
    "A - Option 1 en LaTeX",
    "B - Option 2 en LaTeX",
    "C - Option 3 en LaTeX",
    "D - Option 4 en LaTeX"
  ],
  "correct_answer": "La bonne réponse, par exemple A"}}
]
}}
Respectez les consignes suivantes :
Les questions doivent être conformes au niveau de difficulté spécifié (Facile, Moyen ou Difficile).
Chaque question doit comporter des propositions plausibles, y compris des distracteurs basés sur des idées fausses courantes ou des erreurs typiques liées\
au sujet.
Les questions doivent être clairement formulées, et les expressions mathématiques en LaTeX doivent être correctes et lisibles.
Les questions doivent couvrir différents types de raisonnement : résolution d’équations, compréhension de propositions, raisonnement logique ou application\
de formules.
La réponse correcte doit être clairement identifiable parmi les options.
Ne fournissez aucune explication, uniquement les structures de dictionnaire des questions, telles que définies ci-dessus.
N'utilisez pas de macros dans le code latex que vous fournirez.
Assurez-vous que les questions que vous générez sont des questions QCM.

Générez {} questions en fonction des spécifications fournies ci-dessous:

Niveau scolaire : {}
Matière: {}
Cours: {}
Niveau de difficulté : {}
Exemple d'exercices: 
{}
"""
PROMPT_QCM_GENERAL_WITH_LESSON_SCI = """
Vous êtes une intelligence artificielle spécialisée dans la création de questions à choix multiple (QCM) en format LaTeX. Votre tâche est de générer des questions\
basées sur le contenu du cours, le niveau scolaire, et les exercices d'exemple que je vous fournirai. Veuillez noter que les exemples fournis ne doivent pas être suivis\
exactement, car ils ne sont pas nécessairement au format QCM.

Consignes de génération :
Niveau de difficulté : Toutes les questions doivent correspondre au niveau de difficulté spécifié (Facile, Moyen, ou Difficile).
Structure des questions : Les questions, les options et la réponse correcte doivent être formatées en JSON comme suit :
{{"data": [
{{"question": "Le texte de la question en LaTeX",
  "options": [
    "A - Option 1 en LaTeX",
    "B - Option 2 en LaTeX",
    "C - Option 3 en LaTeX",
    "D - Option 4 en LaTeX"
  ],
  "correct_answer": "La bonne réponse, par exemple A"}}
]
}}
Contenu des questions :
Chaque question doit inclure des options plausibles, y compris des distracteurs fondés sur des idées fausses courantes ou des erreurs fréquentes associées au sujet.
Les questions doivent être claires et bien formulées, avec des expressions mathématiques en LaTeX correctes et lisibles.
Les types de raisonnement doivent varier \
l’application de formules.
La réponse correcte doit être identifiable sans ambiguïté parmi les options.
Aucune explication : Vous ne devez pas inclure d’explications, uniquement la structure des questions telle que décrite ci-dessus.
N'utilisez pas de macros dans le code latex que vous fournirez.
Assurez-vous que les questions que vous générez sont des questions QCM.

Générez {} questions en fonction des spécifications fournies ci-dessous:

Niveau scolaire : {}
Matière : {}
Titre du cours : {}
Niveau de difficulté : {}
Texte du cours : {}
Exemples d'exercices reliés au cours : {}

NOTER BIEN: Pour génerer les question il faut se baser plus sur les exemples fournis que sur le cours.

"""


PROMPT_COURS_GENERATION = """
Vous êtes un créateur de contenu éducatif chargé de concevoir un cours personnalisé basé sur les résultats d’un quiz d’un étudiant.
L’étudiant a répondu incorrectement à certaines questions, révélant des lacunes spécifiques dans sa compréhension.
À l’aide des détails fournis, rédigez une leçon personnalisée pour combler ces lacunes.
Incluez uniquement le contenu du cours dans votre réponse, commencer directement par l'introduction.
Structurez le contenu selon le format suivant :

Structure de la réponse :

## Introduction
Présentez brièvement le sujet et son importance.

## Rappel des définitions
Récapitulez les concepts clés nécessaires pour comprendre la leçon.

## Correction des erreurs
Identifiez les erreurs spécifiques et expliquez la bonne réponse de manière claire et détaillée, en utilisant des exemples si nécessaire.

## Remarques et conseils
Fournissez des astuces ou des recommandations pour éviter ces erreurs à l’avenir.

## Exercice d’entraînement
Proposez une ou plusieurs questions ou exercices pratiques avec les réponses.

Format de sortie attendu :
Votre réponse doit être retournée en JSON avec le champ suivant :
{{
  "title": "Le titre de la leçon",
  "content": "Le contenu de la leçon en format Markdown, incluant les expressions mathématiques en LaTeX."
}}

Directives supplémentaires :

Adaptez la leçon au niveau scolaire et à la matière de l’étudiant.
Concentrez-vous uniquement sur les sujets liés aux questions incorrectes.
Rédigez dans un langage simple, clair, et adapté au niveau indiqué.
Les expressions mathématiques doivent être correctement formatées en LaTeX.
Respectez la hiérarchie indiquée dans le format, sans introduire de titres plus élevés que ceux mentionnés.
N'utilisez pas de macros dans le code latex que vous fournirez.


Détails fournis :

Niveau scolaire : {}
Matière : {}
Titre du cours : {}
Section du cours : {}
Questions incorrectes : {}
Assurez-vous que le contenu respecte la structure et la hiérarchie demandées, tout en maintenant un ton pédagogique et engageant.


"""


PROMPT_REPORT_GENERATION = """
Rédige un rapport synthétique et structuré destiné à un enseignant pour analyser les lacunes d'un élève dans un test QCM.

Instructions :
1. L'entrée sera une liste d'objets, où chaque objet contient :
   - Le nom d'un sous-cours ("sous_cours_name").
   - Une liste des questions incorrectes associées ("question").
2. Analyse chaque sous-cours pour identifier les erreurs conceptuelles liées aux questions incorrectes. 
3. Fournis une analyse des lacunes par sous-cours, sans mentionner explicitement les questions incorrectes.
4. Ajoute une section indiquant, pour chaque sous-cours, le **nombre de questions incorrectes**.
5. Rédige une conclusion globale mentionnant les domaines nécessitant une attention particulière, avec des recommandations pour améliorer la compréhension de l'élève.



Votre réponse doit être en format JSON avec le champs ci-dessous :  
{{
  "analyse_des_lacunes_par_sous_cours": [
    {{
      "sous_cours_name": "Nom du sous-cours",
      "analyse": "Résumé des lacunes conceptuelles associées à ce sous-cours.",
      "nombre_questions_incorrectes_par": "Nombre de questions incorrectes"
    }},
    ...
  ],
  "conclusion": "Synthèse globale des domaines nécessitant une attention particulière et recommandations pour progresser."
}}

Details de l'entrée :
[
{}
]
"""


PROMPT_QCM_PERSONILEZED =  """
Vous êtes une intelligence artificielle spécialisée dans la création de questions à choix multiple (QCM) en format LaTeX. 
Votre tâche est de générer des questions basées sur les réponses incorrectes, le niveau scolaire, et des exercices similaires aux questions fournies. 
Veuillez noter que les exemples fournis ne doivent pas être suivis exactement, car ils ne sont pas nécessairement au format QCM.

Consignes de génération :
1. Niveau de difficulté : Toutes les questions doivent correspondre au niveau de difficulté spécifié (Facile, Moyen, ou Difficile).
2. Structure des questions : Les questions, les options et la réponse correcte doivent être formatées en JSON comme suit :
{{
    "data": [
        {{
            "question": "Le texte de la question en LaTeX",
            "options": [
                "A - Option 1 en LaTeX",
                "B - Option 2 en LaTeX",
                "C - Option 3 en LaTeX",
                "D - Option 4 en LaTeX"
            ],
            "correct_answer": "La bonne réponse, par exemple A"
        }}
    ]
}}
3. Contenu des questions :
    - Chaque question doit inclure des options plausibles, y compris des distracteurs fondés sur des idées fausses courantes ou des erreurs fréquentes associées au sujet.
    - Les questions doivent être claires et bien formulées, avec des expressions mathématiques en LaTeX correctes et lisibles.
    - Les types de raisonnement doivent varier, comme l'application de formules ou l'interprétation de concepts.
    - La réponse correcte doit être identifiable sans ambiguïté parmi les options.
    
4. Aucune explication : Vous ne devez pas inclure d’explications, uniquement la structure des questions telle que décrite ci-dessus just the json output.

5. N'utilisez pas de macros dans le code latex que vous fournirez.
6. Assurez-vous que les questions que vous générez sont des questions QCM.

Informations spécifiques à fournir :
- **Nombre de questions à générer** : {}
- **Niveau scolaire** : {}
- **Matière** : {}
- **Titre du cours** : {}
- **Niveau de difficulté** : {}
- **Questions incorrectes à considérer** : {}
- **Exemples d'exercices similaires aux questions incorrectes** : {}

Note importante : 
Pour générer les questions, vous devez donner la priorité aux réponses incorrectes et vous appuyer sur les exercices similaires fournis, tout en essayant de générer des questions différentes des réponses incorrectes mais ciblant la même compétence de base.
"""

