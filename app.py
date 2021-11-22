from flask import Flask, render_template, request, jsonify
from Movies.recommendations import getRec
import os

# Paths:

rootPath = os.getcwd()
dataPath = os.path.join(rootPath,'assests','Movies_DataSet.csv')


app = Flask(__name__)

@app.route('/')
@app.route('/home')
def home():
	
	return render_template("home.html")

@app.route('/movieDetails' , methods = ["GET","POST"])
def movieDetails():
	
	query = request.form
	movieTitle = query["movie"]
	recommeded = getRec(dataPath,movieTitle)

	return render_template("table.html", movieList = recommeded)

@app.route('/api/getSimilarMovies' , methods = ["POST"])
def API():
	
	query = request.get_json()
	movieTitle = query["movie"]
	recommeded = getRec(dataPath,movieTitle)

	response = {k:v for k,v in enumerate(recommeded)}

	return jsonify(response)


if __name__ == '__main__':
    app.run(debug=True)
	# app.run(host = "0.0.0.0", port = 5000)