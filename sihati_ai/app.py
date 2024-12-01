from flask import Flask, render_template, request, redirect, url_for, session, flash
from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash
from random import randint
from flask_mail import Mail, Message

app = Flask('__name__')
app.secret_key = 'oaqssrb$%£/dsv'  # Replace with a secure secret key.

# MongoDB configuration
client = MongoClient('mongodb://localhost:27017/')
db = client['flask_user']  # Database name
users_collection = db['tbl_users']  # Collection name

# Flask-Mail configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = 'jarnijakawtar6@gmail.com'
app.config['MAIL_PASSWORD'] = 'abxe wywt lcfv udxs'
app.config['MAIL_DEFAULT_SENDER'] = 'jarnijakawtar6@gmail.com'
mail = Mail(app)

# Home Page
@app.route('/')
def index():
    if 'email' in session:
        return render_template('index.html', username=session['email'])
    return render_template('index.html')

# Login Page
# Login Page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        pwd = request.form['password']
        user = users_collection.find_one({'email': email})
        if user and check_password_hash(user['password'], pwd):
            session['email'] = user['email']
            # Redirection vers index1.html
            return render_template('ai/index.html', username=session['email'])
        else:
            return render_template('login.html', error='Invalid credentials')
    return render_template('login.html')


# Sign Up Page
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        phone = request.form['phone']
        email = request.form['email']
        pwd = request.form['password']
        hashed_pwd = generate_password_hash(pwd)
        users_collection.insert_one({
            'first_name': first_name,
            'last_name': last_name,
            'phone': phone,
            'email': email,
            'password': hashed_pwd
        })
        return redirect(url_for('login'))
    return render_template('signup.html')

# Forgot Password Page
@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form['email']
        user = users_collection.find_one({'email': email})
        if user:
            reset_code = randint(100000, 999999)
            users_collection.update_one({'email': email}, {'$set': {'reset_code': reset_code}})
            msg = Message('Password Reset Code', recipients=[email])
            msg.body = f"Your reset code is: {reset_code}"
            mail.send(msg)
            flash(f"A reset code has been sent to {email}.", "success")
            return redirect(url_for('verify_code', email=email))
        else:
            flash("Email address not found.", "danger")
    return render_template('forgot_password.html')

# Verify Code Page
@app.route('/verify_code/<email>', methods=['GET', 'POST'])
def verify_code(email):
    if request.method == 'POST':
        entered_code = request.form['reset_code']
        if entered_code.isdigit():
            entered_code = int(entered_code)
            user = users_collection.find_one({'email': email, 'reset_code': entered_code})
            if user:
                users_collection.update_one({'email': email}, {'$unset': {'reset_code': ""}})
                return redirect(url_for('reset_password', email=email))
            else:
                flash("Invalid reset code.", "danger")
        else:
            flash("The reset code must be a valid number.", "danger")
    return render_template('verify_code.html', email=email)

# Reset Password Page
@app.route('/reset_password/<email>', methods=['GET', 'POST'])
def reset_password(email):
    if request.method == 'POST':
        new_password = request.form['new_password']
        hashed_pwd = generate_password_hash(new_password)
        users_collection.update_one({'email': email}, {'$set': {'password': hashed_pwd}})
        flash("Your password has been successfully reset.", "success")
        return redirect(url_for('login'))
    return render_template('reset_password.html', email=email)

# Contact Us Page
@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        # Retrieve form data
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']
        
        # Create a message to send to your email (administrator)
        msg = Message('New Contact Message', recipients=['jarnijakawtar6@gmail.com'])
        msg.body = f"""
        You have received a new contact message.

        Name: {name}
        Email: {email}
        Message:
        {message}
        """
        
        # Send the email
        mail.send(msg)
        
        # Flash success message
        flash("Your message has been sent successfully. Here is a summary of your message.", "success")
        
        # Return these details in the contact page for display
        return render_template('contact.html', name=name, email=email, message=message)
    
    return render_template('contact.html')

# Logout
@app.route('/logout')
def logout():
    session.pop('email', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
