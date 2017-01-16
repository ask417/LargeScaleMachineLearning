
#Pair, # occurrences, relative # occurrences 

from mrjob.job import MRJob
from mrjob.step import MRStep
from collections import defaultdict
import itertools
import re
WORD_RE = re.compile(r"[\w']+")

class MRShoppingPairs(MRJob):
    
    def map_basket_pairs(self, _, basket):
        #Get all combinations of pairs, turn to set, then iterate and spit out 
        combos = itertools.combinations(sorted(WORD_RE.findall(basket)), 2)
        for combo in combos:
            yield combo, 1
        yield "basket", 1
    
    def group_basket_pairs(self, key, values):
        total = 0 
        for value in values:
            total += value
        if total>=100:
            yield None, (key, total)
    
    def final_basket_sum(self, _, values):
        values, valuesCp = itertools.tee(values)
        #[total for value in values for key, total in value if key=="basket"]
        for value in valuesCp:
            key, total = value
            if key == "basket":
                basketSize = total
        
        for value in values:
            key, total = value
            yield key, (total, float(total)/basketSize)
        
    def steps(self):
        return [MRStep(mapper=self.map_basket_pairs, reducer=self.group_basket_pairs),
                MRStep(reducer=self.final_basket_sum)]
if __name__=='__main__':
    MRShoppingPairs.run()