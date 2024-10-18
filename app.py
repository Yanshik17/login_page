from flask import Flask, render_template, request, redirect, flash, url_for
import mysql.connector
from mysql.connector import Error
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Database configuration
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'yY123456@',
    'database': 'user_database'
}

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_id = request.form['loginUserId']
        password = request.form['loginPassword']

        connection = None
        try:
            connection = mysql.connector.connect(**db_config)
            if connection.is_connected():
                cursor = connection.cursor()
                cursor.execute("SELECT password FROM users WHERE user_id = %s", (user_id,))
                result = cursor.fetchone()

                if result and check_password_hash(result[0], password):
                    flash("Login successful!")
                    return redirect(url_for('welcome'))
                else:
                    flash("Invalid User ID or Password.")

        except Error as e:
            flash(f"Error during login: {str(e)}")
        finally:
            if connection is not None and connection.is_connected():
                cursor.close()
                connection.close()

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        user_id = request.form['registerUserId']
        mobile_number = request.form['mobileNumber']
        password = generate_password_hash(request.form['registerPassword'])

        connection = None
        try:
            connection = mysql.connector.connect(**db_config)
            if connection.is_connected():
                cursor = connection.cursor()
                cursor.execute("INSERT INTO users (user_id, mobile_number, password) VALUES (%s, %s, %s)",
                               (user_id, mobile_number, password))
                connection.commit()
                flash("Registration successful!")
                return redirect(url_for('login'))

        except Error as e:
            flash(f"Error during registration: {str(e)}")
        finally:
            if connection is not None and connection.is_connected():
                cursor.close()
                connection.close()

    return render_template('register.html')

@app.route('/welcome')
def welcome():
    return render_template('welcome.html')  # Create a welcome.html template for the welcome page.

if __name__ == '__main__':
    app.run(debug=True)
