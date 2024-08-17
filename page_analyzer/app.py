import os
from flask import Flask, render_template, request, flash, redirect, url_for
from dotenv import load_dotenv
from page_analyzer.validator import normalize_url, validate_url
from page_analyzer.db import insert_url, get_url_by_id, init_db_pool

load_dotenv()
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['DATABASE_URL'] = os.getenv('DATABASE_URL')

# Инициализируем пул соединений при запуске приложения
init_db_pool(app.config['DATABASE_URL'])

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

    new_id = insert_url(normal_url)
    flash('Страница успешно добавлена', 'success')
    return redirect(url_for('show_url_page', url_id=new_id))


@app.route('/urls/<int:url_id>')
def show_url_page(url_id):
    url = get_url_by_id(url_id)
    if not url:
        flash('URL не найден', 'danger')
        return redirect(url_for('add_url'))
    return render_template('url.html', url=url)
