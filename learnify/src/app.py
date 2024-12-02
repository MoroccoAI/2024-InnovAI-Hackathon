import streamlit as st
import tempfile
import os
import json
from dotenv import load_dotenv
import keys  # Ensure this module contains your OpenAI API key as `key`
import llm  # Ensure this module contains the QueryRunner class
import datetime  # For timestamping saved files
import agents  # Import your prompts from agents.py

# Load environment variables if needed
load_dotenv()

# Set OpenAI API Key
os.environ["OPENAI_API_KEY"] = keys.key

# Import prompts from agents.py
TAXONOMY_AGENT_PROMPT = agents.TAXONOMY_AGENT_PROMPT
SCORING_AGENT_PROMPT = agents.SCORING_AGENT_PROMPT
METACOGNITION_AGENT_PROMPT = agents.METACOGNITION_AGENT_PROMPT

# =====================================
# UI Configuration Variables
# =====================================

# Images
LOGO_IMAGE_LEFT = "../Images/hackatonai_logo.png"
LOGO_IMAGE_RIGHT = "../Images/educai-logo.png"

# Texts
APP_TITLE = "Learnify"
ANSWERS_SUBMITTED_MESSAGE = "✅ Your answers have been submitted and saved!"
STUDENT_SCORED_MESSAGE = "✅ Your performance has been evaluated!"
METACOGNITIVE_SUCCESS_MESSAGE = "✅ Personalized recommendations generated successfully!"

# Taxonomy Level Descriptions
tax_lev_dic = {
    "Remember": "🔍 **Recall what you've learned**",
    "Understand": "💡 **Make sense of the idea**",
    "Apply": "🔧 **Put your knowledge into action**",
    "Analyze": "🕵️ **Break it down and explore the details**",
    "Evaluate": "⚖️ **Make a judgment or decide what's best**",
    "Create": "🛠️ **Build something new from what you've learned**"
}

# Apply custom CSS for styling
st.markdown("""
<style>
    .stApp {
        background-color: #fafafa;
    }
    h1 {
        color: #333333;
    }
    .stButton>button {
        color: #ffffff;
        background-color: #0d6efd;
        border-radius: 10px;
        border: 1px solid #0d6efd;
    }
    .reportview-container .main .block-container{
        padding-top: 5rem;
        padding-left: 5%;
        padding-right: 5%;
    }
</style>
""", unsafe_allow_html=True)

# =====================================
# Initialize Session State for storing answers and data
# =====================================
if 'file_content' not in st.session_state:
    st.session_state['file_content'] = None
if 'answers' not in st.session_state:
    st.session_state['answers'] = {}
if 'transformed_questions' not in st.session_state:
    st.session_state['transformed_questions'] = None
if 'restructured_data' not in st.session_state:
    st.session_state['restructured_data'] = None
if 'restructured_filename' not in st.session_state:
    st.session_state['restructured_filename'] = None
if 'original_filename' not in st.session_state:
    st.session_state['original_filename'] = None
if 'answers_submitted' not in st.session_state:
    st.session_state['answers_submitted'] = False
if 'scored_data' not in st.session_state:
    st.session_state['scored_data'] = None
if 'scored_filename' not in st.session_state:
    st.session_state['scored_filename'] = None
if 'weights' not in st.session_state:
    st.session_state['weights'] = {}
if 'recommendations' not in st.session_state:
    st.session_state['recommendations'] = None
if 'taxonomy_evaluation' not in st.session_state:
    st.session_state['taxonomy_evaluation'] = None  # New entry for Taxonomy-Based Evaluation
if 'selected_language' not in st.session_state:
    st.session_state['selected_language'] = 'English'  # Default language


# Define Taxonomy Levels
taxonomy_levels = ["Remember", "Understand", "Apply", "Analyze", "Evaluate", "Create"]

# Streamlit App Title and Logos
def display_header():
    col1, col2 = st.columns([1, 4])
    with col1:
        st.image(LOGO_IMAGE_RIGHT, width=100)  # Adjust the width as needed
    with col2:
        st.markdown("""
        <h1 style='margin-top: 20px;'>Learnify</h1>
        <p style='color: #4a4a4a; font-size: 24px;'>Tailored Learning, Empowering Success.</p>
        """, unsafe_allow_html=True)

st.sidebar.markdown("""
## Explore
Navigate through the sections to experience personalized learning.
""")

# Upload File and Read Content
def upload_file():
    # Display an engaging message
    st.markdown("""
        ### 🌟 **Elevate Your Learning Experience!** 🌟  
        Ready to grow your skills? Upload your questions—it's simple, engaging, and rewarding. Start now and see your progress unfold!
    """)
    
    # File uploader with friendly label and emoji
    uploaded_file = st.file_uploader("📁 **Drag and drop a `.txt` file here, or click to select one**", type=["txt"])
    
    if uploaded_file is not None:
        st.markdown(f"**📄 Uploaded File:** {uploaded_file.name}")
        try:
            file_content = uploaded_file.read().decode("utf-8")
            with st.expander("🔍 View Uploaded File Content"):
                st.text(file_content)
            st.session_state['file_content'] = file_content  # Store file content in session state
            return True
        except Exception as e:
            st.error(f"❌ An error occurred while processing the file: {e}")
            return False
    else:
        st.info("👉 Please upload a `.txt` file to get started.")
        return False

# Run LLM Query for Taxonomy Agent
def run_llm_query(TAXONOMY_AGENT_PROMPT):
    MODEL_NAME = "gpt-3.5-turbo"  # or "gpt-4", etc.
    file_content = st.session_state['file_content']
    with tempfile.NamedTemporaryFile(delete=False, mode='w', encoding='utf-8', suffix=".txt") as tmp_file:
        tmp_file.write(file_content)
        temp_file_path = tmp_file.name

    try:
        bloom_taxonomy_agent = llm.QueryRunner(document_path=temp_file_path, model_name=MODEL_NAME)
        bloom_taxonomy = bloom_taxonomy_agent.run_query(TAXONOMY_AGENT_PROMPT)
        result_str = bloom_taxonomy.get('result', '').strip()

        if result_str:
            # Remove code block markers if present
            if result_str.startswith("```json") and result_str.endswith("```"):
                result_str = result_str[7:-3].strip()
            elif result_str.startswith("```") and result_str.endswith("```"):
                result_str = result_str[3:-3].strip()

            # Try parsing the JSON
            try:
                json_response = json.loads(result_str)
                st.session_state['transformed_questions'] = json_response.get("Topic Questions", [])
                return True
            except json.JSONDecodeError:
                st.error("An error occurred while processing your questions. Please try again.")
                return False
        else:
            st.error("No response from the language model.")
            return False
    except Exception:
        st.error("An unexpected error occurred. Please try again.")
        return False
    finally:
        # Clean up the temporary file
        if os.path.exists(temp_file_path):
            os.unlink(temp_file_path)
tax_lev_dic = {
    "Remember": "🔍 **Recall what you've learned**",
    "Understand": "💡 **Make sense of the idea**",
    "Apply": "🔧 **Put your knowledge into action**",
    "Analyze": "🕵️ **Break it down and explore the details**",
    "Evaluate": "⚖️ **Make a judgment or decide what's best**",
    "Create": "🛠️ **Build something new from what you've learned**"
}
# Display Questions and Collect Answers
def display_questions_and_collect_answers():
    transformed_questions = st.session_state['transformed_questions']
    if transformed_questions:
        st.subheader("📚 **Answer the following questions:**")
        with st.form(key='answer_form'):
            for idx, question_set in enumerate(transformed_questions):
                original_question = question_set.get("Original Question", f"Question {idx+1}")
                st.markdown(f"**📝 Original Question {idx+1}:** {original_question}")

                for level in taxonomy_levels:
                    taxonomy_question = question_set.get(level, "N/A")
                    if taxonomy_question == "N/A":
                        continue  # Skip if the taxonomy question is not available
                    answer_field = f"{level} Answer_{idx}"
                    st.markdown(f"### {level}")
                    st.write(f"**Question:** {taxonomy_question}")
                    default_value = st.session_state['answers'].get(answer_field, "")
                    answer = st.text_area(
                        label=f"Your Answer for {level}:",
                        value=default_value,
                        key=answer_field,
                        height=100
                    )
                    st.session_state['answers'][answer_field] = answer
                st.markdown("---")
            submit_button = st.form_submit_button(label='🚀 Submit Your Answers')
        if submit_button:
            st.session_state['answers_submitted'] = True
            st.success("🎉 Your answers have been submitted! Great job! 🎉")
            # Collect all answers from session state
            student_answers = {"Topic Questions": []}

            for idx, question_set in enumerate(transformed_questions):
                original_question = question_set.get("Original Question", f"Question {idx+1}")
                answer_set = {
                    "Original Question": original_question,
                    "Sub-Questions": {}
                }

                for level in taxonomy_levels:
                    taxonomy_question = question_set.get(level, "N/A")
                    answer_field = f"{level} Answer_{idx}"  # Unique key per question and level
                    student_answer = st.session_state['answers'].get(answer_field, "")

                    answer_set["Sub-Questions"][level] = {
                        "Question": taxonomy_question,
                        "Answer": student_answer
                    }

                student_answers["Topic Questions"].append(answer_set)

            # Save the student answers to session state
            st.session_state['student_answers'] = student_answers

            # Timestamp for unique filename
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            answers_file_path = f"student_answers_{timestamp}.json"

            try:
                # Save the JSON file locally
                with open(answers_file_path, 'w', encoding='utf-8') as f:
                    json.dump(student_answers, f, ensure_ascii=False, indent=4)
                # Provide a download button for the JSON file
                json_str = json.dumps(student_answers, ensure_ascii=False, indent=4)
                st.download_button(
                    label="📥 Download Your Answers",
                    data=json_str,
                    file_name=answers_file_path,
                    mime='application/json'
                )
            except Exception:
                st.error("Failed to save your answers.")
        return True
    else:
        st.error("No transformed questions to display.")
        return False

# Restructure JSON as per the new format
def restructure_json():
    # Use the student_answers from session state
    student_answers = st.session_state.get('student_answers')
    if student_answers:
        restructured_data = {"Bloom Taxonomy": {level: [] for level in taxonomy_levels}}
        for question_set in student_answers["Topic Questions"]:
            original_question = question_set.get("Original Question")
            sub_questions = question_set.get("Sub-Questions", {})
            for level in taxonomy_levels:
                sub_question = sub_questions.get(level)
                if sub_question:
                    restructured_data["Bloom Taxonomy"][level].append({
                        "Original Question": original_question,
                        "Sub-Question": sub_question
                    })
        st.session_state['restructured_data'] = restructured_data
        return restructured_data
    
    
# Save JSON File Locally
def save_json_file(data, filename_prefix):
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{filename_prefix}_{timestamp}.json"
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        return filename
    except Exception:
        st.error("Failed to save your data.")
        return None

# Run LLM Query for Scoring Agent
def run_scoring_agent():
    MODEL_NAME = "gpt-3.5-turbo"  # or "gpt-4", etc.

    restructured_data = st.session_state['restructured_data']
    # Convert restructured_data to JSON string
    input_json = json.dumps(restructured_data, ensure_ascii=False, indent=4)

    # Prepare the prompt with the input JSON
    scoring_prompt = SCORING_AGENT_PROMPT.replace("{input_json}", input_json)

    # Write the input JSON to a temporary file
    with tempfile.NamedTemporaryFile(delete=False, mode='w', encoding='utf-8', suffix=".json") as tmp_file:
        tmp_file.write(input_json)
        temp_file_path = tmp_file.name

    try:
        scoring_agent = llm.QueryRunner(document_path=temp_file_path, model_name=MODEL_NAME)
        scoring_response = scoring_agent.run_query(scoring_prompt)
        result_str = scoring_response.get('result', '').strip()

        if result_str:
            # Remove code block markers if present
            if result_str.startswith("```json") and result_str.endswith("```"):
                result_str = result_str[7:-3].strip()
            elif result_str.startswith("```") and result_str.endswith("```"):
                result_str = result_str[3:-3].strip()

            # Try parsing the JSON
            try:
                scored_data = json.loads(result_str)
                st.session_state['scored_data'] = scored_data  # Store in session state
                return True
            except json.JSONDecodeError:
                st.error("An error occurred while evaluating your performance.")
                return False
        else:
            st.error("No response from the language model.")
            return False

    except Exception:
        st.error("An unexpected error occurred during evaluation.")
        return False

    finally:
        # Clean up the temporary file
        if os.path.exists(temp_file_path):
            os.unlink(temp_file_path)

# Calculate Taxonomy-Based Evaluation and Store JSON
def calculate_taxonomy_evaluation():
    scored_data = st.session_state['scored_data']
    taxonomy_evaluation = {"Bloom Taxonomy": {}}

    for level in taxonomy_levels:
        if level in scored_data["Bloom Taxonomy"]:
            total_score = 0
            count = 0
            for sub_question in scored_data["Bloom Taxonomy"][level]:
                score = sub_question["Sub-Question"].get("score", 0)
                total_score += score
                count += 1
            average_score = total_score / count if count > 0 else 0
            weight = st.session_state['weights'].get(level, 0)
            weighted_average = average_score * weight
            taxonomy_evaluation["Bloom Taxonomy"][level] = {
                "average_score": average_score,
                "weight": weight,
                "weighted_average": weighted_average
            }
        else:
            taxonomy_evaluation["Bloom Taxonomy"][level] = {
                "average_score": 0,
                "weight": st.session_state['weights'].get(level, 0),
                "weighted_average": 0
            }

    st.session_state['taxonomy_evaluation'] = taxonomy_evaluation
    return taxonomy_evaluation

# Run LLM Query for Metacognitive Recommendation Agent
def run_metacognition_agent():
    MODEL_NAME = "gpt-3.5-turbo"  # or "gpt-4", etc.

    # Retrieve the Taxonomy-Based Evaluation from session state
    taxonomy_evaluation = st.session_state.get('taxonomy_evaluation')

    if not taxonomy_evaluation:
        st.error("Evaluation data is missing.")
        return False

    # Convert the taxonomy_evaluation to a JSON string
    input_json_str = json.dumps(taxonomy_evaluation, ensure_ascii=False, indent=4)

    # Prepare the prompt with the input JSON
    metacognition_prompt = METACOGNITION_AGENT_PROMPT.replace("{input_json}", input_json_str)

    # Write the prompt to a temporary file
    with tempfile.NamedTemporaryFile(delete=False, mode='w', encoding='utf-8', suffix=".txt") as tmp_file:
        tmp_file.write(metacognition_prompt)
        temp_file_path = tmp_file.name

    try:
        # Initialize QueryRunner with document_path and model_name
        metacognition_agent = llm.QueryRunner(document_path=temp_file_path, model_name=MODEL_NAME)

        # Run the query
        metacognition_response = metacognition_agent.run_query(metacognition_prompt)
        result_str = metacognition_response.get('result', '').strip()

        if result_str:
            # Store the recommendations
            st.session_state['recommendations'] = result_str
            return True
        else:
            st.error("No response from the language model.")
            return False

    except Exception:
        st.error("An unexpected error occurred while generating recommendations.")
        return False

    finally:
        # Clean up the temporary file
        if os.path.exists(temp_file_path):
            os.unlink(temp_file_path)

# Display Taxonomy-Based Evaluation
def display_taxonomy_based_evaluation():
    scored_data = st.session_state['scored_data']
    levels_present = [level for level in taxonomy_levels if level in scored_data["Bloom Taxonomy"]]
    num_questions = max(len(scored_data["Bloom Taxonomy"][level]) for level in levels_present) if levels_present else 0

    st.markdown("### Your Learning Progress Overview")
    total_weighted_score = 0.0
    taxonomy_evaluation = {"Bloom Taxonomy": {}}

    for level in taxonomy_levels:
        if level in scored_data["Bloom Taxonomy"]:
            total_score = 0
            level_questions = scored_data["Bloom Taxonomy"][level]
            for sub_question in level_questions:
                score = sub_question["Sub-Question"].get("score", 0)
                total_score += score
            average_score = total_score / len(level_questions) if level_questions else 0
            weight = st.session_state['weights'].get(level, 0)
            weighted_average = average_score * weight
            total_weighted_score += weighted_average

            taxonomy_evaluation["Bloom Taxonomy"][level] = {
                "average_score": average_score,
                "weight": weight,
                "weighted_average": weighted_average
            }

            # Display the score using custom progress bars
            st.write(f"**{level}**")
            st.progress(average_score / 5.0)
            st.write(f"Average Score: {average_score:.2f}/5")
            st.write(f"Weighted Score: {weighted_average:.2f}")
            st.markdown("---")
        else:
            st.warning(f"No data for level '{level}'.")

    st.write(f"**Total Weighted Average Score: {total_weighted_score:.2f} out of 5.00**")

    # Store the taxonomy evaluation for metacognition
    st.session_state['taxonomy_evaluation'] = taxonomy_evaluation

# Display Metacognitive Recommendations
def display_metacognitive_recommendations():
    recommendations = st.session_state['recommendations']
    st.markdown("### Metacognitive Recommendations")
    st.write(recommendations)

    # Optionally, save the recommendations to a file
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"metacognitive_recommendations_{timestamp}.txt"
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(recommendations)

    # Download button for recommendations
    st.download_button(
        label="📥 Download Recommendations",
        data=recommendations,
        file_name=filename,
        mime='text/plain'
    )

    
def main():
    display_header()
    # Language Selection
    st.sidebar.subheader("Select Language")
    language_options = ["English", "French", "Spanish", "German", "Chinese"]
    selected_language = st.sidebar.selectbox(
        "Choose your language",
        language_options,
        index=language_options.index(st.session_state.get('selected_language', 'English'))
    )
    st.session_state['selected_language'] = selected_language
    
    # Step 1: File upload
    if st.session_state['file_content'] is None:
        if not upload_file():
            return  # Stop execution until file is uploaded

    # Step 2: Run LLM Query
    if st.session_state['transformed_questions'] is None:
        if not run_llm_query(TAXONOMY_AGENT_PROMPT,):
            return  # Stop execution if there's an error

    # Step 3: Display Questions and Collect Answers
    if not st.session_state['answers_submitted']:
        if not display_questions_and_collect_answers():
            return  # Wait until answers are submitted

    # Step 4: Restructure Data and Save Files
    if st.session_state['restructured_data'] is None:
        restructure_json()

    if st.session_state['restructured_filename'] is None:
        restructured_filename = save_json_file(st.session_state['restructured_data'], "structured_data")
        st.session_state['restructured_filename'] = restructured_filename

    if st.session_state['original_filename'] is None:
        original_filename = save_json_file({"Topic Questions": st.session_state['transformed_questions']}, "original_questions")
        st.session_state['original_filename'] = original_filename
        
   
    # Display success message
    #st.success(ANSWERS_SUBMITTED_MESSAGE)

    # Step 5: Scoring
    st.markdown("### Reflect on Your Learning Journey!")
    score_button = st.button('🎯 Score My Performance 🎯')
    if score_button:
        if run_scoring_agent():
            scored_filename = save_json_file(st.session_state['scored_data'], "student_score")
            st.session_state['scored_filename'] = scored_filename
            st.success(STUDENT_SCORED_MESSAGE)
            # Calculate taxonomy evaluation
            calculate_taxonomy_evaluation()

    if st.session_state.get('scored_data'):
        # Display Scored Data
        display_taxonomy_based_evaluation()

        # Step 6: Metacognitive Recommendations
        st.markdown("### Get Personalized Recommendations")
        recommend_button = st.button('✨ Get Recommendations')
        if recommend_button:
            if run_metacognition_agent():
                st.success(METACOGNITIVE_SUCCESS_MESSAGE)

        if st.session_state.get('recommendations'):
            display_metacognitive_recommendations()

    # Sidebar Configuration for Weights
    st.sidebar.header("Configuration")
    st.sidebar.subheader("Set Importance Levels")
    default_weights = [1/6]*6  # Default equal weights if none provided
    if not st.session_state['weights']:
        st.session_state['weights'] = dict(zip(taxonomy_levels, default_weights))

    weights_input = {}
    total_weight = 0.0
    for level in taxonomy_levels:
        weight = st.sidebar.number_input(f"Importance of {level}", min_value=0.0, max_value=1.0, value=st.session_state['weights'][level], step=0.05)
        weights_input[level] = weight
        total_weight += weight

    # Normalize weights if total_weight != 1
    if total_weight != 1.0 and total_weight > 0:
        st.sidebar.warning("Weights do not sum to 1. They will be normalized automatically.")
        for level in taxonomy_levels:
            st.session_state['weights'][level] = weights_input[level] / total_weight
    elif total_weight == 0:
        st.sidebar.error("Total weight cannot be zero. Resetting to default values.")
        st.session_state['weights'] = dict(zip(taxonomy_levels, default_weights))
    else:
        st.sidebar.success("Weights are set.")

if __name__ == "__main__":
    main()