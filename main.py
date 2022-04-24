from textblob import TextBlob
import sys, tweepy, json
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

#Example of sentiment analysis
# example = TextBlob("This is a very good item.")
# example2 = TextBlob("What a horrible item.")
#
# print(example.sentiment.polarity)
# print(example2.sentiment.polarity)

#API search params
#API.search_tweets(q, *, geocode, lang, locale, result_type, count, until, since_id,
# max_id, include_entities)

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

    tweets = api.search_tweets(q=searchterm, lang="en", count=numsearch, until=yesterday)

    neutralsample = ""
    positivesample = ""
    negativesample = ""

    for tweet in tweets:
        analysis = TextBlob(tweet.text)
        polarity += analysis.sentiment.polarity

        if (analysis.sentiment.polarity <= 0.05 and analysis.sentiment.polarity >= -0.05):
            neutral += 1
            if (neutralsample == ""):
                neutralsample = tweet
        elif (analysis.sentiment.polarity < -0.05):
            negative += 1
            if (negativesample == ""):
                negativesample = tweet
            elif (negativesample != "" and analysis.sentiment.polarity < TextBlob(negativesample.text).sentiment.polarity):
                negativesample = tweet
        elif (analysis.sentiment.polarity > 0.05):
            positive += 1
            if (positivesample == ""):
                positivesample = tweet
            elif (positivesample != "" and analysis.sentiment.polarity > TextBlob(positivesample.text).sentiment.polarity):
                positivesample = tweet

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

