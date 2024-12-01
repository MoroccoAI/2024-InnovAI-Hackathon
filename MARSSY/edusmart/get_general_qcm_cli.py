from utils.utils import *
import argparse
import os

def main(level, year, branch, subject, lesson, difficulty, num_questions):
    qcm_data = generate_general_qcm_from_cours_parties(level, year, branch, subject, lesson, difficulty, num_questions) #json.loads(cv.example_generated_qcm_v2) #
    # qcm_data =  generate_general_qcm_from_cours(level, year, branch, subject, lesson, difficulty, num_questions) #json.loads(cv.example_generated_qcm)
    print(qcm_data)
    save_qcm_to_html(qcm_data, output_file="qcm_output_reda_test.html")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Description of your script functionality.")

    # Add arguments
    parser.add_argument("--level", type=str, help="lycee, college or primaire", default="lycee")
    parser.add_argument("--year", type=str, help="Ex: tronc_commun, 1_bac, 2_bac", default="1_bac")
    parser.add_argument("--branch", type=str, help="Ex: sci_eco, sci_math...", default="sci_math")
    parser.add_argument("--subject", type=str, help="Ex: math...", default = "math")
    parser.add_argument("--lesson", type=str, help="Ex: notion_de_logique...", default = "notion_de_logique")
    parser.add_argument("--difficulty", type=str, help="Facile, Moyen ou Difficile", default = "Moyen")
    parser.add_argument("--num_questions", type=int, help="Number of questions per lesson part to generate generate", default = 3)


    # Parse arguments and pass them to main
    args = parser.parse_args()
    main(args.level, args.year, args.branch, args.subject, args.lesson, args.difficulty, args.num_questions)


