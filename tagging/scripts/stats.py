"""Print corpus statistics.

Usage:
  stats.py
  stats.py -h | --help

Options:
  -h --help     Show this screen.
"""
from docopt import docopt
from collections import defaultdict

from ancora import SimpleAncoraCorpusReader


class POSStats:
    """Several statistics for a POS tagged corpus.
    """

    def __init__(self, tagged_sents):
        """
        tagged_sents -- corpus (list/iterable/generator of tagged sentences)
        """
        self.tagged_sents_count = 0
        self.tokens_count = 0
        self.tag_words = defaultdict(lambda: defaultdict(int))
        self.word_tags = defaultdict(set)
        self.word_counts = defaultdict(int)

        for sent in tagged_sents:
            self.tagged_sents_count += 1
            self.tokens_count += len(sent)
            for word, tag in sent:
                self.tag_words[tag][word] += 1
                self.word_tags[word].add(tag)
                self.word_counts[word] += 1

        self.tag_words = dict(self.tag_words)
        self.word_tags = dict(self.word_tags)
        self.word_counts = dict(self.word_counts)

    def sent_count(self):
        """Total number of sentences."""
        return self.tagged_sents_count

    def token_count(self):
        """Total number of tokens."""
        return self.tokens_count

    def words(self):
        """Vocabulary (set of word types)."""
        return list(self.word_tags.keys())

    def word_count(self):
        """Vocabulary size."""
        return len(self.words())

    def word_freq(self, w):
        """Frequency of word w."""
        return self.word_counts[w] / self.token_count()

    def unambiguous_words(self):
        """List of words with only one observed POS tag."""
        return self.ambiguous_words(1)

    def ambiguous_words(self, n):
        """List of words with n different observed POS tags.

        n -- number of tags.
        """
        return list(filter(lambda tags: len(tags) == n, self.word_tags))

    def tags(self):
        """POS Tagset."""
        return list(self.tag_words.keys())

    def tag_count(self):
        """POS tagset size."""
        return len(self.tags())

    def tag_freq(self, t):
        """Frequency of tag t."""
        return sum(self.tag_words[t].values()) / self.tag_count()

    def tag_word_dict(self, t):
        """Dictionary of words and their counts for tag t."""
        return dict(self.tag_words[t])


if __name__ == '__main__':
    opts = docopt(__doc__)

    # load the data
    corpus = SimpleAncoraCorpusReader('ancora/ancora-3.0.1es/')
    sents = corpus.tagged_sents()

    # compute the statistics
    stats = POSStats(sents)

    print('Basic Statistics')
    print('================')
    print('sents: {}'.format(stats.sent_count()))
    token_count = stats.token_count()
    print('tokens: {}'.format(token_count))
    word_count = stats.word_count()
    print('words: {}'.format(word_count))
    print('tags: {}'.format(stats.tag_count()))
    print('')

    print('Most Frequent POS Tags')
    print('======================')
    tags = [(t, stats.tag_freq(t)) for t in stats.tags()]
    sorted_tags = sorted(tags, key=lambda t_f: -t_f[1])
    print('tag\tfreq\t%\ttop')
    for t, f in sorted_tags[:10]:
        words = stats.tag_word_dict(t).items()
        sorted_words = sorted(words, key=lambda w_f: -w_f[1])
        top = [w for w, _ in sorted_words[:5]]
        print('{0}\t{1}\t{2:2.2f}\t({3})'.format(t, f, f * 100 / token_count, ', '.join(top)))
    print('')

    print('Word Ambiguity Levels')
    print('=====================')
    print('n\twords\t%\ttop')
    for n in range(1, 10):
        words = list(stats.ambiguous_words(n))
        m = len(words)

        # most frequent words:
        sorted_words = sorted(words, key=lambda w: -stats.word_freq(w))
        top = sorted_words[:5]
        print('{0}\t{1}\t{2:2.2f}\t({3})'.format(n, m, m * 100 / word_count, ', '.join(top)))
