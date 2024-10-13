from flask import Flask, url_for, request, render_template, redirect, session
from flask_mysqldb import MySQL
import MySQLdb.cursors, re

app = Flask(__name__)

app.secret_key = 'sEcrEtKeY'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'auth'

mysql = MySQL(app)

@app.route('/')
def start():
    return redirect(url_for('login'))

@app.route('/login', methods =['GET', 'POST'])
def login():
    message = ''
    if request.method == 'POST' and 'userId' in request.form and 'password' in request.form: 
        userId = request.form['userId']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE userId = %s AND password = %s', (userId, password, ))
        user = cursor.fetchone()
        if user:
            session['loggedin'] = True
            session['id'] = user['id']
            session['userId'] = user['userId']
            message = 'Logged in successfully!'
            return render_template('index.html', user=session)
        else:
            message = 'Incorrect User ID or Password!'
    return render_template('login.html', message = message)
 
@app.route('/logout')
def logout():
    message = 'You have been logged out successfully!'
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('userId', None)
    return render_template('login.html', message = message)
 
@app.route('/register', methods =['GET', 'POST'])
def register():
    message = ''
    if request.method == 'POST' and 'userId' in request.form and 'password' in request.form and 'phNo' in request.form :
        userId = request.form['userId']
        phNo = request.form['phNo']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE userId = %s', (userId, ))
        user = cursor.fetchone()
        if user:
            message = 'User already exists!'
        elif not re.match(r'[A-Za-z0-9]+', userId):
            message = 'User ID must contain only characters and numbers!'
        elif not re.match(r'^\d{10}$', phNo):
            message = 'Invalid phone number!'
        elif not userId or not password or not phNo:
            message = 'Please fill out the form!'
        else:
            cursor.execute('INSERT INTO users VALUES (NULL, %s, %s, %s)', (userId, phNo, password, ))
            mysql.connection.commit()
            message = 'You have successfully registered!'
    elif request.method == 'POST':
        message = 'Please fill out the form!'
    return render_template('register.html', message = message)

if __name__ == "__main__":
    app.run(debug=True)