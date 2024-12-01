import random
import os
import random
from openai import OpenAI
from dotenv import load_dotenv
import json
import pickle
import numpy as np
import json
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[0]))
import openai
import constants.values as cv
import constants.prompts as pmt
import constants.names as cn

load_dotenv()
client = OpenAI()
def get_embedding(text, model="text-embedding-ada-002"):
    """
    Function to get the embedding for a given text using OpenAI's API.

    Args:
        text (str): The text to embed.
        model (str): The model to use for embedding (e.g., "text-embedding-ada-002").

    Returns:
        list: A list containing the embedding vector.
    """
    response = client.embeddings.create(
        model=model,
        input=text,
        encoding_format="float"
    )

    embedding = response.data[0].embedding
    return embedding
def load_embeddings(file_path):
    """
    Load embeddings from a pickle file.
    """
    try:
        with open(file_path, 'rb') as f:
            return pickle.load(f)
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
        return {}
def cosine_similarity(vec1, vec2):
    """
    Calculate the cosine similarity between two vectors.
    """
    dot_product = np.dot(vec1, vec2)
    norm_vec1 = np.linalg.norm(vec1)
    norm_vec2 = np.linalg.norm(vec2)
    if norm_vec1 == 0 or norm_vec2 == 0:
        return 0.0
    return dot_product / (norm_vec1 * norm_vec2)


def get_similar_exo_cours(level, year, branch, subject, lesson):
    """
    Create a dictionary of similar exos for each sous-cours in the lesson.
    The keys are the names of the sous-cours and the values are lists of names of similar exos.
    """
    full_path_exo_txt = cv.ROOT_DATABASE_PATH + level + "/" + year + "/" + branch + "/" + subject + "/" + lesson + cv.EXO_PATH_EMBEDDING_SUFFIX
    full_path_cour_txt = cv.ROOT_DATABASE_PATH + level + "/" + year + "/" + branch + "/" + subject + "/" + lesson + cv.SOUS_COURS_PATH_EMBEDDING_SUFFIX
    sous_cour_embeddings = load_embeddings(full_path_cour_txt)
    exo_embeddings = load_embeddings(full_path_exo_txt)

    sim_sous_cours = {}
    for sous_cours_name, sous_cours_embedding in sous_cour_embeddings.items():
        similarities = [
            (exo_name, cosine_similarity(sous_cours_embedding, exo_embedding))
            for exo_name, exo_embedding in exo_embeddings.items()
        ]
        # Sort by similarity in descending order and take top N
        top_similar = sorted(similarities, key=lambda x: x[1], reverse=True)[:cv.NUM_SIMILARITY_EXO]
        sim_sous_cours[sous_cours_name] = [name for name, _ in top_similar]
    return sim_sous_cours  

def get_similar_exo_qcm(level, year, branch, subject, lesson, wrong_answers):
    """
    Create a dictionary of similar exercises for each sub-course in the lesson.
    The keys are the names of the sub-courses, and the values are lists of names of similar exercises.
    """
    # Construct the full path to the embedding data file
    full_path_exo_txt = f"{cv.ROOT_DATABASE_PATH}{level}/{year}/{branch}/{subject}/{lesson}{cv.EXO_PATH_EMBEDDING_SUFFIX}"

    # Load precomputed embeddings for exercises
    try:
        exo_embeddings = load_embeddings(full_path_exo_txt)
    except FileNotFoundError:
        raise FileNotFoundError(f"Embedding file not found: {full_path_exo_txt}")
    except Exception as e:
        raise RuntimeError(f"An error occurred while loading embeddings: {e}")

    # Initialize a dictionary to store similar exercises for each course with wrong answers
    sim_exo_for_wrong_qcm = {}

    # Loop over each course with wrong answers
    for course in wrong_answers:
        # Ensure the course has the required 'question' field and it is not empty
        questions = course.get('question')


        # Prepare the question text by joining all parts into one string
        question_text = '\n'.join(questions)

        # Compute the embedding for the question
        try:
            questions_embedded = get_embedding(question_text)
        except Exception as e:
            raise RuntimeError(f"Error while embedding question for {course.get('sub_course_name', 'unknown_sub_course')}: {e}")

        # Calculate cosine similarities between the question embedding and all exercise embeddings
        try:
            similarities = [
                (exo_name, cosine_similarity(questions_embedded, exo_embedding))
                for exo_name, exo_embedding in exo_embeddings.items()
            ]
        except Exception as e:
            raise RuntimeError(f"Error calculating cosine similarities: {e}")

        # Sort by similarity in descending order and take the top N similar exercises
        top_similar = sorted(similarities, key=lambda x: x[1], reverse=True)[:cv.NUM_SIMILARITY_EXO]

        # Store the result in the dictionary with the sub-course name as the key
        sub_course_name = course.get("sous_cours_name")
        sim_exo_for_wrong_qcm[sub_course_name] = {
            "questions": question_text,
            "sim_exos": [name for name, _ in top_similar]
        }

    return sim_exo_for_wrong_qcm


def generate_from_prompt_json(prompt):
    """
    Generate text from a prompt using the OpenAI API.
    The output is python string in the format of a JSON object.
    """
    completion = client.chat.completions.create(
        model=cv.OPENAI_MODEL,
        messages=[
            {"role": "user", "content": prompt}
        ],
        response_format = { "type": "json_object" },
        temperature = cv.TEMPERATURE
    )
    return completion.choices[0].message.content

def get_random_exo_examples_from_list(full_path_exos, exos_list):
    """

    """
    if cv.NUM_PRMPT_EXO < len(exos_list):
        selected_exos = random.sample(exos_list, cv.NUM_PRMPT_EXO)
    else:
        selected_exos = exos_list
    output = []
    for exo in selected_exos:
        try:
            with open(full_path_exos + exo + ".txt", 'r') as file:
                output.append(file.read())
        except FileNotFoundError:
            print(f"The file at {full_path_exos} was not found.")
    return output

def load_sous_cours(sous_cours_path):
    try:
        with open(sous_cours_path, 'r') as file:
            return(file.read())
    except FileNotFoundError:
        print(f"The file at {sous_cours_path} was not found.")


def generate_general_qcm_from_cours_parties(level, year, branch, subject, lesson, difficulty, num_questions):
    sim_sous_cours = get_similar_exo_cours(level, year, branch, subject, lesson)
    data = {"data":[]}
    full_path_cours = cv.ROOT_DATABASE_PATH + level + "/" + year + "/" + branch + "/" + subject + "/" + lesson

    for sous_cours_name in sim_sous_cours:
        sous_cours = load_sous_cours(full_path_cours + "/cours/" + sous_cours_name + ".txt")
        example_exos = get_random_exo_examples_from_list(full_path_cours + "/exercices/", sim_sous_cours[sous_cours_name])
        prompt = pmt.PROMPT_QCM_GENERAL_WITH_LESSON_SCI.format(num_questions,f"{cn.level_mapping[level]} {cn.year_mapping[year]} {cn.branch_mapping[branch]} Maroc", cn.subject_mapping[subject], cn.lesson_mapping[lesson], difficulty, sous_cours,example_exos)
        response = generate_from_prompt_json(prompt)
        quizz = json.loads(response)["data"]
        sous_cours_quizz = {"sous_cours_name": sous_cours_name, "content": quizz}
        data["data"].append(sous_cours_quizz)
    return data



def compare_answers(input_data):
    """
    input_data is the dictionary sent at the end of the general qcm.
    It has two fields: answers and qcm.
    """
    results = {}

    for course in input_data['answers']:
        sous_cours_name = course['sous_cours_name']
        user_answers = course['answers']
        
        # Find the corresponding qcm content
        qcm_content = next((item for item in input_data['qcm'] if item['sous_cours_name'] == sous_cours_name), None)
        
        if qcm_content:
            for i, question in enumerate(qcm_content['content']):
                correct_answer = question['correct_answer']
                user_answer_index = user_answers[i]
                
                # Convert user answer index to corresponding option letter (A, B, C, D)
                user_answer_letter = chr(65 + user_answer_index)  # 65 is ASCII for 'A'
                
                if user_answer_letter != correct_answer:
                    if sous_cours_name not in results:
                        results[sous_cours_name] = []
                    results[sous_cours_name].append(question['question'])
    
    # Convert results to the desired output format
    formatted_results = [
        {"sous_cours_name": key, "question": value}
        for key, value in results.items()
    ]
    
    return formatted_results

def generate_customized_cours(general_qcm_submition):
    """
    general_qcm_submition has 3 keys:
    - answers
    - qcm
    - meta (contains: the level, year, branch, subject, lesson)

    returns:
    out = {"data" = [
        {"sub_title": , "content": {}},
    ]}
    """
    raw_meta = general_qcm_submition["meta"]
    meta =  mapping_front_back_meta_form(general_qcm_submition["meta"])
    data = {"data":[]}
    full_path_cours = cv.ROOT_DATABASE_PATH + meta["level"] + "/" + meta["year"] + "/" + meta["branch"] + "/" + meta["subject"] + "/" + meta["lesson"]
    
    lacunes = compare_answers(general_qcm_submition)
    set_exo = get_similar_exo_qcm(meta["level"], meta["year"], meta["branch"], meta["subject"], meta["lesson"], lacunes)
    for item in lacunes:
        sous_cours = load_sous_cours(full_path_cours + "/cours/" + item["sous_cours_name"] + ".txt")
        prompt = pmt.PROMPT_COURS_GENERATION.format(f"{raw_meta["level"]} {raw_meta["year"]} {raw_meta["branch"]} Maroc", raw_meta["subject"], raw_meta["lesson"],sous_cours,item["question"])
        response = generate_from_prompt_json(prompt)
        content = json.loads(response)["content"]
        sous_proposed_cours = {"sub_title": item["sous_cours_name"], "content": content}
        data["data"].append(sous_proposed_cours)
    
    return data 
    
def generate_customized_qcm(general_qcm_submition):
    raw_meta = general_qcm_submition["meta"]
    meta =  mapping_front_back_meta_form(general_qcm_submition["meta"])
    data = {"data":[]}
    full_path_exos = cv.ROOT_DATABASE_PATH + meta["level"] + "/" + meta["year"] + "/" + meta["branch"] + "/" + meta["subject"] + "/" + meta["lesson"]
    lacunes = compare_answers(general_qcm_submition)
    sim_qcm_set = get_similar_exo_qcm(meta["level"], meta["year"], meta["branch"], meta["subject"], meta["lesson"], lacunes)

    for item in lacunes:
        sous_cours_name = item["sous_cours_name"]
        incorrect_questions = sim_qcm_set[sous_cours_name]["questions"]
        exos_sim_list = sim_qcm_set[sous_cours_name]["sim_exos"]
        exos_sim = get_random_exo_examples_from_list(full_path_exos + "/exercices/", exos_sim_list)
        prompt = pmt.PROMPT_QCM_PERSONILEZED.format(meta["num_questions"],f"{raw_meta["level"]} {raw_meta["year"]} {raw_meta["branch"]} Maroc", raw_meta["subject"], raw_meta["lesson"], raw_meta["difficulty"], incorrect_questions,exos_sim)
        response = generate_from_prompt_json(prompt)
        quizz = json.loads(response)["data"]
        sous_cours_quizz = {"sous_cours_name": sous_cours_name, "content": quizz}
        data["data"].append(sous_cours_quizz)
    return data

def generate_customized_report(general_qcm_submition):
    """
    """
    answers_json = compare_answers(general_qcm_submition)
    try:
        # Ensure the JSON is correctly formatted as a string
        answers_json_str = json.dumps(answers_json)

        # Format the prompt with the provided JSON data
        prompt = pmt.PROMPT_REPORT_GENERATION.format(answers_json_str)
        
        result = generate_from_prompt_json(prompt)
        # Try to load the content as a JSON object
        try:
            report_json = json.loads(result)
            return report_json
        except json.JSONDecodeError:
            # If parsing fails, return the raw response for debugging
            raise ValueError(f"Failed to parse JSON response: {result}")

    except Exception as e:
        # Handle errors gracefully and provide useful feedback
        return {"error": str(e)}
    







    







###### hardcoded stuff ########
def mapping_front_back_meta_form(data):
    # Define the mapping dictionary
    mapping_dict = {
        'level': {
            'Lycée': 'lycee',
            'Université': 'University'
        },
        'year': {
            '1ère Bac': '1_bac',
            '2ème Bac': '2nd Year Bachelor'
        },
        'branch': {
            'Sciences Mathématiques': 'sci_math',
            'Sciences Physiques': 'Physical Sciences'
        },
        'subject': {
            'Mathématiques': 'math',
            'Physique': 'Physics'
        },
        'lesson': {
            'Notion de logique': 'notion_de_logique',
            'Algèbre linéaire': 'Linear Algebra'
        },
    }
    
    # Transform the data using the mapping dictionary
    transformed_data = {}
    for key, value in data.items():
        if key in mapping_dict:
            # If a mapping exists for the key, transform the value
            transformed_data[key] = mapping_dict[key].get(value, value)
        else:
            # If no mapping exists, keep the original value
            transformed_data[key] = value

    return transformed_data


#### viz #####
def save_qcm_to_html(qcm_data, output_file="qcm_output.html"):

    """
    Convert QCM data to a formatted HTML file with properly separated text and LaTeX
    """
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>QCM Questions</title>
        <meta charset="UTF-8">
        <style>
            body {
                font-family: Arial, sans-serif;
                max-width: 900px;
                margin: 0 auto;
                padding: 20px;
                line-height: 1.6;
            }
            .question {
                margin-bottom: 30px;
                padding: 20px;
                border: 1px solid #ddd;
                border-radius: 5px;
                background-color: #f9f9f9;
            }
            .question-text {
                font-weight: bold;
                margin-bottom: 15px;
                font-size: 1.2em;
            }
            .question-content {
                margin-bottom: 15px;
                font-style: italic;
            }
            .options {
                margin-left: 20px;
            }
            .option {
                margin: 15px 0;
                padding: 10px;
                background-color: white;
                border-radius: 4px;
                border: 1px solid #eee;
            }
            .correct-answer {
                color: #2e7d32;
                font-weight: bold;
                margin-top: 15px;
                padding: 10px;
                background-color: #e8f5e9;
                border-radius: 5px;
            }
        </style>
        <script>
            MathJax = {
                tex: {
                    inlineMath: [['$', '$']],
                    displayMath: [['$$', '$$']],
                    processEscapes: true,
                    packages: ['base', 'ams', 'noerrors', 'noundefined']
                }
            };
        </script>
        <script id="MathJax-script" async 
            src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js">
        </script>
    </head>
    <body>
        <h1>QCM Questions</h1>
    """
    
    def fix_latex(text):
        """Clean up LaTeX formatting"""
        # Remove extra backslashes and fix spacing
        text = text.replace('\\\\', '\\')
        # Ensure math expressions are properly delimited
        if '\\mathbb' in text or '\\forall' in text or '\\exists' in text or '\\geq' in text:
            if not text.startswith('$'):
                text = '$' + text
            if not text.endswith('$'):
                text = text + '$'
        return text

    def process_option(option):
        """Process each option to separate letter label and content"""
        parts = option.split(' - ', 1)
        if len(parts) == 2:
            label, content = parts
            return f"{label} - {fix_latex(content)}"
        return fix_latex(option)

    # Add each question
    for sous_cours in qcm_data['data']:
        html_content += f"<h2>{sous_cours['sous_cours_name']}</h2>"
        for i, item in enumerate(sous_cours['content'], 1):
            question = fix_latex(item['question'])
            
            html_content += f"""
            <div class="question">
                <div class="question-text">Question {i}:</div>
                <div class="question-content">{question}</div>
                <div class="options">
            """
            
            # Add options
            for option in item['options']:
                processed_option = process_option(option)
                html_content += f'<div class="option">{processed_option}</div>'
            
            # Add correct answer
            html_content += f"""
                </div>
                <div class="correct-answer">Correct Answer: {item['correct_answer']}</div>
            </div>
            """
    
    html_content += """
    </body>
    </html>
    """
    
    # Write to file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"QCM has been saved to {output_file}")