#!/Users/AnthonySpalvieriKruse/anaconda/bin/python

from numpy import random,array
from ShortestPathToyz import ShortestPathToys
import sys 

mr_job = ShortestPathToys(args=[sys.argv[3],"--originNode",sys.argv[1], "--isFirstPass", '1', "--output-dir", "output/"])
visited = set()
firstPass = True
i=0
visitedLength = 0 

#Clear visited file from previous runs
with open('visited.txt', 'w+') as f:
        f.writelines(','.join(str(j) for j in visited))
        
while(1):
    print "iteration ="+str(i)+"  visited =", str(len(visited))
    allVisited = True
    output = {}
    
    with mr_job.make_runner() as runner: 
        runner.run()
        
        # stream_output: get access of the output 
        for line in runner.stream_output():
            # value is the gradient value
            node, value =  mr_job.parse_output_line(line)
            #print node, value
            frontier, distance, path, state = value
            output[node]=value
            
            if state == "V":
                visited.add(node)
            else:
                allVisited = False
    
    if firstPass:
        mr_job = ShortestPathToys(args=['output/', "--file", "indices.txt", "--file", "visited.txt","--originNode", sys.argv[1], "--isFirstPass", '0', "--output-dir", "output/"])
        firstPass = False
        
    i = i + 1
    
    with open('visited.txt', 'w+') as f:
        f.writelines(','.join(str(j) for j in visited))
        
    if allVisited or len(visited)-visitedLength == 0:
        break

    visitedLength = len(visited)
    
print "iteration ="+str(i)+"  visited =", str(len(visited))

print output[sys.argv[2]]