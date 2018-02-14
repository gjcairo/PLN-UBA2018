# https://docs.python.org/3/library/collections.html
from collections import defaultdict
import math


class LanguageModel(object):

    def sent_prob(self, sent):
        """Probability of a sentence. Warning: subject to underflow problems.

        sent -- the sentence as a list of tokens.
        """
        return 0.0

    def sent_log_prob(self, sent):
        """Log-probability of a sentence.

        sent -- the sentence as a list of tokens.
        """
        return -math.inf

    def log_prob(self, sents):
        result = 0.0
        for i, sent in enumerate(sents):
            lp = self.sent_log_prob(sent)
            if lp == -math.inf:
                return lp
            result += lp
        return result

    def cross_entropy(self, sents):
        log_prob = self.log_prob(sents)
        n = sum(len(sent) + 1 for sent in sents)  # count '</s>' events
        e = - log_prob / n
        return e

    def perplexity(self, sents):
        return math.pow(2.0, self.cross_entropy(sents))


class NGram(LanguageModel):

    def add_beg_and_end_of_sentence_chars(self, sent):
        return (["<s>"] * (self._n - 1)) + sent + ["</s>"]

    def __init__(self, n, sents):
        """
        n -- order of the model.
        sents -- list of sentences, each one being a list of tokens.
        """
        assert n > 0
        self._n = n

        count = defaultdict(int)

        for sent in sents:
            sent = self.add_beg_and_end_of_sentence_chars(sent)
            for i in range(len(sent) + 1 - self._n):
                count[tuple(sent[i:i+self._n])] += 1
                count[tuple(sent[i:i+self._n-1])] += 1

        self._count = dict(count)

    def count(self, tokens):
        """Count for an n-gram or (n-1)-gram.

        tokens -- the n-gram or (n-1)-gram tuple.
        """
        return self._count.get(tokens, 0)

    def cond_prob(self, token, prev_tokens=None):
        """Conditional probability of a token.

        token -- the token.
        prev_tokens -- the previous n-1 tokens (optional only if n = 1).
        """
        if not prev_tokens:
            prev_tokens = ()

        ngram_count = self.count(prev_tokens + (token,))
        return 0 if ngram_count == 0 else ngram_count / self.count(prev_tokens)

    def sent_prob(self, sent):
        """Probability of a sentence. Warning: subject to underflow problems.

        sent -- the sentence as a list of tokens.
        """
        sent = self.add_beg_and_end_of_sentence_chars(sent)
        prob = 1
        for i in range(len(sent) + 1 - self._n):
            ngram = tuple(sent[i:i+self._n])
            prob *= self.cond_prob(ngram[-1], ngram[:-1])
        return prob

    def sent_log_prob(self, sent):
        """Log-probability of a sentence.

        sent -- the sentence as a list of tokens.
        """
        sent = self.add_beg_and_end_of_sentence_chars(sent)
        sent_prob = 0
        for i in range(len(sent) + 1 - self._n):
            ngram = tuple(sent[i:i+self._n])
            token_prob = self.cond_prob(ngram[-1], ngram[:-1])
            sent_prob += math.log2(token_prob) if token_prob > 0 else -math.inf
        return sent_prob
