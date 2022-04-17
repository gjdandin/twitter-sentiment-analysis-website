from textblob import TextBlob
import sys, tweepy, json
import app
import unittest

# Import date and timedelta class for yesterdays date.
# from datetime module
from datetime import date
from datetime import timedelta

apiKey = "*********"
apiKeySecret = "************"
bearerToken = '**************'
accessToken = "****************"
accessTokenSecret = "**********************"

def percentage(part, whole):
    """Returns percentages of sentiment analysis"""
    return 100 * float(part)/float(whole)

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

        if (analysis.sentiment.polarity == 0):
            neutral += 1
            if (neutralsample == ""):
                neutralsample = tweet
        elif (analysis.sentiment.polarity < 0.00):
            negative += 1
            if (negativesample == ""):
                negativesample = tweet
        elif (analysis.sentiment.polarity > 0.00):
            positive += 1
            if (positivesample == ""):
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

    #3 examples of positive, negative, tweet processed from sample.
    samples = {}
    return results

# print("Reaction to " + searchterm + " by analyzing " + numSearch + " tweets.")
# if (polarity == 0):
#     print("neutral")
# if (polarity > 0):
#     print("positive")
# elif (polarity < 0):
#     print("negative")


