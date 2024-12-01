import os
import logging
from flask import Flask, request, jsonify, Response
from flask_cors import CORS
from huggingface_hub import InferenceClient
from transformers import pipeline
from PIL import Image
from dotenv import load_dotenv
from io import BytesIO
import requests
from ultralyticsplus import YOLO, postprocess_classify_output
  
# Load environment variables
load_dotenv()
API_URL = os.getenv("API_URL")

# Initialize Flask app
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
logging.basicConfig(level=logging.INFO)

# Initialize Hugging Face API client
client = InferenceClient(api_key=API_URL)

# Load ML models
brain_classifier = pipeline("image-classification", model="Devarshi/Brain_Tumor_Classification")
Alzheimer_classifier = pipeline("image-classification", model="evanrsl/resnet-Alzheimer")
chest_xray_classifier = YOLO('keremberke/yolov8m-chest-xray-classification')

# set model parameters
chest_xray_classifier.overrides['conf'] = 0.25

# Hugging Face BLIP model API setup
BLIP_API_URL = "https://api-inference.huggingface.co/models/Salesforce/blip-image-captioning-large"
HEADERS = {"Authorization": f"Bearer {API_URL}"}

model_details = None


@app.route('/health', methods=['GET'])
def health_check():
    """
    Endpoint for health checks.
    """
    return jsonify({"status": "healthy"}), 200


def estimate_token_count(text):
    """
    Approximate the token count in the given text.
    """
    return len(text.split())

def truncate_chat_history(chat_history, token_limit):
    """
    Truncate the chat history to fit within the token limit.
    """
    truncated_history = []
    current_token_count = 0

    for turn in chat_history:
        if 'role' in turn and 'content' in turn:
            turn_tokens = estimate_token_count(turn['content'])
            if current_token_count + turn_tokens <= token_limit:
                truncated_history.append(turn)
                current_token_count += turn_tokens
            else:
                break  # Stop adding if token limit is reached
    return truncated_history

@app.route('/chat', methods=['POST'])
def chat():
    """
    Chat endpoint to handle AI-driven conversations.
    """
    try:
        # Validate the request
        if not request.is_json:
            return jsonify({"error": "Content-Type must be application/json"}), 400

        data = request.get_json()
        if 'messages' not in data or 'chatHistory' not in data:
            return jsonify({"error": "Missing 'messages' or 'chatHistory' in request body"}), 400

        # Extract chat history and current query
        chat_history = data['chatHistory']
        current_query = data['messages']

        # Truncate chat history to fit within 4000 tokens
        MAX_TOKENS = 4000
        truncated_history = truncate_chat_history(chat_history, MAX_TOKENS)

        # Construct the medical report prompt
        medical_report_prompt = {
            "role": "assistant",
            "content": (
                "You are a Medical AI Assistant tasked to help healthcare professionals make informed decisions. "
                "Your role is to provide accurate, evidence-based medical reports, recommendations, and insights. "
                "Follow standard medical reporting formats, ensure clarity and conciseness, and provide actionable suggestions. "
                "Take into account the chat history and the current classification results (if any).\n\n"

                "Here is the chat history for reference:\n\n"
            )
        }

        # Add truncated chat history to the prompt
        for i, turn in enumerate(truncated_history):
            medical_report_prompt["content"] += f"**Turn {i+1}:**\n**{turn['role'].capitalize()}:** {turn['content']}\n\n"
    

        classification_message = next(
            (msg['content'] for msg in current_query if 'Image Classification:' in msg['content']), None
        )

        if classification_message:
            medical_report_prompt["content"] += f"Image Classification Result: {classification_message}\n\n"
            medical_report_prompt["content"] += "Please generate a medical report based on the result."
            medical_report_prompt["content"] += (
            "When creating the medical report:\n"
            "- Base your findings on the provided classification results, if available.\n"
            "- Include potential diagnoses, detailed explanations, recommendations for follow-up actions, and treatment options.\n"
            "- Ensure your recommendations are grounded in reputable medical knowledge and clearly state any uncertainties.\n\n"

            "### Referencing Guidelines:\n"
            "- Include at least **two to three insightful references** from credible medical sources, such as PubMed, WHO, CDC, or similar platforms.\n"
            "- Present the references as clickable markdown links (e.g., `[description](URL)`).\n"
            "- Ensure references are directly relevant to the discussed findings and support your conclusions with recent and authoritative data.\n"
            "- If referencing studies or guidelines, briefly summarize their relevance to your conclusions.\n\n"

            "### Example of References in the Report:\n"
            "- Potential Diagnosis: Alzheimer's Disease\n"
            "  Reference: [Alzheimer's Diagnosis and Treatment Guidelines - WHO](https://www.who.int/alzheimers)\n\n"
            "- Potential Treatment: Chemotherapy for Brain Tumors\n"
            "  Reference: [PubMed: Advances in Brain Tumor Treatments](https://pubmed.ncbi.nlm.nih.gov/12345678/)\n\n"

            "### Generate the Report:\n"
            "Based on the classification results and chat history, write a detailed medical report that includes:\n"
            "1. An overview of the findings.\n"
            "2. Possible diagnoses with explanations.\n"
            "3. Recommendations for further investigation or treatment.\n"
            "4. Relevant and insightful references to support your conclusions.\n"
            )
            medical_report_prompt["content"] += f'detailes about the model : {model_details}'
        else:
            medical_report_prompt["content"] += "Provide guidance for further steps or clarification if needed."
        
        classification_message = None

        current_query.append(medical_report_prompt)

        # Generate response from the model
        def generate_response():
            stream = client.chat.completions.create(
                model="meta-llama/Meta-Llama-3-8B-Instruct",
                messages=current_query,
                max_tokens=4090,
                stream=True
            )
            for chunk in stream:
                if chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content

        return Response(generate_response(), content_type='text/plain')

    except Exception as e:
        logging.error(f"Server error: {str(e)}")
        return jsonify({"error": str(e)}), 500



@app.route('/classify-image', methods=['POST'])
def classify_image():
    """
    Endpoint to classify uploaded images using pretrained models.
    """
    if 'image' not in request.files:
        return jsonify({"error": "No image file provided"}), 400

    image_file = request.files['image']

    try:
        image = Image.open(image_file)

        # Step 1: Generate image description
        buffer = BytesIO()
        image.save(buffer, format="JPEG")
        buffer.seek(0)
        response = requests.post(BLIP_API_URL, headers=HEADERS, data=buffer.read())
        response.raise_for_status()
        description_response = response.json()
        description = description_response[0]['generated_text']

        logging.info(f"Image description: {description}")

        # Determine the type of image
        if "chest" in description.lower():
            model_details = (
                "Chest X-ray :\n"
                "Model: keremberke/yolov8m-chest-xray-classification\n"
                "Dataset: NIH Chest X-ray Dataset"
            )
            # Step 2: Classify the image
            results = chest_xray_classifier.predict(image)
            processed_result = postprocess_classify_output(chest_xray_classifier, result=results[0])
            probs_tensor = results[0].probs.data  # Access the tensor containing the probabilities
            probs_list = probs_tensor.tolist() 
            logging.info(f"Image description: {str(processed_result)}")
            return jsonify({"label": str(processed_result), "score": probs_list}), 200
            
        elif "brain" in description.lower():
            model_details = (
                "Alzheimer :\n"
                "Model: evanrsl/resnet-Alzheimer\n"
                "Dataset: NIH Chest X-Ray Dataset"
                "Brain_Tumor :\n"
                "Model: Devarshi/Brain_Tumor_Classification\n"
                "Dataset: RSNA-MICCAI Brain Tumor Radiogenomic Classification Challenge"
            )
            # Step 2: Classify the image
            image = image.resize((256, 256))
            results_brain = brain_classifier(image)
            label_b = results_brain[0]['label']
            score_b = results_brain[0]['score']

            results_Alzheimer = Alzheimer_classifier(image)
            label_a = results_Alzheimer[0]['label']
            score_a = results_Alzheimer[0]['score']

            return jsonify({"label": f" : Alzheimer --> {label_a} ; Brain tumor --> {label_b}" , "score": f" : {label_a} --> {score_a} ; {label_b} --> {score_b}"}), 200
        else : return jsonify({"label": "Unrecognized image type", "score": None}), 200
            

        

    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Image description API error: {str(e)}"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
