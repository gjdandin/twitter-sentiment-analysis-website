import re

# cleaning the tweets

def clean_tweets(tweets):
    # remove twitter Return handles (RT @xxx:)
    tweets = tweets.lower()

    # remove twitter handles (@xxx)
    tweets = re.sub('/(?<!\w)@[\w+]{1,15}\b/', '', tweets)

    # remove URL links (httpxxx)
    tweets = re.sub('https?:\/\/\S+', '', tweets)
    tweets = re.sub("www\.[a-z]?\.?(com)+|[a-z]+\.(com)", '', tweets)

    # remove html reference characters
    tweets = re.sub('&[a-z]+;', '', tweets)

    # remove special characters, numbers, punctuations (except for #)
    tweets = re.sub("[^a-z\s\(\-:\)\\\/\];='#]", '', tweets)

    return tweets