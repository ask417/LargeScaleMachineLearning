#!/Users/AnthonySpalvieriKruse/anaconda/bin/python

from numpy import random,array
from PageRankScale import PageRankScale
from PageRankPreprocess import PageRankPreprocess
import sys 

#Plan: Preprocess -> run -> get counter -> 

numIterations = sys.argv[2]
#Don't forget to add -r hadoop
mr_job = PageRankPreprocess(args=[sys.argv[1], "--output-dir", "preprocessed0/", "--N", "11"])
i=0
print numIterations
for i in range(0,int(numIterations)):
    print "iteration: ", i
    
    with mr_job.make_runner() as runner: 
        runner.run()
        lossMap = runner.counters()
        loss = lossMap[0]["loss"]["lossCounter"]
        print loss
    
    #Don't forget to add -r hadoop
    mr_job = PageRankScale(args=['preprocessed'+str(i)+'/', "--N", "11", "--alpha", ".15", "--loss", str(loss), "--output-dir", "preprocessed"+str(i+1)+"/"])
        
    i += 1
    