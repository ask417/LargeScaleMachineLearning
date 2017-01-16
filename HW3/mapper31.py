#!/usr/bin/env python
import sys

sys.stderr.write("reporter:counter:MapperCounters,Calls,1\n")

for line in sys.stdin:
    if "debt" in line:
        sys.stderr.write("reporter:counter:DebtCounter,Total,1\n")
    elif "mortgage" in line:
        sys.stderr.write("reporter:counter:MortgageCounter,Total,1\n")
    else:
        sys.stderr.write("reporter:counter:OtherCounter,Total,1\n")        
    print line