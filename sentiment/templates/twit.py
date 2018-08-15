import  tweepy
import re

from  textblob import TextBlob
import  nltk
from  nltk.corpus import stopwords
from  nltk.tokenize import word_tokenize
from textblob.sentiments import NaiveBayesAnalyzer
import sys
from tweepy import OAuthHandler
import json



consumer_key = "Cifd3ZdKGKTZjL9WSS2dcPHjh"
consumer_secret = "r0EpCWOzPLbxNcSgX4OOKtuSPGvOjXYbq8JsacOGUHPLCYWHMZ"

access_token = "258672146-X8swzTiFO8mDHdPTDlL2pBmnBeV1yWW9Z9T5BBoo"
access_token_secret = "SkBganOTaKV1vU4yzLDwv8GBdv9tXaDGAmshWiHxRylNq"

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

tweets=[]
posts =[]
tweets = api.search(q='jogoo rd traffic  OR jam' , lang="en",location=[33.8935689697, -4.67677, 41.8550830926, 5.506], count=10, tweet_mode='extended')

stop_words = set(stopwords.words('english'))
for tweet in tweets:
    created_at = tweet.created_at
    

    loc = tweet.user.location
    if 'retweeted_status' in tweet._json:
        tweet_text = tweet._json['retweeted_status']['full_text']
    else:
        tweet_text = tweet.full_text
    booby=word_tokenize(tweet_text)



    def clean_tweet(tweet):

        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]) (\w+:\ / \ / \S+)", " ", tweet).split())


    def get_tweet_sentiment(tweet):

         blob = TextBlob(clean_tweet(tweet))

         if blob.sentiment.polarity > 0.0:
             return 'positive'
         elif blob.sentiment.polarity == 0.0:
             return 'neutral'
         else:
             return 'negative'

    prop = get_tweet_sentiment(tweet_text)


    def create_list():
        posts.append({ 'text': tweet_text ,'locati':loc})

    create_list()


print(posts)

