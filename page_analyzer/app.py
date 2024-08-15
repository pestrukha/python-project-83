import os
from flask import Flask, render_template, request, flash
from dotenv import load_dotenv
from page_analyzer.validator import normalize_url, validate_url


load_dotenv()
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['DATABASE_URL'] = os.getenv('DATABASE_URL')


@app.route('/')
def index():
    return render_template('index.html')


@app.post('/urls')
def add_url():
    get_url = request.form.get('url')
    normal_url = normalize_url(get_url)
    url_error = validate_url(normal_url)

    if url_error:
        flash(url_error, 'danger')
        return render_template('index.html'), 422

    return '1111'
