import redis

redis = redis.Redis(host= '34.121.112.234',port= '6379',charset="utf-8", decode_responses=True)
cmpFlag = 'true'

def getAnalysisFlag():
    if cmpFlag in redis.get('movieAnalysisFlag'):
        return 1
    else:
        return 0

def getIdFlag():
    if cmpFlag in redis.get('movieIdFlag'):
        return 1
    else:
        return 0

def getResultFlag():
    if cmpFlag == redis.get('movieResultsFlag'):
        return True
    else:
        return False

def initRedis():
    redis.set('movieIdFlag','false')
    redis.set('movieId','0')
    redis.set('movieReviewFlag','false')
    redis.set('movieReviews','')
    redis.set('category','')
    redis.set('movieResultsFlag','false')
