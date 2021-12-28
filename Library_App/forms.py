from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.fields.choices import SelectField
from wtforms.validators import DataRequired, Regexp, Email, EqualTo, Length
from .models import UserType


class RegisterForm(FlaskForm):
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


class ProfileForm(FlaskForm):
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
            Length(min=9, max=9, message='Numer telefonu musi być 9 cyfrowy.'),
            Regexp('^[0-9]*$' , message='Numer telefonu musi się składać tylko z cyfr.')
        ]
    )
    submit = SubmitField('Zapisz')


class PasswordForm(FlaskForm):
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


class ChangeUser(FlaskForm):

    status = SelectField(
        'Wybierz status użytkownika:', 
        choices=[(item.name, item.value) for item in UserType],
        validators=[DataRequired(message='Pole obowiązkowe.')]
    )
    submit = SubmitField('Zapisz')
