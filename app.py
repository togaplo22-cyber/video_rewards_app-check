
from flask import Flask, render_template, session
import sqlite3
import os

app = Flask(__name__)
app.secret_key = 'secret'

@app.route('/dashboard')
def dashboard():
    try:
        conn = sqlite3.connect('earntowatch.db')
        c = conn.cursor()
        user_id = session.get('user_id', 1)
        c.execute("SELECT username, watch_earnings, referral_earnings FROM users WHERE id = ?", (user_id,))
        user = c.fetchone()
        conn.close()
        if user:
            return render_template('user_dashboard.html', username=user[0], watch_earnings=user[1], referral_earnings=user[2])
        else:
            return render_template('user_dashboard.html')
    except Exception as e:
        return f"Error loading dashboard: {str(e)}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
