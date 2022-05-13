from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound

simple_pages = Blueprint('simple_pages', __name__,
                         template_folder='templates')


def page_not_found(e):
    return render_template("404.html"), 404


@simple_pages.route('/')
def index():
    try:
        return render_template('index.html')
    except TemplateNotFound:
        abort(404)


@simple_pages.route('/about')
def about():
    try:
        return render_template('about.html')
    except TemplateNotFound:
        abort(404)
