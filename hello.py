import os
from sqlalchemy import create_engine, MetaData, Table, Column, ForeignKey, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.automap import automap_base
#from flask_sqlalchemy import SQLAlchemy
from flask import Flask, request, redirect, render_template
#from models import db

app = Flask(__name__)

app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


#from models import Book

#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://hadkins:Louise2007!@pianorolls.cnkqkcboxyt7.us-west-2.rds.amazonaws.com/pianorolls'
#db = SQLAlchemy(app)


Session = sessionmaker()
engine = create_engine("postgresql://hadkins:Louise2007!@pianorolls.cnkqkcboxyt7.us-west-2.rds.amazonaws.com/pianoRolls")
metadata = MetaData()
metadata.reflect(engine)
Base = automap_base(metadata=metadata)
Base.prepare()

Session.configure(bind=engine)
session = Session()

"""
result = engine.execute("select title from songs")
for row in result:
	print("song: ", row['title'])
result.close()
#connection.close()
"""

Songs, Composers, Rolls = Base.classes.songs, Base.classes.composers, Base.classes.rolls

songs = []
for instance in session.query(Songs):
	songs.append(instance.title)

songsStr = ''.join(songs)
print(songsStr)


@app.route("/")
def hello():
	return render_template('hello.html', songs = songsStr)

@app.route("/", methods=["POST"])
def hello_post():
	titleSearch = request.form['title']
	songs = []

	s = text("SELECT songs.title FROM songs WHERE songs.title LIKE :titleSearch")

	query = engine.execute(s, titleSearch='%'+titleSearch+'%').fetchall()

	if(query == None):
		return "No results found for '"+titleSearch+"'"
	else:
		for song in query:
			songs.append(song['title'])

		songsStr = ''.join(songs)
		return songsStr


session.close()
if __name__ == '__main__':
	app.run()
