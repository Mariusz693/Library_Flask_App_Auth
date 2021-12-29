from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from .models import UserType, db, Book, Author, User, Books_Users
from .forms import UserStatusForm, AuthorForm

main = Blueprint(
    'main', __name__,
    template_folder='templates',
    static_folder='static'
    )


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
def users():
    
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
        actuall_loan=actuall_loan,
        admin=True
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

        elif form.date_of_death.data and form.date_of_death.data < form.date_of_birth.data:
        
            flash('Data urodzenia autora nie może być większa od daty śmierci', 'danger')

        else:
            new_author = Author(
                name=form.name.data,
                date_of_birth=form.date_of_birth.data,
                date_of_death=form.date_of_death.data
            )
            db.session.add(new_author)
            db.session.commit()

            flash('Dodano wpis nowego autora', 'success')
    
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

        elif form.date_of_death.data and form.date_of_death.data < form.date_of_birth.data:
        
            flash('Data urodzenia autora nie może być większa od daty śmierci', 'danger')

        else:
            author.name=form.name.data,
            author.date_of_birth=form.date_of_birth.data,
            author.date_of_death=form.date_of_death.data
            db.session.commit()

            flash('Zmieniono wpis autora', 'success')
    
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
