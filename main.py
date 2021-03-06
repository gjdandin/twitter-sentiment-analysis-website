# Import date and timedelta class for yesterdays date.
from datetime import date
from datetime import timedelta
import os
import tweepy
# Import the NLTK lexicon and tweet cleaner
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from tweet_cleaner import clean_tweets, anonymize_tweet

# Environment variables
apiKey = os.environ['TWITTER_API_KEY']
apiKeySecret = os.environ['TWITTER_API_KEY_SECRET']
bearerToken = os.environ['TWITTER_BEARER_TOKEN']
accessToken = os.environ['TWITTER_ACCESS_TOKEN']
accessTokenSecret = os.environ['TWITTER_ACCESS_TOKEN_SECRET']

# Twitter api authentication
auth = tweepy.OAuthHandler(apiKey, apiKeySecret)
auth.set_access_token(accessToken, accessTokenSecret)
api = tweepy.API(auth)


# test authentication snippet
# try:
# api.verify_credentials()
# print("Authentication OK")
# except:
# print("Error during authentication")

def percentage(part, whole):
    """Returns percentages of sentiment analysis"""
    return 100 * float(part) / float(whole)


def processsentiment(searchterm, numsearch):
    # Count of tweet and sentiments
    positive = 0
    neutral = 0
    negative = 0

    # Latest tweets collected should be from yesterday at the very latest to return consistent results.
    today = date.today()
    yesterday = today - timedelta(days=1)

    # Tweet API call are filtering out retweets, purely link(spam) tweets and replies.
    tweets = api.search_tweets(q=searchterm + "-filter:retweets -filter:links -filter:replies",
                               lang="en", count=numsearch, until=yesterday, tweet_mode="extended")

    # Init the samples
    neutralsample = ""
    positivesample = ""
    negativesample = ""

    # Create a dummy sample for sample categories missing a sample.
    dummy_sample = tweets[0]

    analyser = SentimentIntensityAnalyzer()  # Initialize Nltk sentiment analyzer

    for tweet in tweets:
        cleaned_tweet = clean_tweets(tweet.full_text)  # Clean the tweet text before analyzing
        analysis = analyser.polarity_scores(cleaned_tweet)["compound"]  # Get the compound sentiment score

        if analysis == 0.00:
            neutral += 1
            if neutralsample == "":
                neutralsample = tweet

        if analysis < 0.00:
            negative += 1
            if negativesample == "" \
                    or analyser.polarity_scores(clean_tweets(negativesample.full_text))["compound"] > analysis:
                # Replace the negative sample if the current tweet obj has a lesser score
                negativesample = tweet

        if analysis > 0.00:
            positive += 1
            if positivesample == "" \
                    or analyser.polarity_scores(clean_tweets(positivesample.full_text))["compound"] < analysis:
                # Replace the positive sample if the current tweet obj has a greater score
                positivesample = tweet

    # error handling - if sample is empty then set as dummy_sample
    if type(neutralsample) != tweepy.models.Status:
        neutralsample = dummy_sample

    if type(positivesample) != tweepy.models.Status:
        positivesample = dummy_sample

    if type(negativesample) != tweepy.models.Status:
        negativesample = dummy_sample

    # Anonymize the tweet samples
    positivesample.full_text = anonymize_tweet(positivesample.full_text)
    negativesample.full_text = anonymize_tweet(negativesample.full_text)
    neutralsample.full_text = anonymize_tweet(neutralsample.full_text)

    # Create the percentages for the donut graph.
    positivepercent = format(percentage(positive, numsearch), ".2f")
    negativepercent = format(percentage(negative, numsearch), ".2f")
    neutralpercent = format(percentage(neutral, numsearch), ".2f")

    # Pass the results to app as key/val pairs.
    results = {"positivepercent": positivepercent, "negativepercent": negativepercent,
               "neutralpercent": neutralpercent, "positivecount": positive,
               "negativecount": negative, "neutralcount": neutral,
               "samples": {"neutralsample": neutralsample, "positivesample": positivesample,
                           "negativesample": negativesample
                           }
               }

    return results
