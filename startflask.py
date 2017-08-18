# -*- coding: utf-8 -*-

from flask import Flask, render_template,flash


app = Flask(__name__)
app.config['SECRET_KEY']='secret key'



app = Flask(__name__)

@app.route('/')
def index():
	flash( "")
	return render_template('index.html')
	
	
if __name__ == '__main__':
	app.run()
	