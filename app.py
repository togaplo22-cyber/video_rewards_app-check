
import os
import sqlite3
from flask import Flask, render_template, request, redirect, session, url_for
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'supersecretkey'

DB_NAME = 'database.db'

# Initialize database
def init_db():
    with sqlite3.connect(DB_NAME) as conn:
        c = conn.cursor()
        c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT,
            referral TEXT,
            earnings REAL DEFAULT 0
        )
        """)
        c.execute("""
        CREATE TABLE IF NOT EXISTS cashouts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            amount REAL,
            status TEXT DEFAULT 'Pending'
        )
        """)

init_db()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = generate_password_hash(request.form['password'])
        referral = request.form.get('referral', '')
        with sqlite3.connect(DB_NAME) as conn:
            c = conn.cursor()
            try:
                c.execute("INSERT INTO users (username, password, referral) VALUES (?, ?, ?)",
                          (username, password, referral))
                conn.commit()
                return redirect('/login')
            except:
                return "Username already exists."
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        with sqlite3.connect(DB_NAME) as conn:
            c = conn.cursor()
            c.execute("SELECT id, password FROM users WHERE username = ?", (username,))
            user = c.fetchone()
            if user and check_password_hash(user[1], password):
                session['user_id'] = user[0]
                return redirect('/dashboard')
            elif username == 'admin' and password == 'Password1515':
                session['admin'] = True
                return redirect('/admin')
            else:
                return "Invalid credentials"
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/login')
    with sqlite3.connect(DB_NAME) as conn:
        c = conn.cursor()
        c.execute("SELECT username, earnings FROM users WHERE id = ?", (session['user_id'],))
        user = c.fetchone()
    return render_template('dashboard.html', username=user[0], earnings=user[1])

@app.route('/watch')
def watch():
    if 'user_id' not in session:
        return redirect('/login')
    with sqlite3.connect(DB_NAME) as conn:
        c = conn.cursor()
        c.execute("UPDATE users SET earnings = earnings + 0.10 WHERE id = ?", (session['user_id'],))
        conn.commit()
    return render_template('watch.html')

@app.route('/cashout', methods=['GET', 'POST'])
def cashout():
    if 'user_id' not in session:
        return redirect('/login')
    if request.method == 'POST':
        amount = float(request.form['amount'])
        with sqlite3.connect(DB_NAME) as conn:
            c = conn.cursor()
            c.execute("INSERT INTO cashouts (user_id, amount) VALUES (?, ?)", (session['user_id'], amount))
            conn.commit()
        return "Cashout request submitted."
    return render_template('cashout.html')

@app.route('/admin')
def admin():
    if 'admin' not in session:
        return redirect('/login')
    with sqlite3.connect(DB_NAME) as conn:
        c = conn.cursor()
        c.execute("SELECT users.username, cashouts.amount, cashouts.status FROM cashouts JOIN users ON users.id = cashouts.user_id")
        requests = c.fetchall()
    return render_template('admin.html', requests=requests)

if __name__ == '__main__':
    app.run(debug=True)
