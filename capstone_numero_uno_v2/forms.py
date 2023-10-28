from flask_wtf import FlaskForm 
from wtforms import StringField, DateField, EmailField, PasswordField
from wtforms.validators import InputRequired, Email, Length 




class CreateUserForm(FlaskForm):
    """ Create User Form """

    username = StringField('Username:', validators = [InputRequired( message = 'Please enter a valid username!'), Length( min = 6, max = 30 )])
    password = PasswordField('Password:', validators = [InputRequired( message = 'Please enter a valid password!'), Length( min = 6, max = 40)])
    email = EmailField('Email:', validators = [InputRequired( message = 'Please enter a valid email!'), Email( message = 'Please enter a valid email address!')])
    dob = DateField('Date of Birth:', validators = [InputRequired( message = 'Please enter a valid date of birth!')])
    picture = StringField('Picture URL:')



class LoginUserForm(FlaskForm):
    """ Login User Form """

    username = StringField('Username:', validators = [InputRequired( message = 'This field is required!'), Length( min = 6, max = 30 )])
    password = PasswordField('Password:', validators = [InputRequired( message = 'This field is required!'), Length( min = 6, max = 40 )])



class EditUserFrom(FlaskForm):
    """ Edit User Form """  

    username = StringField('Username:', validators = [InputRequired( message = 'This field is required!' ), Length( min = 6, max = 30 )])
    email = EmailField('Email:', validators = [InputRequired( message = 'This field is required!'), Email( message = 'Please enter a valid email address!')])
    dob = DateField('Date of Birth:', validators = [InputRequired( message = 'This field is required!')])
    picture = StringField('Picture URL:')



class SearchPagesForm(FlaskForm):
    """ Searches Pages """

    search_term = StringField('Search:', validators = [InputRequired( message = 'Please enter a search term!')])



class AddFavoritePage(FlaskForm):
    """ Favorite Pages """

    favorited_page = StringField('Favorite:')



class LikePage( FlaskForm ):
    """ Likes Pages """

    liked_page = StringField('Liked:')

