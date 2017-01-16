#!/usr/bin/env python
import sys 

sys.stderr.write("reporter:counter:ReducerCounters,Calls,1\n")
for line in sys.stdin:
    print line
    