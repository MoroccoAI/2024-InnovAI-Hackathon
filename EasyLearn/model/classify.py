# from langchain_ollama import ChatOllama
# import json

# def classify_questions(questions_and_answers, model="qwen2.5:0.5b"):
#     """
#     Classify questions into Basic, Intermediate, or Advanced levels using an LLM.
#     :param questions_and_answers: List of dictionaries containing questions and answers.
#     :param model: LLM model to use.
#     :return: Dictionary with classified questions.
#     """
#     # Extract questions for classification
#     questions = [{"question": qa["question"]} for qa in questions_and_answers]

#     prompt = (
#         "Classify the following questions into Basic, Intermediate, or Advanced levels based on their complexity:\n\n"
#         f"{json.dumps(questions, indent=2)}\n\n"
#         "Format the output as a JSON object where each key is a level and each value is a list of questions, e.g.:\n"
#         '{\n'
#         '  "basic": ["<question>", ...],\n'
#         '  "intermediate": ["<question>", ...],\n'
#         '  "advanced": ["<question>", ...]\n'
#         '}\n'
#     )

#     try:
#         ollama = ChatOllama(model=model)
#         response = ollama.invoke([{"role": "user", "content": prompt}])
        
#         # Parse the JSON response
#         classified = json.loads(response.content.strip())

#         # Validate the structure
#         if not all(key in classified for key in ["basic", "intermediate", "advanced"]):
#             raise ValueError("Response missing required keys.")

#         return classified
#     except json.JSONDecodeError:
#         print("Error: The LLM response is not valid JSON.")
#         return {"basic": [], "intermediate": [], "advanced": []}
#     except Exception as e:
#         print(f"Error during question classification: {e}")
#         return {"basic": [], "intermediate": [], "advanced": []}

import json

from langchain_ollama import ChatOllama

def classify_questions(questions_and_answers, model="qwen2.5:0.5b"):
    """
    Classify questions into difficulty levels.
    """
    try:
        ollama = ChatOllama(model=model)
        classification_prompt = (
            "Classify the following questions into Basic, Intermediate, or Advanced levels:\n\n"
            f"{json.dumps(questions_and_answers, indent=2)}\n\n"
            "Output as JSON with keys 'basic', 'intermediate', 'advanced'."
        )
        classification_response = ollama.invoke([{"role": "user", "content": classification_prompt}])
        return json.loads(classification_response.content.strip())
    except Exception as e:
        print(f"Error classifying questions: {e}")
        return {"basic": [], "intermediate": [], "advanced": []}
