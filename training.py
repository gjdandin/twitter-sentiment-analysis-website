from textblob import TextBlob
from textblob.classifiers import NaiveBayesClassifier

import pandas as pd
import pickle
"""File for training and generating the classifier for NaiveBayesAnalyzer used in Textblob
on Tweets - training set is sts_gold_tweet file."""

#read the file
data = pd.read_csv("sts_gold_tweet.csv", sep=";", encoding="utf-8").drop('id', 1)

#Explanation for the polarity in the files: 0 is negative and 4 is positive.

labels = {0: 'negative', 4: 'positive'}
data['polarity'] = data['polarity'].map(labels)

# convert the data into a list
data = data[['tweet', 'polarity']].values.tolist()

# split the data into a train and test data
L = len(data)
train_index = int(0.60 * L)
train, test = data[:train_index], data[train_index: ]

cl = NaiveBayesClassifier(train) #Use this for first training, afterwards you can create pickled version for faster train.
#cl = pickle.load(open('sentiment_classifier.obj', 'rb'))
cl.accuracy(test)

print(cl.accuracy(test))
print("cl is trained.")

#pickled_classifier_file = open('sentiment_classifier.obj', 'wb')
#pickle.dump(cl, pickled_classifier_file)
#pickled_classifier_file.close()

