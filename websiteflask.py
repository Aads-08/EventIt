# -*- coding: utf-8 -*-
"""
Created on Fri Sep 20 22:53:31 2024

@author: samyu
"""

from flask import Flask, redirect, request, session, url_for, render_template
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Secret key for session management


# Connect to SQLite database (or create it)
def connect_db():
    conn = sqlite3.connect('users.db')
    return conn

# Initialize database and create 'students' and 'admins' tables if not exists
def init_db():
    conn = connect_db()
    cursor = conn.cursor()

    # Students table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            reg_number TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )
    ''')

    # Admins table
    cursor.execute('''
       CREATE TABLE IF NOT EXISTS admins (
           id INTEGER PRIMARY KEY AUTOINCREMENT,
           reg_number TEXT NOT NULL UNIQUE,
           password TEXT NOT NULL,
           club_name TEXT
       )
    ''')

    # Events table (club_name is a foreign key)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            club_name TEXT,
            event_name TEXT NOT NULL,
            event_description TEXT,
            date DATE NOT NULL,
            time TIME NOT NULL,
            venue TEXT NOT NULL,
            enrollment_form TEXT,
            FOREIGN KEY (club_name) REFERENCES admins(club_name) ON DELETE CASCADE
        )
    ''')

    conn.commit()
    conn.close()


@app.route('/')
def home():
    return render_template("index.html")


# Student login form route
@app.route('/studentlogin')
def studentlogin():
    return render_template('studentlogin.html')


# Student login POST route
@app.route('/login', methods=['POST'])
def login():
    reg_number = request.form['reg_number']
    password = request.form['password']

    # Connect to database and check credentials
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students WHERE reg_number = ? AND password = ?", (reg_number, password))
    student = cursor.fetchone()
    conn.close()

    if student:
        session['reg_number'] = reg_number
        return redirect(url_for('student'))  # Redirect to student dashboard
    else:
        error = "Invalid registration number or password"
        return render_template('studentlogin.html', error=error)


# Student dashboard
@app.route('/student')
def student():
    if 'reg_number' in session:
        return render_template("student.html")
    else:
        return redirect(url_for('home'))


# Admin login form route
@app.route('/adminlogin')
def adminlogin():
    return render_template('adminlogin.html')


# Admin login POST route
@app.route('/login2', methods=['POST'])
def login2():
    reg_number = request.form['reg_number']
    password = request.form['password']

    # Connect to database and check credentials
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM admins WHERE reg_number = ? AND password = ?", (reg_number, password))
    admin = cursor.fetchone()
    conn.close()

    if admin:
        session['reg_number'] = reg_number
        return redirect(url_for('admin'))  # Redirect to student dashboard
    else:
        error = "Invalid registration number or password"
        return render_template('adminlogin.html', error=error)


# Student dashboard
@app.route('/admin')
def admin():
    if 'reg_number' in session:
        return render_template("admincalendar.html")
    else:
        return redirect(url_for('home'))


if __name__ == '__main__':
    init_db()  # Initialize the database when the app starts
    app.run(debug=True)
