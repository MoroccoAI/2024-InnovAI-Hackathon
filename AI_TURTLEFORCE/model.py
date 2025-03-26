import os
import gradio as gr
import cv2
import librosa
import librosa.display
import torch
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter
from fer import FER
from transformers import Wav2Vec2ForSequenceClassification, Wav2Vec2FeatureExtractor
from flask import Flask, request, jsonify
from flask_cors import CORS
from groq import Groq
import requests
from threading import Thread
import concurrent.futures

# Set the environment variables before importing libraries
os.environ['KMP_DUPLICATE_LIB_OK'] = 'TRUE'  # Allow duplicate OpenMP libraries
os.environ['OMP_NUM_THREADS'] = '1'  # Limit the number of OpenMP threads to 1

# Flask app for Groq Chatbot
app = Flask(__name__)
CORS(app)

# Groq API Setup
client = Groq(api_key="your_api_key")


# Configuration des modèles
weight_model1 = 0.7  # Pondération pour le modèle FER
weight_model2 = 0.3  # Pondération pour le modèle audio
pain_threshold = 0.4  # Seuil pour détecter la douleur
confidence_threshold = 0.3  # Seuil de confiance pour les émotions
pain_emotions = ["angry", "fear", "sad"]  # Émotions liées à la douleur

# Fonction pour détecter si l'entrée est un audio ou une vidéo
def detect_input_type(file_path):
    _, ext = os.path.splitext(file_path)
    if ext.lower() in ['.mp3', '.wav', '.flac']:
        return 'audio'
    elif ext.lower() in ['.mp4', '.avi', '.mov', '.mkv']:
        return 'video'
    else:
        return 'unknown'

# ---- Modèle FER (Vision) ----
def extract_frames_and_analyze(video_path, fer_detector, sampling_rate=1):
    cap = cv2.VideoCapture(video_path)
    pain_scores = []
    frame_indices = []
    frame_count = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Ne traiter qu'une frame sur n pour optimiser la performance
        if frame_count % sampling_rate == 0:
            # Détecter l'émotion dominante
            emotion, score = fer_detector.top_emotion(frame)
            if emotion in pain_emotions and score >= confidence_threshold:
                pain_scores.append(score)
                frame_indices.append(frame_count)

        frame_count += 1

    cap.release()

    # Si des scores sont détectés, appliquer le smoothing
    if pain_scores:
        window_length = min(5, len(pain_scores))
        if window_length % 2 == 0:
            window_length = max(3, window_length - 1)

        # Ensure window_length is less than or equal to the length of pain_scores
        window_length = min(window_length, len(pain_scores))

        # Ensure polyorder is less than window_length
        polyorder = min(2, window_length - 1)

        pain_scores = savgol_filter(pain_scores, window_length, polyorder=polyorder)

    return pain_scores, frame_indices

# ---- Modèle Audio ----
def analyze_audio(audio_path, model, feature_extractor):
    try:
        audio, sr = librosa.load(audio_path, sr=16000)
        inputs = feature_extractor(audio, sampling_rate=sr, return_tensors="pt", padding=True)
        with torch.no_grad():
            logits = model(**inputs).logits
        probs = torch.nn.functional.softmax(logits, dim=-1)

        pain_scores = []
        for idx, prob in enumerate(probs[0]):
            emotion = model.config.id2label[idx]
            if emotion in pain_emotions:
                pain_scores.append(prob.item())
        return pain_scores
    except Exception as e:
        print(f"Erreur lors de l'analyse audio : {e}")
        return []

# ---- Fusion des scores ----
def combine_scores(scores_model1, scores_model2, weight1, weight2):
    """Combine scores from FER and audio models using weights."""

    # If any list is empty, fill it with 0 values to match the other model's length
    if len(scores_model1) == 0:
        scores_model1 = [0] * len(scores_model2)
    if len(scores_model2) == 0:
        scores_model2 = [0] * len(scores_model1)

    # Combine the scores using weights
    combined_scores = [
        (weight1 * score1 + weight2 * score2)
        for score1, score2 in zip(scores_model1, scores_model2)
    ]

    return combined_scores

# ---- Traitement de l'entrée audio ou vidéo ----
def process_input(file_path, fer_detector, model, feature_extractor):
    input_type = detect_input_type(file_path)

    if input_type == 'audio':
        pain_scores_model1 = []
        pain_scores_model2 = analyze_audio(file_path, model, feature_extractor)
        final_scores = pain_scores_model2  # Pas de normalisation nécessaire ici
    elif input_type == 'video':
        # Traitement en parallèle des vidéos et de l'audio
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future_video = executor.submit(extract_frames_and_analyze, file_path, fer_detector, sampling_rate=5)
            future_audio = executor.submit(analyze_audio, file_path, model, feature_extractor)

            pain_scores_model1, frame_indices = future_video.result()
            pain_scores_model2 = future_audio.result()

        final_scores = combine_scores(pain_scores_model1, pain_scores_model2, weight_model1, weight_model2)
    else:
        return "Type de fichier non pris en charge. Veuillez fournir un fichier audio ou vidéo."

    # Décision finale
    average_pain = sum(final_scores) / len(final_scores) if final_scores else 0
    pain_detected = average_pain > pain_threshold
    result = "Pain" if pain_detected else "No Pain"

    # Affichage des résultats
    if not final_scores:
        plt.text(0.5, 0.5, "No Data Available", ha='center', va='center', fontsize=16)
    else:
        plt.plot(range(len(final_scores)), final_scores, label="Combined Pain Scores", color="purple")
        plt.axhline(y=pain_threshold, color="green", linestyle="--", label="Pain Threshold")
        plt.xlabel("Frame / Sample Index")
        plt.ylabel("Pain Score")
        plt.title("Pain Detection Scores")
        plt.legend()
        plt.grid(True)
    
    # Save the graph as a file
    graph_filename = "pain_detection_graph.png"
    plt.savefig(graph_filename)
    plt.close()

    return result, average_pain, graph_filename


@app.route('/message', methods=['POST'])
def handle_message():
    user_input = request.json.get('message', '')
    completion = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[{"role": "user", "content": user_input}],
        temperature=1,
        max_tokens=1024,
        top_p=1,
        stream=True,
        stop=None,
    )

    response = ""
    for chunk in completion:
        response += chunk.choices[0].delta.content or ""

    return jsonify({'reply': response})

# Chatbot interaction function
def gradio_interface(file, chatbot_input, state_pain_results):
    model_name = "superb/wav2vec2-large-superb-er"
    model = Wav2Vec2ForSequenceClassification.from_pretrained(model_name)
    feature_extractor = Wav2Vec2FeatureExtractor.from_pretrained(model_name)
    detector = FER(mtcnn=True)

    chatbot_response = "How can I assist you today?"  # Default chatbot response
    pain_result = ""
    average_pain = ""
    graph_filename = ""

    # Handle file upload and process it when Submit is clicked
    if file:
        result, average_pain, graph_filename = process_input(file.name, detector, model, feature_extractor)
        state_pain_results["result"] = result
        state_pain_results["average_pain"] = average_pain
        state_pain_results["graph_filename"] = graph_filename

        # Custom chatbot response based on pain detection
        if result == "No Pain":
            chatbot_response = "It seems there's no pain detected. How can I assist you further?"
        else:
            chatbot_response = "It seems you have some pain. Would you like me to help with it or provide more details?"

        # Update pain result and graph filename
        pain_result = result
    else:
        # Use the existing state if no new file is uploaded
        pain_result = state_pain_results.get("result", "")
        average_pain = state_pain_results.get("average_pain", "")
        graph_filename = state_pain_results.get("graph_filename", "")

        # If the chatbot_input field is not empty, process the chat message
        if chatbot_input:
            # Send message to Flask server to get the response from Groq model
            response = requests.post(
                'http://localhost:5000/message', json={'message': chatbot_input}
            )
            data = response.json()
            chatbot_response = data['reply']

    # Ensure 4 outputs: pain_result, average_pain, graph_output, chatbot_output
    return pain_result, average_pain, graph_filename, chatbot_response


# Start Flask server in a thread
def start_flask():
    app.run(debug=True, use_reloader=False)

# Launch Gradio and Flask
if __name__ == "__main__":
    # Start Flask in a separate thread
    flask_thread = Thread(target=start_flask)
    flask_thread.start()

    # Gradio interface
    with gr.Blocks() as interface:
        gr.Markdown("<h1 style='text-align:center;'>PainSense: AI-Driven Pain Detection and Chatbot Assistance</h1>")

        with gr.Row():
            with gr.Column(scale=1):
                file_input = gr.File(label="Upload Audio or Video File")
                with gr.Row():  # Place buttons next to each other
                    clear_button = gr.Button("Clear", elem_id="clear_btn")
                    submit_button = gr.Button("Submit", variant="primary", elem_id="submit_button")
                chatbot_input = gr.Textbox(label="Chat with AI", placeholder="Ask a question...", interactive=True)
                chatbot_output = gr.Textbox(label="Chatbot Response", interactive=False)

            with gr.Column(scale=1):
                pain_result = gr.Textbox(label="Pain Detection Result")
                average_pain = gr.Textbox(label="Average Pain")
                graph_output = gr.Image(label="Pain Detection Graph")

        state = gr.State({"result": "", "average_pain": "", "graph_filename": ""})

        # Clear button resets the UI, including the file input, chatbot input, and outputs
        clear_button.click(lambda: (None, None, "", ""), outputs=[pain_result, average_pain, graph_output, chatbot_output, file_input])

        # File input only triggers processing when the submit button is clicked
        submit_button.click(
            gradio_interface,
            inputs=[file_input, chatbot_input, state],
            outputs=[pain_result, average_pain, graph_output, chatbot_output],
        )

        # Chat input triggers chatbot response when 'Enter' is pressed
        chatbot_input.submit(
            lambda file, chatbot_input, state: gradio_interface(file, chatbot_input, state)[-1],  # Only update chatbot_output
            inputs=[file_input, chatbot_input, state],
            outputs=[chatbot_output]  # Only update chatbot output
        )

    interface.launch(debug=True)
