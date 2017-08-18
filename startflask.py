# -*- coding: utf-8 -*-

from flask import Flask, render_template, flash


app = Flask(__name__)
app.config['SECRET_KEY']='secret key'


@app.route('/')
def index(methods=['GET','POST']):
	flash("Welcome my friend")
	return render_template('index.html')
	
	
if __name__ == '__main__':
	app.run()
	