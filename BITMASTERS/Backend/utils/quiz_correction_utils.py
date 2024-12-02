from entities.quiz_entities import *

def calculate_module_score(module_name, user_answers):
    # Get answers for this module
    module_answers = user_answers
    correct_answers = 0
    total_questions = len(module_answers)

    for answer in module_answers:
        # Compare user answers to the correct answers
        user_answer_set = set(answer.user_answers)
        correct_answer_set = set(answer.correct_answers)

        # If the user answers match the correct answers, count as correct
        if user_answer_set == correct_answer_set:
            correct_answers += 1

    # Calculate the module score as percentage
    module_score = (correct_answers / total_questions) * 100 if total_questions > 0 else 0
    return module_score


def calculate_overall_score(user_answers):
    total_correct = 0
    total_questions = 0
    module_scores = {}

    # Loop through each module to calculate the module score
    for module in user_answers:
        module_score = calculate_module_score(module.module_name, module.questions)
        module_scores[module.module_name] = module_score
        total_correct += (module_score / 100) * len(module.questions)
        total_questions += len(module.questions)

    # Calculate overall score as a percentage
    overall_score = (total_correct / total_questions) * 100 if total_questions > 0 else 0
    return overall_score, module_scores