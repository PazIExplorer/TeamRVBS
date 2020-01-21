from app import app
from flask import render_template

@app.route('/')
@app.route('/index')
@app.route('/login')
def index():
    return render_template('index.html')
