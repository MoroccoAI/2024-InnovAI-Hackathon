# EduPulse

![logo](assets/logo.jpeg)
> An AI-powered educational platform that transforms individual student assessments into actionable insights for personalized learning and school-wide improvement.

---

## Abstract

### Background and Problem Statement
High school teachers, particularly in mathematics, face challenges in effectively assessing individual student understanding, identifying specific weaknesses, and creating personalized learning paths. Moreover, tracking improvement and developing data-driven teaching strategies is time-consuming and resource-intensive. This lack of scalable, data-driven solutions limits the overall educational outcomes.

### Impact and Proposed Solution
EduPulse addresses these challenges by providing an AI-powered platform that automates assessment, delivers personalized learning experiences, and enables data-driven decision-making. By focusing on a cycle of diagnosis, intervention, and improvement, EduPulse transforms student data into actionable insights, helping educators improve outcomes at both individual and institutional levels.

### Project Outcomes and Deliverables
The project delivers:
1. A diagnostic survey system for targeted assessments.
2. AI-generated personalized learning materials.
3. Progress tracking for individual students.
4. Teacher dashboards for detailed analytics.
5. School-wide analytics for strategic decision-making.

---

## Table of Contents
- [Abstract](#abstract)
- [Team](#team)
- [Usage](#usage)
- [Technologies Used](#technologies-used)
- [Data Types and Sources](#data-types-and-sources)
- [Key Features](#key-features)
- [Instructions](#instructionss)

---

## Team
**MARSSY Team Members**:
- Reda NASSIF
- Soufiane AIT EL AOUAD
---

## Usage
EduPulse follows a systematic workflow:

1. **Initial Assessment**  
   Teachers create topic-specific diagnostic surveys, and students complete them to identify strengths and weaknesses.

2. **Personalized Learning**  
   The system analyzes survey results, generating customized learning materials tailored to each student’s needs.

3. **Progress Tracking**  
   Students undergo reassessment to measure improvement. Teachers receive detailed analytics on performance.

4. **Strategic Insights**  
   Teachers and administrators access dashboards to guide data-driven educational strategies.

---

## Technologies Used

**Frontend**:
- React  
  - Modern UI components, interactive dashboards, and responsive design.

**Backend**:
- Flask  
  - RESTful API architecture, secure authentication, database integration, and analytics processing.

**AI/ML**:
- OpenAI  
  - GPT models for content generation and personalized learning paths.

---

## Data Types and Sources
1. **Student Assessment Data**:  
   - Multiple-choice questions, topic-specific surveys, and performance metrics.

2. **Learning Materials**:  
   - Customized content, topic resources, and practice exercises.

3. **Analytics Data**:  
   - Individual and class-wide performance metrics, as well as school-level insights.

---

## Key Features

### 1. Diagnostic Survey System
- Automated assessment creation  
- Weakness identification  
- Strength mapping  

### 2. Personalized Learning Materials
- AI-generated resources  
- Gap-targeted content  
- Adaptive learning paths  

### 3. Teacher Performance Dashboard
- Individual student analytics  
- Class-wide performance metrics  
- Progress tracking  

### 4. School-Wide Analytics
- Cross-class performance tracking  
- Institutional insights  
- Department-level analytics  

### 5. Classroom Strategy Builder
- Data-driven recommendations  
- Resource optimization  
- Improvement tracking  

--- 



## Instructions

### Prerequisites
1. **Python**: Ensure you have Python 3.12.3 installed.
2. **Node.js**: Make sure Node.js is installed on your system.

### Steps

#### 1. Configure Environment Variables
- **Backend (.env for `edusmart`):**  
  Create a `.env` file inside the `./edusmart` directory with the following content:  
  ```env
  OPENAI_API_KEY="sk-***"
  ```
  Replace `sk-***` with your OpenAI API key. You can refer to `.env.prod` for an example.

- **Frontend (.env for `frontend`):**  
  Create a `.env` file inside the `./frontend` directory with the following content:  
  ```env
  VITE_BACKEND_URL=http://127.0.0.1:5000
  ```


#### 2. Set Up Backend
- Navigate to the `./edusmart` directory.  
- Create a Python virtual environment and activate it:  
  ```bash
  python -m venv venv
  source venv/bin/activate   # For Linux/Mac
  venv\Scripts\activate      # For Windows
  ```
- Install the required dependencies:  
  ```bash
  pip install -r requirements.txt
  ```
- Start the backend server:  
  ```bash
  python app.py
  ```

#### 3. Set Up Frontend
- Navigate to the `./frontend` directory.  
- Install dependencies:  
  ```bash
  npm install
  ```
- Start the development server:  
  ```bash
  npm run dev
  ```

### Additional Resources
- You can access the demo and pitch video in the `./videos` directory.