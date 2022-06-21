from imdb import IMDb
import json
import redis
import pickle
import time
import logging
from fetchMovieId import getIdFlag
from fetchMovieId import initRedis

redis = redis.Redis(host= '34.121.112.234',port= '6379')
logging.warning("Connected with Redis Server")

def getReviews():
    try:
        logging.warning('Ready to get requests')
        ia = IMDb()
        movieId = redis.get('movieId') ##get movie ID from Redis
        
        ##Using movie ID collect moview reviews
        movieObj1 = ia.get_movie(movieId)
        ia.update(movieObj1,['reviews'])
        movieReviews = movieObj1['reviews']
        # print(movieReviews)
        
        ## Dump moview reviews in redis
        redis.set('movieReviews',pickle.dumps(movieReviews))

        ##Set movie ID flag to FALSE to stop collecting reviews
        redis.set('movieIdFlag','false')

        ##Set movieAnalysisFlag to TRUE, this will trigger anlz.py
        redis.set('movieAnalysisFlag','true')
        logging.warning('SUCESS: Fetched reviews and pushed to Redis')
        logging.warning('Ready to read data from Redis')
    except:
        logging.warning('ERROR: Unable to get reviews. Check API')

while(1):
    flag = getIdFlag()
    if flag == 1:
        getReviews()
