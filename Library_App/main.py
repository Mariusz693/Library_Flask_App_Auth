from flask import Blueprint, render_template, request
from . import db
from .models import Book
main = Blueprint('main', __name__)


@main.route('/')
def index():
    return render_template('index.html')


@main.route('/books/')
def books():
    search = request.args.get('search')
    if search:
        books_list = Book.query.filter(Book.title.ilike(f'{search}%')).all()
    else:
        books_list = Book.query.order_by(Book.title).all()
    
    return render_template(
        'books.html',
        books_list=books_list
        )


@main.route('/authors/')
def authors():
    return 'Authors'


@main.route('/profile/')
def profile():
    return 'Profile XXX'