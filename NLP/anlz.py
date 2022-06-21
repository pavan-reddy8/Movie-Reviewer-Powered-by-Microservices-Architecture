# Imports the Google Cloud client library
import string
from google.cloud import language_v1
import redis
import pickle
import ast
import os
from fetchMovieId import getAnalysisFlag


redis = redis.Redis(host= '34.121.112.234',port= '6379')
#cmpFlag = 'true'

def nlp():    
    reviews = pickle.loads(redis.get('movieReviews'))
    # os.system('export GOOGLE_APPLICATION_CREDENTIALS="cloudcomputing-341517-8964d68172a7.json"')
    i = 0

    # for review in reviews:
    #     i +=1
    #     print(review['content'])
    #     print(i)

    # Instantiates a client
    client = language_v1.LanguageServiceClient()
    lst =[]
    category=""
    # The text to analyze
    i=0
    for review in reviews:
        text = review['content']
        #print(text)
        
        text = text.replace(".", "")
        document = language_v1.Document(
            content=text, type_=language_v1.Document.Type.PLAIN_TEXT
        )

        # Detects the sentiment of the text
        sentiment = client.analyze_sentiment(
            request={"document": document}
        ).document_sentiment
         # print(sentiment.score)
        lst.append(sentiment.score)
        i +=1

    average=sum(lst)/len(lst)                                #Calculating average score of users review
    score=pickle.dumps(average)     
    redis.set('score', score)                           #Storing the average score value in redis db
    # print("Score of the film %f" %(average))
    if(average==0):                                     #Classifying the users review into 5 categories based on average score
        category="average and one time watch"
    elif (0 <average <=0.5):
        category="a good movie and entertaining for watching"
    elif(average>0.5):
        category=" a strongly recommeded movie."
    elif((average>-0.5) and (average<0)):
        category=" below average and one time watch"
    else:
        category="bad and better if its avoided"
    
    ## Set movieAnalysisFlag = FALSE to stop NLP() execution
    redis.set('movieAnalysisFlag','false')
    
    ## Set final result in Redis
    redis.set('category', category)
    # print(category)

    ## Set movieResultsFlag = TRUE, this will trigger results ready condition in getMovieName.py
    redis.set('movieResultsFlag','true')

while(1):
    flag = getAnalysisFlag()
    if flag == 1:
        nlp()
    # else:
    #     print("Waiting...")
