import os
from sqlalchemy import create_engine, MetaData, Table, Column, ForeignKey, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.automap import automap_base
from flask import Flask, request, redirect, render_template, Markup

app = Flask(__name__)

app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


Session = sessionmaker()
engine = create_engine("postgresql://hadkins:Louise2007!@pianorolls.cnkqkcboxyt7.us-west-2.rds.amazonaws.com/pianoRolls")
metadata = MetaData()
metadata.reflect(engine)
Base = automap_base(metadata=metadata)
Base.prepare()

Session.configure(bind=engine)
session = Session()


Songs, Composers, Rolls = Base.classes.songs, Base.classes.composers, Base.classes.rolls

@app.route("/")
def hello():
	return render_template('hello.html')

@app.route("/", methods=["POST"])
def hello_post():
	titleSearch = request.form['title'].lower()
	songs = []

	s = text("SELECT songs.title FROM songs WHERE LOWER(songs.title) LIKE :titleSearch")

	query = engine.execute(s, titleSearch='%'+titleSearch+'%').fetchall()

	if(query == None):
		return "No results found for '"+titleSearch+"'"
	else:
		for song in query:
			songs.append(song['title'] + '<br>')

		songsStr = ''.join(songs)
		return Markup('<strong> '+songsStr +'</strong>')


session.close()
if __name__ == '__main__':
	app.run()
