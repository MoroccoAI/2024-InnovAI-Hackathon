from flask import Flask, render_template, request, jsonify
from gradio_client import Client, handle_file
import os
from datetime import datetime
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

class ChatbotBackend:
    def __init__(self):
        try:
            self.client = Client("https://9235e3160b054ea104.gradio.live/")
            self.chat_history = []
            logger.info("ChatbotBackend initialized successfully")
        except Exception as e:
            logger.error(f"Error initializing ChatbotBackend: {e}")
            raise

    def get_response(self, darija_prompt: str, agent_type: str = "الإرشاد الغذائي", image_path: str = None):
        try:
            logger.info(f"Processing request - Message: {darija_prompt}, Agent: {agent_type}, Image: {'Yes' if image_path else 'No'}")
            
            params = {
                'message': darija_prompt,
                'agent_selection': agent_type,
                'history': self.chat_history,
                'api_name': "/respond_and_clear"
            }

            if image_path and os.path.exists(image_path):
                params['img'] = handle_file(image_path)
                logger.info(f"Added image to request: {image_path}")
            else:
                params['img'] = None

            logger.info("Sending request to Gradio backend")
            result = self.client.predict(**params)
            
            if not result or not result[2]:
                logger.warning("Received empty response from backend")
                return "عذراً، لم يتم تلقي رد."

            self.chat_history = result[2]
            return result[2][-1][1]

        except Exception as e:
            logger.error(f"Error in get_response: {e}")
            return f"عذراً، حدث خطأ: {str(e)}"

# Initialize chatbot
chatbot = ChatbotBackend()

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

        logger.info(f"Received message request - Message: {message}, Agent: {agent_type}")

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
        
        # Cleanup image file
        if image_path and os.path.exists(image_path):
            try:
                os.remove(image_path)
                logger.info("Cleaned up temporary image file")
            except Exception as e:
                logger.warning(f"Error removing temporary image: {e}")

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
    # Ensure the uploads directory exists
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    # Start the Flask app
    app.run(debug=True, host='0.0.0.0', port=5000)