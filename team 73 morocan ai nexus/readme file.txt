# Easy - Information and services powered by AI App

## Overview

Easy is a user authentication application that allows users to register and log in using their email and password. The app is built using an Android frontend, a Node.js backend, and a MongoDB database. This project demonstrates how to implement user registration and login functionality with secure password hashing and JSON Web Tokens (JWT) for authentication. Also it gives the user the capability of exploring the different services offered by Easy like Khadamat Al Mowatin that offers a range of info without missing our chatbot that helps you find information with a single tap

## Table of Contents

- [Features](#features)
- [Technologies Used](#technologies-used)
- [Dependencies](#dependencies)
- [Installation](#installation)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Contributing](#contributing)
- [License](#license)

## Features

- User registration with unique username and email.
- Secure password storage using bcrypt hashing.
- User login with email and password.
- JSON Web Token (JWT) for secure authentication.
- User-friendly Android interface.

## Technologies Used

- Frontend: Android Studio, Java, XML
- Backend: Node.js, Express.js
- Database: MongoDB

## Dependencies

### Android Dependencies
- Volley: A networking library for Android that simplifies making HTTP requests.
- Gson: A library to convert Java Objects into JSON and back, used for parsing API responses.

### Node.js Dependencies
- Express: A web framework for Node.js that simplifies server creation and routing.
- Mongoose: An ODM (Object Data Modeling) library for MongoDB and Node.js, used for data validation and schema management.
- Bcrypt: A library to hash passwords securely.
- Jsonwebtoken: A library to issue and verify JSON Web Tokens for authentication.
- Cors: A package to enable Cross-Origin Resource Sharing, allowing your API to be accessed from different origins.

## Installation

### Prerequisites

- Node.js and npm installed on your machine.
- MongoDB installed and running.
- Android Studio installed.

### Backend Setup

1. Clone the repository:
   bash
   git clone <repository-url>
   cd back_ana
Install the required packages:
bash
npm install
Start your MongoDB server:
bash

mongod
Run the backend server:

bash
node server.js

### Frontend Setup
Open the project in Android Studio.
Update the LOGIN_URL and REGISTER_URL in LoginActivity.java and RegisterActivity.java to match your backend server's IP address and port (e.g., http://192.168.1.30:5000/api/auth/login).
Run the application on your Android device or emulator.
Usage
Launch the app on your Android device.
Navigate to the registration screen to create a new account.
#### After successful registration, log in using the following credentials:
- Email: zekri@gmail.com
- Password: test

Upon successful login, you will be redirected to the home screen.
## API Endpoints
Registration
Endpoint: /api/auth/register
Method: POST

Login
Endpoint: /api/auth/login
Method: POST
## Fonctionnalités principales

- **Navigation Drawer :** Permet d'accéder facilement aux différentes sections de l'application via un menu latéral interactif.
- **Interface utilisateur intuitive :** Des logos animés pour rendre l'expérience plus engageante.
- **Animations personnalisées :** 
  - Logo supérieur avec une animation de mise à l'échelle au clic.
  - Logo central avec une animation d'apparition (translation et fade-in).
  - Effet dynamique sur le menu latéral.
- **Transitions fluides entre les activités.**
## Technologies utilisées

- **Langage :** Java
- **Framework :** Android SDK
- **IDE :** Android Studio
- **Bibliothèques utilisées :**
  - Support pour Navigation Drawer.
  - Animations personnalisées avec des fichiers XML.
## Détails sur l'interface

L'interface utilisateur de l'application EEEASY a été conçue pour être simple, moderne et réactive. Voici quelques points marquants :

- **Logo central :** Placé au milieu de l'écran pour attirer l'attention. Il apparaît avec une animation de translation fluide.
- **Logo supérieur :** Agit comme un bouton interactif pour naviguer vers une autre activité. Lors du clic, il s'agrandit légèrement grâce à une animation de mise à l'échelle.
- **Navigation Drawer :** 
  - Permet un accès rapide aux différentes fonctionnalités.
  - Inclut un effet de réduction pour améliorer l'expérience utilisateur.
## Étapes de développement

1. **Configuration du projet :** 
   - Création d'un projet Android dans Android Studio.
   - Ajout des dépendances nécessaires pour le Navigation Drawer.

2. **Conception de l'interface utilisateur :**
   - Mise en place du `Navigation Drawer` dans le fichier XML.
   - Ajout de deux `ImageButton` pour les logos central et supérieur.
   - Création des animations personnalisées dans le dossier `res/anim`.

3. **Ajout des animations :**
   - Création de fichiers XML (`scale_up.xml` et `slide_in.xml`) pour les animations.
   - Implémentation des animations dans le code Java pour les logos et le menu latéral.

4. **Navigation entre les activités :**
   - Configuration de l'`Intent` pour permettre la transition entre les écrans via le logo supérieur.

5. **Test et amélioration :**
   - Tests sur un appareil Redmi pour s'assurer que toutes les fonctionnalités fonctionnent correctement.
   - Ajustement des animations et de l'interface utilisateur pour une meilleure fluidité.
## Installation et exécution

1. Clonez le dépôt GitHub :
   bash
   git clone https://github.com/votre-utilisateur/eeeasy.git

---

### 7. *Aperçu*
Ajoutez des captures d'écran ou des GIFs montrant les animations et l'interface utilisateur.

```markdown
## Aperçu

![Logo Central Animation](https://your-screenshot-link)
![Menu Latéral](https://your-screenshot-link)
## Contributions

Les contributions sont les bienvenues ! Veuillez soumettre une issue ou un pull request pour toute amélioration ou suggestion.



Comments or Notes for Organizers/Jury

We would like to highlight the following:

Project Status:
While the application is not fully deployed, it functions perfectly when executed in the terminal. This demonstrates the potential of our solution and its foundational strength.

Scope of Innovation:
The idea behind this project is ambitious and has the potential to bring significant positive change to Morocco. We believe it can pave the way for transformative solutions in the future.

Development Timeline:
Given the limited time available, we focused on building a robust core functionality. Some planned features, such as the RAG module and full deployment, are not yet implemented but remain integral to our vision.

Request for Consideration:
We kindly ask the organizers and jury to evaluate the project based on its potential, technical soundness, and scalability rather than its current deployment status. Your understanding and support are greatly appreciated.

Thank you for taking the time to review our work and for considering the vision we aim to bring to life.