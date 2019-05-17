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

	titleRequest = request.form['title']
	compRequest = request.form['composer']
	performRequest = request.form['performer']
	mfgrRequest = request.form['mfgr']
	rollNrRequest = request.form['rollNr']
	nrCopiesRequest = request.form['nrCopies']

#***************************************************************************************

	"""All fields."""
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

#***************************************************************************************
#	"""Fields: Title, Artist, Roll number, Number of copies."""
	elif(titleRequest and performRequest and rollNrRequest and nrCopiesRequest):

		titleSearch = titleRequest.lower()
#		titleQuery = engine.execute(s, titleSearch='%'+titleSearch+'%').fetchall()

		performerSearch = performRequest.lower()
#		performerQuery = engine.execute(p, performerSearch='%'+performerSearch+'%').fetchall()

		#mfgrSearch = mfgrRequest.lower()
#		mfgrQuery = engine.execute(m, mfgrSearch='%'+mfgrSearch+'%').fetchall()

		rollNrSearch = rollNrRequest.lower()
		#rollNrQuery = engine.execute(rn, rollNrSearch='%'+rollNrSearch+'%').fetchall()

		nrCopiesSearch = nrCopiesRequest.lower()
		#nrCopiesQuery = engine.execute(nc, nrCopiesSearch='%'+nrCopiesSearch+'%').fetchall()
		
		query = text("SELECT songs.title, composers.composer_name," +
			" artists.name, rolls.rollnr, rolls.num_copies FROM artists"+
			" NATURAL JOIN rolls NATURAL JOIN songs" + 
			" WHERE LOWER(songs.title) LIKE :titleSearch AND" +
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


#***************************************************************************************
#	"""Fields: Composer, Artist, Roll number, Number of copies."""
	elif(compRequest and performRequest and rollNrRequest and nrCopiesRequest):

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
			" WHERE LOWER(composers.composer_name) LIKE :composerSearch AND" + 
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

#***************************************************************************************

#	"""Fields: Title, Artist, Roll number, Number of copies."""
	elif(titleRequest and performRequest and rollNrRequest and nrCopiesRequest):

		titleSearch = titleRequest.lower()
#		titleQuery = engine.execute(s, titleSearch='%'+titleSearch+'%').fetchall()

		performerSearch = performRequest.lower()
#		performerQuery = engine.execute(p, performerSearch='%'+performerSearch+'%').fetchall()

		#mfgrSearch = mfgrRequest.lower()
#		mfgrQuery = engine.execute(m, mfgrSearch='%'+mfgrSearch+'%').fetchall()

		rollNrSearch = rollNrRequest.lower()
		#rollNrQuery = engine.execute(rn, rollNrSearch='%'+rollNrSearch+'%').fetchall()

		nrCopiesSearch = nrCopiesRequest.lower()
		#nrCopiesQuery = engine.execute(nc, nrCopiesSearch='%'+nrCopiesSearch+'%').fetchall()
		
		query = text("SELECT songs.title, composers.composer_name," +
			" artists.name, rolls.rollnr, rolls.num_copies FROM artists"+
			" NATURAL JOIN rolls NATURAL JOIN songs" + 
			" WHERE LOWER(songs.title) LIKE :titleSearch AND" +
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

#***************************************************************************************

#	"""Fields: Title, Composer, Artist, Roll number."""
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
			" artists.name, rolls.rollnr, rolls.num_copies FROM composers" + 
			" NATURAL JOIN artists NATURAL JOIN rolls NATURAL JOIN songs" + 
			" WHERE LOWER(songs.title) LIKE :titleSearch AND" +
			" LOWER(composers.composer_name) LIKE :composerSearch AND" + 
			" LOWER(artists.name) LIKE :performerSearch AND" +  
			" rolls.rollnr = :rollNrSearch")
			
		allFieldsResult = engine.execute(query, titleSearch='%'+titleSearch+'%', composerSearch='%'+composerSearch+'%', performerSearch='%'+performerSearch+'%', rollNrSearch=rollNrSearch).fetchall()

		if(allFieldsResult):
			for line in allFieldsResult:
				songs.append("Title: " + line['title'] + "<br>Composer: " + line['composer_name'] + "<br>Artist name: " + line['name'] + "<br>Roll number: " + str(line['rollnr']) + "<br>Number of copies: " + str(line['num_copies'])+ '<br><br>')

			songsStr = ''.join(songs)
			allResults.append(Markup('<strong> '+songsStr +'</strong>'))
		else:
			allResults.append("No results found.")
		return ''.join(allResults)

#***************************************************************************************
#	"""Fields: Num copies, Composer, Roll number"""
	elif(nrCopiesRequest and compRequest and rollNrRequest):


		composerSearch = compRequest.lower()
#		composerQuery = engine.execute(c, composerSearch='%'+composerSearch+'%').fetchall()

		nrCopiesSearch = nrCopiesRequest.lower()
		rollNrSearch = rollNrRequest.lower()

		query = text("SELECT songs.title, composers.composer_name," +
			" artists.name, rolls.rollnr, rolls.num_copies FROM composers" + 
			" NATURAL JOIN artists NATURAL JOIN rolls NATURAL JOIN songs" + 
			" WHERE rolls.num_copies = :nrCopiesSearch AND" +
			" LOWER(composers.composer_name) LIKE :composerSearch AND" + 
			" rolls.rollnr = :rollNrSearch")
			
		allFieldsResult = engine.execute(query, nrCopiesSearch='%'+nrCopiesSearch+'%', composerSearch='%'+composerSearch+'%', rollNrSearch='%'+rollNrSearch+'%').fetchall()

		if(allFieldsResult):
			for line in allFieldsResult:
				songs.append("Title: " + line['title'] + "<br>Composer: " + line['composer_name'] + "<br>Artist name: " + line['name'] + "<br>Roll number: " + str(line['rollnr']) + "<br>Number of copies: " + str(line['num_copies'])+ '<br><br>')

			songsStr = ''.join(songs)
			allResults.append(Markup('<strong> '+songsStr +'</strong>'))
		else:
			allResults.append("No results found.")
		return ''.join(allResults)

#***************************************************************************************
#	"""Fields: Title, Composer, Roll number"""
	elif(titleRequest and compRequest and rollNrRequest):

		titleSearch = titleRequest.lower()
#		titleQuery = engine.execute(s, titleSearch='%'+titleSearch+'%').fetchall()

		composerSearch = compRequest.lower()
#		composerQuery = engine.execute(c, composerSearch='%'+composerSearch+'%').fetchall()

		rollNrSearch = rollNrRequest.lower()

		query = text("SELECT songs.title, composers.composer_name," +
			" artists.name, rolls.rollnr, rolls.num_copies FROM composers" + 
			" NATURAL JOIN artists NATURAL JOIN rolls NATURAL JOIN songs" + 
			" WHERE LOWER(songs.title) LIKE :titleSearch AND" +
			" LOWER(composers.composer_name) LIKE :composerSearch AND" + 
			" rolls.rollnr = :rollNrSearch")
			
		allFieldsResult = engine.execute(query, titleSearch='%'+titleSearch+'%', composerSearch='%'+composerSearch+'%', rollNrSearch='%'+rollNrSearch+'%').fetchall()

		if(allFieldsResult):
			for line in allFieldsResult:
				songs.append("Title: " + line['title'] + "<br>Composer: " + line['composer_name'] + "<br>Artist name: " + line['name'] + "<br>Roll number: " + str(line['rollnr']) + "<br>Number of copies: " + str(line['num_copies'])+ '<br><br>')

			songsStr = ''.join(songs)
			allResults.append(Markup('<strong> '+songsStr +'</strong>'))
		else:
			allResults.append("No results found.")
		return ''.join(allResults)
	
#***************************************************************************************
#	"""Fields: Title, Composer, Artist"""
	elif(titleRequest and compRequest and performRequest):

		titleSearch = titleRequest.lower()
#		titleQuery = engine.execute(s, titleSearch='%'+titleSearch+'%').fetchall()

		composerSearch = compRequest.lower()
#		composerQuery = engine.execute(c, composerSearch='%'+composerSearch+'%').fetchall()

		performerSearch = performRequest.lower()
#		performerQuery = engine.execute(p, performerSearch='%'+performerSearch+'%').fetchall()

		query = text("SELECT songs.title, composers.composer_name," +
			" artists.name, rolls.rollnr, rolls.num_copies FROM composers" + 
			" NATURAL JOIN artists NATURAL JOIN rolls NATURAL JOIN songs" + 
			" WHERE LOWER(songs.title) LIKE :titleSearch AND" +
			" LOWER(composers.composer_name) LIKE :composerSearch AND" + 
			" LOWER(artists.name) LIKE :performerSearch")
			
		allFieldsResult = engine.execute(query, titleSearch='%'+titleSearch+'%', composerSearch='%'+composerSearch+'%', performerSearch='%'+performerSearch+'%').fetchall()

		if(allFieldsResult):
			for line in allFieldsResult:
				songs.append("Title: " + line['title'] + "<br>Composer: " + line['composer_name'] + "<br>Artist name: " + line['name'] + "<br>Roll number: " + str(line['rollnr']) + "<br>Number of copies: " + str(line['num_copies'])+ '<br><br>')

			songsStr = ''.join(songs)
			allResults.append(Markup('<strong> '+songsStr +'</strong>'))
		else:
			allResults.append("No results found.")
		return ''.join(allResults)
	
#***************************************************************************************

	#Fields: Title, Composer.
	elif(titleRequest and compRequest):

		titleSearch = titleRequest.lower()
#		titleQuery = engine.execute(s, titleSearch='%'+titleSearch+'%').fetchall()

		composerSearch = compRequest.lower()
#		composerQuery = engine.execute(c, composerSearch='%'+composerSearch+'%').fetchall()


		query = text("SELECT songs.title, composers.composer_name," +
			" artists.name, rolls.rollnr, rolls.num_copies FROM composers" + 
			" NATURAL JOIN artists NATURAL JOIN rolls NATURAL JOIN songs" + 
			" WHERE LOWER(songs.title) LIKE :titleSearch AND" +
			" LOWER(composers.composer_name) LIKE :composerSearch")
	
		allFieldsResult = engine.execute(query, titleSearch='%'+titleSearch+'%', composerSearch='%'+composerSearch+'%').fetchall()

		if(allFieldsResult):
			for line in allFieldsResult:
				songs.append("Title: " + line['title'] + "<br>Composer: " + line['composer_name'] + "<br>Artist name: " + line['name'] + "<br>Roll number: " + str(line['rollnr']) + "<br>Number of copies: " + str(line['num_copies'])+ '<br><br>')

			songsStr = ''.join(songs)
			allResults.append(Markup('<strong> '+songsStr +'</strong>'))
		else:
			allResults.append("No results found.")
		return ''.join(allResults)

#***************************************************************************************

	#"""Field: Title."""
	elif(titleRequest):

		titleSearch = titleRequest.lower()
#		titleQuery = engine.execute(s, titleSearch='%'+titleSearch+'%').fetchall()

		query = text("SELECT songs.title, composers.composer_name," +
			" artists.name, rolls.rollnr, rolls.num_copies FROM composers" + 
			" NATURAL JOIN artists NATURAL JOIN rolls NATURAL JOIN songs" + 
			" WHERE LOWER(songs.title) LIKE :titleSearch")
			
		allFieldsResult = engine.execute(query, titleSearch='%'+titleSearch+'%').fetchall()

		if(allFieldsResult):
			for line in allFieldsResult:
				songs.append("Title: " + line['title'] + "<br>Composer: " + line['composer_name'] + "<br>Artist name: " + line['name'] + "<br>Roll number: " + str(line['rollnr']) + "<br>Number of copies: " + str(line['num_copies'])+ '<br><br>')

			songsStr = ''.join(songs)
			allResults.append(Markup('<strong> '+songsStr +'</strong>'))
		else:
			allResults.append("No results found.")
		return ''.join(allResults)

#***************************************************************************************
	#"""Field: Artist."""
	elif(performRequest):

		performerSearch = performRequest.lower()
		query = text("SELECT songs.title, composers.composer_name," +
			" artists.name, rolls.rollnr, rolls.num_copies FROM composers" + 
			" NATURAL JOIN artists NATURAL JOIN rolls NATURAL JOIN songs" + 
			" WHERE LOWER(artists.name) LIKE :performerSearch")
			
		allFieldsResult = engine.execute(query, performerSearch='%'+performerSearch+'%').fetchall()

		if(allFieldsResult):
			for line in allFieldsResult:
				songs.append("Title: " + line['title'] + "<br>Composer: " + line['composer_name'] + "<br>Artist name: " + line['name'] + "<br>Roll number: " + str(line['rollnr']) + "<br>Number of copies: " + str(line['num_copies'])+ '<br><br>')

			songsStr = ''.join(songs)
			allResults.append(Markup('<strong> '+songsStr +'</strong>'))
		else:
			allResults.append("No results found.")
		return ''.join(allResults)

#***************************************************************************************
	#"""Field: Roll number."""
	elif(rollNrRequest):

		rollNrSearch = rollNrRequest.lower()

		query = text("SELECT songs.title, composers.composer_name," +
			" artists.name, rolls.rollnr, rolls.num_copies FROM composers" + 
			" NATURAL JOIN artists NATURAL JOIN rolls NATURAL JOIN songs" + 
			" WHERE rolls.rollnr = rollNrSearch")
			
		allFieldsResult = engine.execute(query, rollNrSearch='%'+rollNrSearch+'%').fetchall()

		if(allFieldsResult):
			for line in allFieldsResult:
				songs.append("Title: " + line['title'] + "<br>Composer: " + line['composer_name'] + "<br>Artist name: " + line['name'] + "<br>Roll number: " + str(line['rollnr']) + "<br>Number of copies: " + str(line['num_copies'])+ '<br><br>')

			songsStr = ''.join(songs)
			allResults.append(Markup('<strong> '+songsStr +'</strong>'))
		else:
			allResults.append("No results found.")
		return ''.join(allResults)

#***************************************************************************************
	#"""Field: Composer."""
	elif(compRequest):

		composerSearch = compRequest.lower()
#		composerQuery = engine.execute(c, composerSearch='%'+composerSearch+'%').fetchall()

		query = text("SELECT songs.title, composers.composer_name," +
			" artists.name, rolls.rollnr, rolls.num_copies FROM composers" + 
			" NATURAL JOIN artists NATURAL JOIN rolls NATURAL JOIN songs" + 
			" WHERE LOWER(composers.composer_name) LIKE :composerSearch")
			
		allFieldsResult = engine.execute(query, composerSearch='%'+composerSearch+'%').fetchall()

		if(allFieldsResult):
			for line in allFieldsResult:
				songs.append("Title: " + line['title'] + "<br>Composer: " + line['composer_name'] + "<br>Artist name: " + line['name'] + "<br>Roll number: " + str(line['rollnr']) + "<br>Number of copies: " + str(line['num_copies'])+ '<br><br>')

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
