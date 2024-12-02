import json

def save_outputs(summary, questions_and_answers, file_path):
    with open(file_path, "w") as f:
        json.dump({"summary": summary, "questions_and_answers": questions_and_answers}, f)
