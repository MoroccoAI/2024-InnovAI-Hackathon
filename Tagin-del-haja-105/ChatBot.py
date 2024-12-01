import os
import json
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.memory import ConversationBufferMemory
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
import re

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
    def get_response(self, user_input, user_profile=None):
        try:
            if user_profile:
                # Add user profile to context only once at the beginning of the conversation
                profile_context = f"User Profile:\nName: {user_profile['name']}\nCareer Goals: {user_profile['career_goals']}\nEducation: {user_profile['education']}\nSkills: {user_profile['skills']}\n\n"
                # Update prompt to include the user profile once
                prompt_with_profile = ChatPromptTemplate.from_messages([
                    ("system", f"You are a career counseling AI assistant. Use the following external knowledge when relevant:\n{self.external_context}\n{profile_context}\n\nRespond conversationally, guiding the user towards their career goals and suggesting personalized advice."),
                    MessagesPlaceholder(variable_name="chat_history"),
                    ("human", "{input}")
                ])
                self.chat_chain = self.create_chat_chain()  # Reinitialize chain with new prompt including user profile
                self.prompt = prompt_with_profile  # Set the prompt with the user profile context

            # Generate response
            response = self.chat_chain.invoke({"input": user_input})
            
            # Add messages to memory
            self.memory.chat_memory.add_user_message(user_input)
            self.memory.chat_memory.add_ai_message(response)
            
            # Clean up response formatting before returning
            return response

        except Exception as e:
            print(f"An error occurred: {e}")
            return "Sorry, I couldn't process that request."