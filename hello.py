import os
from sqlalchemy import create_engine, MetaData, Table, Column, ForeignKey
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
	songs.append(instance.title + '\n')

songsStr = ''.join(songs)
print(songsStr)

#print("{}", Song.title_id)
#print("{}", Song.__tablename__)


#from app import models
#db.create_all()

@app.route("/")
def hello():
    #return "Hello World!"
	#return songsStr
	return render_template('hello.html', name = songsStr)

@app.route("/name/<name>")
def get_book_name(name):
    return "name : {}".format(name)

@app.route("/details")
def get_book_details():
    author=request.args.get('author')
    published=request.args.get('published')
    return "Author : {}, Published: {}".format(author,published)

#app.config['DEBUG'] = True
#db.init_app(app)

session.close()
if __name__ == '__main__':
	#redirect('http://web.cecs.pdx.edu/~hadkins/pianorolls/')
	app.run()
