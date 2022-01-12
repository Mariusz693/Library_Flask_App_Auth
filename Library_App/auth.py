from datetime import datetime
from flask import Blueprint, request, redirect, render_template, url_for, flash
from flask_login import login_user, current_user, logout_user, login_required
from .models import db, User, UserType, Books_Users
from .forms import LoginForm, UserRegisterForm, UserEditForm, UserPasswordForm
from . import login_manager

auth = Blueprint(
    'auth', __name__,
    template_folder='templates',
    static_folder='static'
    )


@auth.context_processor
def admin_type():
    return dict(admin=UserType.Admin.name)


@auth.route('/login', methods=['GET', 'POST'])
def login():

    if current_user.is_authenticated:
        
        return redirect(url_for('main.index'))

    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(password=form.password.data):
            login_user(user)
            user.last_login = datetime.now()
            db.session.commit()
            next_page = request.args.get('next')

            return redirect(next_page or url_for('main.index'))
        
        elif user:
            flash('Błąd logowania, błędnie podane hasło.')
        else:
            flash('Błąd logowania, brak użytkownika o podanym adresie email.')

    return render_template(
        'login.html',
        form=form
    )


@auth.route('/logout')
def logout():

    logout_user()

    return redirect(url_for('main.index'))


@auth.route('/register', methods=['GET', 'POST'])
def register():
    
    form = UserRegisterForm()

    if form.validate_on_submit():
        existing_user = User.query.filter_by(email=form.email.data).first()
        if existing_user is None:
            user = User(
                first_name=form.first_name.data,
                last_name=form.last_name.data,
                email=form.email.data,
                phone_number=form.phone_number.data,
                created_on=datetime.now()
            )
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
            login_user(user)
            user.last_login = datetime.now()
            db.session.commit()

            return redirect(url_for('main.index'))
        
        flash('Użytkownik o podanym adresie email już istnieje w bazie.')
            
    return render_template(
        'user_register.html',
        form=form
        )


@auth.route('/profile')
@login_required
def profile():
    
    actuall_loan = Books_Users.query.filter_by(user=current_user, return_date=None).order_by(
        Books_Users.loan_date.asc()).all()
    
    return render_template(
        'user_profile_logged.html',
        actuall_loan=actuall_loan
        )


@auth.route('/user_edit', methods=['GET', 'POST'])
@login_required
def user_edit():
    
    form = UserEditForm(obj=current_user)

    if form.validate_on_submit():
        existing_user = User.query.filter_by(email=form.email.data).first()
        
        if existing_user == current_user or existing_user is None:
            current_user.first_name = form.first_name.data
            current_user.last_name = form.last_name.data
            current_user.email = form.email.data
            current_user.phone_number = form.phone_number.data
            db.session.commit()

            return redirect(url_for('auth.profile'))

        flash('Użytkownik o podanym adresie email już istnieje w bazie.')
            
    return render_template(
        'user_edit.html',
        form=form
        )


@auth.route('/user_password', methods=['GET', 'POST'])
@login_required
def user_password():
    
    form = UserPasswordForm()

    if form.validate_on_submit():
        if current_user.check_password(password=form.password.data):
            current_user.set_password(form.new_password.data)
            db.session.commit()
            logout_user()

            return redirect(url_for('auth.login'))
        
        flash('Błądne hasło, wpisz poprawnie stare hasło.')

    return render_template(
        'user_password.html',
        form=form
        )


@auth.route('/user_remove', methods=['GET', 'POST'])
@login_required
def user_remove():

    if request.method == 'POST':
        if current_user.status.name == 'Admin' and User.query.filter_by(status=UserType.Admin.name).count() < 2:    
            flash('Jestes jedynym administratorem, nie możesz usunąć profilu', 'danger')
        
        else:
            for loan in current_user.books:
                if loan.return_date is None:
                    flash('Posiadasz książki na wypożyczeniu, zwróć wszystkie', 'danger')
                    break
            else:
                db.session.delete(current_user)
                db.session.commit()

                return redirect(url_for('main.index'))
        
    else:
        flash('Usuwając profil usuwasz historię wypożyczeń', 'warning')

    return render_template(
        'user_remove.html',
        user=current_user,
        )


@auth.route('/loan_user_logged')
@login_required
def loan_user_logged():
    
    loaned = request.args.get('loaned')
    loan_list = Books_Users.query.filter_by(user=current_user).order_by(
        Books_Users.return_date.desc(), Books_Users.loan_date.desc()).all()
    
    if loaned == 'True':
        loan_list = [item for item in loan_list if item.return_date == None]
        flash('Aktualnie wypożyczone książki', 'success')
    
    return render_template(
        'loan_user_logged.html',
        loan_list=loan_list,
        )


@login_manager.user_loader
def load_user(user_id):
    """Check if user is logged-in on every page load."""
    if user_id is not None:
        return User.query.get(user_id)
    return None


@login_manager.unauthorized_handler
def unauthorized():
    """Redirect unauthorized users to Login page."""
    flash('Musisz być zalogowany aby otworzyć tą stronę.')
    
    return redirect(url_for('auth.login') + f"?next={request.path}")