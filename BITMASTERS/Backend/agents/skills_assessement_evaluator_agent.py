from entities.skills_evaluator_entities import *
import json

class SkillAssessmentEvaluator:
    def __init__(self):
        self.level_thresholds = {
            (0, 50): PerformanceLevel.BEGINNER,
            (50, 75): PerformanceLevel.INTERMEDIATE,
            (75, 90): PerformanceLevel.ADVANCED,
            (90, 101): PerformanceLevel.EXPERT
        }

    def evaluate(self, skill_data: 'Skill', user_answers: List[str]) -> DetailedEvaluation:

        question_index = 0
        skill_results = {}

        for related_skill in skill_data.related_skills:
            skill_name = related_skill.related_skill_name
            correct_count = 0
            answers = []

            for question in related_skill.mcq_questions:
                user_answer = user_answers[question_index]
                is_correct = user_answer == question.correct_answer
                correct_count += 1 if is_correct else 0
                answers.append(is_correct)
                question_index += 1

            skill_score = (correct_count / len(related_skill.mcq_questions)) * 100
            skill_results[skill_name] = skill_score

        overall_score = sum(skill_results.values()) / len(skill_results)

        strengths = [SkillScore(name=k, score=v) for k, v in skill_results.items() if v >= 70]
        weaknesses = [SkillScore(name=k, score=v) for k, v in skill_results.items() if v < 70]

        return DetailedEvaluation(
            course_name=skill_data.main_skill,
            level=self._determine_level(overall_score),
            score=round(overall_score, 2),
            weaknesses=weaknesses,
            strengths=strengths,
        )

    def _determine_level(self, score: float) -> PerformanceLevel:
        for (min_score, max_score), level in self.level_thresholds.items():
            if min_score <= score < max_score:
                return level
        return PerformanceLevel.BEGINNER

    def generate_report(self, eval_result: DetailedEvaluation) -> str:
        # Transform SkillScore objects into lists of skill names
        weaknesses = [skill.name for skill in eval_result.weaknesses]
        strengths = [skill.name for skill in eval_result.strengths]

        # Create a dictionary with the desired structure
        report_dict = {
            "course_name": eval_result.course_name,
            "level": eval_result.level.value,
            "score": eval_result.score,
            "weaknesses": weaknesses,
            "strengths": strengths
        }
        # Serialize the dictionary to a JSON string
        return report_dict