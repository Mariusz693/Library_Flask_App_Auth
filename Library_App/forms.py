from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, DateField, IntegerField, TextAreaField
from wtforms.validators import DataRequired, Regexp, Email, EqualTo, Length, Optional, NumberRange
from .models import Category, UserType, Author, Book, User
from .validators import EqualDateTo, DateRange
from wtforms_sqlalchemy.fields import QuerySelectField
from wtforms_sqlalchemy.fields import QueryCheckboxField


class LoginForm(FlaskForm):
    """User Login Form."""
    email = StringField(
        label='Email: *',
        validators=[
            DataRequired(message='Pole obowiązkowe.'),
            Email(message='Nie poprawny adres email.')
        ]
    )
    password = PasswordField(label='Hasło: *', validators=[DataRequired(message='Pole obowiązkowe.')])
    submit = SubmitField('Zaloguj')


class UserRegisterForm(FlaskForm):
    """User Register Form."""
    first_name = StringField(label='Imię: *', validators=[DataRequired(message='Pole obowiązkowe.')])
    last_name = StringField(label='Nazwisko: *', validators=[DataRequired(message='Pole obowiązkowe.')])
    email = StringField(
        label='Email: *',
        validators=[
            DataRequired(message='Pole obowiązkowe.'),
            Length(min=6, message='Adres email zbyt krótki.'),
            Email(message='Nie poprawny adres email.')
        ]
    )
    phone_number = StringField(
        label='Numer telefonu (+48..):',
        validators=[
            Optional(),
            Length(min=9, max=9, message='Numer telefonu musi być 9 cyfrowy.'),
            Regexp('^[0-9]*$' , message='Numer telefonu musi się składać tylko z cyfr.')
        ]
    )
    password = PasswordField(
        label='Hasło: *',
        validators=[
            DataRequired(message='Pole obowiązkowe.'),
            Length(min=8, message='Wpisz mocniejsze hasło.')
        ]
    )
    repeat_password = PasswordField(
        label='Powtórz hasło: *',
        validators=[
            DataRequired(message='Pole obowiązkowe.'),
            EqualTo('password', message='Hasła muszą być identyczne.')
        ]
    ) 
    submit = SubmitField('Rejestruj')


class UserEditForm(FlaskForm):
    """User Edit Profile Form."""
    first_name = StringField(label='Imię: *', validators=[DataRequired(message='Pole obowiązkowe.')])
    last_name = StringField(label='Nazwisko: *', validators=[DataRequired(message='Pole obowiązkowe.')])
    email = StringField(
        label='Email: *',
        validators=[
            DataRequired(message='Pole obowiązkowe.'),
            Length(min=6, message='Adres email zbyt krótki.'),
            Email(message='Nie poprawny adres email.')
        ]
    )
    phone_number = StringField(
        label='Numer telefonu (+48..):',
        validators=[
            Optional(),
            Length(min=9, max=9, message='Numer telefonu musi być 9 cyfrowy.'),
            Regexp('^[0-9]*$' , message='Numer telefonu musi się składać tylko z cyfr.')
        ]
    )
    submit = SubmitField('Zapisz')


class UserPasswordForm(FlaskForm):
    """User Password Check Form."""
    password = PasswordField(label='Hasło: *', validators=[DataRequired(message='Pole obowiązkowe.')])
    new_password = PasswordField(
        label='Nowe hasło: *',
        validators=[
            DataRequired(message='Pole obowiązkowe.'),
            Length(min=8, message='Wpisz mocniejsze hasło.')
        ]
    )
    new_password_repeat = PasswordField(
        label='Powtórz nowe hasło: *',
        validators=[
            DataRequired(message='Pole obowiązkowe.'),
            EqualTo('new_password', message='Hasła muszą być identyczne.')
        ]
    ) 
    submit = SubmitField('Zapisz')


class UserStatusForm(FlaskForm):

    status = SelectField(
        label='Wybierz status:', 
        choices=[(item.name, item.value) for item in UserType],
        validators=[DataRequired(message='Pole obowiązkowe.')]
    )
    submit = SubmitField('Zapisz')


class AuthorForm(FlaskForm):
    """Author Add or Edit Form."""
    name = StringField(label='Imię i nazwisko (pseudonim): *', validators=[DataRequired(message='Pole obowiązkowe.')])
    date_of_birth = DateField(
        label='Data urodzenia: *',
        validators=[
            DataRequired(message='Pole obowiązkowe.'),
            DateRange(message='Data nie może być datą przyszłą.') 
        ] 
    )
    date_of_death = DateField(
        label='Data śmierci:',
        validators=[
            Optional(), 
            EqualDateTo('date_of_birth', message='Data śmierci nie może być mniejsza niż urodzenia'), 
            DateRange(message='Data nie może być datą przyszłą.') 
        ]
    )
    submit = SubmitField('Zapisz')


class BookForm(FlaskForm):
    """Book Add or Edit Form."""

    def query_choices_authors():

        return Author.query.order_by(Author.name).all()
    
    def query_choices_categories():

        return Category.query.order_by(Category.name).all()
    
    title = StringField('Tytuł: *', validators=[DataRequired(message='Pole obowiązkowe.')])
    isbn = StringField(
        label='Numer ISBN: *', 
        validators=[
            DataRequired(message='Pole obowiązkowe.'),
            Length(min=13, max=13, message='Numer ISBN musi być 13-to cyfrowy'),
            Regexp('^[0-9]*$' , message='Numer ISBN musi się składać tylko z cyfr.')
        ]
    )
    description = TextAreaField(label='Opis:', validators=[Optional()])
    copies = IntegerField(
        label='Egzemplarze: *',
        default=1,
        validators=[
            DataRequired(message='Pole obowiązkowe.'),
            NumberRange(min=1, message='Minimalna ilość egzemplarzy to jeden')
        ]
    )
    author = QuerySelectField(
        label='Autor: *',
        query_factory=query_choices_authors,
        allow_blank=True,
        blank_text='Wybierz',
        validators=[
            DataRequired(message='Pole obowiązkowe.'),
        ]
    )
    categories = QueryCheckboxField(
        label='Wybierz kategorie:',
        query_factory=query_choices_categories,
        validators=[Optional()],
    )
    submit = SubmitField('Zapisz')


class LoanForm(FlaskForm):
    """Loan Book Form."""

    def query_choices_books():

        books = Book.query.order_by(Book.title).all()

        return [book for book in books if book.copies > book.borrowed_copies]
    
    def query_choices_users():

        return User.query.order_by(User.last_name).all()
    
    book = QuerySelectField(
        label='Wybierz książkę: *',
        query_factory=query_choices_books,
        allow_blank=True,
        blank_text='Wybierz',
        validators=[DataRequired(message='Pole obowiązkowe.')]
    )
    user = QuerySelectField(
        label='Wybierz użytkownika: *',
        query_factory=query_choices_users,
        allow_blank=True,
        blank_text='Wybierz',
        validators=[DataRequired(message='Pole obowiązkowe.')]
    )
    submit = SubmitField('Zapisz')
