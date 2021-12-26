from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from .models import db, Book, Author, User, Books_Users


main = Blueprint(
    'main', __name__,
    template_folder='templates',
    static_folder='static'
    )


@main.route('/')
def index():

    return render_template('index.html')


@main.route('/books')
# @login_required
def books():

    # if not current_user.is_authenticated:
    #     flash('Musisz być zalogowany aby otworzyć tą stronę.')
    #     return redirect(url_for('auth.login') + f"?next={request.path}")

    search = request.args.get('search')
    if search:
        books_list = Book.query.filter(Book.title.ilike(f'{search}%')).all()
    else:
        books_list = Book.query.order_by(Book.title).all()
    
    return render_template(
        'books.html',
        books_list=books_list
        )


@main.route('/authors')
def authors():
    
    search = request.args.get('search')
    if search:
        authors_list = Author.query.filter(Author.name.ilike(f'{search}%')).all()
    else:
        authors_list = Author.query.order_by(Author.name).all()
    
    return render_template(
        'authors.html',
        authors_list=authors_list
        )


@main.route('/users')
def users():
    
    search = request.args.get('search')
    if search:
        users_list = User.query.filter(User.name.ilike(f'{search}%')).all()
    else:
        users_list = User.query.order_by(User.name).all()
    
    return render_template(
        'users.html',
        users_list=users_list
        )


@main.route('/profile')
@login_required
def profile():
    
    actuall_loan = Books_Users.query.filter_by(user=current_user, return_date=None).order_by(
        Books_Users.loan_date.asc()).all()
    
    return render_template(
        'profile.html',
        user=current_user,
        actuall_loan=actuall_loan
        )


@main.route('/delete_user/<int:user_id>')
@login_required
def delete_user(user_id):
    # user = User.query.get_or_404(current_user.id)
    # actuall_loan = Books_Users.query.filter_by(user=user, return_date=None).order_by(Books_Users.loan_date.asc()).all()
    
    # return render_template(
    #     'profile.html',
    #     user=user,
    #     actuall_loan=actuall_loan
    #     )
    return render_template('index.html')



@main.route('/user_loan/<int:user_id>')
@login_required
def user_loan(user_id):
    # user = User.query.get_or_404(current_user.id)
    # actuall_loan = Books_Users.query.filter_by(user=user, return_date=None).order_by(Books_Users.loan_date.asc()).all()
    
    # return render_template(
    #     'profile.html',
    #     user=user,
    #     actuall_loan=actuall_loan
    #     )
    return render_template('index.html')