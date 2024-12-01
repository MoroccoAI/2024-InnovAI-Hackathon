import os
import json
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.memory import ConversationBufferMemory
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

class CareerCounselingChatbot:
    def __init__(self, json_file_path, groq_api_key):
        # Set up Groq API key
        os.environ["GROQ_API_KEY"] = groq_api_key

        # Load external JSON data for career-related content
        self.external_data = self.load_json_data(json_file_path)
        
        # Create context from JSON data
        self.external_context = self.create_context_from_json(self.external_data)

        # Create memory for conversation history
        self.memory = ConversationBufferMemory(return_messages=True, memory_key="chat_history")

        # Create a chat model
        self.chat_model = ChatGroq(
            model="llama3-8b-8192",
            temperature=0.7
        )

        # Create a prompt template with chat history and external context
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", f"You are a career counseling AI assistant. Use the following external knowledge when relevant:\n{self.external_context}\n\nRespond conversationally, guiding the user towards their career goals and suggesting personalized advice."),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{input}")
        ])

        # Create the chain with memory
        self.chat_chain = self.create_chat_chain()

    # Function to load JSON data
    def load_json_data(self, file_path):
        try:
            with open(file_path, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            print(f"Error: File {file_path} not found.")
            return {}
        except json.JSONDecodeError:
            print(f"Error: Invalid JSON in {file_path}")
            return {}

    # Function to create context from JSON data
    def create_context_from_json(self, data):
        context = "External Knowledge Base for Career Counseling:\n"
        for key, item in data.items():
            if isinstance(item, dict):
                context += f"Entity: {item.get('entity', 'N/A')}\n"
                context += f"URL: {item.get('url', 'N/A')}\n"
                
                if 'topics' in item:
                    context += "Career-related Topics:\n"
                    for topic in item['topics']:
                        context += f"- {topic.get('data-title', 'Unknown Topic')}\n"
                        if 'subtopic' in topic:
                            for subtopic in topic['subtopic']:
                                context += f"  * {subtopic}\n"
                context += "\n"
        return context

    # Function to create the chat chain
    def create_chat_chain(self):
        chain = (
            RunnablePassthrough.assign(
                chat_history=lambda _: self.memory.chat_memory.messages
            )
            | self.prompt
            | self.chat_model
            | StrOutputParser()
        )
        return chain

    # Function to create a user profile (Can be extended for web input)
    def create_user_profile(self, name, career_goals, education, skills):
        return {
            "name": name,
            "career_goals": career_goals,
            "education": education,
            "skills": skills
        }

    # Function to interact with the chatbot and get responses
    def get_response(self, user_input, user_profile):
        try:
            # Customize the chatbot's response based on the user profile
            customized_input = f"{user_profile['career_goals']} | {user_profile['education']} | {user_profile['skills']} | {user_input}"
            
            # Generate response
            response = self.chat_chain.invoke({"input": customized_input})
            
            # Add messages to memory
            self.memory.chat_memory.add_user_message(user_input)
            self.memory.chat_memory.add_ai_message(response)
            
            return response

        except Exception as e:
            print(f"An error occurred: {e}")
            return "Sorry, I couldn't process that request."

# Example usage:
if __name__ == "__main__":
    # Initialize the chatbot
    json_file_path = 'topics_data.json'  # Replace with your JSON file path
    groq_api_key = "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"  # Replace with your Groq API key
    chatbot = CareerCounselingChatbot(json_file_path, groq_api_key)

    # Example user profile
    user_profile = chatbot.create_user_profile(
        name="John Doe",
        career_goals="Data Science",
        education="Bachelor's in Computer Science",
        skills="Python, Machine Learning"
    )

    # Simulating a conversation
    user_input = "What courses should I take to improve my skills?"
    response = chatbot.get_response(user_input, user_profile)
    print("AI Chatbot:", response)
