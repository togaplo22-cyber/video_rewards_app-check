
from flask import Flask, render_template, session
import sqlite3
import os

app = Flask(__name__)
app.secret_key = 'secret123'

@app.route('/')
def home():
    session['user_id'] = 1
    return redirect('/dashboard')

@app.route('/dashboard')
def dashboard():
    conn = sqlite3.connect('earntowatch.db')
    c = conn.cursor()
    c.execute("SELECT username, watch_earnings, referral_earnings FROM users WHERE id = ?", (session['user_id'],))
    user = c.fetchone()
    conn.close()
    return render_template('user_dashboard.html', username=user[0], watch_earnings=user[1], referral_earnings=user[2])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
