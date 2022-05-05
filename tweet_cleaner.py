import re


def clean_tweets(tweets):
    """Cleans the tweet text for easier/more accurate processing in NLTK"""
    # set to lower case
    tweets = tweets.lower()

    # remove twitter handles (@xxx)
    tweets = re.sub('/(?<!\w)@[\w+]{1,15}\b/', '', tweets)

    # remove URL links (httpxxx)
    tweets = re.sub('https?://\S+', '', tweets)
    tweets = re.sub("www\.[a-z]?\.?(com)+|[a-z]+\.(com)", '', tweets)

    # remove html reference characters
    tweets = re.sub('&[a-z]+;', '', tweets)

    # remove special characters, numbers, punctuations (except for #)
    tweets = re.sub("[^a-z\s(\-:)\\\/\];='#]", '', tweets)

    return tweets


def anonymize_tweet(tweets):
    """Anonymizes the tweet text"""
    # remove twitter handles (@xxx)
    tweets = re.sub('\B(@[\w\d_]+)', '@anonymizeduser', tweets)

    # remove URL links (httpxxx)
    tweets = re.sub('https?://\S+', '', tweets)
    tweets = re.sub("www\.[a-z]?\.?(com)+|[a-z]+\.(com)", '', tweets)

    return tweets
