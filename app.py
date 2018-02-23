from flask import Flask, flash, redirect, render_template, request, session, abort, url_for
import os
from flask_mysqldb import MySQL
from passlib.hash import sha256_crypt

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

@app.route('/about')
def about():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method=='POST':

        #Get the fields
        POST_USERNAME = request.form['username']
        POST_PASSWORD = request.form['password']

        #Create a cursor
        cur = mysql.connection.cursor()
        #Get user by username
        result = cur.execute("SELECT * FROM users WHERE username = %s", [POST_USERNAME])
        if result > 0:
            #Get the stored hash
            data = cur.fetchone()
            password = data['password']
            #Compare the passwords
        if sha256_crypt.verify(POST_PASSWORD, password):
            session['logged_in'] = True
            session['username'] = POST_USERNAME

            flash('You are now logged in', 'success')
            return redirect(url_for('dashboard'))

        else:
            error = 'Invalid Login'
            return render_template('login.html', error=error)
        #Close connection
        cur.close()
    else:
        return render_template('login.html')

    @app.route("/logout")
    def logout():
        session.clear()
        flash('You are now logged out', 'success')
        return redirect(url_for('login'))
        return home()

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=False)
