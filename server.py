from flask import Flask, request, redirect, render_template, session, flash
from mysqlconnection import MySQLConnector
app = Flask(__name__)
app.secret_key = 'sSFdlk224fa'
mysql = MySQLConnector('mydb')
@app.route('/')
def index():
	users = mysql.fetch("SELECT * FROM users")
	return render_template('index.html', users=users)
# This function will take you to the profile of the user
@app.route('/users/show/<user_id>')
def show_user(user_id):
	user = mysql.fetch("SELECT * FROM users WHERE id = '{}'".format(user_id))
	return render_template('profile.html', user=user)
# This function will take you to a page to add a new user
@app.route('/new')
def new_user():
	return render_template('new.html')
# This function will add a new user
@app.route('/create', methods=['POST'])
def create():
	first_name = request.form['first_name']
	last_name = request.form['last_name']
	email = request.form['email']
	query = "INSERT INTO users (first_name, last_name, email, created_at, updated_at) VALUES ('{}', '{}', '{}', NOW(), NOW())".format(first_name, last_name, email)
	mysql.run_mysql_query(query)
	return redirect('/')
# This function will show you the edit user page
@app.route('/users/edit/<user_id>')
def edit_user(user_id):
	user = mysql.fetch("SELECT * FROM users WHERE id = '{}'".format(user_id))
	return render_template('edit.html', user=user)
# This function will update a current user
@app.route('/update/<user_id>', methods=['POST'])
def update(user_id):
	first_name = request.form['first_name']
	last_name = request.form['last_name']
	email = request.form['email']
	query = "UPDATE users SET first_name = '{}', last_name = '{}', email='{}' WHERE id = '{}'".format(first_name, last_name, email, user_id)
	mysql.run_mysql_query(query)
	return redirect('/')
# This function will take you back to the main page
@app.route('/back')
def go_back():
	return redirect('/')
# This function will delete a user
@app.route('/users/delete/<user_id>', methods=['POST'])
def destroy(user_id):
	query = "DELETE FROM users WHERE id = '{}'".format(user_id)
	mysql.run_mysql_query(query)
	return redirect('/')
app.run(debug=True)