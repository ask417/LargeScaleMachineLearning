urls = open("JustUrls.txt","r")
all = open("anonymous-msweb-preprocessed.data", "r")

urlKeys = set()
allKeys = set()

for line in urls:
	line = line.strip("\n").split(",")
	key = line[1]
	urlKeys.add(key)

for line in all:
	line = line.strip("\n").split(",")
	key = line[1]
	allKeys.add(key)

print "url length: " + str(len(urlKeys))
print "all length: " + str(len(allKeys))

print "Url keys not in all keys"
print [key for key in urlKeys if key not in allKeys]
print "All keys not in url keys"
print [key for key in allKeys if key not in urlKeys]
