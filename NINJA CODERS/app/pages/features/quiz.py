
from dotenv import load_dotenv
import streamlit as st
import os
import google.generativeai as genai
from typing import Iterator, Dict, List
import logging
import json
import random
import hashlib

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GeminiQuiz:
    def __init__(self):
        load_dotenv()
        # self.api_key = os.getenv("GOOGLE_API_KEY")
        try:
            self.api_key = os.getenv("GOOGLE_API_KEY") or st.secrets["GOOGLE_API_KEY"]
        except KeyError:
            st.error("Google API Key is not set. Please provide it as an environment variable or in Streamlit secrets.")



        if not self.api_key:
            raise ValueError("GOOGLE_API_KEY not found in environment variables")
        
        self.setup_genai()
        self.max_retries = 5
        
        # Initialize question history in session state if not exists
        if 'question_history' not in st.session_state:
            st.session_state.question_history = set()
        
        # Track used difficulties to ensure variety
        if 'used_difficulties' not in st.session_state:
            st.session_state.used_difficulties = []
            
    def setup_genai(self) -> None:
        try:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel("gemini-pro")
        except Exception as e:
            logger.error(f"Error setting up Gemini: {str(e)}")
            raise

    def get_balanced_difficulty(self) -> str:
        """Ensure a balanced distribution of difficulty levels"""
        difficulties = ["beginner", "intermediate", "advanced"]
        
        if len(st.session_state.used_difficulties) >= 10:  # Reset after 10 questions
            st.session_state.used_difficulties = []
            
        # Count current difficulty distribution
        difficulty_counts = {diff: st.session_state.used_difficulties.count(diff) for diff in difficulties}
        
        # Filter out overused difficulties (more than 1/3 of total questions)
        available_difficulties = [
            diff for diff in difficulties 
            if difficulty_counts[diff] < (len(st.session_state.used_difficulties) + 1) / 3
        ]
        
        # If all difficulties are equally distributed, allow any
        if not available_difficulties:
            available_difficulties = difficulties
            
        selected_difficulty = random.choice(available_difficulties)
        st.session_state.used_difficulties.append(selected_difficulty)
        return selected_difficulty

    def get_language_prompt(self, user_language: str, target_language: str, category: str) -> str:
        """Generate appropriate prompt based on languages and category"""
        difficulty_levels = {
            "beginner": "basic vocabulary and simple structures",
            "intermediate": "moderate complexity and common usage patterns",
            "advanced": "complex language features and nuanced usage"
        }
        
        base_difficulty = self.get_balanced_difficulty()
        
        # Add specific constraints to ensure uniqueness
        base_constraints = f"""
            Constraints for generating unique questions:
            - Use diverse question formats (fill-in-blank, scenario-based, translation, etc.)
            - Include practical, real-world contexts
            - Vary the topics within the category
            - Ensure cultural relevance to {target_language}-speaking regions
            - Don't repeat common textbook examples
        """
        
        prompts = {
            "Grammar": f"""
                Generate a {base_difficulty}-level multiple-choice question for language learning.
                Context: Question about {target_language} grammar, written in {user_language}.
                Focus Area: {difficulty_levels[base_difficulty]}
                {base_constraints}
                Additional Grammar-specific requirements:
                - Include varied sentence structures
                - Focus on practical usage rather than technical terms
                - Incorporate common language patterns
                
                Return strictly in this JSON format:
                {{
                    "question": "Clear, well-formulated question",
                    "options": ["Option 1", "Option 2", "Option 3", "Option 4"],
                    "correct_answer": "The correct option exactly as written in options",
                    "explanation": "Detailed explanation of why the answer is correct",
                    "difficulty": "{base_difficulty}",
                    "topic": "Specific grammar topic covered"
                }}
            """,
            "Vocabulary": f"""
                Generate a {base_difficulty}-level vocabulary question for language learning.
                Context: Question about {target_language} vocabulary, written in {user_language}.
                Focus Area: {difficulty_levels[base_difficulty]}
                {base_constraints}
                Additional Vocabulary-specific requirements:
                - Use words in context-rich situations
                - Include collocations and common word pairs
                - Focus on frequency-based vocabulary selection
                
                Return strictly in this JSON format:
                {{
                    "question": "Clear, well-formulated question",
                    "options": ["Option 1", "Option 2", "Option 3", "Option 4"],
                    "correct_answer": "The correct option exactly as written in options",
                    "explanation": "Detailed explanation including usage examples",
                    "difficulty": "{base_difficulty}",
                    "topic": "Specific vocabulary theme"
                }}
            """,
            "Common Phrases": f"""
                Generate a {base_difficulty}-level question about common phrases.
                Context: Question about {target_language} expressions, written in {user_language}.
                Focus Area: {difficulty_levels[base_difficulty]}
                {base_constraints}
                Additional Phrase-specific requirements:
                - Include contemporary expressions
                - Focus on situational appropriateness
                - Cover various social contexts
                
                Return strictly in this JSON format:
                {{
                    "question": "Clear, well-formulated question",
                    "options": ["Option 1", "Option 2", "Option 3", "Option 4"],
                    "correct_answer": "The correct option exactly as written in options",
                    "explanation": "Detailed explanation with cultural context",
                    "difficulty": "{base_difficulty}",
                    "topic": "Specific phrase category or situation"
                }}
            """
        }
        
        return prompts[category] + "\nProvide only the JSON response without any additional text."

    def calculate_question_hash(self, question_data: Dict) -> str:
        """Calculate a unique hash for a question based on its content"""
        # Create a string combining multiple aspects of the question
        question_string = (
            f"{question_data['question'].lower()}"
            f"{','.join(sorted(opt.lower() for opt in question_data['options']))}"
            f"{question_data['correct_answer'].lower()}"
            f"{question_data.get('topic', '').lower()}"
        )
        return hashlib.md5(question_string.encode()).hexdigest()

    def is_question_unique(self, question_data: Dict) -> bool:
        """Check if a question is unique based on its content"""
        question_hash = self.calculate_question_hash(question_data)
        if question_hash in st.session_state.question_history:
            return False
        st.session_state.question_history.add(question_hash)
        return True

    def generate_question(self, user_language: str, target_language: str, category: str) -> Dict:
        for attempt in range(self.max_retries):
            try:
                prompt = self.get_language_prompt(user_language, target_language, category)
                response = self.model.generate_content(prompt)
                
                # Clean and parse response
                response_text = response.text.strip()
                if "```json" in response_text:
                    response_text = response_text.split("```json")[1].split("```")[0]
                elif "```" in response_text:
                    response_text = response_text.split("```")[1]
                
                response_text = (
                    response_text.strip()
                    .replace('\n', '')
                    .replace('\r', '')
                    .replace('\t', '')
                )
                
                question_data = json.loads(response_text)
                
                # Validate question format
                required_fields = ["question", "options", "correct_answer", "explanation", "difficulty"]
                if not all(field in question_data for field in required_fields):
                    logger.warning("Missing required fields, retrying...")
                    continue
                
                if not isinstance(question_data["options"], list) or len(question_data["options"]) != 4:
                    logger.warning("Invalid options format, retrying...")
                    continue
                
                if question_data["correct_answer"] not in question_data["options"]:
                    logger.warning("Correct answer not in options, retrying...")
                    continue
                
                if self.is_question_unique(question_data):
                    return question_data
                
                logger.info(f"Duplicate question on attempt {attempt + 1}, retrying...")
                
            except Exception as e:
                logger.error(f"Error on attempt {attempt + 1}: {str(e)}")
                continue
        
        raise ValueError("Failed to generate a valid unique question after maximum retries")
    
class QuizApp:
    def __init__(self):
        self.setup_page()
        self.initialize_session_state()
        self.quiz = GeminiQuiz()
        self.available_languages = {
            "English": "🇬🇧",
            "Spanish": "🇪🇸",
            "French": "🇫🇷",
            "German": "🇩🇪",
            "Italian": "🇮🇹",
            "Portuguese": "🇵🇹",
            "Chinese": "🇨🇳",
            "Japanese": "🇯🇵",
            "Korean": "🇰🇷"
        }
        self.categories = ["Grammar", "Vocabulary", "Common Phrases"]
        self.num_questions = 10

    def setup_page(self) -> None:
        st.set_page_config(
            page_title="Languito Quiz",
            page_icon="🌍",
            layout="wide"
        )

    def initialize_session_state(self) -> None:
        if 'quiz_started' not in st.session_state:
            st.session_state['quiz_started'] = False
        if 'current_questions' not in st.session_state:
            st.session_state['current_questions'] = []
        if 'current_question_idx' not in st.session_state:
            st.session_state['current_question_idx'] = 0
        if 'score' not in st.session_state:
            st.session_state['score'] = 0
        if 'user_answers' not in st.session_state:
            st.session_state['user_answers'] = {}
        if 'quiz_completed' not in st.session_state:
            st.session_state['quiz_completed'] = False

    def generate_quiz_questions(self, user_language: str, target_language: str, category: str) -> List[Dict]:
        questions = []
        for _ in range(self.num_questions):
            try:
                question = self.quiz.generate_question(user_language, target_language, category)
                questions.append(question)
            except Exception as e:
                logger.error(f"Error generating question: {str(e)}")
                continue
        return questions

    def display_progress(self) -> None:
        progress = (st.session_state['current_question_idx'] + 1) / self.num_questions
        st.progress(progress)
        st.write(f"Question {st.session_state['current_question_idx'] + 1} of {self.num_questions}")

    def display_final_results(self) -> None:
        st.title("Quiz Complete! 🎉")
        final_score = st.session_state['score']
        percentage = (final_score / self.num_questions) * 100
        
        st.header(f"Your Score: {final_score}/{self.num_questions} ({percentage:.1f}%)")
        
        if percentage >= 90:
            st.balloons()
            st.success("Outstanding! You're a language master! 🌟")
        elif percentage >= 70:
            st.success("Great job! Keep up the good work! 👏")
        elif percentage >= 50:
            st.info("Good effort! Keep practicing! 💪")
        else:
            st.warning("Keep studying! You'll improve! 📚")

        # Display question review
        st.subheader("Review Your Answers")
        for idx, question in enumerate(st.session_state['current_questions']):
            with st.expander(f"Question {idx + 1}: {question['question']}"):
                user_answer = st.session_state['user_answers'].get(idx, "Not answered")
                st.write(f"Your answer: {user_answer}")
                st.write(f"Correct answer: {question['correct_answer']}")
                if user_answer == question['correct_answer']:
                    st.success("Correct! ✅")
                else:
                    st.error("Incorrect ❌")
                st.info(f"Explanation: {question['explanation']}")

    def main(self) -> None:
        st.title("🌍 Languito Quiz")
        
        # Sidebar selections
        with st.sidebar:
            st.title("Quiz Settings")
            user_language = st.selectbox(
                "Select your language:",
                list(self.available_languages.keys()),
                format_func=lambda x: f"{self.available_languages[x]} {x}",
                key="user_language"
            )
            
            target_language = st.selectbox(
                "Select language to learn:",
                [lang for lang in self.available_languages.keys() if lang != user_language],
                format_func=lambda x: f"{self.available_languages[x]} {x}",
                key="target_language"
            )
            
            selected_category = st.selectbox(
                "Select a category:",
                self.categories,
                help="Grammar: Learn language rules\nVocabulary: Learn new words\nCommon Phrases: Learn expressions"
            )
            
            if not st.session_state['quiz_started']:
                if st.button("Start Quiz"):
                    st.session_state['current_questions'] = self.generate_quiz_questions(
                        user_language, target_language, selected_category
                    )
                    st.session_state['quiz_started'] = True
                    st.session_state['current_question_idx'] = 0
                    st.session_state['score'] = 0
                    st.session_state['user_answers'] = {}
                    st.session_state['quiz_completed'] = False
                    st.rerun()

            st.divider()
            st.metric("Current Score", f"{st.session_state['score']}/{self.num_questions}")

        # Main content area
        if st.session_state['quiz_started'] and not st.session_state['quiz_completed']:
            self.display_progress()
            
            current_q = st.session_state['current_questions'][st.session_state['current_question_idx']]
            
            st.subheader(current_q["question"])
            
            user_answer = st.radio(
                "Choose your answer:",
                current_q["options"],
                key=f"q_{st.session_state['current_question_idx']}"
            )

            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("Submit Answer"):
                    st.session_state['user_answers'][st.session_state['current_question_idx']] = user_answer
                    if user_answer == current_q["correct_answer"]:
                        st.session_state['score'] += 1
                    
                    if st.session_state['current_question_idx'] < self.num_questions - 1:
                        st.session_state['current_question_idx'] += 1
                    else:
                        st.session_state['quiz_completed'] = True
                    st.rerun()
            
            with col2:
                if st.session_state['current_question_idx'] > 0:
                    if st.button("Previous Question"):
                        st.session_state['current_question_idx'] -= 1
                        st.rerun()

        elif st.session_state['quiz_completed']:
            self.display_final_results()
            
            if st.button("Start New Quiz"):
                st.session_state['quiz_started'] = False
                st.session_state['current_questions'] = []
                st.session_state['current_question_idx'] = 0
                st.session_state['score'] = 0
                st.session_state['user_answers'] = {}
                st.session_state['quiz_completed'] = False
                st.rerun()

try:
    app = QuizApp()
    app.main()
except Exception as e:
    st.error(f"Application failed to start: {str(e)}")
    logger.error(f"Application error: {str(e)}")
