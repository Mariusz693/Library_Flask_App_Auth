import json
from flask import Blueprint, render_template, request, flash, redirect, url_for, make_response
from flask_login import login_required, current_user
from datetime import datetime
from .models import db, UserType, Book, Author, User, Books_Users, Category
from .forms import UserStatusForm, AuthorForm, BookForm, LoanForm

main = Blueprint(
    'main', __name__,
    template_folder='templates',
    static_folder='static'
    )


@main.context_processor
def admin_type():
    return dict(admin=UserType.Admin.name, today=datetime.now().date())


@main.route('/')
def index():

    return render_template('index.html')


@main.route('/books')
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
@login_required
def users():
    
    if current_user.status.name != UserType.Admin.name:
    
        return redirect(url_for('main.wrong_access'))

    search = request.args.get('search')
    status = request.args.get('status')
    if search:
        users_list = User.query.filter(User.last_name.ilike(f'{search}%')).filter_by(status=UserType.User.name).all()
    elif status == UserType.Admin.name:
        users_list = User.query.filter_by(status=UserType.Admin.name).order_by(User.last_name).all()
    else:
        users_list = User.query.filter_by(status=UserType.User.name).order_by(User.last_name).all()
    
    return render_template(
        'users.html',
        users_list=users_list
        )


@main.route('/wrong_access')
def wrong_access():
    
    flash('Brak uprawnień administratora aby otworzyć tą stronę.')
    
    return render_template(
        'wrong_access.html',
        )


@main.route('/user_profile/<int:user_id>')
@login_required
def user_profile(user_id):
    
    if current_user.status.name != UserType.Admin.name:
    
        return redirect(url_for('main.wrong_access'))

    user = User.query.get_or_404(user_id)
    actuall_loan = Books_Users.query.filter_by(user=user, return_date=None).order_by(
        Books_Users.loan_date.asc()).all()
    
    return render_template(
        'user_profile.html',
        user=user,
        actuall_loan=actuall_loan
        )


@main.route('/user_status/<int:user_id>', methods=['GET', 'POST'])
@login_required
def user_status(user_id):
    
    if current_user.status.name != UserType.Admin.name:
    
        return redirect(url_for('main.wrong_access'))

    user = User.query.get_or_404(user_id)
    
    if user.status.name == UserType.User.name:
        flash('Zmieniając status użytkownika dodajesz mu wszystkie uprawnienia', 'warning')
    else:
        flash('Zmieniając status użytkownika zabierasz mu wszystkie uprawnienia', 'warning')

    form = UserStatusForm()
    
    if form.validate_on_submit():
        if user.status.name == UserType.Admin.name and User.query.filter_by(status=UserType.Admin.name).count() < 2 and form.status.data == UserType.User.name:
            flash('Jestes jedynym administratorem, udziel komuś uprawnień administratora', 'danger')
        else:
            user.status = form.status.data
            db.session.commit()

            return redirect(url_for('main.user_profile', user_id=user.id))
    
    form.status.default = user.status.name
    form.process()

    return render_template(
        'user_status.html',
        user=user,
        form=form
        )


@main.route('/user_delete/<int:user_id>', methods=['GET', 'POST'])
@login_required
def user_delete(user_id):
    
    if current_user.status.name != UserType.Admin.name:
    
        return redirect(url_for('main.wrong_access'))

    user = User.query.get_or_404(user_id)
    
    if request.method == 'POST':
        if user.status.name == 'Admin' and User.query.filter_by(status=UserType.Admin.name).count() < 2:
            flash('Jestes jedynym administratorem, nie możesz usunąć profilu', 'danger')
        else:
            for loan in user.books:
                if loan.return_date is None:
                    flash('Użytkownik posiada książki na wypożyczeniu, poczekaj na zwrot wszystkich', 'danger')
                    break
            else:
                status = user.status
                db.session.delete(user)
                db.session.commit()
                if status == UserType.Admin:

                    return redirect(url_for('main.users') + '?status=Admin')

                return redirect(url_for('main.users'))
        
    else:
        flash('Usuwając profil użytkownika usuwasz historię jego wypożyczeń', 'warning')

    return render_template(
        'user_remove.html',
        user=user,
        admin=True
        )


@main.route('/author_add', methods=['GET', 'POST'])
@login_required
def author_add():
    
    if current_user.status.name != UserType.Admin.name:
    
        return redirect(url_for('main.wrong_access'))

    form = AuthorForm()
    
    if form.validate_on_submit():

        existing_author = Author.query.filter_by(name=form.name.data).first()
        
        if existing_author:

            flash('Autor istnieje już w bazie danych', 'danger')

        else:
            new_author = Author(
                name=form.name.data,
                date_of_birth=form.date_of_birth.data,
                date_of_death=form.date_of_death.data
            )
            db.session.add(new_author)
            db.session.commit()

            return redirect(url_for('main.authors'))
    
    return render_template(
        'author_form.html',
        form=form
        )


@main.route('/author_edit/<int:author_id>', methods=['GET', 'POST'])
@login_required
def author_edit(author_id):
    
    if current_user.status.name != UserType.Admin.name:
    
        return redirect(url_for('main.wrong_access'))
    
    author = Author.query.get_or_404(author_id)

    form = AuthorForm(obj=author)
    
    if form.validate_on_submit():

        existing_author = Author.query.filter_by(name=form.name.data).first()
        
        if existing_author and existing_author != author:

            flash('Autor istnieje już w bazie danych', 'danger')

        else:
            author.name=form.name.data,
            author.date_of_birth=form.date_of_birth.data,
            author.date_of_death=form.date_of_death.data
            db.session.commit()

            return redirect(url_for('main.author_profile', author_id=author.id))
    
    return render_template(
        'author_form.html',
        form=form,
        author=author
        )


@main.route('/author_profile/<int:author_id>')
def author_profile(author_id):

    author = Author.query.get_or_404(author_id)
    
    return render_template(
        'author_profile.html',
        author=author
        )


@main.route('/author_delete/<int:author_id>', methods=['GET', 'POST'])
@login_required
def author_delete(author_id):

    if current_user.status.name != UserType.Admin.name:
    
        return redirect(url_for('main.wrong_access'))
    
    author = Author.query.get_or_404(author_id)

    if request.method == 'POST':
        for book in author.books:
            if book.borrowed_copies > 0:
                flash('Książki autora na wypożyczeniu, poczekaj na zwrot wszystkich', 'danger')
                break
        else:
            db.session.delete(author)
            db.session.commit()

            return redirect(url_for('main.authors'))
            
    else:
        flash('Usuwając profil autora usuwasz wszystkie jego książki', 'warning')

    return render_template(
        'author_delete.html',
        author=author
        )


@main.route('/book_add', methods=['GET', 'POST'])
@login_required
def book_add():
    
    if current_user.status.name != UserType.Admin.name:
    
        return redirect(url_for('main.wrong_access'))

    form = BookForm()
    
    if form.validate_on_submit():
        existing_isbn = Book.query.filter_by(isbn=form.isbn.data).first()
        
        if existing_isbn:
            flash('Numer ISBN istnieje już w bazie danych', 'danger')
            
        else:
            if form.author.data or (form.name.data and form.date_of_birth.data):
                existing_author = Author.query.filter_by(name=form.name.data).first()
                if existing_author:
                    flash('Autor istnieje już w bazie danych, wybierz z listy', 'warning')
                else:
                    if form.author.data:
                        author = form.author.data
                    else:
                        author = Author(
                            name=form.name.data,
                            date_of_birth=form.date_of_birth.data,
                            date_of_death=form.date_of_death.data
                        )   
                        db.session.add(author)
                    
                    new_book = Book(
                        isbn=form.isbn.data, 
                        title=form.title.data,
                        description=form.description.data,
                        copies=form.copies.data,
                        author=author
                        )
                    new_book.categories.extend(form.categories.data)
                    db.session.add(new_book)
                    db.session.commit()

                    return redirect(url_for('main.books'))

            else:
                flash('Wybierz lub dodaj poprawnie nowego autora', 'danger')
    
    return render_template(
        'book_form.html',
        form=form,
        )


@main.route('/book_edit/<int:book_id>', methods=['GET', 'POST'])
@login_required
def book_edit(book_id):
    
    if current_user.status.name != UserType.Admin.name:
    
        return redirect(url_for('main.wrong_access'))

    book = Book.query.get_or_404(book_id)

    form = BookForm(obj=book)
    
    if form.validate_on_submit():    
        existing_isbn = Book.query.filter_by(isbn=form.isbn.data).first()
        
        if existing_isbn and existing_isbn != book:
            flash('Numer ISBN istnieje już w bazie danych', 'danger')

        elif form.copies.data < book.borrowed_copies:
            flash(f'Ilość egzemplarzy na wypożyczeniu większa niż podana - {book.borrowed_copies}', 'danger')
        
        else:
            if form.author.data or (form.name.data and form.date_of_birth.data):
                existing_author = Author.query.filter_by(name=form.name.data).first()
                if existing_author:
                    flash('Autor istnieje już w bazie danych, wybierz z listy', 'warning')
                else:
                    if form.author.data:
                        author = form.author.data
                    else:
                        author = Author(
                            name=form.name.data,
                            date_of_birth=form.date_of_birth.data,
                            date_of_death=form.date_of_death.data
                        )   
                        db.session.add(author)
                    
                    book.isbn=form.isbn.data, 
                    book.title=form.title.data,
                    book.description=form.description.data,
                    book.copies=form.copies.data,
                    book.author=author
                    book.categories.extend(form.categories.data)
                    db.session.commit()

                    return redirect(url_for('main.book_profile', book_id=book.id))

            else:
                flash('Wybierz lub dodaj poprawnie nowego autora', 'danger')
    
    return render_template(
        'book_form.html',
        form=form,
        book=book
        )


@main.route('/book_profile/<int:book_id>')
def book_profile(book_id):

    book = Book.query.get_or_404(book_id)
    
    return render_template(
        'book_profile.html',
        book=book
        )


@main.route('/book_delete/<int:book_id>', methods=['GET', 'POST'])
@login_required
def book_delete(book_id):

    if current_user.status.name != UserType.Admin.name:
    
        return redirect(url_for('main.wrong_access'))
    
    book = Book.query.get_or_404(book_id)

    if request.method == 'POST':
        if book.borrowed_copies > 0:
            flash('Książki na wypożyczeniu, poczekaj na zwrot wszystkich', 'danger')
        else:
            db.session.delete(book)
            db.session.commit()

            return redirect(url_for('main.authors'))
            
    else:
        flash('Usuwając profil książki usuwasz historię wypożyczeń', 'warning')

    return render_template(
        'book_delete.html',
        book=book
        )


@main.route('/loan_add', methods=['GET', 'POST'])
@login_required
def loan_add():
    
    if current_user.status.name != UserType.Admin.name:
    
        return redirect(url_for('main.wrong_access'))

    form = LoanForm()
    today_date = datetime.now().date()
    
    if form.validate_on_submit():
        book = form.book.data
        user = form.user.data
        existing_loan = Books_Users.query.filter_by(book=book).filter_by(user=user).filter_by(return_date=None).first()
        if existing_loan:
            flash('Użytkownik ma aktulanie tą książkę na wypożyczeniu', 'danger')

        else:
            new_loan = Books_Users(
                book=book,
                user=user,
                loan_date=today_date
            )
            db.session.add(new_loan)
            book.borrowed_copies += 1
            db.session.commit()
            flash(f'Dodano wypożyczenie książki "{book}" - {user}', 'success')
    
    return render_template(
        'loan_form.html',
        form=form,
        today_date=today_date
        )


@main.route('/loan_user/<int:user_id>', methods=['GET', 'POST'])
@login_required
def loan_user(user_id):
    
    if current_user.status.name != UserType.Admin.name:
    
        return redirect(url_for('main.wrong_access'))

    user = User.query.get_or_404(user_id)
    loaned = request.args.get('loaned')
    loan_list = Books_Users.query.filter_by(user=user).order_by(
        Books_Users.return_date.desc(), Books_Users.loan_date.desc()).all()
    
    if loaned == 'True':
        loan_list = [item for item in loan_list if item.return_date == None]
        flash('Aktualnie wypożyczone książki', 'success')
    
    if request.method == 'POST':
        data = request.get_json(force=True)
        loan = Books_Users.query.get_or_404(data['loan'])
        loan.return_date = datetime.now().date()
        loan.book.borrowed_copies -= 1
        db.session.commit()
        flash(f'Zapisano zwrot książki - {loan.user}', 'success')

        return make_response({}, 200)

    if request.method == 'DELETE':
        data = request.get_json(force=True)
        loan = Books_Users.query.get_or_404(data['loan'])
        db.session.delete(loan)
        db.session.commit()
        flash(f'Usunięto z historii wybraną pozycję - {loan.user}', 'success')

        return make_response({}, 200)
    
    return render_template(
        'loan_user.html',
        user=user,
        loan_list=loan_list,
        )


@main.route('/loan_book/<int:book_id>', methods=['GET', 'POST', 'DELETE'])
@login_required
def loan_book(book_id):
    
    if current_user.status.name != UserType.Admin.name:
    
        return redirect(url_for('main.wrong_access'))

    book = Book.query.get_or_404(book_id)
    loaned = request.args.get('loaned')
    loan_list = Books_Users.query.filter_by(book=book).order_by(
        Books_Users.return_date.desc(), Books_Users.loan_date.desc()).all()
    
    if loaned == 'True':
        loan_list = [item for item in loan_list if item.return_date == None]
        flash('Aktualnie wypożyczone książki', 'success')

    if request.method == 'POST':
        data = request.get_json(force=True)
        loan = Books_Users.query.get_or_404(data['loan'])
        loan.return_date = datetime.now().date()
        loan.book.borrowed_copies -= 1
        db.session.commit()
        flash(f'Zapisano zwrot książki - {loan.user}', 'success')

        return make_response({}, 200)

    if request.method == 'DELETE':
        data = request.get_json(force=True)
        loan = Books_Users.query.get_or_404(data['loan'])
        db.session.delete(loan)
        db.session.commit()
        flash(f'Usunięto z historii wybraną pozycję - {loan.user}', 'success')

        return make_response({}, 200)
    
    return render_template(
        'loan_book.html',
        book=book,
        loan_list=loan_list,
        )


@main.route("/categories", methods=['GET', 'POST', 'DELETE'])
@login_required
def categories():
    
    if current_user.status.name != UserType.Admin.name:
    
        return redirect(url_for('main.wrong_access'))

    categories = Category.query.order_by(Category.name).all()
    
    if request.method == 'POST':
        data = request.get_json(force=True)
        existing_category = Category.query.filter_by(name=data['name']).first()
                    
        if existing_category:

            return make_response({}, 409)
        
        else:
            new_category = Category(name=data['name'])
            db.session.add(new_category)
            db.session.commit()    
            flash(f'Dodano kategorię - {new_category}', 'success')

            return make_response({}, 200)

    if request.method == 'DELETE':
        data = request.get_json(force=True)
        category = Category.query.get_or_404(data['category'])
        db.session.delete(category)
        db.session.commit()
        flash(f'Usunięto kategorię - {category}', 'success')

        return make_response({}, 200)

    return render_template(
        'categories.html',
        categories=categories
        )
