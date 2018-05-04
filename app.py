from flask import Flask, flash, abort, redirect, render_template, request, session, abort, url_for
import os
import random
from flask_mysqldb import MySQL
from passlib.handlers.sha2_crypt import sha256_crypt
from register_form import RegisterForm
import datetime
import time

app = Flask(__name__)

#config
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_PORT'] = 3306
app.config['MYSQL_USER'] = 'dt_admin'
app.config['MYSQL_PASSWORD'] = 'Mar1010n'
app.config['MYSQL_DB'] = 'studentsattendance'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

#initialize MySQL
mysql = MySQL(app)

trusted_proxies = ('42.42.42.42', '127.0.0.1', '192.168.0.100')  # restrict access to only these ip addresses


@app.before_request
def limit_remote_addr():
    if request.remote_addr != '127.0.0.1':  # we insert here KEAs ip address and also in the last line: host=...
        abort(403)


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':

        #  Get the fields
        POST_USERNAME = request.form['username']
        POST_PASSWORD = request.form['password']

        #  Create a cursor
        cur = mysql.connection.cursor()
        #  Get user by username
        result = cur.execute("SELECT * FROM users WHERE username = %s", [POST_USERNAME])
        if result > 0:
            #  Get the stored hash
            data = cur.fetchone()
            password = data['password']
            #  Compare the passwords
        if sha256_crypt.verify(POST_PASSWORD, password):
            session['logged_in'] = True
            session['username'] = POST_USERNAME

            flash('You are now logged in', 'success')
            return redirect(url_for('dashboard'))

        else:
            error = 'Invalid Login'
            return render_template('login.html', error=error)
        #  Close connection
        cur.close()
    else:
        return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)

    if request.method == 'POST' and form.validate():
        name = form.name.data
        email = form.email.data
        username = form.username.data
        password = sha256_crypt.encrypt(str(form.password.data))

        # create a cursor
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users(name, email, username, password) VALUES(%s, %s, %s, %s)",
                    (name, email, username, password))

        # commit to db
        mysql.connection.commit()
        cur.close()

        flash('You are now registered and can login', 'success')

        return redirect(url_for('login'))

    return render_template('register.html', form=form)


@app.route('/dashboard')
def dashboard():
    #create cursor
    cur = mysql.connection.cursor()
    #Get users
    result = cur.execute("SELECT * FROM users")
    users = cur.fetchall()
    timeout = datetime.datetime.today()
    tdelta = datetime.timedelta(minutes=30)

    if result > 0:
        return render_template('dashboard.html', users=users)
    else:
        msg = 'No Projects found'
        return render_template('dashboard.html', msg=msg)




    #Close the connection
    cur.close()


@app.route('/codegenerator', methods=['GET', 'POST'])
def codegenerator():

        error = None
        passwordd = ''
        codetime = datetime.datetime.today()
        #  tdelta = datetime.timedelta(minutes=30)

        if request.method == 'GET' or 'POST':

            for n in range(0, 8):

                x = random.randint(0, 9)
                if x <= 3:
                    passwordd += str(random.choice('abcdefghijklmnopqrstuvxyz'))
                elif x <= 6:
                    passwordd += str(random.choice(',.;:-_*%&/()=?!'))
                else:
                    passwordd += str(random.randrange(0, 9))

            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO generatedcode(password, timeout) VALUES (%s, %s)", [passwordd, codetime])
            mysql.connection.commit()
            cur.close()
            return passwordd
        return render_template('codegenerator.html', error=error)


@app.route('/teacherprofile', methods=['GET', 'POST'])
def teacherprofile():
    error = None
    if request.method == 'POST':
        if request.form['submit'] == 'Generate':
            redirect(url_for('codegenerator'))
    elif request.method == 'GET':
        redirect(url_for('codegenerator'))

    return render_template('teacherprofile.html', error=error)


@app.route('/teacherSignin', methods=['GET', 'POST'])
def teacher():
    error = None
    if request.method == 'POST':
        if request.form['user'] != 'admin' or request.form['pass'] != 'admin':
            error = 'Invalid Credentials. Please try again.'
        else:
            return redirect(url_for('teacherprofile'))
    return render_template('teacherSignin.html', error=error)


@app.route("/logout")
def logout():
    session.clear()
    flash('You are now logged out', 'success')
    return redirect(url_for('login'))
    return home()


if __name__ == "__main__":
    app.secret_key = 'secret123'
    app.run(host='127.0.0.1', debug=False)
