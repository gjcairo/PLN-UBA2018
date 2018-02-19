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


class AddOneNGram(NGram):

    def __init__(self, n, sents):
        """
        n -- order of the model.
        sents -- list of sentences, each one being a list of tokens.
        """
        # call superclass to compute counts
        super().__init__(n, sents)

        # compute vocabulary
        self._voc = voc = set()

        for ngram in self._count.keys():
            for word in ngram:
                if word != "<s>":
                    voc.add(word)

        self._V = len(voc)  # vocabulary size

    def V(self):
        """Size of the vocabulary.
        """
        return self._V

    def cond_prob(self, token, prev_tokens=None):
        """Conditional probability of a token.

        token -- the token.
        prev_tokens -- the previous n-1 tokens (optional only if n = 1).
        """
        n = self._n
        if not prev_tokens:
            # if prev_tokens not given, assume 0-uple:
            prev_tokens = ()
        assert len(prev_tokens) == n - 1

        return (self.count(prev_tokens + (token,)) + 1) / (self.count(prev_tokens) + self.V())


class InterpolatedNGram(NGram):

    def __init__(self, n, sents, gamma=None, addone=True):
        """
        n -- order of the model.
        sents -- list of sentences, each one being a list of tokens.
        gamma -- interpolation hyper-parameter (if not given, estimate using
            held-out data).
        addone -- whether to use addone smoothing (default: True).
        """
        assert n > 0
        self._n = n

        if gamma is not None:
            # everything is training data
            train_sents = sents
        else:
            # 90% training, 10% held-out
            m = int(0.9 * len(sents))
            train_sents = sents[:m]
            held_out_sents = sents[m:]

        print('Computing counts...')
        count = dict()
        for k in range(1, self._n + 1):
            ngram = NGram(k, train_sents)
            count.update(ngram._count)
        self._count = dict(count)

        # compute vocabulary size for add-one in the last step
        self._addone = addone
        if addone:
            print('Computing vocabulary...')
            self._voc = voc = set()

            for ngram in self._count.keys():
                for word in ngram:
                    if word != "<s>":
                        voc.add(word)

            self._V = len(voc)

        # compute gamma if not given
        if gamma is not None:
            self._gamma = gamma
        else:
            print('Computing gamma...')
            # use grid search to choose gamma
            min_gamma, min_p = None, float('inf')

            for gamma in [10 + i * 10 for i in range(20)]:
                self._gamma = gamma
                p = self.perplexity(held_out_sents)
                print('  {} -> {}'.format(gamma, p))

                if p < min_p:
                    min_gamma, min_p = gamma, p

            print('  Choose gamma = {}'.format(min_gamma))
            self._gamma = min_gamma

    def count(self, tokens):
        """Count for an k-gram for k <= n.

        tokens -- the k-gram tuple.
        """
        return self._count.get(tokens, 0)

    def cond_prob(self, token, prev_tokens=None):
        """Conditional probability of a token.

        token -- the token.
        prev_tokens -- the previous n-1 tokens (optional only if n = 1).
        """
        n = self._n
        if not prev_tokens:
            # if prev_tokens not given, assume 0-uple:
            prev_tokens = ()
        assert len(prev_tokens) == n - 1

        tokens = prev_tokens + (token,)
        prob = 0.0
        cum_lambda = 0.0  # sum of previous lambdas
        for i in range(n):
            # i-th term of the sum
            if i < n - 1:
                lambdaa = (1 - cum_lambda) * (self.count(tokens[i:-1]) / (self.count(tokens[i:-1]) + self._gamma))
                cond_ml = super(type(self), self).cond_prob(tokens[-1], tokens[i:-1])
            else:
                lambdaa = (1 - cum_lambda)
                if self._addone:
                    cond_ml = (self.count(tokens) + 1) / (self.count(tokens[:-1]) + self._V)
                else:
                    cond_ml = super(type(self), self).cond_prob(tokens[-1], tokens[i:-1])

            prob += lambdaa * cond_ml
            cum_lambda += lambdaa

        return prob
