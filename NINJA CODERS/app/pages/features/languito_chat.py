from dotenv import load_dotenv
import streamlit as st
import os
import logging
import json
from datetime import datetime
from langchain import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
import warnings

warnings.filterwarnings("ignore")

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GeminiChat:
    def __init__(self):
        load_dotenv()
        # self.api_key = os.getenv("GOOGLE_API_KEY")
        try:
            self.api_key = os.getenv("GOOGLE_API_KEY") or st.secrets["GOOGLE_API_KEY"]
        except KeyError:
            st.error("Google API Key is not set. Please provide it as an environment variable or in Streamlit secrets.")

        if not self.api_key:
            raise ValueError("GOOGLE_API_KEY not found in environment variables")
        
        self.setup_chat()
        
    def setup_chat(self) -> None:
        """Initialize the ChatGoogleGenerativeAI with memory"""
        try:
            self.llm = ChatGoogleGenerativeAI(
                model="gemini-pro",
                google_api_key=self.api_key,
                temperature=0.7
            )

            # Initialize conversation memory
            self.memory = ConversationBufferMemory()
            
            # Create conversation chain with memory
            self.conversation = ConversationChain(
                llm=self.llm,
                memory=self.memory,
                verbose=False
            )

            self.template = """
            You are a multilingual language teacher specializing in teaching and translating various languages.
            your name is Languito. 
            When answering questions:
            1. If the user asks for translations, provide accurate translations for the requested languages.
            2. If the user asks for grammar rules or language tips, explain them clearly and concisely.
            3. If the user asks for examples, provide them with practical, everyday scenarios.
            4. If the user asks for a quiz, create a brief, fun language quiz with answers.

            Previous conversation:
            {history}

            Current Question: {question}
            if it is no question answer as human
            Response:
            """
            self.prompt_template = PromptTemplate(
                template=self.template,
                input_variables=["history", "question"]
            )
        except Exception as e:
            logger.error(f"Error setting up Chat: {str(e)}")
            raise

    def get_response(self, question: str, chat_history: list) -> str:
        """Get response from ChatGoogleGenerativeAI with conversation history"""
        try:
            # Format chat history
            history_text = "\n".join([f"{role}: {msg}" for role, msg in chat_history])
            
            # Get response using the conversation chain
            response = self.conversation.predict(
                input=self.prompt_template.format(
                    history=history_text,
                    question=question
                )
            )
            return response
        except Exception as e:
            logger.error(f"Error getting response: {str(e)}")
            raise

class StreamlitApp:
    def __init__(self):
        self.setup_page()
        self.initialize_session_state()
        self.load_chat_history()
        self.gemini = GeminiChat()

    def setup_page(self) -> None:
        """Configure Streamlit page settings"""
        st.set_page_config(
            page_title="Language Teacher",
            page_icon="🤖",
            layout="wide"
        )
        
    def initialize_session_state(self) -> None:
        """Initialize session state variables"""
        if 'chats' not in st.session_state:
            st.session_state['chats'] = {}
        if 'current_chat_id' not in st.session_state:
            st.session_state['current_chat_id'] = None
        if 'chat_history' not in st.session_state:
            st.session_state['chat_history'] = []

    def save_chat_history(self) -> None:
        """Save chat history to a JSON file"""
        try:
            data = {
                'chats': st.session_state['chats'],
                'current_chat_id': st.session_state['current_chat_id']
            }
            with open('chat_history.json', 'w') as f:
                json.dump(data, f)
        except Exception as e:
            logger.error(f"Error saving chat history: {str(e)}")

    def load_chat_history(self) -> None:
        """Load chat history from JSON file"""
        try:
            if os.path.exists('chat_history.json'):
                with open('chat_history.json', 'r') as f:
                    data = json.load(f)
                    st.session_state['chats'] = data.get('chats', {})
                    st.session_state['current_chat_id'] = data.get('current_chat_id')
                    if st.session_state['current_chat_id']:
                        st.session_state['chat_history'] = st.session_state['chats'][st.session_state['current_chat_id']]['messages']
        except Exception as e:
            logger.error(f"Error loading chat history: {str(e)}")

    def create_new_chat(self) -> None:
        """Create a new chat session"""
        if st.session_state['current_chat_id']:
            current_chat = st.session_state['chats'][st.session_state['current_chat_id']]
            if not current_chat['messages']:
                st.warning("The current chat is empty. Use it before creating a new one.")
                return

        chat_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        st.session_state['chats'][chat_id] = {
            'name': f"Chat {len(st.session_state['chats']) + 1}",
            'messages': []
        }
        st.session_state['current_chat_id'] = chat_id
        st.session_state['chat_history'] = []
        self.save_chat_history()

    def switch_chat(self, chat_id: str) -> None:
        """Switch to a different chat session"""
        st.session_state['current_chat_id'] = chat_id
        st.session_state['chat_history'] = st.session_state['chats'][chat_id]['messages']
        self.save_chat_history()

    def display_chat_selector(self) -> None:
        """Display chat selection sidebar"""
        with st.sidebar:
            st.title("Chats")
            
            if st.button("New Chat", type="secondary", key="new_chat", use_container_width=True):
                self.create_new_chat()
                st.rerun()

            for chat_id, chat_data in list(st.session_state['chats'].items()):
                cols = st.columns([5, 1])

                if cols[0].button(
                    chat_data['name'], 
                    key=f"chat_{chat_id}",
                    type="secondary" if chat_id != st.session_state['current_chat_id'] else "primary",
                    use_container_width=True
                ):
                    self.switch_chat(chat_id)
                    st.rerun()

                if cols[1].button("🗑️", key=f"delete_{chat_id}"):
                    del st.session_state['chats'][chat_id]
                    
                    if st.session_state['current_chat_id'] == chat_id:
                        st.session_state['current_chat_id'] = None
                        st.session_state['chat_history'] = []
                    
                    self.save_chat_history()
                    st.rerun()

    def display_chat_messages(self) -> None:
        """Display chat messages"""
        for role, text in st.session_state['chat_history']:
            with st.chat_message("user" if role == "You" else "assistant"):
                st.write(text)

    def main(self) -> None:
        """Main application logic"""
        if not st.session_state['chats']:
            self.create_new_chat()

        self.display_chat_selector()
        
        st.title("💬 Languito Chat!")
        
        self.display_chat_messages()
        if prompt := st.chat_input("Type your message here..."):
            try:
                with st.chat_message("user"):
                    st.write(prompt)
                st.session_state['chat_history'].append(("You", prompt))
                
                with st.chat_message("assistant"):
                    with st.spinner("Thinking..."):
                        response = self.gemini.get_response(prompt, st.session_state['chat_history'])
                        st.write(response)
                    
                    st.session_state['chat_history'].append(("Bot", response))
                
                if st.session_state['current_chat_id']:
                    st.session_state['chats'][st.session_state['current_chat_id']]['messages'] = st.session_state['chat_history']
                    self.save_chat_history()
                
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
                logger.error(f"Error in main loop: {str(e)}")

try:
    app = StreamlitApp()
    app.main()
except Exception as e:
    st.error(f"Application failed to start: {str(e)}")
    logger.error(f"Application error: {str(e)}")
