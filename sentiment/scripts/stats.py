"""Print corpus statistics.

Usage:
  stats.py
  stats.py -h | --help

Options:
  -h --help     Show this screen.
"""
from docopt import docopt
from collections import defaultdict

from sentiment.tass import InterTASSReader, GeneralTASSReader


class SentimentStats:
    """Several statistics for a Sentiment tagged corpus.
    """

    def __init__(self, tweet_contents, tweet_tags):
        """
        tweet_contents -- corpus of tweets
        tweet_tags -- sentiment tags for tweets
        """
        self.tweet_contents = list(tweet_contents)
        self.tweet_contents_count = len(self.tweet_contents)

        self.tweet_tags = tweet_tags
        self.tweets_per_tag = defaultdict(list)
        for i, tag in enumerate(tweet_tags):
            self.tweets_per_tag[tag].append(self.tweet_contents[i])

    def tweet_count(self):
        """Total number of tweets"""
        return self.tweet_contents_count

    def tweet_count_per_sentiment(self):
        """Total number of tweets grouped by sentiment"""
        return dict([(sentiment, len(tweets)) for sentiment, tweets in self.tweets_per_tag.items()])


if __name__ == '__main__':
    opts = docopt(__doc__)

    # load the data
    inter_corpus = InterTASSReader('../TASS/InterTASS/tw_faces4tassTrain1000rc.xml')
    inter_tweets_contents = inter_corpus.X()
    inter_tweet_tags = inter_corpus.y()

    general_corpus = GeneralTASSReader('../TASS/GeneralTASS/general-tweets-train-tagged.xml')
    general_tweets_contents = general_corpus.X()
    general_tweet_tags = general_corpus.y()

    # compute the statistics
    inter_stats = SentimentStats(inter_tweets_contents, inter_tweet_tags)
    general_stats = SentimentStats(general_tweets_contents, general_tweet_tags)

    print('InterTASS Statistics')
    print('================')
    print('Tweets: {}'.format(inter_stats.tweet_count()))
    print('Tweets per sentiment: {}'.format(inter_stats.tweet_count_per_sentiment()))
    print('')

    print('GeneralTASS Statistics')
    print('================')
    print('Tweets: {}'.format(general_stats.tweet_count()))
    print('Tweets per sentiment: {}'.format(general_stats.tweet_count_per_sentiment()))
    print('')