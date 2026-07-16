import re
import os
import nltk
import logging
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from camel_tools.tokenizers.word import simple_word_tokenize

# Ensure you have the necessary NLTK resources
nltk.download('punkt')
nltk.download('stopwords')

# Configure logging
log_folder = 'log'
os.makedirs(log_folder, exist_ok=True)
logging.basicConfig(filename=os.path.join(log_folder, 'nlp.log'), level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Arabic stopwords (can be adjusted based on your needs)
stop_words = set(stopwords.words('arabic'))

# Function to remove unnecessary formatting and metadata
def clean_text(text):
    logging.info('Cleaning text')
    text = re.sub(r"\*\*([^\*]+)\*\*", r"\1", text)  # Remove bold (**) formatting
    text = re.sub(r"\*\*([^\*]+)\*\*", r"\1", text)  # Remove italic (_) formatting
    text = re.sub(r'\d{1,2} ذو \w+ \d{4} \(\d{1,2} \w+ \d{4}\)', '', text)
    text = re.sub(r"-\d+-", "", text)
    text = re.sub(r'[-_]+', ' ', text)
    return text.strip()

# Function to remove stopwords (optional, based on use case)
def remove_stopwords(text):
    logging.info('Removing stopwords')
    tokens = word_tokenize(text)
    filtered_tokens = [word for word in tokens if word not in stop_words]
    return ' '.join(filtered_tokens)

# Function to tokenize and normalize Arabic text (optional: can use Farasa or CamelTools for more accurate Arabic tokenization)
def tokenize_text(text):
    logging.info('Tokenizing text')
    tokens = simple_word_tokenize(text)  # Using CamelTools simple tokenizer for Arabic
    return ' '.join(tokens)

# Function to split the text into articles based on the pattern "المادة {i}"
def split_text_into_articles(text):
    logging.info('Splitting text into articles')
    article_pattern = re.compile(r'(المادة \d+)(.*?)(?=(المادة \d+)|$)', re.DOTALL)
    articles = []
    current_article = ''
    current_article_number = 0

    for match in article_pattern.finditer(text):
        article_title = match.group(1).strip()
        article_content = match.group(2).strip()
        article_number_match = re.match(r'المادة (\d+)', article_title)
        if article_number_match:
            article_number = int(article_number_match.group(1))
            if article_number == current_article_number + 1:
                if current_article:
                    articles.append(current_article.strip())
                current_article = article_title + '\n' + article_content
                current_article_number = article_number
            else:
                current_article += '\n' + article_title + '\n' + article_content
    if current_article:
        articles.append(current_article.strip())
    return articles

# Preprocessing function for entire text
def preprocess_arabic_text(text):
    logging.info('Preprocessing Arabic text')
    cleaned_text = clean_text(text)
    articles = split_text_into_articles(cleaned_text)
    processed_articles = []
    for article in articles:
        tokenized_article = tokenize_text(article)
        final_article = remove_stopwords(tokenized_article)
        processed_articles.append(final_article)
    return processed_articles

# Function to read and preprocess the text from a file
def read_and_preprocess_file(file_path):
    logging.info(f'Reading and preprocessing file: {file_path}')
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()
    processed_text = preprocess_arabic_text(text)
    return processed_text

# Function to save the processed articles to separate text files in a new folder
def save_articles_to_files(articles, output_folder='laws'):
    logging.info(f'Saving articles to files in folder: {output_folder}')
    os.makedirs(output_folder, exist_ok=True)
    for i, article in enumerate(articles, start=1):
        file_path = os.path.join(output_folder, f"article_{i}.txt")
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(article)

# Example usage with 'water-law-36-15.txt'
file_path = 'data/water-laws-36-15.txt'  # Update with the correct path to your text file
processed_articles = read_and_preprocess_file(file_path)
save_articles_to_files(processed_articles)

logging.info("Processed articles have been saved to the 'laws' folder.")
print(f"Processed articles have been saved to the 'laws' folder.")
