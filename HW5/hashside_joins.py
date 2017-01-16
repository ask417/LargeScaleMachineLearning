#!/usr/bin/env python

from mrjob.job import MRJob
from mrjob.step import MRStep
from collections import defaultdict
import itertools
import re

class HashsideJoin(MRJob):

    def configure_options(self):
        super(HashsideJoin, self).configure_options()
        self.add_passthrough_option("--join_type", type="str")
        self.add_passthrough_option("--right_table_length", type="int")
        self.add_file_option("--left_table")
    
    def __init__(self, *args, **kwargs):
        super(HashsideJoin, self).__init__(*args, **kwargs)
        self.join_type = self.options.join_type
        self.right_table_length = self.options.right_table_length
    
    def mapper_init(self):
        self.urlTable = {}
        self.keyMatch = {}
        with open(self.options.left_table, 'r') as f:
            for line in f:
                line = line.strip("\n").split(",")
                pageId = line[1]
                leftTableRow = line[:1] + line[2:]
                self.urlTable[pageId] = leftTableRow
                self.keyMatch[pageId] = False

    #Emit Only matches
    def mapper(self, _, line):
        line = line.strip("\n").split(",")
        pageId = line[1]
        rightTableRow = line[:1]+line[2:]
        
        if self.join_type == "inner":
            if pageId in self.urlTable.keys():
                value = self.urlTable[pageId] + rightTableRow
                value = ",".join(value)
                yield pageId,value
        if self.join_type == "right":
            #Need to output the rightTableRow no matter what, 
            #i'm either padding with Nulls, or i'm tacking on the key match
            if pageId in self.urlTable.keys():
                value = self.urlTable[pageId] + rightTableRow
                value = ",".join(value)
            else:
                value = ["null"]*len(self.urlTable.values()[0]) + rightTableRow
                value = ",".join(value)
            yield pageId, value
        if self.join_type == "left":
            if pageId in self.urlTable.keys():
                value = self.urlTable[pageId] + rightTableRow
                value = ",".join(value)
                self.keyMatch[pageId] = True
                yield pageId,value    
                
    def mapper_final(self):
        if self.join_type == "left":
            for key in self.keyMatch.keys():
                #If there were right table keys matching the left table key 
                if self.keyMatch[key] == False:
                    #Output Null padded rows 
                    value = self.urlTable[key] + ["null"]*self.right_table_length
                    value = ",".join(value)
                    yield key, value

    def steps(self):
        return [MRStep(mapper_init=self.mapper_init, mapper=self.mapper, mapper_final=self.mapper_final)]

if __name__=='__main__':
    HashsideJoin.run()