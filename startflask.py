# -*- coding: utf-8 -*-

from flask import Flask, render_template, flash
from content_manager import Content

TOPIC_DICT = Content() 

app = Flask(__name__)
app.config['SECRET_KEY']='secret key'


@app.route('/')
def Index(methods=['GET','POST']):
	flash("Welcome my friend")
	return render_template('index.html')
	
	
@app.route('/dashboard/')
def Dashboard(methods=['GET','POST']):
	flash("Welcome to dashboard")
	return render_template('dashboard.html', TOPIC_DICT=TOPIC_DICT)
	
	
#Error Handling	
@app.errorhandler(404)
def Page_Not_Found(e):
	flash("Page not found!!")
	return render_template('404.html')

if __name__ == '__main__':
	app.run(debug = True)
	