from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Regexp, Email, EqualTo, Length


class RegisterForm(FlaskForm):
    """User Register Form."""
    first_name = StringField('Imię *', validators=[DataRequired(message='Pole obowiązkowe')])
    last_name = StringField('Nazwisko *', validators=[DataRequired(message='Pole obowiązkowe')])
    email = StringField(
        'Email *',
        validators=[
            DataRequired(message='Pole obowiązkowe'),
            Length(min=6, message='Adres email zbyt krótki'),
            Email(message='Nie poprawny adres email')
        ]
    )
    phone_number = StringField(
        'Numer telefonu (+48..)',
        validators=[
            Length(min=9, max=9, message='Numer telefonu musi być 9 cyfrowy'),
            Regexp('^[0-9]*$' , message='Numer telefonu musi się składać tylko z cyfr')
        ]
    )
    password = PasswordField(
        'Hasło *',
        validators=[
            DataRequired(message='Pole obowiązkowe'),
            Length(min=8, message='Wpisz mocniejsze hasło.')
        ]
    )
    repeat_password = PasswordField(
        'Powtórz hasło *',
        validators=[
            DataRequired(message='Pole obowiązkowe'),
            EqualTo('password', message='Hasła muszą być identyczne.')
        ]
    ) 
    submit = SubmitField('Rejestruj')


class LoginForm(FlaskForm):
    """User Login Form."""
    email = StringField(
        'Email *',
        validators=[
            DataRequired(message='Pole obowiązkowe'),
            Email(message='Nie poprawny adres email')
        ]
    )
    password = PasswordField('Hasło *', validators=[DataRequired(message='Pole obowiązkowe')])
    submit = SubmitField('Zaloguj')