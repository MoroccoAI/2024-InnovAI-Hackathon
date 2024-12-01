
# AI Resume Analyzer

## Overview
The **AI Resume Analyzer** is a comprehensive web application developed using Streamlit that empowers users to gain insights into their resumes, identify skill gaps, and receive relevant course and job recommendations. This application leverages advanced NLP tools, resume parsing, and machine learning to provide users with personalized resume feedback, recommended fields, and job opportunities.


https://github.com/user-attachments/assets/9f39dbad-5aae-467e-bb40-ee42b90b84a8


## Key Features
- **Resume Analysis**: Extracts and analyzes the content of resumes to highlight skills, education, and work experience.
- **Skill and Field Recommendations**: Suggests courses and fields based on the analyzed skills.
- **Job Search**: Integrates web scraping to help users find job listings tailored to their profile.
- **Feedback Collection**: Enables users to submit feedback, which is stored for continuous improvement.
- **Admin Dashboard**: Provides an admin interface for managing and visualizing user data and feedback, including analytics such as user activity and experience distribution.
- **Chatbot**: Our application includes a chatbot feature that assists recruiters in obtaining information about candidates, streamlining communication and enhancing the overall recruitment process.

## Impact and Proposed Solution

**Problem**:  
In Morocco, recruiters often receive an overwhelming number of resumes, sometimes up to 400 within just 48 hours. This makes it nearly impossible for recruiters to thoroughly review each one, causing delays in the recruitment process and potentially missing out on qualified candidates.

**Impact**:  
The **AI Resume Analyzer** significantly alleviates the burden on recruiters by automating the initial stages of resume evaluation. It not only helps recruiters save valuable time by quickly identifying the most relevant resumes but also provides job seekers with personalized feedback and recommendations for improvement. This helps job seekers enhance their resumes and better align their skills with the needs of the job market.

**Proposed Solution**:  
To address the challenge faced by Moroccan recruiters, our application uses advanced resume analysis techniques to automatically process large numbers of resumes, highlighting key skills, qualifications, and areas for improvement. Recruiters can quickly assess candidate profiles, saving time while ensuring no potential talent is overlooked. Meanwhile, job seekers benefit from tailored recommendations on which skills to improve and which fields to pursue, boosting their chances of securing employment.
## Technologies Used
- **Frontend**: Streamlit for user interface
- **Backend**: Python with libraries such as Pandas, Spacy, NLTK, Selenium, Plotly, beautifulsoup adn openai 
- **Database**: MySQL for storing user and feedback data
- **PDF Parsing**: pdfminer for text extraction from resumes
- **NLP**: Spacy and NLTK for text processing and entity recognition

## Installation
### Prerequisites
- Python 3.7+
- pip (Python package installer)

### Installation Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/mouncefik/talent-triage.git
   cd AI_Resume_Analyzer
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up the database:
   - Ensure you have a MySQL server running.
   - Create a database named `resume_analyzer`.
   - Configure `.env` with your database credentials:
     ```
     DB_HOST=localhost
     DB_USER=root
     DB_PASSWORD=yourpassword
     DB_NAME=resume_analyzer
     NEBIUS_API_KEY=""
     ```
4. Run the application:
   ```bash
   streamlit run app.py
   ```

## Project Structure
```
.
├── app.py                 # Main application script
├── requirements.txt       # Python dependencies
├── README.md              # Project documentation
└── .env                   # Environment variables for database configuration
└── asset
      
```

## Usage Guide
1. **Upload Your Resume**: Navigate to the 'User' section and upload a PDF resume to get detailed analysis and feedback.
2. **Find Jobs**: Use the 'Find Jobs' page to search for jobs based on title and location.
3. **Admin Access**: Log in to access the admin dashboard, where you can view user data, feedback, and various analytics.
4. **Feedback**: Provide Feedback on the app.
5. **Improvement**:Improve your resume based on the suggestions.

## Security and Privacy
Your resume data is only used during your session for analysis and is not permanently stored.

### Known Issues
1. **Slow Job Finding Process**: The job search feature using web scraping can be slow, affecting user experience. Optimization efforts are in progress to improve response times.
2. **Improper Admin Visualization**: The admin dashboard may show inconsistent or unclear visual representations of user data. Enhancements to data visualization are planned for the next update.
3. **Limited Feedback Options**: The current feedback system provides basic text input, limiting user interaction. An expanded feedback mechanism with more structured input options will be implemented soon.

## Running the Project
To run the project, follow these steps:

1. Clone the repository:
   ```bash
   git clone https://github.com/mouncefik/talent-triage.git
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up the database:
   - Ensure you have a MySQL server running.
   - Create a database named `resume_analyzer`.
   - Configure `.env` with your database credentials:
     ```
     DB_HOST=localhost
     DB_USER=root
     DB_PASSWORD=yourpassword
     DB_NAME=resume_analyzer
     NEBIUS_API_KEY=""
     ```
4. Run the application:
   ```bash
   streamlit run app.py
   ```

## Troubleshooting
If you encounter any issues during the installation or running process, please refer to the following troubleshooting steps:

* Ensure that you have the latest version of pip installed by running `pip install --upgrade pip`.
* Verify that your MySQL server is running and that you have created the `resume_analyzer` database.
* Check that your `.env` file is correctly configured with your database credentials.
* If you encounter any errors during the installation process, try reinstalling the dependencies by running `pip install -r requirements.txt`.
