import pkg_resources
from metanl.general import preprocess_text

CACHE = {}

class Wordlist(object):
    """
    A list mapping words to frequencies, loaded from a .txt file on disk, and
    cached so that it's loaded at most once.
    """
    def __init__(self, worddict):
        self.worddict = worddict
        self._sorted_words = None

    @property
    def sorted_words(self):
        if self._sorted_words is None:
          self._sorted_words = sorted(self.worddict.keys(),
            key=lambda word: (-self.worddict[word], word))
        return self._sorted_words

    def words(self):
        return list(self.sorted_words)
    keys = words

    def iterwords(self):
        return iter(self.sorted_words)
    iterkeys = iterwords
    __iter__ = iterwords

    def iteritems(self):
        for word in self.sorted_words:
            yield word, self.worddict[word]

    def get(self, word, default=0):
        return self.worddict.get(word, default)
    
    def __getitem__(self, word):
        return self.get(word)

    @classmethod
    def load(cls, filename):
        if filename in CACHE:
            return CACHE[filename]
        else:
            stream = pkg_resources.resource_stream(__name__, 'data/%s' % filename)
            wordlist = cls._load_stream(stream)
            CACHE[filename] = wordlist
        return wordlist

    @classmethod
    def _load_stream(cls, stream):
        worddict = {}
        for line in stream:
            word, freq = line.strip().split(',')
            worddict[word] = int(freq)
        return cls(worddict)
