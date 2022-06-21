from flask import Flask, render_template, request
#from imdb import IMDb
#import imdb
from imdb import Cinemagoer
import json
import redis
import pickle
import time
import logging
import string 
from fetchMovieId import initRedis
from fetchMovieId import getResultFlag

redis = redis.Redis(host= '34.121.112.234',port= '6379')
initRedis()
app = Flask(__name__)

@app.route('/')
def index():
     return render_template('home.html')

@app.route('/getMovieName', methods=['POST'])
def getMovieName():
     movieName = request.form['movieName']
     ia = Cinemagoer()
     movieObj = ia.search_movie(movieName)   
     #print(movieObj[0])
     movieId = movieObj[0].movieID
     movieObj1 = ia.get_movie(movieId)
     print(movieId)
     # print(movieObj1)
     redis.set('movieId',movieId) ##set the movie ID in Redis
     
     ##set the movie ID flag true, this will trigger second service (getMoviewReviews.py)
     redis.set('movieIdFlag','true') 

     movie = ia.get_movie(movieId)

     while getResultFlag() == False:
          i = 0
     category = redis.get('category')
     print(type(category))
     category = category.decode("utf-8")
     redis.set('movieResultsFlag','false')
     return render_template('movies.html' , value=category, m=movie)

if __name__ == '__main__':
    app.run(host = '0.0.0.0', port = 3000)