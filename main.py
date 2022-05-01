from textblob import TextBlob
import sys, tweepy, json
import gunicorn
from textblob.en.sentiments import NaiveBayesAnalyzer
from textblob.classifiers import NaiveBayesClassifier
from textblob import Blobber
import pickle

import app
import unittest
import os

# Import date and timedelta class for yesterdays date.
# from datetime module
from datetime import date
from datetime import timedelta

#Environment variables
apiKey = os.environ['TWITTER_API_KEY']
apiKeySecret = os.environ['TWITTER_API_KEY_SECRET']
bearerToken = os.environ['TWITTER_BEARER_TOKEN']
accessToken = os.environ['TWITTER_ACCESS_TOKEN']
accessTokenSecret = os.environ['TWITTER_ACCESS_TOKEN_SECRET']

#Twitter api authentication
auth = tweepy.OAuthHandler(apiKey, apiKeySecret)
auth.set_access_token(accessToken,accessTokenSecret)
api = tweepy.API(auth)

# test authentication
#try:
   #api.verify_credentials()
    #print("Authentication OK")
#except:
    #print("Error during authentication")


def percentage(part, whole):
    """Returns percentages of sentiment analysis"""
    return 100 * float(part)/float(whole)

def processsentiment(searchterm, numsearch):
    #Count of tweet and sentiments
    positive = 0
    neutral = 0
    negative = 0
    polarity = 0

    # Latest tweets collected should be from yesterday at the very latest to return consistent results.
    today = date.today()
    yesterday = today - timedelta(days = 1)

    tweets = api.search_tweets(q=searchterm + "-filter:retweets -filter:links", lang="en", count=numsearch, until=yesterday, tweet_mode="extended")

    neutralsample = ""
    positivesample = ""
    negativesample = ""
    dummy_sample = tweets[0]

    #cl = pickle.load(open('sentiment_classifier.obj', 'rb')) #Loading pickled classifier trained on training.py
    tb = Blobber(analyzer=NaiveBayesAnalyzer())

    for tweet in tweets:
        analysis = tb(tweet.full_text)
        polarity += (analysis.sentiment.p_pos - analysis.sentiment.p_neg)

        if (-0.1 <= (analysis.sentiment.p_pos - analysis.sentiment.p_neg) <= 0.1):
            neutral += 1
            if (neutralsample == ""):
                neutralsample = tweet

        if ((analysis.sentiment.p_pos - analysis.sentiment.p_neg) < -0.1):
            negative += 1
            if (negativesample == ""):
                negativesample = tweet

        if ((analysis.sentiment.p_pos - analysis.sentiment.p_neg) > 0.1):
            positive += 1
            if (positivesample == ""):
                positivesample = tweet


    # error handling - if sample is empty then set as dummy_sample
    if type(neutralsample) != tweepy.models.Status:
        neutralsample = dummy_sample

    if type(positivesample) != tweepy.models.Status:
        positivesample = dummy_sample

    if type(negativesample) != tweepy.models.Status:
        negativesample = dummy_sample


    positivepercent = format(percentage(positive, numsearch), ".2f")
    negativepercent = format(percentage(negative, numsearch), ".2f")
    neutralpercent = format(percentage(neutral, numsearch), ".2f")

    results = {"positivepercent" : positivepercent, "negativepercent" : negativepercent,
               "neutralpercent" : neutralpercent, "positivecount" : positive,
               "negativecount" : negative, "neutralcount" : neutral,
               "samples" : {"neutralsample": neutralsample, "positivesample": positivesample,
                          "negativesample": negativesample}
               }

    return results

