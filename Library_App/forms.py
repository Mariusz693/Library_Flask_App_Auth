from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.fields.choices import SelectField
from wtforms.fields.datetime import DateField
from wtforms.validators import DataRequired, Regexp, Email, EqualTo, Length, ValidationError, Optional
from .models import UserType
from datetime import datetime


class LoginForm(FlaskForm):
    """User Login Form."""
    email = StringField(
        'Email: *',
        validators=[
            DataRequired(message='Pole obowiązkowe.'),
            Email(message='Nie poprawny adres email.')
        ]
    )
    password = PasswordField('Hasło: *', validators=[DataRequired(message='Pole obowiązkowe.')])
    submit = SubmitField('Zaloguj')


class UserRegisterForm(FlaskForm):
    """User Register Form."""
    first_name = StringField('Imię: *', validators=[DataRequired(message='Pole obowiązkowe.')])
    last_name = StringField('Nazwisko: *', validators=[DataRequired(message='Pole obowiązkowe.')])
    email = StringField(
        'Email: *',
        validators=[
            DataRequired(message='Pole obowiązkowe.'),
            Length(min=6, message='Adres email zbyt krótki.'),
            Email(message='Nie poprawny adres email.')
        ]
    )
    phone_number = StringField(
        'Numer telefonu (+48..):',
        validators=[
            Optional(),
            Length(min=9, max=9, message='Numer telefonu musi być 9 cyfrowy.'),
            Regexp('^[0-9]*$' , message='Numer telefonu musi się składać tylko z cyfr.')
        ]
    )
    password = PasswordField(
        'Hasło: *',
        validators=[
            DataRequired(message='Pole obowiązkowe.'),
            Length(min=8, message='Wpisz mocniejsze hasło.')
        ]
    )
    repeat_password = PasswordField(
        'Powtórz hasło: *',
        validators=[
            DataRequired(message='Pole obowiązkowe.'),
            EqualTo('password', message='Hasła muszą być identyczne.')
        ]
    ) 
    submit = SubmitField('Rejestruj')


class UserEditForm(FlaskForm):
    """User Edit Profile Form."""
    first_name = StringField('Imię: *', validators=[DataRequired(message='Pole obowiązkowe.')])
    last_name = StringField('Nazwisko: *', validators=[DataRequired(message='Pole obowiązkowe.')])
    email = StringField(
        'Email: *',
        validators=[
            DataRequired(message='Pole obowiązkowe.'),
            Length(min=6, message='Adres email zbyt krótki.'),
            Email(message='Nie poprawny adres email.')
        ]
    )
    phone_number = StringField(
        'Numer telefonu (+48..):',
        validators=[
            Optional(),
            Length(min=9, max=9, message='Numer telefonu musi być 9 cyfrowy.'),
            Regexp('^[0-9]*$' , message='Numer telefonu musi się składać tylko z cyfr.')
        ]
    )
    submit = SubmitField('Zapisz')


class UserPasswordForm(FlaskForm):
    """User Password Check Form."""
    password = PasswordField('Hasło: *', validators=[DataRequired(message='Pole obowiązkowe.')])
    new_password = PasswordField(
        'Nowe hasło: *',
        validators=[
            DataRequired(message='Pole obowiązkowe.'),
            Length(min=8, message='Wpisz mocniejsze hasło.')
        ]
    )
    repeat_new_password = PasswordField(
        'Powtórz nowe hasło: *',
        validators=[
            DataRequired(message='Pole obowiązkowe.'),
            EqualTo('new_password', message='Hasła muszą być identyczne.')
        ]
    ) 
    submit = SubmitField('Zapisz')


class UserStatusForm(FlaskForm):

    status = SelectField(
        'Wybierz status użytkownika:', 
        choices=[(item.name, item.value) for item in UserType],
        validators=[DataRequired(message='Pole obowiązkowe.')]
    )
    submit = SubmitField('Zapisz')


def my_data_check(form, field):
    today = datetime.now().date()
    if field.data > today:
        raise ValidationError('Podano datę przyszłą.')



class AuthorForm(FlaskForm):
    """Author Add or Edit Form."""
    name = StringField('Imię i nazwisko (pseudonim): *', validators=[DataRequired(message='Pole obowiązkowe.')])
    date_of_birth = DateField(
        'Data urodzenia: *',
        validators=[DataRequired(message='Pole obowiązkowe.'), my_data_check] 
    )
    date_of_death = DateField(
        'Data śmierci:',
        validators=[Optional(), my_data_check]
    ) 
    submit = SubmitField('Zapisz')
