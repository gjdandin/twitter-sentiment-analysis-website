# Interactive Twitter sentiment analysis website
By Gilhan Dandin


An interactive website that analyses and visualizes the overall emotional sentiment of many tweets on a user-inserted topic through the use of the Natural Language Processing. Topic and amount of tweets to analyze are user inputs. Includes anonymized tweet samples as well from the topic dataset.

Sentiment analysis are made with NLTK framework.
Visualizations are generated in real-time by Plotly.
API calls are made with Tweepy.

# Tweet Scraping with a free account has been depreciated since 2023
However, this application still works with a paid twitter basic developer account - set the right accessTokens/api keys

### Getting started
1. Start a Flask project
2. Install the dependencies on requirements.txt
3. Register a developer account on Twitter to access their API
4. Add accessTokens and API keys as environment variables in main.py
5. Run the flask app by writing "python app.py" on console.

#### About the branches
The other branches use different NLP frameworks/methods than NLTK. Mainly Textblob and Textblobs NaiveBayesAnalyzer with an inferior trained model.
After testing, NLTK was the most accurate framework at reading tweet data.


#### Tasks left to do:
1. Tests
2. Create a separate non-anonymized branch (all tweet samples are currently anonymized).
3. Mobile responsive
4. Add a loading circle when generating graphs
5. Save states(session cookies)
