from flask import Flask, render_template, flash, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime 
import pymysql
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import date
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from webforms import PostForm, UserForm, NamerForm, PasswordForm, LoginForm, SearchForm
from flask_ckeditor import CKEditor



# Creat a Flask Instance
app = Flask(__name__)
# Add CKEditor
ckeditor = CKEditor(app)

# Old sqlite Database
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'

# New mysql Database
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:password123@localhost/our_users'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://coqqjfdwcyocoz:a3ea0cfca2bb17158dd6ec9594c39ccbc13db08533066272ccfc2fc465901080@ec2-23-23-182-238.compute-1.amazonaws.com:5432/dcatnkijnqf67t'
# Secret Key!
app.config['SECRET_KEY'] = "my super secret key"
# intialize The Database
db = SQLAlchemy(app) 
migrate = Migrate(app, db)
author = db.Column(db.String(255))
date_posted = db.Column(db.DateTime, default=datetime.utcnow )
slug = db.Column(db.String(255))



# Create root decorator
@app.route('/admin')
@login_required
def admin():
	id = current_user.id
	if id == 17:
		return render_template('admin.html')
	else:
		flash("You must be Admin to Access Admin Page")
		return redirect(url_for('posts'))



# Pass Stuff To Navbar
@app.context_processor
def base():
	form = SearchForm()
	return dict(form=form)



# Create Search Function
@app.route('/search', methods=["POST"])
def search():
	form = SearchForm()
	posts = Posts.query
	if form.validate_on_submit():
		# Get data from submitted form
		post.searched = form.searched.data
		# Query the Database
		posts = posts.filter(Posts.content.like('%' + post.searched + '%'))
		posts = posts.order_by(Posts.title).all()

		return render_template("search.html",
		 form=form,
		 searched = post.searched,
		 posts = posts)


# Flask login stuff
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
	return Users.query.get(int(user_id)) 




# Create a login Page
@app.route('/login', methods=['GET', 'POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		user = Users.query.filter_by(username=form.username.data).first()
		if user:
			# Check the hash
			if check_password_hash(user.password_hash, form.password.data):
				login_user(user) 
				flash("Login Successful")
				return redirect(url_for('dashboard')) 
			else:
				flash("Wrong Password - Please Try Again")

		else:
			flash("That User Dosen't exist - Please Try Again")
	return render_template('login.html', form=form)

@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
	logout_user()
	flash("You Have Been Logged Out! - Thanks")
	return redirect(url_for('login'))



#Create Dashboard Page
@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
	form = UserForm()
	id = current_user.id
	name_to_update = Users.query.get_or_404(id) 
	if request.method == "POST":
		name_to_update.name = request.form['name']
		name_to_update.email = request.form['email']
		name_to_update.favourite_color = request.form['favourite_color']
		name_to_update.username = request.form['username']
		name_to_update.about_author = request.form['about_author']
		
		try:
			db.session.commit()
			flash("User Update Successfully")
			return render_template('dashboard.html', form=form, name_to_update=name_to_update)
		except: 
			db.session.commit()
			flash("Error, Looks like there was a problem..Try again...")
			return render_template('dashboard.html', form=form, name_to_update=name_to_update)

	else:
		return render_template('dashboard.html', form=form, name_to_update=name_to_update, id=id)

	return render_template('dashboard.html')

# Update database Record
@app.route('/update/<int:id>', methods=['GET', 'POST'])
@login_required
def update(id):
	form = UserForm()
	name_to_update = Users.query.get_or_404(id) 
	if request.method == "POST":
		name_to_update.name = request.form['name']
		name_to_update.email = request.form['email']
		name_to_update.favourite_color = request.form['favourite_color']
		name_to_update.username = request.form['username']
		try:
			db.session.commit()
			flash("User Update Successfully")
			return render_template('update.html', form=form, name_to_update=name_to_update)
		except: 
			db.session.commit()
			flash("Error, Looks like there was a problem..Try again...")
			return render_template('update.html', form=form, name_to_update=name_to_update)

	else:
		return render_template('update.html', form=form, name_to_update=name_to_update, id=id) 

		

# Create a route decorator 



@app.route('/user/add', methods=['GET', 'POST'])
def add_user():
	name = None
	form = UserForm()
	if form.validate_on_submit():
		user = Users.query.filter_by(email=form.email.data).first()
		if user is None:
			# Hash the Password
			hashed_pw = generate_password_hash(form.password_hash.data, "sha256")
			user = Users(username=form.username.data, name=form.name.data, email=form.email.data, favourite_color=form.favourite_color.data, password_hash=hashed_pw) 
			db.session.add(user)
			db.session.commit()
		name=form.name.data
		form.username.data = ''
		form.name.data = ''
		form.email.data = ''
		form.favourite_color.data = ''
		form.password_hash = ''

		flash("User Added Successfully!")
	our_users = Users.query.order_by(Users.date_added)		
	return render_template('add_user.html', form=form, name=name, our_users=our_users) 		





@app.route('/posts/delete/<int:id>')
@login_required
def delete_post(id):
	post_to_delete = Posts.query.get_or_404(id)
	id = current_user.id
	if id == post_to_delete.poster.id:
		try:
			db.session.delete(post_to_delete)
			db.session.commit()

			# Return a message
			flash("Blog Post Was Deleted!")

			# Grab all the posts from the database
			posts = Posts.query.order_by(Posts.date_posted)
			return render_template("posts.html", posts=posts)


		except:
			# Return an error message
			flash("Whoops! There was a problem deleting post, try again...")

			# Grab all the posts from the database
			posts = Posts.query.order_by(Posts.date_posted)
			return render_template("posts.html", posts=posts)
	else:
		# Return a message
		flash("You Aren't Authorized To Delete That Post!")

		# Grab all the posts from the database
		posts = Posts.query.order_by(Posts.date_posted)
		return render_template("posts.html", posts=posts)

@app.route('/posts')
def posts():
	# Grab all the posts from Database
	posts = Posts.query.order_by(-Posts.date_posted)
	return render_template('posts.html', posts=posts)


 # Creat a Post Detaile page
@app.route('/posts/<int:id>')
def post(id):
	post = Posts.query.get_or_404(id)
	return render_template('post.html', post=post)

# Edit Blog Posts
@app.route('/posts/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_post(id):
	post = Posts.query.get_or_404(id)
	form = PostForm()
	if form.validate_on_submit():
		post.title = form.title.data
		#post.author = form.author.data
		post.slug = form.slug.data
		post.content = form.content.data
		
		# update Database
		db.session.add(post)
		db.session.commit() 

		#Return message
		flash("Post Has Been Updated") 
		return redirect(url_for('post', id=post.id)) 

	if post.poster.id == current_user.id: 

		form.title.data = post.title
		#form.author.data = post.author
		form.slug.data = post.slug
		form.content.data = post.content
		return render_template('edit_post.html', form=form)

	else:
		#Return message
		flash("You Can't Edit This Post...") 
		posts = Posts.query.order_by(Posts.date_posted)
		return render_template('posts.html', posts=posts)






# Add Post Page
@app.route('/add-post', methods=['GET', 'POST'])
# @login_required
def add_post():
	form = PostForm()

	if form.validate_on_submit():
		poster = current_user.id
		post = Posts(title=form.title.data, content=form.content.data, poster_id=poster, slug=form.slug.data)

		form.title.data = ''
		form.content.data = ''
		#form.author.data = ''
		form.slug.data = ''

		# Add data Post to Database
		db.session.add(post)
		db.session.commit()
		# Return message
		flash("Blog Post Submitted Successfully")

	# Redirect to the webpage..
	return render_template('add_post.html', form=form)  


# Json Thing
@app.route('/date')
def get_current_date():
	return { "Date": date.today() } 


@app.route('/delete/<int:id>')
def delete(id):
	user_to_delete = Users.query.get_or_404(id)
	name = None
	form = UserForm()

	try: 
		db.session.delete(user_to_delete)
		db.session.commit()
		flash("User Deleted Successfully")
		our_users = Users.query.order_by(Users.date_added)		
		return render_template('add_user.html', form=form, name=name, our_users=our_users) 

	except: 
		flash("Whoops! There was a problem deleting the user, Try again")
		return render_template('add_user.html', form=form, name=name, our_users=our_users) 







# Create Name Pgae
@app.route('/name', methods=['GET', 'POST'])
def name():
	name = None
	form = NamerForm()
	#validate Form
	if form.validate_on_submit():
		name = form.name.data
		form.name.data = ''
		flash("Form Submitted Successfully")


	return render_template('name.html',
			 			   name = name, 
			 			   form = form)

# Create Password Test Pgae
@app.route('/test_pw', methods=['GET', 'POST'])
def test_pw():
	email = None
	password = None
	pw_to_check = None
	passed = None
	form = PasswordForm()

	#validate Form
	if form.validate_on_submit():
		email = form.email.data
		password = form.password_hash.data 

		form.email.data = ''
		form.password_hash.data = ''

		pw_to_check = Users.query.filter_by(email=email).first()

		passed = check_password_hash(pw_to_check.password_hash, password)

		# flash("Form Submitted Successfully")


	return render_template('test_pw.html',
			 			   email = email,
			 			   password = password,
			 			   pw_to_check = pw_to_check, 
			 			   passed = passed,
			 			   form = form)


# Create a Blog Post Model
class Posts(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(255))
	slug = db.Column(db.String(255))
	# author = db.Column(db.String(255))
	content = db.Column(db.Text)
	date_posted = db.Column(db.DateTime, default=datetime.utcnow)
	# Foreign Key To Link Users (refer to primary key of the user)
	poster_id = db.Column(db.Integer, db.ForeignKey('users.id'))



# Create Model
class Users(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(20), nullable=False, unique=True)
	name = db.Column(db.String(200), nullable=False)
	email = db.Column(db.String(120), nullable=False, unique=True)
	favourite_color = db.Column(db.String(120))
	about_author = db.Column(db.Text(), nullable=True) 
	date_added = db.Column(db.DateTime, default=datetime.utcnow) 
	
	
	
	# Do something password Stuff!!!
	password_hash = db.Column(db.String(128))
	# User Can Have Many Posts 
	posts = db.relationship('Posts', backref='poster')



	@property
	def password(self):
		raise AttributeError('password is a not readable attribute!')
		
	@password.setter
	def password(self, password):
		self.password_hash = generate_password_hash(password)

	def verify_password(self, password):
		return check_password_hash(self.password_hash, password)


	
	# Create a String
	def __repr__(self):
		return '<Name %r>' % self.name

# Create root decorator
@app.route('/')
def index():
	return render_template('index.html')


@app.route('/user/<name>')
def user(name):
	return render_template('user.html', user_name=name)

# Create Custom Error Page

# invalid URL

@app.errorhandler(404)
def page_naot_found(e):
	return render_template('404.html'), 404

# internal Server Error

@app.errorhandler(500)
def page_naot_found(e):
	return render_template('500.html'), 500
