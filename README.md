# Interactive Twitter sentiment analysis website
A website that analyses and visualizes the overall emotional sentiment of tweets on a topic through the use of the Natural Language Processing.
Sentiment analysis are made with NLTK framework. Visualizations are generated in real-time by Plotly. API calls are made with Tweepy.

## Live website
Check out the live website here: https://twitterreactionanalyse.herokuapp.com/
>Apologies for the slow bootup time, it's hosted on a free dyno on Heroku :)

### Getting started
1. Start a Flask project
2. Install the dependencies on requirements.txt
3. Register a developer account on Twitter to access their API
4. Add accessTokens and API keys as environment variables in main.py
5. Run the flask app by writing "manage.py runserver" on console.

#### About the branches
The other branches use different NLP frameworks/methods than NLTK. Mainly Textblob and Textblobs NaiveBayesAnalyzer with an inferior trained model.
After testing, NLTK was the most accurate framework at reading tweet data.


#### Tasks left to do:
1. Tests
2. Create a separate non-anonymized branch (all tweet samples are currently anonymized).
3. Mobile responsive
4. Add a loading circle when generating graphs
5. Save states(session cookies)
