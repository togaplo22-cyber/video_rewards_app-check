
from flask import Flask, render_template, request, redirect
import sqlite3, os

app = Flask(__name__)

@app.route('/')
def home():
    return redirect('/login')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/admin')
def admin_dashboard():
    conn = sqlite3.connect('earntowatch.db')
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM users")
    total_users = c.fetchone()[0]
    conn.close()
    return render_template('admin_dashboard.html', total_users=total_users)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
