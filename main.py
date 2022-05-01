from textblob import TextBlob
import sys,json, os
import gunicorn
import tweepy
import app

# Import the NLTK and tweet cleaner
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from tweet_cleaner import clean_tweets

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

    # Latest tweets collected should be from yesterday at the very latest to return consistent results.
    today = date.today()
    yesterday = today - timedelta(days = 1)

    tweets = api.search_tweets(q=searchterm + "-filter:retweets -filter:links", lang="en", count=numsearch, until=yesterday, tweet_mode="extended")
    #Tweets are filtering out retweets and purely link(spam) tweets.

    neutralsample = ""
    positivesample = ""
    negativesample = ""
    dummy_sample = tweets[0]

    analyser = SentimentIntensityAnalyzer() #Initialize Nltk sentiment analyzer

    for tweet in tweets:
        cleaned_tweet = clean_tweets(tweet.full_text) #Clean the tweet text before analyzing
        analysis = analyser.polarity_scores(cleaned_tweet)["compound"]

        if (analysis == 0.00):
            neutral += 1
            if (neutralsample == ""):
                neutralsample = tweet

        if (analysis < 0.00):
            negative += 1
            if (negativesample == ""):
                negativesample = tweet

        if (analysis > 0.00):
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

