# -*- coding: utf-8 -*-
import sqlite3 # or import mysql.connector or MySQLdb

'''or def Connection():
		MySQLdb.connect(host='localhost',
							user='root',
							password='ilove773',
							db='startflask')'''
def connection():
	conn = sqlite3.connect('sqlite3_flask.db')		
	c = conn.cursor()
	return c, conn