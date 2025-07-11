from flask import Flask, render_template, session, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "secret_key"

@app.route('/')
def home():
  if not 'user' in session:
    return render_template('index.html')
  
  return render_template('dashboard.html', user=session['user'])

@app.route('/dashboard')
def dashboard():
  if not 'user' in session:
    return redirect(url_for('login'))
  return render_template('dashboard.html', user=session['user'])

@app.route('/login', methods=['GET', 'POST'])
def login():
  if 'user' in session:
    return redirect(url_for('home'))
  
  if request.method == 'POST':
    username = request.form['username']
    password = request.form['password']
    datas = open('database/login.txt', 'r').read().split('\n')
  
    for data in datas:
        if username in data:
            real_password = data.split('|')[1]
            if check_password_hash(real_password, password):
              session['user'] = username
              return redirect(url_for('dashboard'))
        flash("Wrong password or username")
        return render_template('login.html')
  
  return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
  if 'user' in session:
    return redirect(url_for('home'))
  
  if request.method == 'POST':
    username = request.form['username']
    password = request.form['password']
    password = generate_password_hash(password)
    
    with open('database/login.txt', 'a') as f:
      f.write(f"{username}|{password}\n")
    
    session['user'] = username
    return redirect(url_for('dashboard'))
  
  return render_template('register.html')

@app.route('/logout')
def logout():
  session.pop('user', None)
  flash("logout success")
  return redirect(url_for('home'))

if __name__ == '__main__':
  app.run(debug=True)