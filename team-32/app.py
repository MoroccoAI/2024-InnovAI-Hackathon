import streamlit as st
st.set_page_config(page_title="AI Resume Analyzer", page_icon=":page_facing_up:")
import os
import io
import uuid
import time
import random
import socket
import secrets
import datetime
import platform
import base64
import time
import base64
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import streamlit as st
import numpy as np
import plotly.express as px
import geocoder
import pymysql
from geopy.geocoders import Nominatim
from selenium import webdriver
from pdfminer.high_level import extract_text
from streamlit_tags import st_tags
from PIL import Image
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.tokenize import word_tokenize
from selenium.webdriver.common.by import By
import spacy
from spacy.cli import download
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
load_dotenv() 
#gensim
import gensim
from gensim import corpora
import math
#Visualization
from spacy import displacy
import pyLDAvis.gensim_models
from wordcloud import WordCloud
import jsonlines
import matplotlib.pyplot as plt
import matplotlib.cm as cm
#nltk
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
nltk.download(['stopwords','wordnet'])
#warning
from openai import OpenAI
import warnings 
warnings.filterwarnings('ignore')
#download("en_core_web_sm")
nlp = spacy.load("en_core_web_sm")

#nlp = spacy.load('en_core_web_sm')
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('maxent_ne_chunker')
nltk.download('words')

def generate_session_token():
    return secrets.token_hex(16)

def get_geolocation():
    g = geocoder.ip('me')
    return g.latlng, g.city, g.state, g.country

def get_device_info():
    return {
        "ip_address": socket.gethostbyname(socket.gethostname()),
        "hostname": socket.gethostname(),
        "os": f"{platform.system()} {platform.release()}",
    }

def init_database():
    connection = get_database_connection()
    if connection:
        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS users (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        name VARCHAR(255) NOT NULL,
                        email VARCHAR(255) NOT NULL,
                        resume_score INT NOT NULL,
                        recommended_field VARCHAR(255),
                        experience_level VARCHAR(50),
                        timestamp DATETIME NOT NULL
                    )
                """)

                # Create feedback table
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS feedback (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        name VARCHAR(255) NOT NULL,
                        email VARCHAR(255) NOT NULL,
                        rating INT NOT NULL,
                        comments TEXT NOT NULL,
                        timestamp DATETIME NOT NULL
                    )
                """)
            connection.commit()
        except Exception as e:
            st.error(f"Error initializing database: {e}")
        finally:
            connection.close()


def get_database_connection():
    try:
        connection = pymysql.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            user=os.getenv('DB_USER', 'root'),
            password=os.getenv('DB_PASSWORD', 'SQLpassword')
        )

        # Create a cursor object
        with connection.cursor() as cursor:
            # Create the database if it does not exist
            database_name = os.getenv('DB_NAME', 'resume_Anlyser') 
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{database_name}`")
            #cursor.execute("CREATE DATABASE IF NOT EXISTS {os.getenv('DB_NAME', 'resume_Anlyser')}")

        # Reconnect to the MySQL server with the database
        connection.close()
        connection = pymysql.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            user=os.getenv('DB_USER', 'root'),
            password=os.getenv('DB_PASSWORD', 'SQLpassword'),
            database=os.getenv('DB_NAME', 'resume_Anlyser'),
        )

        return connection
    except Exception as e:
        st.error(f"Error connecting to the database: {e}")
        return None 
    
    
@st.cache_data

def analyze_resume(pdf_path):
    import pdfplumber
    import re
    import pandas as pd
    import json
    from nltk.corpus import stopwords
    from nltk.stem import WordNetLemmatizer
    import nltk
    import pickle
    # Download NLTK data
    nltk.download(['stopwords', 'wordnet'])
    nlp = spacy.load("en_core_web_lg")
    # Add an entity ruler to recognize skills
    skill_pattern_path = "skill_patterns.jsonl"
    ruler = nlp.add_pipe("entity_ruler", before="ner")
    ruler.from_disk(skill_pattern_path)
    # Load the SpaCy models
    
    # nlp = spacy.load("nlp_model")  # Uncomment if you have a custom model

    # Define the function to extract skills
    def get_skills(text):
        doc = nlp(text)
        myset = []
        subset = []
        for ent in doc.ents:
            if ent.label_ == "SKILL":
                subset.append(ent.text)
        myset.append(subset)
        return subset

    # Function to remove duplicates from skills
    def unique_skills(x):
        return list(set(x))

    # Initialize the WordNetLemmatizer and stopwords
    lm = WordNetLemmatizer()
    stop_words = set(stopwords.words("english"))

    # Extract text from the PDF using pdfplumber
    with pdfplumber.open(pdf_path) as pdf:
        full_text = ""
        for page in pdf.pages:
            full_text += page.extract_text()

    clean = []
    # Clean the extracted text
    review = re.sub(
        r'(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)|^rt|http.+?"',  # Regex to clean text
        " ",
        full_text,  # Use the extracted text from the PDF
    )

    review = review.lower()  # Convert to lowercase
    review = review.split()  # Split the text into words

    # Lemmatization and stopwords removal
    review = [
        lm.lemmatize(word)  # Lemmatize each word
        for word in review
        if word not in stop_words  # Remove stopwords
    ]

    review = " ".join(review)  # Join the words back into a single string
    clean.append(review)

    # Convert the cleaned text to a DataFrame (simulating the resumes2_df)
    resumes2_df = pd.DataFrame(clean, columns=["Clean_Resume"])

    # Apply the skill extraction functions
    resumes2_df["skills"] = resumes2_df["Clean_Resume"].apply(get_skills)  # Extract skills
    resumes2_df["skills"] = resumes2_df["skills"].apply(unique_skills)  # Get unique skills

    # Adding a Job category column (you may want to define categories based on resume content or your own logic)
    resumes2_df["Category"] = "IT"  # Replace with your own categories

    # Job categories you want to filter on
    Job_cat = ["IT", "Software Developer", "ALL"]

    # Initialize the Total_skills list
    Total_skills = []

    for Job_category in Job_cat:
        if Job_category != "ALL":
            fltr = resumes2_df[resumes2_df["Category"] == Job_category]["skills"]
            for x in fltr:
                for i in x:
                    Total_skills.append(i)
        else:
            fltr = resumes2_df["skills"]
            for x in fltr:
                for i in x:
                    Total_skills.append(i)

    # Process the resume text using SpaCy NLP model
    resume_doc = nlp(full_text)

    # Extract personal information (email and phone)
    email = None
    phone = None
    for ent in resume_doc.ents:
        if ent.label_ == "EMAIL" and not email:
            email = ent.text
        elif ent.label_ == "PHONE_NUMBER" and not phone:
            phone = ent.text

    # Extract email and phone number using regular expressions if not found
    if not email:
        email_pattern = re.compile(r'[a-zA-Z0-9+_.-]+@[a-zA-Z0-9.-]+')
        emails = re.findall(email_pattern, full_text)
        email = emails[0] if emails else "Not found"

    if not phone:
        phone_pattern = r"""(\(?\d{3}\)?[-\s.]?\d{3}[-\s.]?\d{4}|\d{3}[-\s.]?\d{4}|\d{10}|\(?\d{3}\)?[-\s.]?\d{3}[-\s.]?\d{2}[-\s.]?\d{2})"""
        phone_pattern = re.compile(phone_pattern, re.VERBOSE)
        phones = re.findall(phone_pattern, full_text)
        # Filter out empty matches and join the parts
        phones = [''.join(filter(None, phone)) for phone in phones]
        phone = phones[0] if phones else "Not found"

    # Extract education
    education = set()
    text_r = extract_text(pdf_path)
    #doc_resume = nlp(text_r)
    doc_resume = nlp(text_r.lower())
    with open('education_degrees.json', 'r') as f:
        data = json.load(f)
        education_degrees = data['degrees']

    for keyword in education_degrees:
        matcher = spacy.matcher.PhraseMatcher(nlp.vocab)
        pattern = [nlp(keyword)]
        matcher.add("EDUCATION_KEYWORD", pattern)
        matches = matcher(doc_resume)
        for match_id, start, end in matches:
            span = doc_resume[start:end]
            education.add(span.text)
    education_list = list(education)    
    if education_list:
        degree = education_list[0]
    else:
        degree = None
    

    skills_found = [ent.text for ent in resume_doc.ents if ent.label_ == "SKILL"]

    # Extract experience
    experience = []

    # Define a regular expression pattern to extract experience mentions
    experience_pattern = r'(\d+[\+]{0,1}\s?(?:years?|yr|yrs?))'

    # Use regex to find experience mentions
    experience_matches = re.findall(experience_pattern, full_text)

    # Extract job titles and roles using SpaCy NER (optional, can be fine-tuned further)
    roles = [ent.text for ent in resume_doc.ents if ent.label_ == "ORG"]  # This can be adjusted if needed

    # Append both the experience and roles to the experience list as tuples
    for exp in experience_matches:
        for role in roles:
            experience.append((exp, role))

    experience = list(set(experience))  # Convert to set to remove duplicates
    
    # Calculate the resume score(adapted of each job offer)
    required_skills = set([
        "Python", "Machine Learning", "Data Analysis", "Project Management",
        "Cloud Computing", "SQL"
    ])
    
    matched_skills = required_skills.intersection(skills_found)
    resume_score = len(matched_skills) / len(required_skills) * 100
    resume_score = round(resume_score, 2)
    
    # Create the resume data dictionary
    resume_data = {
        #"name": name,
        "email": email,
        "mobile_number": phone,
        "skills": set(list(skills_found)),
        "degree": degree,
        #"education": education,
        "experience": experience,
        "resume_score": resume_score
    }

    return resume_data


def generate_pdf_report(resume_data, resume_score, score_breakdown, recommended_skills, recommended_field, recommended_courses):
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import letter
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from io import BytesIO

    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    elements = []

    elements.append(Paragraph("Resume Analysis Report", styles['Title']))
    elements.append(Spacer(1, 12))

    elements.append(Paragraph("Basic Information", styles['Heading2']))
    basic_info = [
        ["Name", resume_data.get('name', '')],
        ["Email", resume_data.get('email', '')],
        ["Phone", resume_data.get('mobile_number', '')],
        ["Degree", resume_data.get('degree', '')]
    ]
    t = Table(basic_info)
    t.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                           ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                           ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                           ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                           ('FONTSIZE', (0, 0), (-1, 0), 14),
                           ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                           ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                           ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
                           ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                           ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
                           ('FONTSIZE', (0, 0), (-1, -1), 12),
                           ('TOPPADDING', (0, 1), (-1, -1), 6),
                           ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
                           ('GRID', (0, 0), (-1, -1), 1, colors.black)]))
    elements.append(t)
    elements.append(Spacer(1, 12))

    elements.append(Paragraph(f"Resume Score: {resume_score}/100", styles['Heading2']))
    elements.append(Spacer(1, 12))

    elements.append(Paragraph("Score Breakdown", styles['Heading2']))
    score_table = [[category, f"{score}/10"] for category, score in score_breakdown.items()]
    t = Table(score_table)
    t.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                           ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                           ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                           ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                           ('FONTSIZE', (0, 0), (-1, 0), 14),
                           ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                           ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                           ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
                           ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                           ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
                           ('FONTSIZE', (0, 0), (-1, -1), 12),
                           ('TOPPADDING', (0, 1), (-1, -1), 6),
                           ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
                           ('GRID', (0, 0), (-1, -1), 1, colors.black)]))
    elements.append(t)
    elements.append(Spacer(1, 12))

    elements.append(Paragraph("Recommendations", styles['Heading2']))
    elements.append(Paragraph(f"Recommended Field: {recommended_field}", styles['Normal']))
    elements.append(Paragraph("Recommended Skills:", styles['Normal']))
    for skill in recommended_skills:
        elements.append(Paragraph(f"- {skill}", styles['Normal']))
    elements.append(Paragraph("Recommended Courses:", styles['Normal']))
    for course in recommended_courses[:5]:
        elements.append(Paragraph(f"- {course}", styles['Normal']))

    doc.build(elements)
    buffer.seek(0)
    return buffer


def user_page():
    """
    Renders the user page of the AI Resume Analyzer application.
    This function handles the resume upload, analysis, and display of results.
    It includes features such as basic information extraction, skills analysis,
    field and course recommendations, resume scoring, and PDF report generation.
    """
    if 'session_id' not in st.session_state:
        st.session_state.session_id = generate_unique_id()

    st.title("AI Resume Analyzer & Recommendation")
    st.write("Upload your resume and get insights!")
    # User name input
    user_name = st.text_input("Enter your name", "")
    uploaded_file = st.file_uploader("Choose your resume (PDF)", type="pdf")
    
    if uploaded_file is not None:
        try:
            with st.spinner("Analyzing your resume..."):
                
                temp_directory = "temp"
                if not os.path.exists(temp_directory):
                    os.makedirs(temp_directory)  

                temp_file_path = os.path.join(temp_directory, f"resume_{st.session_state.session_id}.pdf")
                with open(temp_file_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())

                
                resume_text = extract_text(temp_file_path)
                
                progress_bar = st.progress(0)
                for i in range(100):
                    time.sleep(0.01)
                    progress_bar.progress(i + 1)
                #resume_data = parse_resume(temp_file_path)
                resume_data = analyze_resume(temp_file_path)
                

            display_resume_analysis(resume_data, user_name)

            offer_pdf_download(resume_data)
            #display_additional_resources()

            os.remove(temp_file_path)

        except Exception as e:
            st.error(f"An error occurred while processing your resume: {str(e)}")
            st.error("Please make sure you've uploaded a valid PDF file and try again.")
    if st.button("Clear Session"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

def display_resume_analysis(resume_data, user_name):
    """
    Displays the results of the resume analysis.
    
    Args:
    resume_data (dict): A dictionary containing the analyzed resume data.
    """
    
    #st.subheader("Basic Information")
    st.subheader(f"Resume Analysis Results for {user_name}")
    st.write(f"Name: {resume_data.get('name', user_name)}")
    st.write(f"Email: {resume_data.get('email', '')}")
    st.write(f"Phone: {resume_data.get('mobile_number', ' ')}")
    #st.write(f"Degree: {resume_data.get('degree', 'No Degree')}")
    st.write(f"Degree: {resume_data.get('degree', 'No Degree')}")
    
    experience = resume_data.get('total_experience', 0)
    level = "Fresher" if experience == 0 else "Intermediate" if experience < 3 else "Experienced"
    st.write(f"Experience Level: {level}")
    
    skills = resume_data.get('skills', [])
    st.subheader("Skills")
    st.write(", ".join(skills))
    
    st.subheader("Skills Recommendation")
    recommended_skills = recommend_skills(skills)
    st.write("Based on your current skills, we recommend developing these skills:")
    st.write(", ".join(recommended_skills))

    st.subheader("Field Recommendation")
    recommended_field = recommend_field(skills)
    st.write(f"Based on your skills, we recommend exploring the field of: {recommended_field}")

    st.subheader("Course Recommendation")
    recommended_courses = recommend_courses(recommended_field)
    st.write("Here are some courses we recommend:")
    #for course in recommended_courses[:5]:
    #    st.write(f"- {course}")
    #table = []
    table = [["Course"]]
    for course in recommended_courses[:5]:
        table.append([course])

    # Display the table
    st.table(table)
    
    st.subheader("Resume Score")
    resume_score = calculate_resume_score(resume_data)
    st.write(f"Your resume score: {resume_score}/100")
    
    st.subheader("Resume Score Breakdown")
    score_breakdown = get_resume_score_breakdown(resume_data)
    for category, score in score_breakdown.items():
        st.write(f"{category}: {score}/10")

    categories = list(score_breakdown.keys())
    scores = list(score_breakdown.values())

    fig = px.bar(x=categories, y=scores, 
                 title="Resume Score Distribution by Category",
                 labels={'x': 'Category', 'y': 'Score'})
    st.plotly_chart(fig)


    

    user_data = {
        "name": resume_data.get('name', user_name),
        "email": resume_data.get('email', 'Not found'),
        "resume_score": resume_score,
        "recommended_field": recommended_field,
        "experience_level": level
    }
    if store_user_data(user_data):
        st.success("Your resume analysis has been saved!")
    else:
        st.warning("There was an issue saving your resume analysis. Your data may not be stored for future reference.")

def offer_pdf_download(resume_data):
    """
    Generates and offers a downloadable PDF report of the resume analysis.

    Args:
    resume_data (dict): A dictionary containing the analyzed resume data.
    """
    resume_score = calculate_resume_score(resume_data)
    score_breakdown = get_resume_score_breakdown(resume_data)
    recommended_skills = recommend_skills(resume_data.get('skills', []))
    recommended_field = recommend_field(resume_data.get('skills', []))
    recommended_courses = recommend_courses(recommended_field)

    pdf_buffer = generate_pdf_report(resume_data, resume_score, score_breakdown, recommended_skills, recommended_field, recommended_courses)
    st.download_button(
        label="Download Resume Analysis Report",
        data=pdf_buffer,
        file_name="resume_analysis_report.pdf",
        mime="application/pdf"
    )


def calculate_resume_score(resume_data):
    score_breakdown = get_resume_score_breakdown(resume_data)
    return sum(score_breakdown.values())

def get_resume_score_breakdown(resume_data):
    score_breakdown = {
        "Contact Information": 0,
        "Education": 0,
        "Skills": 0,
        "Experience": 0,
        "Projects": 0,
        "Certifications": 0,
        "Summary/Objective": 0,
        #"Achievements": 0,
        "Formatting": 0,
        "Keywords": 0
    }
    
    if resume_data.get('name'): score_breakdown["Contact Information"] += 3
    if resume_data.get('email'): score_breakdown["Contact Information"] += 3
    if resume_data.get('mobile_number'): score_breakdown["Contact Information"] += 4
    
    if resume_data.get('degree'): score_breakdown["Education"] += 10
    if resume_data.get('college_name'): score_breakdown["Education"] += 5
    
    skills = resume_data.get('skills', [])
    score_breakdown["Skills"] = min(len(skills), 15)
    
    experience = resume_data.get('total_experience', 0)
    score_breakdown["Experience"] = min(experience * 2, 10)
    
    projects = resume_data.get('projects', [])
    score_breakdown["Projects"] = min(len(projects) * 2, 10)
    
    certifications = resume_data.get('certifications', [])
    score_breakdown["Certifications"] = min(len(certifications) * 2, 10)
    
    if resume_data.get('summary'): score_breakdown["Summary/Objective"] = 10
    
    #achievements = resume_data.get('achievements', [])
    #score_breakdown["Achievements"] = min(len(achievements) * 2, 10)
    
    score_breakdown["Formatting"] = 8
    score_breakdown["Keywords"] = 7
    
    return score_breakdown

def recommend_skills(skills):
    all_skills = set(["Python", "Java", "C++", "JavaScript", "HTML", "CSS", "SQL", "Machine Learning", "Data Analysis", "React", "Node.js", "Angular", "Vue.js", "Docker", "Kubernetes", "AWS", "Azure", "GCP", "Git", "Agile"])
    recommended = list(all_skills - set(skills))
    return random.sample(recommended, min(5, len(recommended)))

def recommend_field(skills):
    import json
    with open('field.json') as f:
        fields = json.load(f)    
    max_match = 0
    recommended_field = "General Software Development"
    
    for field, field_skills in fields.items():
        match = len(set(skills) & set(field_skills))
        if match > max_match:
            max_match = match
            recommended_field = field
    
    return recommended_field

def recommend_courses(field):
    
    #url = f"https://www.coursera.org/browse/{field}"
    #url = f"https://www.coursera.org/browse/{field.replace(' ', '-')}"
    #url1 = f"https://www.coursera.org/learn/{field.replace(' ', '-')}"
    #https://coursera.org/search?query=machine%20learning
    url = f"https://coursera.org/search?query={field.replace(' ', '%20')}"
    
    response = requests.get(url)    
    soup = BeautifulSoup(response.content, 'html.parser')
    courses = soup.find_all('a', class_='cds-119 cds-113 cds-115 cds-CommonCard-titleLink css-si869u cds-142')[:5]    
    course_list = []
    for course in courses:
        #title = course.text.strip()
        title = course.find('h3', class_='cds-CommonCard-title css-6ecy9b').text.strip() 
        #link = "https://www.coursera.org"+course.find_parent('a')['href']
        link = "https://www.coursera.org"+course['href']  
        course_list.append(f'{title} : {link}')
    return course_list
    #return courses.get(field, '')

def find_jobs_page():
    """
    Renders the job search page of the AI Resume Analyzer application.

    This function allows users to search for jobs based on job title and location.
    It uses web scraping to fetch job listings from LinkedIn and displays the results.
    Users can also download the job search results as a CSV file.
    """
    st.title("Find Jobs")
    st.write("Search for jobs based on job title and location.")
    
    job_title = st.text_input("Job Title")
    location = st.text_input("Location")
    
    if st.button("Search Jobs"):
        with st.spinner("Searching for jobs..."):
            jobs = scrape_linkedin_jobs(job_title, location)
        
        if jobs:
            display_job_results(jobs)
        else:
            st.write("No jobs found. Try different search terms.")


def scrape_linkedin_jobs(job_title, location):
    """
    Scrapes job listings from LinkedIn based on the given job title and location.
    """
    url = f"https://www.linkedin.com/jobs/search/?keywords={job_title}&location={location}"
    
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    
    driver = None
    try:
        driver = webdriver.Firefox(options=options)
        driver.get(url)
        
        wait = WebDriverWait(driver, 10)
        job_cards = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "base-card")))
        
        jobs = []
        for card in job_cards[:10]:
            try:
                title_element = card.find_element(By.CLASS_NAME, "base-card__full-link")
                company_element = card.find_element(By.CLASS_NAME, "job-card-container__company-name")
                location_element = card.find_element(By.CLASS_NAME, "job-card-container__metadata-item")
                link_element = card.find_element(By.CLASS_NAME, "base-card__full-link")
                
                # Extract text and link
                title = title_element.text
                company = company_element.text
                job_location = location_element.text
                link = link_element.get_attribute("href")
                
                jobs.append({
                    "title": title,
                    "company": company,
                    "location": job_location,
                    "link": link
                })
            except Exception as e:
                st.error(f"Error scraping job card: {e}")
        
        return jobs
    except Exception as e:
        st.error(f"Error initializing web driver: {e}")
        return []
    finally:
        if driver:
            driver.quit()

def display_job_results(jobs):
    """
    Displays the job search results and provides an option to download them as a CSV file.

    Args:
    jobs (list): A list of dictionaries containing job information.
    """
    st.subheader("Job Results")
    if jobs:
        for job in jobs:
            st.write(f"**{job['title']}**")
            st.write(f"Company: {job['company']}")
            st.write(f"Location: {job['location']}")
            st.write(f"[Link]({job['link']})")
            st.write("---")
        
        # Download results as CSV
        if st.button("Download Results as CSV"):
            df = pd.DataFrame(jobs)
            csv = df.to_csv(index=False)
            st.download_button(label="Download CSV", data=csv, file_name='job_results.csv', mime='text/csv')
    else:
        st.write("No jobs found.")

def feedback_page():
    """
    Renders the feedback page of the AI Resume Analyzer application.

    This function allows users to submit feedback about the application.
    It collects user name, email, rating, and comments, and stores the feedback in a database.
    """
    st.title("Feedback")
    st.write("We'd love to hear your thoughts!")
    
    name = st.text_input("Name")
    email = st.text_input("Email")
    rating = st.slider("Rating", 1, 5, 3)
    comments = st.text_area("Comments")
    
    if st.button("Submit Feedback"):
        if name and email and comments:
            feedback_data = {
                "name": name,
                "email": email,
                "rating": rating,
                "comments": comments,
                "timestamp": datetime.datetime.now()
            }
            
            if store_feedback(feedback_data):
                st.success("Thank you for your feedback!")
            else:
                st.error("There was an error submitting your feedback. Please try again.")
        else:
            st.warning("Please fill out all fields before submitting.")

def store_feedback(feedback_data):
    """
    Stores the user feedback in the database.

    Args:
    feedback_data (dict): A dictionary containing the feedback information.

    Returns:
    bool: True if the feedback was successfully stored, False otherwise.
    """
    
    try:
        connection = pymysql.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            user=os.getenv('DB_USER', 'root'),
            password=os.getenv('DB_PASSWORD', 'SQLpassword'),
            database=os.getenv('DB_NAME', 'resume_Anlyser'),
        )
        
        with connection.cursor() as cursor:
            sql = """INSERT INTO feedback (name, email, rating, comments, timestamp) 
                     VALUES (%s, %s, %s, %s, %s)"""
            cursor.execute(sql, (
                feedback_data['name'],
                feedback_data['email'],
                feedback_data['rating'],
                feedback_data['comments'],
                feedback_data['timestamp']
            ))
        
        connection.commit()
        return True
    except Exception as e:
        st.error(f"Error storing feedback: {e}")
        return False
    finally:
        if connection:
            connection.close()

def about_page():
    """
    Renders the about page of the AI Resume Analyzer application.

    This function provides information about the application, its features,
    and how to use it effectively.
    """
    st.title("About TalentTriage's Resume Analyzer")
    st.write("Welcome to TalentTriage's Resume Analyzer and Recommendation System, a cutting-edge tool designed to help job seekers and recruiters alike. Our system is powered by advanced AI technology, providing personalized insights and recommendations to enhance your resume and find the perfect job match.")
    
    st.subheader("Features")
    st.markdown("""
    * ✅ Resume Analysis: Receive a comprehensive analysis of your resume's strengths and weaknesses, highlighting areas for improvement.
    * ✅ Skills Recommendation: Discover new skills that can boost your profile and increase your chances of landing your dream job.
    * ✅ Job Field Recommendation: Get expert advice on which job fields align with your skills and experience.
    * ✅ Course Recommendations: Receive tailored suggestions for courses to upskill and reskill, enhancing your employability.
    * ✅ Job Search: Access a curated list of relevant job listings based on your profile, increasing your chances of finding the perfect fit.
    * ✅ Resume Score: Get a quantitative assessment of your resume, providing a clear understanding of its effectiveness.
    """)
    
    st.subheader("How to Use 👉")
    st.markdown("""
    1. Upload your resume in PDF format
    2. Review the analysis and recommendations
    3. Use the job search feature to find relevant opportunities
    4. Improve your resume based on the suggestions
    5. Repeat the process to track your progress
    """)
  
    st.subheader("Privacy 🔒")
    st.write("At TalentTriage, we prioritize your privacy and security. Our system is designed to ensure that your resume data is only used for analysis during your session and is not stored permanently.")

def store_user_data(user_data):
    """
    Stores the user data in the database.
    
    Args:
    user_data (dict): A dictionary containing the user information.
    
    Returns:
    bool: True if the data was successfully stored, False otherwise.
    """
    try:
        connection = pymysql.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            user=os.getenv('DB_USER', 'root'),
            password=os.getenv('DB_PASSWORD', 'SQLpassword'),
            database=os.getenv('DB_NAME', 'resume_Anlyser'),
        )
        
        with connection.cursor() as cursor:
            sql = """INSERT INTO users (name, email, resume_score, recommended_field, experience_level, timestamp) 
                     VALUES (%s, %s, %s, %s, %s, %s)"""
            cursor.execute(sql, (
                user_data['name'],
                user_data['email'],
                user_data['resume_score'],
                user_data['recommended_field'],
                user_data['experience_level'],
                datetime.datetime.now()
            ))
        
        connection.commit()
        return True
    except Exception as e:
        st.error(f"Error storing user data: {e}")
        return False
    finally:
        if connection:
            connection.close()


def admin_page():
    """
    Renders the admin page of the AI Resume Analyzer application.
    """
    if not st.session_state.get('admin_logged_in', False):
        admin_login()
    else:
        show_admin_dashboard()

def admin_login():
    """
    Handles the admin login process with improved security.
    """
    st.title("Admin Login")
    
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    
    if st.button("Login"):
        if username == "TriageTalent" and password == "2024":  # Replace with secure authentication
            st.session_state.admin_logged_in = True
            st.success("Logged in successfully!")
            show_admin_dashboard()
        else:
            st.error("Invalid username or password")
    st.write("Username : TriageTalent")
    st.write("Password : 2024")
# Set your NeBius API key
nebius_api_key = os.getenv('NEBIUS_API_KEY')

# Initialize the NeBius client
client = OpenAI(
    base_url="https://api.studio.nebius.ai/v1/",
    api_key=nebius_api_key,
)

# Function to handle chatbot
def chatbot():
    st.sidebar.title("Admin Chatbot 🤖")
    st.sidebar.markdown("Ask me anything about candidates!")

    # Ensure chat history is tracked
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []

    # Sidebar input and send button
    user_input = st.sidebar.text_input("You:", value="", key="user_input")
    if st.sidebar.button("Send"):
        st.session_state.chat_history.append(("You", user_input))
        response = get_chatbot_response(user_input)  # Call the chatbot response logic
        st.session_state.chat_history.append(("Bot", response))

    # Display chat history in the sidebar
    st.sidebar.markdown("### Chat History")
    for message in st.session_state.chat_history:
        if message[0] == "You":
            st.sidebar.markdown(f"**{message[0]}:** {message[1]}")
        else:
            st.sidebar.markdown(f"**{message[0]}:** {message[1]}")
    
# Function to get chatbot response using NeBius API with context
def get_chatbot_response(user_input):
    try:
        # Fetch user data and feedback data
        user_data = get_user_data()
        feedback_data = get_feedback_data()
        
        # Convert data to string for context
        user_data_str = user_data.to_string(index=False)
        feedback_data_str = feedback_data.to_string(index=False)
        
        # Create context for the chatbot
        context = f"""
        You are an AI assistant for the Admin Dashboard.
        Here is the current user data:
        {user_data_str}
        
        Here is the current feedback data:
        {feedback_data_str}
        """
        
        completion = client.chat.completions.create(
            model="meta-llama/Meta-Llama-3.1-70B-Instruct",
            messages=[
                {
                    "role": "system",
                    "content": context
                },
                {
                    "role": "user",
                    "content": user_input
                }
            ],
            temperature=0.6
        )
        return completion.choices[0].message.content.strip()
    except Exception as e:
        return f"Error: {e}"
    
# Function to show admin dashboard with chatbot
def show_admin_dashboard():
    
    st.title("👨‍💼 Admin Dashboard")
    st.title("Testing a Job Description with Required Skills")
    st.markdown("""
    We are seeking a highly skilled Data Scientist with expertise in machine learning, data analysis, and project management to join our dynamic team. The ideal candidate will leverage their technical skills to drive data-driven insights and solutions, manage projects effectively, and ensure the scalability and efficiency of our computing infrastructure.
    
    **Required Skills:**

    The job description is based on the following required skills:
    - **Python**: Proficiency in using Python for scripting, automation, and software development.
    - **Machine Learning**: Ability to apply machine learning techniques for data modeling and prediction.
    - **Data Analysis**: Skills in analyzing and interpreting data to drive business decisions.
    - **Project Management**: Experience in managing projects from inception to completion, ensuring timely delivery and quality.
    - **Cloud Computing**: Knowledge of cloud platforms and services for scalable and efficient computing solutions.
    - **SQL**: Expertise in using SQL for data manipulation, querying, and database management.
    """)
    st.subheader("📊 User Data")
    user_data = get_user_data()
    st.dataframe(user_data)
    
    if st.button("Download User Data", key="download_user_data_button"):
        csv = user_data.to_csv(index=False)
        b64 = base64.b64encode(csv.encode()).decode()
        href = f'<a href="data:file/csv;base64,{b64}" download="user_data.csv">Download CSV File</a>'
        st.markdown(href, unsafe_allow_html=True)
        
    st.subheader("💬 Feedback Data")
    feedback_data = get_feedback_data()
    st.dataframe(feedback_data)
    
    if st.button("Download Feedback Data", key="download_feedback_data_button"):
        csv = feedback_data.to_csv(index=False)
        b64 = base64.b64encode(csv.encode()).decode()
        href = f'<a href="data:file/csv;base64,{b64}" download="feedback_data.csv">Download CSV File</a>'
        st.markdown(href, unsafe_allow_html=True)
    
    st.subheader("📈 Analytics")
    show_analytics()

    if st.button("Logout", key="admin_logout_button"):
        st.session_state.admin_logged_in = False
        st.success("You have been logged out.")
    
    # Chatbot Integration
    chatbot()

def get_user_data():
    try:
        connection = pymysql.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            user=os.getenv('DB_USER', 'root'),
            password=os.getenv('DB_PASSWORD', 'SQLpassword'),
            database=os.getenv('DB_NAME', 'resume_Anlyser')
        )
        
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM users")
            result = cursor.fetchall()
            column_names = [desc[0] for desc in cursor.description]
            df = pd.DataFrame(result, columns=column_names)
            
        return df
    except Exception as e:
        st.error(f"Error fetching user data: {e}")
        return pd.DataFrame()
    finally:
        if connection:
            connection.close()



def get_feedback_data():
    try:
        connection = pymysql.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            user=os.getenv('DB_USER', 'root'),
            password=os.getenv('DB_PASSWORD', 'SQLpassword'),
            database=os.getenv('DB_NAME', 'resume_Anlyser'),
        )
        
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM feedback")
            result = cursor.fetchall()
            
        df = pd.DataFrame(result, columns=['id', 'name', 'email', 'rating', 'comments', 'timestamp'])
        return df
    except Exception as e:
        st.error(f"Error fetching feedback data: {e}")
        return pd.DataFrame()
    finally:
        if connection:
            connection.close()

def show_analytics():
    user_data = get_user_data()
    feedback_data = get_feedback_data()
    
    st.title("Admin Analytics Dashboard")
    
    st.subheader("User Activity Over Time")
    if not user_data.empty and 'timestamp' in user_data.columns:
        user_data['timestamp'] = pd.to_datetime(user_data['timestamp'])
        
        last_30_days = datetime.datetime.now() - datetime.timedelta(days=30)
        recent_user_data = user_data[user_data['timestamp'] >= last_30_days]
        
        user_counts = recent_user_data.groupby(user_data['timestamp'].dt.date).size().reset_index(name='counts')
        
        fig_users = px.line(user_counts, x='timestamp', y='counts', title='Number of Users Over the Last 30 Days')
        fig_users.update_layout(xaxis_title='Date', yaxis_title='Number of Users')
        st.plotly_chart(fig_users)
    else:
        st.write("No user data available for the specified period.")
    
    st.subheader("Predicted Fields")
    if not user_data.empty and 'recommended_field' in user_data.columns:
        field_counts = user_data['recommended_field'].value_counts()
        fig_fields = px.pie(values=field_counts.values, names=field_counts.index, title="Predicted Fields")
        st.plotly_chart(fig_fields)
    else:
        st.write("No data available for Predicted Fields.")
    
    st.subheader("Experience Levels")
    if not user_data.empty and 'experience_level' in user_data.columns:
        level_counts = user_data['experience_level'].value_counts()
        fig_levels = px.pie(values=level_counts.values, names=level_counts.index, title="Experience Levels")
        st.plotly_chart(fig_levels)
    else:
        st.write("No data available for Experience Levels.")
    
    st.subheader("Resume Score Distribution")
    if not user_data.empty and 'resume_score' in user_data.columns:
        fig_scores = px.histogram(user_data, x="resume_score", nbins=20, title="Resume Score Distribution")
        fig_scores.update_layout(xaxis_title="Score", yaxis_title="Count")
        st.plotly_chart(fig_scores)
    else:
        st.write("No data available for Resume Scores.")
    
    st.subheader("Feedback Ratings")
    if not feedback_data.empty and 'rating' in feedback_data.columns:
        rating_counts = feedback_data['rating'].value_counts().sort_index()
        fig_ratings = px.bar(x=rating_counts.index, y=rating_counts.values, title="Feedback Ratings")
        fig_ratings.update_layout(xaxis_title="Rating", yaxis_title="Count")
        st.plotly_chart(fig_ratings)
    else:
        st.write("No data available for Feedback Ratings.")

        
def generate_unique_id():
    return str(uuid.uuid4())

def main():
    try:
        
        init_database()
        
        if 'session_token' not in st.session_state:
            st.session_state.session_token = generate_session_token()
        
        latlng, city, state, country = get_geolocation()
        device_info = get_device_info()
        
        user_info = {
            "session_token": st.session_state.session_token,
            "geolocation": {
                "latitude": latlng[0] if latlng else None,
                "longitude": latlng[1] if latlng else None,
                "city": city,
                "state": state,
                "country": country
            },
            "device_info": device_info
        }
        
        #st.sidebar.title("AI Resume Analyzer & Recommendation System")
        st.sidebar.markdown("<span style='color:orange; font-size: 1.5em; font-weight: bold'>AI Resume Analyzer & Recommendation System</span>", unsafe_allow_html=True)
        st.sidebar.image("asset/logo_orange.svg")        
        pages = ["User", "Find Jobs", "Feedback", "About", "Admin"]
        #page = st.sidebar.radio("Navigation", pages)
        page = st.sidebar.selectbox("Navigation", pages)
        st.sidebar.subheader("Session")
        #st.sidebar.text(f"Session ID: {st.session_state.session_token[:8]}...")
        st.sidebar.text(f"Location: {city}, {country}")
        
        if page == "User":
            user_page()
        elif page == "Find Jobs":
            find_jobs_page()
        elif page == "Feedback":
            feedback_page()
        elif page == "About":
            about_page()
        elif page == "Admin":
            admin_page()
        
        st.sidebar.markdown("---")
        #st.sidebar.info("© 2024 resume Analyser. Designed by TalentTriage, All right reserved")
        st.sidebar.markdown("<font color='#3498db'>© 2024 Resume Analyser. Designed by TalentTriage, All right reserved</font>", unsafe_allow_html=True)
        if st.session_state.get('admin_logged_in', False) and st.sidebar.button("Logout"):
            st.session_state.admin_logged_in = False
            
            st.rerun()
        
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        st.error("Please try refreshing the page or contact support if the issue persists.")

if __name__ == "__main__":
    main()





