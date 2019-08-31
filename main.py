from flask import send_file
from flask import Flask
from clint.textui import progress
import requests
import sqlite3
from pymongo import MongoClient
from bson.objectid import ObjectId
import os







app = Flask(__name__)

@app.route('/')
def my_tracker():
	return "Download tracker"


@app.route('/track/')
def show():
	db = client['test-database']
	res = {}
	track_id = os.environ['track_id']
	#track_id = request.args.get('track_id')
	cursor = db.track.find_one({"_id": ObjectId(track_id)})

	#db.close()
	chunk_dwnled = float(cursor['downloaded'])
	file_size = float(cursor['file_size'])

	percent = (chunk_dwnled/file_size)*100

	return str("Download status: " + str(int(percent)) + "%")
	 
	


@app.route('/download', methods = ['POST', 'GET'])
def download():
	
	db = client['test-database']
	
	document = {"downloaded" : 0}
	track_id = db.track.insert_one(document).inserted_id
	os.environ['track_id'] = str(track_id)


	url = 'http://www.pdf995.com/samples/pdf.pdf'
	#url = request.forms['file_url']
	r = requests.get(url, stream=True)
	path = 'test_downloaded.pdf'

	with open(path, 'wb') as f:
		ctr = 0
		total_length = int(r.headers.get('content-length'))
		total_chunk = total_length/256
		for chunk in progress.bar(r.iter_content(chunk_size=256), expected_size=(total_chunk) + 1): 
			ctr = ctr + 1
			#print(ctr)
			if chunk:
				f.write(chunk)
				f.flush()
			db.track.update_one({"_id":track_id}, {"$set":{"downloaded": ctr, "file_size" : total_chunk}})
	#db.close()
	return {"status": "success", "track_id" : str(track_id)}
	

if __name__ == '__main__':

	client = MongoClient('mongodb://localhost:27017/')
	db = client['test-database']
	print("Database connected")

	app.run(debug=True)
