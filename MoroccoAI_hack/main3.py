from flask import Flask, render_template, request, jsonify
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch
import subprocess
from typing import Optional, List
from PIL import Image
import os
from datetime import datetime
import logging
import base64

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Load translation models
logger.info("Loading translation models...")
darija_to_english_tokenizer = AutoTokenizer.from_pretrained("ychafiqui/darija-to-english-2")
darija_to_english_model = AutoModelForSeq2SeqLM.from_pretrained("ychafiqui/darija-to-english-2")
english_to_darija_tokenizer = AutoTokenizer.from_pretrained("atlasia/Terjman-Ultra")
english_to_darija_model = AutoModelForSeq2SeqLM.from_pretrained("atlasia/Terjman-Ultra")

# Setup devices
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
darija_to_english_model = darija_to_english_model.to(device)
english_to_darija_model = english_to_darija_model.to("cpu")

def translate_darija_to_english(darija_text):
    try:
        input_tokens = darija_to_english_tokenizer(darija_text, return_tensors="pt", padding=True, truncation=True).to(device)
        output_tokens = darija_to_english_model.generate(**input_tokens)
        torch.cuda.empty_cache()
        return darija_to_english_tokenizer.decode(output_tokens[0], skip_special_tokens=True)
    except Exception as e:
        logger.error(f"Error in Darija to English translation: {e}")
        return darija_text

def translate_english_to_darija(english_text):
    try:
        input_tokens = english_to_darija_tokenizer(english_text, return_tensors="pt", padding=True, truncation=True).to("cpu")
        output_tokens = english_to_darija_model.generate(
            **input_tokens,
            max_length=768,
            temperature=0.7,
            top_k=50
        )
        
        translation = english_to_darija_tokenizer.decode(output_tokens[0], skip_special_tokens=True)
        
        # Check for any ending punctuation
        if not any(translation.endswith(p) for p in ['.', '!', '?']):
            indices = [translation.rfind(p) for p in ['.', '!', '?']]
            last_punct_index = max(indices)
            
            if last_punct_index != -1:
                translation = translation[:last_punct_index + 1]
        
        return translation
    except Exception as e:
        logger.error(f"Error in English to Darija translation: {e}")
        return english_text

class PregnancyAgent:
    def __init__(self):
        self.model = "llava:7b"

    def _run_model(self, prompt: str, image_path: str = None) -> str:
        try:
            if image_path:
                command = f'ollama run {self.model} "{prompt}" "{image_path}"'
            else:
                command = f'ollama run {self.model} "{prompt}"'
            
            logger.info(f"Running command: {command}")
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            
            if result.stderr:
                logger.error(f"Model error: {result.stderr}")
            
            return result.stdout.strip() or "عذراً، لم أتمكن من معالجة طلبك."
            
        except Exception as e:
            logger.error(f"Error running model: {e}")
            return f"عذراً، حدث خطأ: {str(e)}"

    def process_image(self, image: Image.Image) -> Optional[str]:
        if image:
            try:
                image_path = os.path.join(app.config['UPLOAD_FOLDER'], 'temp_image.jpg')
                if image.mode != 'RGB':
                    image = image.convert('RGB')
                image.save(image_path, 'JPEG')
                logger.info(f"Saved image to: {image_path}")
                return image_path
            except Exception as e:
                logger.error(f"Error processing image: {e}")
        return None

class DietaryGuidanceAgent(PregnancyAgent):
    def respond(self, history: List[List[str]], darija_prompt: str, image: Optional[Image.Image] = None) -> List[List[str]]:
        english_prompt = translate_darija_to_english(darija_prompt)
        image_path = self.process_image(image) if image else None

        try:
            if image_path:
                system_prompt = (
                    f"You are a nutritional specialist for pregnant women. "
                    f"Analyze this image and provide advice about the food or medication shown. "
                    f"Question: {english_prompt}"
                )
            else:
                system_prompt = f"""You are a pregnancy nutritionist. Briefly answer in one short paragraph this question: {english_prompt}
                - Focus on food safety during pregnancy
                - Provide clear nutritional guidance
                - Suggest healthy alternatives if needed
                - Include portion recommendations"""

            english_response = self._run_model(system_prompt, image_path)
            
            if image_path and os.path.exists(image_path):
                os.remove(image_path)

            darija_response = translate_english_to_darija(english_response)
            history = history or []
            history.append([darija_prompt, darija_response])
            return history

        except Exception as e:
            logger.error(f"Error in dietary guidance: {e}")
            history = history or []
            history.append([darija_prompt, "عذراً، حدث خطأ في معالجة طلبك."])
            return history

class QuestionAnsweringAgent(PregnancyAgent):
    def respond(self, history: List[List[str]], darija_prompt: str, image: Optional[Image.Image] = None) -> List[List[str]]:
        english_prompt = translate_darija_to_english(darija_prompt)
        image_path = self.process_image(image) if image else None

        try:
            if image_path:
                system_prompt = (
                    f"You are a pregnancy health specialist. "
                    f"Analyze this medical image and provide advice about the situation shown. "
                    f"Question: {english_prompt}"
                )
            else:
                system_prompt = f"""You are a pregnancy expert. Briefly answer in one short paragraph this question: {english_prompt}
                - Provide clear medical information
                - Focus on general wellness
                - Recommend consulting healthcare providers when needed"""

            english_response = self._run_model(system_prompt, image_path)
            
            if image_path and os.path.exists(image_path):
                os.remove(image_path)

            darija_response = translate_english_to_darija(english_response)
            history = history or []
            history.append([darija_prompt, darija_response])
            return history

        except Exception as e:
            logger.error(f"Error in question answering: {e}")
            history = history or []
            history.append([darija_prompt, "عذراً، حدث خطأ في معالجة طلبك."])
            return history

class PostPregnancyAgent(PregnancyAgent):
    def respond(self, history: List[List[str]], darija_prompt: str, image: Optional[Image.Image] = None) -> List[List[str]]:
        english_prompt = translate_darija_to_english(darija_prompt)
        image_path = self.process_image(image) if image else None

        try:
            if image_path:
                system_prompt = (
                    f"You are a postpartum and baby care specialist. "
                    f"Analyze this image and provide advice about the situation shown. "
                    f"Question: {english_prompt}"
                )
            else:
                system_prompt = f"""You are a postpartum specialist. Briefly answer in one short paragraph this question: {english_prompt}
                - Focus on mother and baby care
                - Provide practical advice
                - Include safety guidelines
                - Emphasize recovery and wellness"""

            english_response = self._run_model(system_prompt, image_path)
            
            if image_path and os.path.exists(image_path):
                os.remove(image_path)

            darija_response = translate_english_to_darija(english_response)
            history = history or []
            history.append([darija_prompt, darija_response])
            return history

        except Exception as e:
            logger.error(f"Error in postpartum guidance: {e}")
            history = history or []
            history.append([darija_prompt, "عذراً، حدث خطأ في معالجة طلبك."])
            return history

class ChatbotBackend:
    def __init__(self):
        self.agents = {
            'الإرشاد الغذائي': DietaryGuidanceAgent(),
            'الأسئلة العامة': QuestionAnsweringAgent(),
            'دعم ما بعد الولادة': PostPregnancyAgent()
        }
        self.chat_history = []
        logger.info("ChatbotBackend initialized successfully")

    def get_response(self, darija_prompt: str, agent_type: str = "الإرشاد الغذائي", image_path: str = None):
        try:
            logger.info(f"Processing request - Message: {darija_prompt}, Agent: {agent_type}")
            
            agent = self.agents.get(agent_type)
            if not agent:
                return "عذراً، لم يتم العثور على الوكيل المطلوب."

            # Convert image path to PIL Image if exists
            image = None
            if image_path and os.path.exists(image_path):
                image = Image.open(image_path)

            # Get response from appropriate agent
            new_history = agent.respond(self.chat_history, darija_prompt, image)
            
            # Update history and return latest response
            self.chat_history = new_history
            return new_history[-1][1] if new_history else "عذراً، لم يتم تلقي رد."

        except Exception as e:
            logger.error(f"Error in get_response: {e}")
            return f"عذراً، حدث خطأ: {str(e)}"

# Initialize chatbot
chatbot = ChatbotBackend()

# Flask routes
@app.route('/')
def home():
    return render_template('welcome.html')

@app.route('/agents')
def agents():
    return render_template('agents.html')

@app.route('/chat/<agent_type>')
def chat(agent_type):
    agent_types = {
        'dietary': "الإرشاد الغذائي",
        'qa': "الأسئلة العامة",
        'postpartum': "دعم ما بعد الولادة"
    }
    
    agent_type_arabic = agent_types.get(agent_type)
    if not agent_type_arabic:
        return "Coming Soon!", 404
        
    return render_template('chat.html', agent_type=agent_type_arabic)

@app.route('/send_message', methods=['POST'])
def send_message():
    try:
        message = request.form.get('message', '')
        agent_type = request.form.get('agent_type', 'الإرشاد الغذائي')
        image = request.files.get('image')
        image_path = None

        if image:
            try:
                filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{image.filename}"
                image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                image.save(image_path)
                logger.info(f"Saved image to: {image_path}")
            except Exception as e:
                logger.error(f"Error saving image: {e}")
                return jsonify({
                    'status': 'error',
                    'message': 'Error processing image'
                }), 500

        response = chatbot.get_response(message, agent_type, image_path)
        
        if image_path and os.path.exists(image_path):
            os.remove(image_path)

        return jsonify({
            'status': 'success',
            'response': response,
            'timestamp': datetime.now().strftime("%I:%M %p")
        })

    except Exception as e:
        logger.error(f"Error in send_message: {e}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)