#Import the necessary methods from tweepy library
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import tweepy
import time
import json
from couchdb import Server
import couchdb

remote_server = Server()
db = remote_server['search_tweets']

#Var  iables that contains the user credentials to access Twitter API 
access_token = "546643485-WaT1mm4EwJe2RrnxMk5xfNxiUxnvfHc3HQgk6jFO"
access_token_secret = "GbaChVqU98h8NpUQ1FzfSG2AonWFBVdtalv5d9LNDfUrU"
consumer_key = "Orgmlwvc3OVi8UtyB1Idk1ArM"
consumer_secret = "GItv17P5pNOqtf2eRnjpfTTyuveo4LoCHUw4OZz3HJtEOo7i7p"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)


#Put your search term
searchquery = "Donald Trump"

contents =tweepy.Cursor(api.search,q=searchquery,lang="en").items()
count = 0
errorCount=0


#file = open('tweets_search_data.json', 'wb') 

while True:
    try:
        content = next(contents)
        count += 1
        #use count-break during dev to avoid twitter restrictions
        #if (count>10):
        #    break
    except tweepy.TweepError:
        #catches TweepError when rate limiting occurs, sleeps, then restarts.
        #nominally 15 minnutes, make a bit longer to avoid attention.
        print "sleeping...."
        time.sleep(60*16)
        content = next(contents)
    except StopIteration:
        break
    try:
        print "Writing to JSON tweet number:"+str(count)
       # json.dump(content._json,file,sort_keys = True,indent = 4)

        njson = json.dumps(content._json,ensure_ascii=False)
        doc = json.loads(njson)
        nid = doc['id_str']
     
        ntext = doc['text']
  
        ncoordinates = doc['coordinates']
        nuser = doc['user']
        ntime = doc['created_at']
        nplace = doc['place']
       # nid = content._json.u'id'
        ndoc={'_id':nid,'text':ntext, 'user':nuser, 'coordinates':ncoordinates, 'create_time':ntime,'place':nplace,'addressed':False}
        db.save(ndoc)
        print('-------------------------------------')
    except UnicodeEncodeError:
        errorCount += 1
        print "UnicodeEncodeError,errorCount ="+str(errorCount)

print "completed, errorCount ="+str(errorCount)+" total tweets="+str(count)