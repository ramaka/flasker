from flask import Flask, render_template

# Create a Flask instance

# FILTERS
# safe
# capitalize
# lower
# upper
# title
# trim
# striptags


app = Flask(__name__)

# Create a route decorattor

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

