import os
import streamlit as st
import sqlite3
import pandas as pd
import json
from pathlib import Path
import google.generativeai as genai
from typing import Dict, TypedDict, List, Tuple, Optional
from langgraph.graph import Graph, StateGraph
from langchain_core.messages import HumanMessage, AIMessage
from langchain_google_genai import ChatGoogleGenerativeAI

# Define GraphState
class GraphState(TypedDict):
    question: str
    sql_query: Optional[str]
    sql_result: Optional[pd.DataFrame]
    answer: Optional[str]
    error: Optional[str]
    thinking_process: List[str]
    question_type: Optional[str]
    history: Optional[str]
    settings_context: Optional[Dict]

# Define Gemini
if 'GOOGLE_API_KEY' in st.secrets:
    os.environ['GOOGLE_API_KEY'] = st.secrets['GOOGLE_API_KEY']
    genai.configure(api_key=st.secrets['GOOGLE_API_KEY'])
else:
    st.error("Please set your Google API key in .streamlit/secrets.toml")
    st.stop()

# Initialize Gemini model
model = ChatGoogleGenerativeAI(model="gemini-1.5-flash")

# Database connection
def get_db_connection():
    return sqlite3.connect('SIIR.AI_chatbot/afcon2025.db')

# Retrieve the current database schema
def get_db_schema():
    """Retrieve the current database schema."""
    conn = sqlite3.connect('SIIR.AI_chatbot/afcon2025.db')
    cursor = conn.cursor()
    
    try:
        # Get list of all tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        
        if not tables:
            return "No tables found in database"
        
        schema = []
        for table in tables:
            table_name = table[0]
            # Get column info for each table
            cursor.execute(f"PRAGMA table_info({table_name});")
            columns = cursor.fetchall()
            
            # Get row count for each table
            cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
            row_count = cursor.fetchone()[0]
            
            # Format column information
            columns_info = [f"{col[1]} ({col[2]})" for col in columns]
            schema.append(f"Table: {table_name} ({row_count} rows)\nColumns: {', '.join(columns_info)}")
        
        return "\n\n".join(schema)
    except Exception as e:
        return f"Error getting schema: {str(e)}"
    finally:
        conn.close()

# SQL Agent that generates and executes SQL queries
def sql_agent(state: Dict) -> Dict:
    """Generate SQL query based on the question."""
    question = state['question']
    history = state.get('history', '')
    
    # Log the start of processing
    state['thinking_process'].append("🤔 Understanding your question and context...")
    
    # Get current database schema and verify tables
    db_schema = get_db_schema()
    state['thinking_process'].append(f"📊 Current database schema:\n{db_schema}")
    
    # Create the Gemini model for SQL generation
    model = ChatGoogleGenerativeAI(model="gemini-pro")
    
    # Prepare the prompt for SQL generation
    prompt = f"""Given the following database schema:
{db_schema}

Generate a SQL query to answer this question: {question}

Previous conversation context (if any):
{history}

Requirements:
1. Return ONLY the SQL query, no explanations
2. Use proper SQL syntax for SQLite
3. If the question cannot be answered with the available schema, return 'INVALID'
"""
    
    # Generate SQL query
    response = model.invoke([HumanMessage(content=prompt)])
    sql_query = response.content.strip()
    
    # Clean the SQL query by removing markdown formatting
    sql_query = sql_query.replace('```sql', '').replace('```', '').strip()
    
    if sql_query == 'INVALID':
        state['error'] = "I cannot answer this question with the available data"
        state['thinking_process'].append("❌ Question cannot be answered with available data")
        return state
    
    # Execute the query
    try:
        conn = get_db_connection()
        df = pd.read_sql_query(sql_query, conn)
        conn.close()
        
        if df.empty:
            state['error'] = "No results found for your query"
            state['thinking_process'].append("ℹ️ Query executed successfully but no results found")
        else:
            state['sql_result'] = df
            state['thinking_process'].append("✅ Query executed successfully")
        
        state['sql_query'] = sql_query
        
    except Exception as e:
        state['error'] = f"Error executing query: {str(e)}"
        state['thinking_process'].append(f"❌ Error during query execution: {str(e)}")
    
    return state

# Answer Generation Agent that creates natural language responses
def answer_agent(state: Dict) -> Dict:
    state['thinking_process'].append("🤖 Generating natural language response...")
    history = state.get('history', '')
    
    if state.get('error'):
        state['answer'] = f"I encountered an error: {state['error']}"
        state['thinking_process'].append("❌ Error encountered, providing error message")
        return state
    
    # Handle cases where there's no SQL result (conversation continuations)
    if state.get('sql_result') is None:
        system_prompt = """You are a friendly AI assistant specializing in AFCON 2025. 
        Provide a helpful response to continue the conversation, acknowledging the user's input.
        If they're asking for more time or information, be accommodating and explain what you can do to help."""
        
        context = f"""
        Previous conversation:
        {history}
        
        Current question: {state['question']}
        """
        
        messages = [
            HumanMessage(content=system_prompt),
            HumanMessage(content=context)
        ]
        
        response = model.invoke(messages).content
        state['answer'] = response
        state['thinking_process'].append("✅ Generated conversational response")
        return state
    
    # Handle database query responses
    df = state['sql_result']
    question = state['question']
    
    system_prompt = """You are an expert on AFCON 2025. Given the conversation history, question, and query results, 
    provide a natural, conversational response. Make it informative but concise. Maintain context from previous messages."""
    
    context = f"""
    Previous conversation:
    {history}
    
    Current question: {question}
    Query Results: {df.to_string()}
    """
    
    messages = [
        HumanMessage(content=system_prompt),
        HumanMessage(content=context)
    ]
    
    response = model.invoke(messages).content
    state['answer'] = response
    state['thinking_process'].append("✅ Response generated successfully!")
    
    return state

# General answer agent
def general_answer_agent(state: Dict) -> Dict:
    """Handle non-database questions."""
    state['thinking_process'].append("💭 Generating general response...")
    
    # Load settings for personalization
    settings = load_settings()
    custom_settings = settings.get('custom_settings', {})
    
    # Analyze if the question is asking about personal information
    system_prompt_analyzer = """You are an expert at analyzing questions about personal information.
    Determine if the question is asking about any personal details and if so, which specific detail.
    Return ONLY the key from custom settings that would answer this question, or 'none' if no match.
    Example: For 'how old are you' return 'age', for 'what's my name' return 'personal name'"""
    
    analyzer_messages = [
        HumanMessage(content=system_prompt_analyzer),
        HumanMessage(content=f"Question: {state['question']}\nAvailable custom settings: {list(custom_settings.keys())}")
    ]
    
    try:
        requested_info = model.invoke(analyzer_messages).content.strip().lower()
        
        if requested_info != 'none' and requested_info in custom_settings:
            # Question is about available personal info
            state['thinking_process'].append(f"📍 Question requests personal info: {requested_info}")
            
            system_prompt = f"""You are an AI assistant for AFCON 2025.
            The user ({custom_settings.get('personal name', 'User')}) is asking about their {requested_info}.
            Their {requested_info} is: {custom_settings[requested_info]}
            
            Guidelines:
            1. Answer naturally using the available information
            2. Use their name if available
            3. Match their preferred language style: {settings.get('language_style', 'professional')}
            4. Keep response length: {settings.get('response_length', 'concise')}"""
            
        else:
            # General question or unavailable personal info
            state['thinking_process'].append("📍 General question or unavailable personal info")
            
            system_prompt = f"""You are an AI assistant for AFCON 2025.
            
            Available personal information:
            {json.dumps(custom_settings, indent=2)}
            
            Guidelines:
            1. If the question asks for unavailable personal info, politely explain you don't have that information
            2. For general questions, provide helpful AFCON 2025 information
            3. Use their name ({custom_settings.get('personal name', 'User')}) naturally if available
            4. Match their preferred language style: {settings.get('language_style', 'professional')}
            5. Keep response length: {settings.get('response_length', 'concise')}"""
    
        context = f"""
        Previous conversation:
        {state.get('history', '')}
        
        Current question: {state['question']}
        """
        
        messages = [
            HumanMessage(content=system_prompt),
            HumanMessage(content=context)
        ]
        
        response = model.invoke(messages).content
        state['answer'] = response
        state['thinking_process'].append("✅ Generated personalized response")
        
    except Exception as e:
        state['error'] = str(e)
        state['thinking_process'].append(f"❌ Error generating response: {str(e)}")
    
    return state

# Classify question type
def classify_question(state: Dict) -> Dict:
    """Determine if the question requires database access."""
    question = state['question']
    history = state.get('history', '')
    
    system_prompt = """Determine if the question requires querying the AFCON 2025 database.
    Return ONLY 'database' or 'general' without any other text.
    
    Database questions examples:
    - "Which teams are in Group A?"
    - "Show me hotels in Casablanca"
    - "When is Morocco playing?"
    
    General questions examples:
    - "What is AFCON?"
    - "How are you?"
    - "Tell me about yourself"
    - "it's ok to take more time"
    - "can you show me more?"
    """
    
    context = f"""
    Previous conversation:
    {history}
    
    Current question: {question}
    """
    
    messages = [
        HumanMessage(content=system_prompt),
        HumanMessage(content=context)
    ]
    
    response = model.invoke(messages).content.strip().lower()
    state['question_type'] = 'database' if 'database' in response else 'general'
    state['thinking_process'].append(f"🤔 Question classified as: {state['question_type']}")
    return state

def load_settings():
    """Load settings from JSON file"""
    settings_file = Path(__file__).parent / "settings.json"
    try:
        if settings_file.exists():
            with open(settings_file, 'r') as f:
                return json.load(f)
        return {}
    except Exception as e:
        st.error(f"Error loading settings: {str(e)}")
        return {}

def settings_preprocessor(state: Dict) -> Dict:
    """Agent that checks if question relates to settings and adds context"""
    state['thinking_process'].append("🔍 Checking for relevant settings...")
    
    # Load current settings
    settings = load_settings()
    if not settings:
        state['thinking_process'].append("ℹ️ No settings found or error loading settings")
        return state
    
    # Prepare context for settings analysis
    system_prompt = """You are an expert at analyzing questions and determining relevant settings.
    Given a question and available settings, determine which settings are relevant and how they should modify the query.
    Return ONLY a JSON object with the relevant settings and their impact. Return an empty object if no settings are relevant."""
    
    context = f"""
    Question: {state['question']}
    Available Settings: {json.dumps(settings, indent=2)}
    
    Example outputs:
    {{"preferred_currency": "EUR", "impact": "convert prices to EUR"}}
    {{"date_format": "DD-MM-YYYY", "impact": "format dates accordingly"}}
    {{"language_style": "technical", "impact": "use technical terms"}}
    """
    
    messages = [
        HumanMessage(content=system_prompt),
        HumanMessage(content=context)
    ]
    
    try:
        response = model.invoke(messages).content.strip()
        relevant_settings = json.loads(response)
        
        if relevant_settings:
            state['settings_context'] = relevant_settings
            state['thinking_process'].append(f"✅ Found relevant settings: {relevant_settings}")
        else:
            state['thinking_process'].append("ℹ️ No relevant settings for this query")
            
    except Exception as e:
        state['thinking_process'].append(f"⚠️ Error analyzing settings: {str(e)}")
        state['settings_context'] = {}
    
    return state

def settings_postprocessor(state: Dict) -> Dict:
    """Agent that enhances the final response based on settings"""
    if not state.get('answer'):
        return state
        
    state['thinking_process'].append("🎨 Cleaning and formatting response...")
    
    # Load current settings
    settings = load_settings()
    if not settings:
        return state
    
    system_prompt = """You are an expert at formatting responses.
    Clean up the given response by:
    1. Removing any technical comments or explanations about settings/formatting
    2. Removing parenthetical explanations about processing
    3. Keeping only the actual response content
    4. Ensuring the response is natural and conversational
    
    Example Input: "Your name is John. (Response formatted according to professional style, no currency conversion needed)"
    Example Output: "Your name is John."
    """
    
    context = f"Original Response: {state['answer']}"
    
    messages = [
        HumanMessage(content=system_prompt),
        HumanMessage(content=context)
    ]
    
    try:
        cleaned_response = model.invoke(messages).content.strip()
        state['answer'] = cleaned_response
        state['thinking_process'].append("✅ Cleaned response format")
    except Exception as e:
        state['thinking_process'].append(f"⚠️ Error cleaning response: {str(e)}")
    
    return state

# Create LangGraph workflow
workflow = StateGraph(GraphState)

# Add nodes
workflow.add_node("classifier", classify_question)
workflow.add_node("settings_preprocessor", settings_preprocessor)
workflow.add_node("sql_agent", sql_agent)
workflow.add_node("answer_agent", answer_agent)
workflow.add_node("settings_postprocessor", settings_postprocessor)
workflow.add_node("general_answer", general_answer_agent)

# Add edges with conditions
def should_query_database(state):
    return state['question_type'] == 'database'

# Add edges with conditions
workflow.add_conditional_edges(
    "classifier",
    should_query_database,
    {
        True: "settings_preprocessor",  # If DB query needed, check settings first
        False: "general_answer"     # If no DB query needed, go to general answer
    }
)

# Add remaining edges
workflow.add_edge('settings_preprocessor', 'sql_agent')
workflow.add_edge('sql_agent', 'answer_agent')
workflow.add_edge('answer_agent', 'settings_postprocessor')
workflow.add_edge('general_answer', 'settings_postprocessor')

# Set entry point
workflow.set_entry_point("classifier")

# Compile workflow
app = workflow.compile()

# Streamlit UI
st.title("AFCON 2025 AI Assistant ")

st.markdown("""
This AI assistant can answer your questions about AFCON 2025 matches and related information.
Ask questions like:
- Which teams are in Group A?
- When is Morocco playing their first match?
- How many matches are scheduled in Casablanca?
""")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("What would you like to know about AFCON 2025?"):
    # Display user message
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Create placeholders for all expandable sections
    thinking_placeholder = st.empty()
    sql_placeholder = st.empty()
    data_placeholder = st.empty()
    answer_placeholder = st.empty()
    
    try:
        # Initialize response dictionary
        response = {'thinking_process': []}
        
        # Process the query with spinner
        with st.spinner("🤔 Thinking..."):
            response = app.invoke({
                "question": prompt,
                "sql_query": None,
                "sql_result": None,
                "answer": None,
                "error": None,
                "thinking_process": [],
                "question_type": None,
                "history": "\n".join([f"User: {msg['content']}" if msg["role"] == "user" else f"Assistant: {msg['content']}" for msg in st.session_state.messages[-5:]])
            })
        
        # Show thinking process in collapsible section
        with thinking_placeholder.expander("View Thinking Process 🧠"):
            for step in response.get('thinking_process', []):
                st.write(step)
        
        # Display SQL query in expander if available
        if response.get('sql_query'):
            with sql_placeholder.expander("View SQL Query 🔍"):
                st.code(response['sql_query'], language='sql')
        
        # Display results in a table if available
        if response.get('sql_result') is not None and not response['sql_result'].empty:
            with data_placeholder.expander("View Raw Data 📊"):
                st.dataframe(response['sql_result'])
        
        # Display answer if available
        if response.get('answer'):
            with answer_placeholder:
                st.chat_message("assistant").markdown(response['answer'])
                st.session_state.messages.append({"role": "assistant", "content": response['answer']})
                    
    except Exception as e:
        # Clear all placeholders on error
        thinking_placeholder.empty()
        sql_placeholder.empty()
        data_placeholder.empty()
        answer_placeholder.empty()
        st.error(f"An error occurred: {str(e)}")
        if "error" in response:
            st.error(f"Agent error: {response['error']}")