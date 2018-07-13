import psycopg2
from flask import *

connection = psycopg2.connect("dbname='intdb' user='postgres' host='localhost' password='cocopine1' port='5432'")
cur = connection.cursor()

#creates table in the database
def create_tables():
	connection = psycopg2.connect("dbname='intdb' user='postgres' host='localhost' password='cocopine1' port='5432'")
	with connection.cursor() as cursor:
	    cursor.execute ("CREATE TABLE IF NOT EXISTS admin (id serial PRIMARY KEY ,username varchar(100) NOT NULL,password varchar(100) NOT NULL)")
	    cursor.execute ("INSERT INTO admin(username,password)VALUES('brian ryb','12345')")
	    cursor.execute ("CREATE TABLE IF NOT EXISTS comments (commentID serial PRIMARY KEY,username varchar(200) NOT NULL,comment text NOT NULL,comment_time timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP)")
	    cursor.execute ("CREATE TABLE IF NOT EXISTS users(id serial PRIMARY KEY, name varchar(100),username varchar(100) NOT NULL,email varchar(100) NOT NULL,password varchar(100) NOT NULL,registration_time timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP)")
	connection.commit()
	connection.close()