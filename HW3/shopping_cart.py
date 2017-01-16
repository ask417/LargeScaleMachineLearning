#!/usr/bin/env python

#Same as above but we run on complaints data and isolate the issue column

from mrjob.job import MRJob
import re
from mrjob.step import MRStep
from collections import defaultdict

WORD_RE = re.compile(r"[\w']+")

class MRShoppingCart(MRJob):

    def mapper_get_words(self, _, line):
        # yield each word in the line
        basket = len(WORD_RE.findall(line))
        for word in WORD_RE.findall(line):
            yield (word.lower(), (1,basket))

    def combiner_count_words(self, word, counts):
        # sum the words we've seen so far
        #I want to sum the words but also hold on to the basket 
        total=0
        for count in counts:
            sums, basket = count
            total+=sums
        yield word, (total, basket)

    def reducer_count_words(self, word, counts):
        # send all (num_occurrences, word) pairs to the same reducer.
        # num_occurrences is so we can easily use Python's max() function.
        self.increment_counter('group','num_reducer_calls',1)  
        wordCount = 0
        basketSize = 0
        for count in counts:
            sums, basket = count
            basketSize = basket if basket > basketSize else basketSize
            wordCount+=sums
        
        yield None, (word, wordCount, basketSize)

    # discard the key; it is just None
    def reducer_find_max_word(self, _, product_counts):
        # each item of word_count_pairs is (count, word),
        # so yielding one results in key=counts, value=word
        prodCounts = defaultdict(int)
        maxBasket = 0
        total=0
        for count in product_counts:
            prod, prodCount, basket = count
            maxBasket = basket if basket > maxBasket else maxBasket
            prodCounts[prod]+=prodCount
            total+=prodCount

        for k,v in prodCounts.iteritems():
            yield k, (v, float(v)/total, maxBasket)

    def steps(self):
        return [
            MRStep(mapper=self.mapper_get_words,
                   combiner=self.combiner_count_words,
                   reducer=self.reducer_count_words),
            MRStep(reducer=self.reducer_find_max_word)
        ]


if __name__ == '__main__':
    MRShoppingCart.run()