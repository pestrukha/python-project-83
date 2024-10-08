import os
import requests
from flask import Flask, render_template, request, flash, redirect, url_for
from dotenv import load_dotenv
from page_analyzer.validator import normalize_url, validate_url
from page_analyzer.html_parser import parse_html
from page_analyzer.db import (
    init_db_pool,
    insert_url,
    insert_check,
    get_checks,
    get_checked_urls,
    get_url_by_name,
    get_url_by_id
)


load_dotenv()
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['DATABASE_URL'] = os.getenv('DATABASE_URL')

init_db_pool(app.config['DATABASE_URL'])


@app.errorhandler(404)
def page_not_found(e):
    return render_template('errors/404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('errors/500.html'), 500


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

    if get_url_by_name(normal_url):
        old_url = get_url_by_name(normal_url)
        flash('Страница уже существует', 'primary')
        return redirect(url_for('show_url_page', url_id=old_url['id']))

    new_id = insert_url(normal_url)
    flash('Страница успешно добавлена', 'success')
    return redirect(url_for('show_url_page', url_id=new_id))


@app.route('/urls/<int:url_id>')
def show_url_page(url_id):
    url = get_url_by_id(url_id)
    all_checks = get_checks(url_id)
    if not url:
        flash('URL не найден', 'danger')
        return redirect(url_for('add_url'))
    return render_template(
        'url.html',
        url_data=url,
        all_checks=all_checks
    )


@app.get('/urls')
def show_all_urls():
    checked_urls = get_checked_urls()
    return render_template(
        'urls.html',
        checked_urls=checked_urls
    )


@app.post('/urls/<id>/checks')
def check_url(id):
    url = get_url_by_id(id)

    try:
        response = requests.get(url['name'])
        response.raise_for_status()

    except requests.exceptions.RequestException:
        flash('Произошла ошибка при проверке', 'danger')
        return redirect(url_for('show_url_page', url_id=id))

    status_code = response.status_code
    h1, title, description = parse_html(response.text)
    insert_check(id, status_code, h1, title, description)
    flash('Страница успешно проверена', 'success')
    return redirect(url_for('show_url_page', url_id=id))
