from flask import Blueprint, render_template
from . import db

main = Blueprint('main', __name__)


@main.route('/')
def index():
    return render_template('index.html')


@main.route('/books/')
def books():
    return 'Books'


@main.route('/authors/')
def authors():
    return 'Authors'


@main.route('/profile/')
def profile():
    return 'Profile XXX'