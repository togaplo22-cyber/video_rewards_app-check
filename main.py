
from flask import Flask, render_template, request, redirect, session
app = Flask(__name__)
app.secret_key = 'supersecretkey'

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    password = request.form.get('password')
    if password == 'Password1515':
        return redirect('/admin')
    session['user'] = request.form.get('username')
    return redirect('/dashboard')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/admin')
def admin():
    return render_template('admin.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/cashout')
def cashout():
    return render_template('cashout.html')

if __name__ == '__main__':
    app.run(debug=True)
