# Import date and timedelta class for yesterdays date.
from datetime import date
from datetime import timedelta
from flask import url_for
import os
import tweepy
import plotly
import plotly.graph_objects as go
import json

from nltk.sentiment.vader import SentimentIntensityAnalyzer # Import the NLTK lexicon
from tweet_cleaner import clean_tweets, anonymize_tweet #tweet cleaner

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


def twittersentimentgraph(searchterm="Norway", numsearch="10"): #These are default values
    """Main function that generates the charts based on data from process sentiment"""
    data = processsentiment(searchterm, numsearch)

    # First figure - piechart - percentages
    colors = ['lightgreen', 'darkred', 'gold']
    sentiment = ["😃 Positive", "😠 Negative", "😐 Neutral"]
    values = [data["positivepercent"], data["negativepercent"], data["neutralpercent"]]

    fig = go.Figure(data=[go.Pie(labels=sentiment,
                                 values=values,
                                 textinfo='label+percent',
                                 insidetextorientation='radial',
                                 hole=.3,
                                 )]
                    )

    fig.update_traces(hoverinfo='label+percent', textinfo='label+percent', textfont_size=24,
                      textposition="inside",
                      marker=dict(colors=colors, line=dict(color='#000000', width=2)))

    fig.update_layout(
        title_text="Percentage of reactions to #" + searchterm + " by analyzing " + numsearch + " recent tweets",
        title=dict(
            font=dict(
                family="Verdana",
                size=24
            )
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        width=900, height=600
    )

    fig.add_annotation(x=0.5, y=0.5,
                       text=numsearch + " Tweets",
                       font=dict(
                           size=16,
                           family='Verdana',
                           color='black'
                       ),
                       showarrow=False
                       )

    piegraph_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    # Second graph - bar charts - counts
    colors2 = ['#006f61', '#721817', '#F1B434']
    valuescount = [data["positivecount"], data["negativecount"], data["neutralcount"]]
    # noinspection PyTypeChecker
    fig2 = go.Figure(data=[go.Bar(
        x=sentiment,
        y=valuescount,
        marker_color=colors2,
        text=valuescount,
        textposition='auto',
    )])

    fig2.update_traces(textfont_size=18)

    fig2.update_layout(
        title_text="Number of reactions to #" + searchterm + " by analyzing " + numsearch + " recent tweets",
        uniformtext_minsize=15,
        title=dict(
            font=dict(
                family="Verdana",
                size=24,
            )),
        yaxis=dict(
            title='Tweet reactions by count',
            titlefont_size=20,
            tickfont_size=20,
        ),
        xaxis=dict(
            tickfont_size=20
        ),
        legend=dict(
            x=0,
            y=1.0,
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        width=900,
        height=600,
    )

    fig2.update_xaxes(fixedrange=True)
    fig2.update_yaxes(fixedrange=True)

    bargraph_json = json.dumps(fig2, cls=plotly.utils.PlotlyJSONEncoder)

    # Samples
    positivesample = data["samples"]["positivesample"]
    negativesample = data["samples"]["negativesample"]
    neutralsample = data["samples"]["neutralsample"]

    # Get the data we need from the sample and wrap it up in a JSON
    positivesamplejson = json.dumps({"text": positivesample.full_text, "author": "AnonymousPositiveUser",
                                     "img": url_for('static', filename='img/happy.png'),
                                     "twitter_handle": "AnonymousPositiveUser",
                                     "link": f"https://twitter.com/{positivesample.user.screen_name}/status/{positivesample.id}",
                                     "created_at": positivesample.created_at.strftime("%m/%d/%Y, %H:%M:%S")})

    negativesamplejson = json.dumps({"text": negativesample.full_text, "author": "AnonymousNegativeUser",
                                     "img": url_for('static', filename='img/angry.png'),
                                     "twitter_handle": "AnonymousNegativeUser",
                                     "link": f"https://twitter.com/{negativesample.user.screen_name}/status/{negativesample.id}",
                                     "created_at": negativesample.created_at.strftime("%m/%d/%Y, %H:%M:%S")})

    neutralsamplejson = json.dumps({"text": neutralsample.full_text, "author": "AnonymousNeutralUser",
                                    "img": url_for('static', filename='img/neutral.png'),
                                    "twitter_handle": "AnonymousNeutralUser",
                                    "link": f"https://twitter.com/{neutralsample.user.screen_name}/status/{neutralsample.id}",
                                    "created_at": neutralsample.created_at.strftime("%m/%d/%Y, %H:%M:%S")})

    # Data count - for detecting sentiment categories with no sample
    positivedatacount = data["positivecount"]
    neutraldatacount = data["neutralcount"]
    negativedatacount = data["negativecount"]

    funcresults = {"piegraphJSON": piegraph_json, "bargraphJSON": bargraph_json,
                   "positivesample": positivesamplejson,
                   "negativesample": negativesamplejson,
                   "neutralsample": neutralsamplejson,
                   "positivedatacount": positivedatacount,
                   "neutraldatacount": neutraldatacount,
                   "negativedatacount": negativedatacount
                   }

    return funcresults