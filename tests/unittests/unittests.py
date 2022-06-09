import pytest
from main import processsentiment
import tweet_cleaner
import tweepy

"""
    Testing for main.py and tweet_cleaner.py functions. Main.twittersentimentgraph() is tested on testroutes.py
    because it needs an active flask application to generate static image URLs.
"""

def test_process_sentiment_function_return_types():
    """Test that process sentiment function works and returns dictionary + correct key/val pairs"""
    """ 
       # Example of a return from process sentiment function
       dummy_return = {"positivepercent": "60.00", "negativepercent": "30.00",
                   "neutralpercent": "10.00", "positivecount": 6,
                   "negativecount": 3, "neutralcount": 1,
                   "samples": {"neutralsample": neutralsample, "positivesample": positivesample,
                               "negativesample": negativesample
                               }
                   } 
       # Samples should be of type tweepy.models.Status
    """
    response = processsentiment("Finland", 10) #Has a String searchterm and an integer query count

    # Assert that response is a dictionary
    assert type(response) == dict

    # Assert that counts are integers
    assert type(response["negativecount"]) == int
    assert type(response["positivecount"]) == int
    assert type(response["neutralcount"]) == int

    # Assert that percentages are floats - has to convert from string to float since its string formatted
    assert float(response["negativepercent"]).__class__ == float
    assert float(response["positivepercent"]).__class__ == float
    assert float(response["neutralpercent"]).__class__ == float

    # Assert that samples are tweepy tweet model type
    assert type(response["samples"]["neutralsample"]) == tweepy.models.Status
    assert type(response["samples"]["positivesample"]) == tweepy.models.Status
    assert type(response["samples"]["negativesample"]) == tweepy.models.Status


def test_process_sentiment_function_returns_query_data():
    """Tests that process sentiment function returns correct data based on function parameters"""
    response = processsentiment("Finland", 30)

    # Assert that tweet sample text has "Finland"
    assert "Finland" in response["samples"]["neutralsample"].full_text
    assert "Finland" in response["samples"]["negativesample"].full_text
    assert "Finland" in response["samples"]["positivesample"].full_text

    # Assert that tweet objects count are same as query
    assert response["negativecount"] + response["neutralcount"] + response["positivecount"] == 30

    # Assert that percentages equal to 100%
    assert float(response["negativepercent"]) + float(response["neutralpercent"]) + float(response["positivepercent"]) == 100.00


def test_tweet_cleaner_clean_tweets_function():
    """ Test that checks if clean_tweets returns lower case string with no special characters and twitter handles"""
    mock_text = "TAKE NO MORE @Seb_Kirby ★★★★★ review !?!$`^|2 ‘NEVER would have guessed who the culprit was.’ http://ow.ly/osCYo Pls RT #BYNR (@Seb_Kirby)"

    #Test that all characters are lower case once cleaned
    assert str.islower(tweet_cleaner.clean_tweets(mock_text))

    # Assert that there are no special characters once cleaned
    assert "[^a-z\s(\-:)\\\/\];='#]" not in tweet_cleaner.clean_tweets(mock_text)

    # Assert that there are no more urls once cleaned
    assert "[www\.[a-z]?\.?(com)+|[a-z]+\.(com)]" not in tweet_cleaner.clean_tweets(mock_text)
    assert "[https?://\S+]" not in tweet_cleaner.clean_tweets(mock_text)

    # Assert that there are no html references once cleaned
    assert '[&[a-z]+;]' not in tweet_cleaner.clean_tweets(mock_text)

    # Assert that there are no more twitter handles once cleaned
    assert '[/(?<!\w)@[\w+]{1,15}\b/]' not in tweet_cleaner.clean_tweets(mock_text)

    # print(tweet_cleaner.clean_tweets(mock_text))


def test_tweet_cleaner_anonymize_tweets_function():
    """Test that checks if anonymize_tweets replaces all twitter handles with @anonymizeduser and all urls are removed"""
    mock_text = "TAKE NO MORE @Seb_Kirby ★★★★★ review !?!$`^|2 ‘NEVER would have guessed who the culprit was.’ http://ow.ly/osCYo Pls RT #BYNR (@Seb_Kirby)"

    # Assert that there are no more urls once cleaned
    assert "[www\.[a-z]?\.?(com)+|[a-z]+\.(com)]" not in tweet_cleaner.anonymize_tweet(mock_text)
    assert "[https?://\S+]" not in tweet_cleaner.anonymize_tweet(mock_text)

    # Assert that all twitter handles are replaced with @anonymizeduser
    assert "@Seb_Kirby" not in tweet_cleaner.anonymize_tweet(mock_text)
    assert "@anonymizeduser" in tweet_cleaner.anonymize_tweet(mock_text)

    # print(tweet_cleaner.anonymize_tweet(mock_text))