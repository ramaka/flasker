from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, ValidationError, TextAreaField
from wtforms.validators import DataRequired, EqualTo, Length
from wtforms.widgets import TextArea
from flask_ckeditor import CKEditor
from flask_ckeditor import CKEditorField 



 

# Create A Search Form
class SearchForm(FlaskForm):
	searched = StringField("Searched", validators=[DataRequired()])
	submit = SubmitField("Submit")



# Creat a Posts Forum
class PostForm(FlaskForm):
	title = StringField('Title', validators=[DataRequired()])
	# content = StringField('Content', validators=[DataRequired()], widget=TextArea()) 
	content = CKEditorField('Content', validators=[DataRequired()])
	author = StringField('Author')
	slug = StringField('Slug', validators=[DataRequired()])
	submit = SubmitField('Submit')


# Create a UserForm class
class UserForm(FlaskForm):
	username = StringField("User Name", validators=[DataRequired()])
	name = StringField("Name", validators=[DataRequired()])
	email = StringField("Email", validators=[DataRequired()])
	favourite_color = StringField("Favourite Color")
	about_author = TextAreaField("About Author")
	password_hash = PasswordField('password', validators=[DataRequired(), EqualTo('password_hash2', message='Password Must Match')])
	password_hash2 = PasswordField('Confirm Password', validators=[DataRequired()]) 
	submit = SubmitField("Submit")

# Create a NamerForm class
class NamerForm(FlaskForm):
	name = StringField("What's Your Name?", validators=[DataRequired()])
	submit = SubmitField("Submit")

# Create a PasswordForm class
class PasswordForm(FlaskForm):
	email = StringField("What's Your Email?", validators=[DataRequired()])
	password_hash = PasswordField("What's Your Password?", validators=[DataRequired()])
	submit = SubmitField("Submit")


# Create Login Form
class LoginForm(FlaskForm):
	username = StringField("Username", validators=[DataRequired()])
	password = PasswordField("Password", validators=[DataRequired()])
	submit = SubmitField("Submit")
