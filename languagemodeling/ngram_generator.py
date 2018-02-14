from collections import defaultdict
import random


class NGramGenerator(object):

    def __init__(self, model):
        """
        model -- n-gram model.
        """
        self._n = model._n

        # compute the probabilities
        probs = defaultdict(dict)
        for *ngram, count in model._count.items():
            ngram = ngram[0]
            if len(ngram) == self._n:
                probs[ngram[:-1]].update({ngram[-1] : model.count(ngram) / model.count(ngram[:-1])})

        self._probs = dict(probs)

        # sort in descending order for efficient sampling
        self._sorted_probs = sorted_probs = {}
        for *ngram, probs in self._probs.items():
            ngram = ngram[0]
            sorted_probs[ngram] = sorted(list(probs.items()), key = lambda prob: prob[1])

    def generate_sent(self):
        """Randomly generate a sentence."""
        n = self._n

        sent = []
        prev_tokens = ['<s>'] * (n - 1)
        token = self.generate_token(tuple(prev_tokens))
        while token != '</s>':
            sent.append(token)
            prev_tokens.append(token)
            prev_tokens.pop(0)
            token = self.generate_token(tuple(prev_tokens))

        return sent

    def generate_token(self, prev_tokens=None):
        """Randomly generate a token, given prev_tokens.

        prev_tokens -- the previous n-1 tokens (optional only if n = 1).
        """
        n = self._n
        if not prev_tokens:
            prev_tokens = ()
        assert len(prev_tokens) == n - 1

        r = random.random()
        probs = self._sorted_probs[prev_tokens]
        i = 0
        token, prob = probs[0]
        acum = prob
        while r > acum:
            i += 1
            token, prob = probs[i]
            acum += prob
    
        return token
