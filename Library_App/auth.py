from datetime import datetime
from flask import Blueprint, request, redirect, render_template, url_for, flash
from flask_login import login_user
from .models import db, User
# from . import db
from .forms import RegisterForm

auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    return 'Login'

@auth.route('/register', methods=['GET', 'POST'])
def register():
    
    form = RegisterForm()

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
        
        flash('Użytkownik o podanym adresie email już istnieje w bazie')
            
    return render_template(
        'add_user.html',
        form=form
        )

@auth.route('/logout')
def logout():
    return 'Logout'