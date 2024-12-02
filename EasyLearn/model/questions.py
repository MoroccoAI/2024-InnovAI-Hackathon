# from langchain_ollama import ChatOllama

# def generate_questions_and_answers(summary, model="qwen2.5:0.5b", min_questions=20):
#     """
#     Generate a set of questions and answers from the summary.
#     :param summary: Text summary to generate questions from.
#     :param model: LLM model to use.
#     :param min_questions: Minimum number of questions to generate.
#     :return: List of question-answer pairs.
#     """
#     prompt = (
#         f"Based on the following summary, generate at least {min_questions} questions and their answers. "
#         "Include questions at Basic, Intermediate, and Advanced levels:\n\n"
#         f"Summary:\n{summary}\n\n"
#         "Format the output as:\n"
#         "- Basic Question: <question>\n"
#         "- Basic Answer: <answer>\n"
#         "- Intermediate Question: <question>\n"
#         "- Intermediate Answer: <answer>\n"
#         "- Advanced Question: <question>\n"
#         "- Advanced Answer: <answer>\n"
#     )
#     try:
#         ollama = ChatOllama(model=model)
#         response = ollama.invoke([{"role": "user", "content": prompt}])
#         return response.content.strip().split("\n\n")
#     except Exception as e:
#         print(f"Error during question generation: {e}")
#         return []
# up date to better output 


from langchain_ollama import ChatOllama
import json

def generate_questions_and_answers(summary, model="qwen2.5:0.5b", min_questions=20):
    """
    Refine the summary using the LLM and then generate a set of questions and answers.
    :param summary: Text summary to generate questions from.
    :param model: LLM model to use.
    :param min_questions: Minimum number of questions to generate.
    :return: List of dictionaries containing question, answer, and difficulty level.
    """
    # Step 1: Refine the summary
    refine_prompt = (
        f"The following summary is provided to generate questions. "
        f"Please refine it to make it more concise and focused:\n\n"
        f"Summary:\n{summary}\n\n"
        "Provide the refined summary in plain text, without additional explanations."
    )

    try:
        ollama = ChatOllama(model=model)
        refine_response = ollama.invoke([{"role": "user", "content": refine_prompt}])
        refined_summary = refine_response.content.strip()

        print(f"Refined Summary: {refined_summary}")  # Debug log

    except Exception as e:
        print(f"Error during summary refinement: {e}")
        return []

    # Step 2: Generate questions and answers
    qa_prompt = (
        f"Based on the following refined summary, generate at least {min_questions} questions and their answers. "
        "Include questions at Basic, Intermediate, and Advanced levels:\n\n"
        f"Refined Summary:\n{refined_summary}\n\n"
        "Provide the output as a JSON array where each element has keys 'difficulty', 'question', and 'answer'."
    )

    try:
        qa_response = ollama.invoke([{"role": "user", "content": qa_prompt}])
        raw_output = qa_response.content.strip()

        # Debug: Print raw response
        print(f"Raw response: {raw_output}")

        # Parse the JSON response
        questions_and_answers = json.loads(raw_output)

        # Validate structure
        if not isinstance(questions_and_answers, list):
            raise ValueError("Response is not a valid list.")

        for qa in questions_and_answers:
            if not all(k in qa for k in ("difficulty", "question", "answer")):
                raise ValueError(f"Invalid question structure: {qa}")

        return questions_and_answers

    except json.JSONDecodeError:
        print("Error: LLM response is not valid JSON.")
        return []
    except Exception as e:
        print(f"Error during question generation: {e}")
        return []


# from langchain_ollama import ChatOllama

# def generate_questions_and_answers(summary, model="qwen2.5:0.5b", min_questions=20):
#     """
#     Generate questions and answers from the provided summary using an LLM.
#     :param summary: Summarized text to generate questions from.
#     :param model: LLM model to use.
#     :param min_questions: Minimum number of questions to generate.
#     :return: List of question-answer pairs.
#     """
#     prompt = (
#         f"Generate at least {min_questions} questions and answers based on the following summary.\n\n"
#         f"Summary:\n{summary}\n\n"
#         "Ensure that questions are evenly distributed across the following levels:\n"
#         "- Basic: Simple factual questions.\n"
#         "- Intermediate: Reasoning or explanation-based questions.\n"
#         "- Advanced: Analytical or critical thinking questions.\n\n"
#         "Format:\n"
#         "- Basic Question: <question>\n"
#         "- Basic Answer: <answer>\n"
#         "- Intermediate Question: <question>\n"
#         "- Intermediate Answer: <answer>\n"
#         "- Advanced Question: <question>\n"
#         "- Advanced Answer: <answer>\n"
#     )

#     try:
#         ollama = ChatOllama(model=model)
#         response = ollama.invoke([{"role": "user", "content": prompt}])
#         questions_and_answers = response.content.strip().split("\n\n")
#         return questions_and_answers
#     except Exception as e:
#         print(f"Error during question generation: {e}")
#         return []


# def classify_questions_with_llm(questions_and_answers, model="qwen2.5:0.5b"):
#     """
#     Classify questions into Basic, Intermediate, and Advanced using LLM.
#     :param questions_and_answers: List of questions and answers to classify.
#     :param model: LLM model to use for classification.
#     :return: Dictionary with classified questions.
#     """
#     prompt = (
#         f"Classify the following questions into Basic, Intermediate, and Advanced levels. "
#         f"Ensure classification is based on complexity and depth of thought required to answer.\n\n"
#         f"Questions and Answers:\n\n"
#         + "\n\n".join(questions_and_answers) +
#         "\n\n"
#         "Format:\n"
#         "- Basic: [List of Basic Questions and Answers]\n"
#         "- Intermediate: [List of Intermediate Questions and Answers]\n"
#         "- Advanced: [List of Advanced Questions and Answers]\n"
#     )

#     try:
#         ollama = ChatOllama(model=model)
#         response = ollama.invoke([{"role": "user", "content": prompt}])
#         classification = {"basic": [], "intermediate": [], "advanced": []}

#         # Parse LLM's response into the classification dictionary
#         sections = response.content.strip().split("\n\n")
#         for section in sections:
#             if section.startswith("- Basic:"):
#                 classification["basic"] = section.replace("- Basic:", "").strip().split("\n")
#             elif section.startswith("- Intermediate:"):
#                 classification["intermediate"] = section.replace("- Intermediate:", "").strip().split("\n")
#             elif section.startswith("- Advanced:"):
#                 classification["advanced"] = section.replace("- Advanced:", "").strip().split("\n")

#         return classification
#     except Exception as e:
#         print(f"Error during classification: {e}")
#         return {"basic": [], "intermediate": [], "advanced": []}




# from langchain_ollama import ChatOllama

# def generate_questions_and_answers(summary, model="qwen2.5:0.5b", min_questions=20):
#     prompt = f"Generate {min_questions} questions with answers from the summary:\n{summary}"
#     ollama = ChatOllama(model=model)
#     response = ollama.invoke([{"role": "user", "content": prompt}])
#     return response.content.strip().split("\n")
