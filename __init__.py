from flask import Flask, render_template

app = Flask(__name__)

@app.route('/home')
def dashboard():
    return render_template('home.html')

@app.route('/register')
def dashboard():
    return render_template('register.html')

@app.route('/SignIn')
def dashboard():
    return render_template('Sigin.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/admin')
def dashboard():
    return render_template('admin.html')

if __name__ == '__main__':
    app.run(debug=True)