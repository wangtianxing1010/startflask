# -*- coding: utf-8 -*-

from flask import Flask, render_template, flash, session, url_for, redirect, request, send_file,
					send_from_directory
from content_manager import Content
from wtforms import Form, TextField, PasswordField, BooleanField, validators
from passlib.hash import sha256_crypt
#from mysql.connector import mysql_real_escape_string as thwart

from functools import wraps

from sqlite3_connect import connection
TOPIC_DICT = Content() 

import gc

#import smtplib
from flask_mail import Mail, Message

app = Flask(__name__)
app.config['SECRET_KEY']='secret key'
app.config.update(
					DEBUG = True,
					MAIL_SEVER = 'smtp.gmail.com',
					MAIL_PORT = 465,
					MAIL_USE_SSL = True,
					MAIL_USERNAME= 'tianxing.smartisan@gmail.com',
					MAIL_PASSWORD = 'password')
					
mail= Mail(app)

@app.route('/<path:urlpath>/', methods=['GET','POST'])
@app.route('/')  
def Index(urlpath='/'):
	flash("Welcome my friend","info")
	return render_template('index.html', title = 'Startflask')
	
	
@app.route('/dashboard/')
def Dashboard():
	flash("Welcome to dashboard",'info')
	return render_template('dashboard.html', TOPIC_DICT=TOPIC_DICT, title ='Startflask Dashboard')
	
def logged_in_required(f):
	@wraps(f)
	def wrap(*args, **kwargs):
		#if session['logged_in']:  ??why this is wrong?
		if 'logged_in' in session:
			return f(*args, **kwargs)
		else:
			flash("You need to log in first",'warning')
			return redirect(url_for('Login'))
		
	return wrap

@app.route('/logout/')
@logged_in_required
def Logout():
	session.clear()
	flash("You have logged out",'info')
	gc.collect()
	return redirect(url_for('Index'))

@app.route('/login/', methods=['GET','POST'])
def Login():
	flash("Please Log In","info")
	error = ''
	try:
		form = RegistrationForm(request.form)#request.form?
		c, conn = connection()# watch out for upper and lower case
		if request.method == "POST":
			data = c.execute("SELECT * FROM users WHERE username = (?)",(request.form['username'],) )# inside execute, the variable should be a tuple
			data = c.fetchone()[3] # uid is also count as fetched data
			print data
			if sha256_crypt.verify(request.form['password'],  data):
				session['logged_in'] = True
				session['username'] = request.form['username']
				#session['admin']
				flash('You are logged in','info')
				
				return redirect(url_for('Dashboard'))# watch out for upper and lower case
			else:
				error = 'Invalid credentials, try again'
				
		gc.collect()						
		
		return render_template('login.html', title = 'Login', form = form, error =error) #because using WTForms rather than hard code in html, form has to be passed in
	
	except Exception as e:
		
		return render_template('login.html', title = 'Login', form = form, error =e)

		
		
class RegistrationForm(Form):
	username= TextField('Username',[validators.Length(min=4,max=20)])	
	email= TextField('Email',[validators.Length(min=4,max=20)])	
	password = PasswordField('Password',[validators.Required(),
										validators.EqualTo('confirm',message='not the same')])	
	confirm= PasswordField('Repeat password')
	
	accept_tos = BooleanField('I accept all <a href ="/tos/">terms and conditions</a>',[validators.Required()])
		
		
		
		
@app.route('/register/', methods=['GET','POST'])
def Register():
	flash("Please Log Up","info")
	try: 
		form = RegistrationForm(request.form)
		if request.method =="POST" and form.validate():
			username = form.username.data
			email = form.email.data
			password = sha256_crypt.encrypt(str(form.password.data))
		 	
		 	c, conn = connection()
		 	c.execute('SELECT * FROM users WHERE username = (?)', (username,))# sqlite placeholder is ? rather than %s for MySQLdb
		 	x=c.fetchall()
		 	#x= c.execute('SELECT * FROM users WHERE username = (?)', (username,))

		 	if int(len(x)) >0: #if int(len(x))>0:
		 		flash('username taken') 
				return render_template('register.html', title = 'Register', form=form)
			else:
				c.execute('INSERT INTO users (username, password, email, tracking) VALUES(?,?,?,?)',
							(username, password, email, "/127.0.0.1:5000/"))

				conn.commit()
				flash('Thanks for registering')
				c.close()
				conn.close()
				gc.collect()
				
				session['Logged in'] = True
				session['username'] = username
				
				return redirect(url_for('Dashboard'))
		return render_template('register.html', title = 'Register', form=form)
	except Exception as e:
		return str(e)
				


@app.route('/dangdaishenghuo/')  
def dangdaishenghuo():
	title = '当代生活'
	return render_template('downloads.html', title = title.decode('utf-8')
)

@app.route('/return-file/')  
def return_file():
	return send_file('./static/images/ms-icon-310x310.png', attachment_filename ='ms-icon-310x310.png')
	#./ is a the top working directory

@app.route('/robots.txt/' )
@app.route('/#/')
def On_My_Way():
	flash("Coming Soon!!",'info')
	return render_template('Error.html', title = 'Coming Soon!')
		
#Error Handling	
@app.errorhandler(404)
def Page_Not_Found(e):
	flash(str(e),'danger')
	return render_template('Error.html', title ='404')
	
@app.errorhandler(405)
def Method_Not_Allowed(e):
	flash(str(e),'danger')
	return render_template('Error.html', title ='405')
	
@app.errorhandler(500)
def Internal_Server_Error(e):
	flash(str(e),'danger')
	return render_template('Error.html', title ='500')
if __name__ == '__main__':
	app.run(debug = True)
	