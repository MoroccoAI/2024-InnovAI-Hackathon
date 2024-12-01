import os
from dotenv import load_dotenv
import openai
import pickle

# Load the environment variables from the .env file
load_dotenv()

# Check if the API key is loaded properly
api_key = os.getenv('OPENAI_API_KEY')
if api_key is None:
    raise ValueError("OPENAI_API_KEY is not set. Please set it in the .env file.")

# Set the OpenAI API key
openai.api_key = api_key

# Path to the folder containing the text files
folder_path = "C:/Users/Reda NASSIF/Documents/GitHub/EduSmart_Morocco/edusmart/database/lycee/1_bac/sci_math/math/notion_de_logique/exercices"

# Dictionary to store the content of the text files
Exercices = {}

# Read the content of each .txt file in the folder
for filename in os.listdir(folder_path):
    if filename.endswith('.txt'):
        # Remove the .txt extension from the filename
        base_filename = os.path.splitext(filename)[0]
        print(f"Processing file: {base_filename}")
        with open(os.path.join(folder_path, filename), 'r', encoding='utf-8') as file:
            Exercices[base_filename] = file.read()

# Function to get an embedding for a given text
def get_embedding(text, model="text-embedding-ada-002"):
    """
    Function to get the embedding for a given text using OpenAI's API.

    Args:
        text (str): The text to embed.
        model (str): The model to use for embedding (e.g., "text-embedding-ada-002").

    Returns:
        list: A list containing the embedding vector.
    """
    
    response = openai.Embedding.create(
        model=model,
        input=text
    )
    embedding = response['data'][0]['embedding']
    return embedding


# Dictionary to store the embeddings of the exercises
Exercices_embeddings = {}

# Generate embeddings for each text and store them
for filename, text in Exercices.items():
    embedding = get_embedding(text)
    if embedding is not None:
        print('')
        Exercices_embeddings[filename] = embedding

# Save the embeddings to a file
with open('exercices_embeddings.pkl', 'wb') as f:
    pickle.dump(Exercices_embeddings, f)

print("Embeddings have been generated and saved successfully.")
