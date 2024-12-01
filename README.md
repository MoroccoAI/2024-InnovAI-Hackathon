# Expense Tracker Application

## Project Overview

The application is designed as an expense management tool. Its primary feature is an AI-powered system that identifies items, their costs, and categories from grocery store receipts. Users can upload a receipt image through the app or capture one directly using their device's camera.

It includes a section where users can get chatbot recommendations about the expenses.

The app includes a data visualization module with graphs and charts to help users analyze spending patterns, track expenses by category, view trends, alongside predictions.

---

## Folder Structure

### 1. Demo
The `demo` folder contains the **front-end** implementation of the application, built with **Expo** for mobile compatibility using **React Native**.

#### Key Features:
- **Dashboard:** The home screen is designed as a dashboard providing users with an overview of their expenses.
  - **Visual Representations:** Includes a **pie chart** for expense categories and a **line chart** for expense trends over time.
  - **Filter by Period:** Allows users to filter expenses for a specific time period.
- **Receipt Management:**
  - **Scan Receipts:** Use the device's native camera to scan receipts directly.
  - **Upload Receipts:** Upload receipt images from the device's storage.
  - **Manual Input:** Enter expense details manually for complete control.

### 2. Backend
The `backend` folder contains the server-side logic, managing the application's data and functionality.

#### Key Features:
- **Models:** Defines data models using **MongoDB** to store user data, expenses, and other application-specific information.
- **Routing:** Handles all API endpoints to support the functionalities of the front-end, including:
  - Receipt processing.
  - Expense filtering and categorization.
  - User data management.

### 3. Service
The `service` folder is responsible for handling image processing, enabling the automatic classification of expenses from scanned or uploaded receipts.

#### Key Features:
- **Image Processing:** Extracts relevant data from receipts using advanced algorithms.
- **Expense Classification:** Processes images to categorize expenses and outputs the results as a **JSON** format.
- **Integration:** Seamlessly integrates with the backend to update the user's expense data.

---

## Technologies Used

- **Front-End:** React Native (Expo)
- **Back-End:** Node.js with Express.js
- **Database:** MongoDB
- **Image Processing:** Custom services for expense classification from images
- **Server:** Flask for Python-based services

---

## Setup Instructions

### Prerequisites
- Python 3.8+
- Flask Framework
- MongoDB
- Node.js 18.12.1

### Installation
1. Clone the Repository:
    git clone https://github.com/aBenbou/2024-InnovAI-Hackathon.git
    cd team-51
    cd service

2. Install Dependencies:
    pip install -r requirements.txt

3. Seed the Database:
    python seed.py

4. Start the Flask Server:
    python app.py

5. Start the Backend:
    cd backend
    npm start

6. Start the React Native App:
    cd demo
    npm install
    npm start
