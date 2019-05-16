import os
from sqlalchemy import create_engine, MetaData, Table, Column, ForeignKey, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.automap import automap_base
from flask import Flask, request, redirect, render_template, Markup

app = Flask(__name__)

#app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

Session = sessionmaker()
engine = create_engine("postgresql://hadkins:Louise2007!@pianorolls.cnkqkcboxyt7.us-west-2.rds.amazonaws.com/pianoRolls")
metadata = MetaData()
metadata.reflect(engine)
Base = automap_base(metadata=metadata)
Base.prepare()

Session.configure(bind=engine)
session = Session()


@app.route("/")
def hello():
        return render_template('hello.html')

@app.route("/search_results", methods=["POST"])
def search_results():

	songs = []
	composers = []
	performers = []
	mfgrs = []
	rollNrs = []
	nrCopies = []
	titleSearch = ""
	titleQuery = ""
	composerSearch = ""
	composerQuery = ""
	performerSearch = ""
	performerQuery = ""
	mfgrSearch = ""
	mfgrQuery = ""
	rollNrSearch = ""
	rollNrQuery = ""

	allResults = []
	"""
	s = text("SELECT songs.title FROM songs WHERE LOWER(songs.title) LIKE :titleSearch")
	c = text("SELECT composers.composer_name FROM composers WHERE LOWER(composers.composer_name) LIKE :composerSearch")
	p = text("SELECT artists.name FROM artists WHERE LOWER(artists.name) LIKE :performerSearch")
	m = text("SELECT manufacturer.name FROM manufacturer WHERE LOWER(manufacturer.name LIKE :mfgrSearch")
	rn = text("SELECT rolls.rollnr FROM rolls WHERE LOWER(rolls.rollNr LIKE :rollNrSearch")
	nc = text("SELECT rolls.nrcopies FROM rolls WHERE LOWER(rolls.nrCopies) LIKE: nrCopiesSearch")
	"""
	titleRequest = request.form['title']
	compRequest = request.form['composer']
	performRequest = request.form['performer']
	mfgrRequest = request.form['mfgr']
	rollNrRequest = request.form['rollNr']
	nrCopiesRequest = request.form['nrCopies']

	if(titleRequest and compRequest and performRequest and rollNrRequest and nrCopiesRequest):

		titleSearch = titleRequest.lower()
#		titleQuery = engine.execute(s, titleSearch='%'+titleSearch+'%').fetchall()

		composerSearch = compRequest.lower()
#		composerQuery = engine.execute(c, composerSearch='%'+composerSearch+'%').fetchall()

		performerSearch = performRequest.lower()
#		performerQuery = engine.execute(p, performerSearch='%'+performerSearch+'%').fetchall()

		#mfgrSearch = mfgrRequest.lower()
#		mfgrQuery = engine.execute(m, mfgrSearch='%'+mfgrSearch+'%').fetchall()

		rollNrSearch = rollNrRequest.lower()
		#rollNrQuery = engine.execute(rn, rollNrSearch='%'+rollNrSearch+'%').fetchall()

		nrCopiesSearch = nrCopiesRequest.lower()
		#nrCopiesQuery = engine.execute(nc, nrCopiesSearch='%'+nrCopiesSearch+'%').fetchall()
		
		query = text("SELECT songs.title, composers.composer_name," +
			" artists.name, rolls.rollnr, rolls.num_copies FROM composers" + 
			" NATURAL JOIN artists NATURAL JOIN rolls NATURAL JOIN songs" + 
			" WHERE LOWER(songs.title) LIKE :titleSearch AND" +
			" LOWER(composers.composer_name) LIKE :composerSearch AND" + 
			" LOWER(artists.name) LIKE :performerSearch AND" +  
			" rolls.rollnr = :rollNrSearch AND" + 
			" rolls.num_copies = :nrCopiesSearch")
			
		allFieldsResult = engine.execute(query, titleSearch='%'+titleSearch+'%', composerSearch='%'+composerSearch+'%', performerSearch='%'+performerSearch+'%', rollNrSearch=rollNrSearch, nrCopiesSearch=nrCopiesSearch).fetchall()

		if(allFieldsResult):
			for line in allFieldsResult:
				songs.append("Title: " + line['title'] + "<br>Composer: " + line['composer_name'] + "<br>Artist name: " + line['name'] + "<br>Roll number: " + str(line['rollnr']) + "<br>Number of copies: " + str(line['num_copies'])+ '<br><br>')

			songsStr = ''.join(songs)
			allResults.append(Markup('<strong> '+songsStr +'</strong>'))
		else:
			allResults.append("No results found.")
		return ''.join(allResults)

	elif(titleRequest and compRequest and performRequest and rollNrRequest):

		titleSearch = titleRequest.lower()
#		titleQuery = engine.execute(s, titleSearch='%'+titleSearch+'%').fetchall()

		composerSearch = compRequest.lower()
#		composerQuery = engine.execute(c, composerSearch='%'+composerSearch+'%').fetchall()

		performerSearch = performRequest.lower()
#		performerQuery = engine.execute(p, performerSearch='%'+performerSearch+'%').fetchall()

		rollNrSearch = rollNrRequest.lower()
		#rollNrQuery = engine.execute(rn, rollNrSearch='%'+rollNrSearch+'%').fetchall()

		query = text("SELECT songs.title, composers.composer_name," +
			" artists.name, rolls.rollnr FROM composers" + 
			" NATURAL JOIN artists NATURAL JOIN rolls NATURAL JOIN songs" + 
			" WHERE LOWER(songs.title) LIKE :titleSearch AND" +
			" LOWER(composers.composer_name) LIKE :composerSearch AND" + 
			" LOWER(artists.name) LIKE :performerSearch AND" +  
			" rolls.rollnr = :rollNrSearch")
			
		allFieldsResult = engine.execute(query, titleSearch='%'+titleSearch+'%', composerSearch='%'+composerSearch+'%', performerSearch='%'+performerSearch+'%', rollNrSearch=rollNrSearch).fetchall()

		if(allFieldsResult):
			for line in allFieldsResult:
				songs.append("Title: " + line['title'] + "<br>Composer: " + line['composer_name'] + "<br>Artist name: " + line['name'] + "<br>Roll number: " + str(line['rollnr'])+ '<br><br>')

			songsStr = ''.join(songs)
			allResults.append(Markup('<strong> '+songsStr +'</strong>'))
		else:
			allResults.append("No results found.")
		return ''.join(allResults)

	










		"""
		if(titleQuery):
			for song in titleQuery:
				songs.append(song['title'] + '<br>')

			songsStr = ''.join(songs)
			allResults.append(Markup('<strong> '+songsStr +'</strong>'))
		else:
			allResults.append("No results found for '"+titleSearch+"'")
	return ''.join(allResults)
	"""

	session.close()
if __name__ == '__main__':
	app.run()
