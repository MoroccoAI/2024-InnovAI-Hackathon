from flask import Flask, render_template, session, url_for, redirect, request, jsonify, make_response
from pymongo import MongoClient
import os
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime
from bson.objectid import ObjectId
import random

from form import *
from functions import *

import json
import pickle
from ChatBot import *
from Bot_functions import *
from keras.models import load_model

# Initialize the chatbot
json_file_path = 'Model/topics_data.json'  # Replace with your JSON file path
groq_api_key = "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"  # Replace with your Groq API key
chatbot = CareerCounselingChatbot(json_file_path, groq_api_key)
        
# # Example user profile
# user_profile = chatbot.create_user_profile(
#     name="John Doe",
#     career_goals="Data Science",
#     education="Bachelor's in Computer Science",
#     skills="Python, Machine Learning"
# )


app = Flask(__name__)
secret_key = os.urandom(12).hex()
app.config['SECRET_KEY'] = secret_key

# Mongo
client = MongoClient("mongodb+srv://namezyasser3:admin@cluster0.ga0p0.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client.get_database("db_bot")

user_name = None

pred = False
predMsg = ""

emailSent = False
code = ""
resetPass = False
emailPointed = ""
recFinished = False


@app.route("/")
def home():
    if "id" in session:
        return redirect(url_for('bot'))
        
    return render_template("index.html")

@app.route("/login", methods=("POST", "GET"))
def login():
    if "id" in session:
        return redirect(url_for('bot'))

    form = LoginForm()
    error = ""
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        # Checking if user with such email exists
        records = db.users
        user = records.find_one({"email": email})
        if user:
            # User Exists -> Checking passwords
            if check_password_hash(user["password"], password):
                # Correct Password
                session["id"] = str(user["_id"])
                return redirect(url_for('bot'))
            else:
                # Wrong Password
                error = "Wrong Password."
        else:
            error = "User does not exist."

    return render_template("login.html", form=form, error=error)

@app.route("/signup", methods=("POST", "GET"))
def signup():
    if "id" in session:
        return redirect(url_for('bot'))
    
    form = SignupForm()
    error = ""
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data
        confirm = form.conpassword.data

        if password!=confirm:
            error="Passwords do not match."

        # Verifying if data already exist
        records = db.users
        if list(records.find({'email': email})):
            # User Already Exists
            error="User Already Exists."
        else:
            # User Doesn't Exist
            new_user = {
                "username": username,
                "email": email,
                "password": generate_password_hash(password) # Hashing Password
            }
            records.insert_one(new_user) # Inserting User Records to DB
            user = records.find_one({"email": email})
            session["id"] = str(user["_id"])

            # Creating a new chat for the new user
            records = db.chats
            records.insert_one({"user":session["id"]})
            return redirect(url_for('bot'))
            
    return render_template("signup.html", form=form, error=error)

@app.route("/bot", methods=("POST", "GET"))
def bot():
    # Redirecting Users to Login Page if they aren't logged
    if "id" not in session:
        return redirect(url_for('login'))

    # Storing Message In DB when sent
    if request.method=="POST":
        data = request.get_data().decode("utf-8").split(" ")
        # AJAX SENDS DATA AS FOLLOWING [ACTION] [MESSAGE] [TARGET]
        # WE TRY TO CLASSIFY THE ACTION TYPE BY CHECKING THE VALUE OF [ACTION]
        action = data[0]
        print(data)

        if action=="AddChat":
            #ADD CHAT
            records = db.chats
            records.insert_one({"user":session['id']})
        elif action=="DeleteChat":
            #DELETE CHAT
            target = data[-1]
            records = db.chats
            if(len(list(records.find({"user":session['id']})))>1):
                records.delete_one({"_id":ObjectId(target)})
                # Deleting Messages
                records = db.messages
                imgs = []
                for record in records.find({"chat":target}):
                    if type(record['message'])==list and record['message'][0] in ("GRAPH PLOT", "GRAPH PRED"):
                        imgs.append(record['message'][1])
                records.delete_many({"chat":target})
                # Deleting Pictures
                for img in imgs:
                    try:
                        os.remove(f"./static/data/{img}.png")
                    except:
                        pass

        else:
            #INSERT MESSAGE
            global pred
            global predMsg
            global user_name
            global item_pred
            message = " ".join(data[1:-1])
            target = data[-1]
            print(message, target)
            records = db.messages
            now = datetime.now()
            dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
            records.insert_one({"user": session["id"], "chat": target, "message": message, "type": "user", "date":dt_string})
            
            # AI Thingie Here
            
            response = chatbot.get_response(message)
            response = clean_response_for_html(response)
            records.insert_one({"bot": session["id"], "chat": target, "message": ['NORMAL REPLY',response], "type": "bot", "date":dt_string})

    return render_template("bot.html")

@app.route('/api/<cat>/<val>/<chat>', methods=("POST", "GET"))
@app.route("/api/<cat>/<val>", methods=("POST", "GET"), defaults={'chat': None})
def api(cat, val, chat):
    data = []
    if "id" in session:
        if cat=="msgs":
            records = db.messages
            for record in list(records.find({"chat": chat})):
                data.append((record["message"], record["type"]))
        if cat=="curr" and val=="user":
            data = session['id']
        if cat=="chats":
            records = db.chats
            for record in list(records.find({"user":val})):
                data.append((str(record["_id"])))

    return make_response(jsonify(data))

@app.route('/recovery', methods=("POST", "GET"))
def recovery():
    global code
    global emailSent
    global resetPass
    global emailPointed
    global recFinished

    if 'id' in session:
        return render_template(url_for('bot'))

    form = RecoveryForm()

    if not(recFinished) and form.validate_on_submit():
        emailSent = False
        code = ""
        resetPass = False
        emailPointed = ""

    if not(emailSent) and form.validate_on_submit():
        records = db.users
        email = form.email.data
        emailPointed = email
        if not(len(list(records.find({"email":email})))):
            return render_template('reset.html', form=form, error="User with such records not found.")
        #Generating random 6-digit-code
        code = random.randint(100000, 999999)
        htmlcode = """<link rel="preconnect" href="https://fonts.googleapis.com">
                    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
                    <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@100;400&display=swap" rel="stylesheet"> 
                    <body>
                    <style>
                    * {
                            font-family: 'Roboto';
                        }
                    </style>
                    <p>Hi, this email contains a recovery code that you can use to change the password of your account. Here's the <strong>Recovery Code</strong>: </p>
                    <center>
                    <p style="font-size:34px;background: white; width: fit-content; padding: .75em 1em; border-radius: 6px; color: #ff123d; font-weight: bold; box-shadow: rgb(0, 0, 0, .25) 0 2px 5px;">"""+str(code)+"""</p>
                    </center>
                    </body>"""
        sendMail(email, 'Account Recovery', htmlcode)
        emailSent = True
        return render_template('verify.html' , form=VerifyForm(), code=code)
    elif emailSent and VerifyForm().validate_on_submit():
        userCode = VerifyForm().code.data
        if(int(userCode)==code):
            resetPass = True
            return render_template("resetpassword.html", form=ResetPasswordForm())
    elif resetPass and ResetPasswordForm().validate_on_submit():
        password = ResetPasswordForm().newpassword.data
        records = db.users
        myquery = { "email": emailPointed }
        newvalues = { "$set": { "password":generate_password_hash(password)  } }
        records.update_one(myquery, newvalues)

        recFinished = True

        return redirect(url_for('login'))

    return render_template('reset.html', form=form)


@app.route("/destroy", methods=("POST", "GET"))
def destroy():
    if 'id' in session:
        session.pop('id')

    return redirect(url_for('login'))

if __name__ == "__main__":
    app.run(debug=True)