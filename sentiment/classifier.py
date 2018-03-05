from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import LinearSVC
from sklearn.linear_model import LogisticRegression
from nltk import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
from sentiment.analysis import print_feature_weights_for_item
from sentiment.analysis import print_maxent_features
import re


classifiers = {
    'maxent': LogisticRegression,
    'mnb': MultinomialNB,
    'svm': LinearSVC,
}

class StemmedCountVectorizer(CountVectorizer):
    def build_analyzer(self):
        analyzer = super(StemmedCountVectorizer, self).build_analyzer()
        return lambda doc: ([SnowballStemmer('spanish').stem(w) for w in analyzer(doc)])

class NormalizedCountVectorizer(CountVectorizer):
    def build_tokenizer(self):
        tokenizer = super(NormalizedCountVectorizer, self).build_tokenizer()
        mentionRegex = r"(?:@[^\s]+)"
        urlRegex = r"(?:https?\://t.co/[\w]+)"
        
        def removeRepeatedVowels(word):
            return re.sub(r"(.)\1{2,}", r"\1", word)

        def removeURLs(word):
            return re.sub(urlRegex, '', word)

        def removeMentions(word):
            return re.sub(mentionRegex, '', word)

        def remove_urls_and_mentions(doc):
            return removeRepeatedVowels(removeMentions(removeURLs(tokenizer(doc)))).strip()

        return remove_urls_and_mentions

class SentimentClassifier(object):

    def __init__(self, clf='svm', enhancement=None):
        """
        clf -- classifying model, one of 'svm', 'maxent', 'mnb' (default: 'svm').
        enhancement -- an enhancement to use, one of 'tokenizer', 'binary', 'stopwords', 'stemmer', 'normalize'
        """
        self._clf = clf

        vectorizer = CountVectorizer()
        if enhancement == 'tokenizer':
            vectorizer = CountVectorizer(tokenizer=word_tokenize)
        elif enhancement == 'binary':
            vectorizer = CountVectorizer(binary=True)
        elif enhancement == 'stopwords':
            vectorizer = CountVectorizer(stop_words=stopwords.words('spanish'))
        elif enhancement == 'stemmer':
            vectorizer = StemmedCountVectorizer()
        elif vectorizer == 'normalize':
            vectorizer = NormalizedCountVectorizer()

        self._pipeline = pipeline = Pipeline([
            ('vect', vectorizer),
            ('clf', classifiers[clf]()),
        ])

    def fit(self, X, y):
        self._pipeline.fit(X, y)

    def predict(self, X):
        return self._pipeline.predict(X)

    def print_stats(self, tweet):
        print(tweet)
        vect = self._pipeline.named_steps['vect']
        clf = self._pipeline.named_steps['clf']
        print_maxent_features(vect, clf)
        print_feature_weights_for_item(vect, clf, tweet)
