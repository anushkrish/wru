#!/usr/bin/python
import re
import datetime as dt
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import argparse

# command line arguments
parser = argparse.ArgumentParser(description='Analyse Whatsapp conversations', formatter_class= argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('-file', dest='inputFile', default='wru.txt', help='File containing Whatsapp history')
args = parser.parse_args()

people={}
for f in open(args.inputFile):
	hasNamelikeString=''
	isMessageOrUpdate=None
	try:
		hasNamelikeString = re.search(r'[A-z]+ *[A-z]*:|\+[0-9]+ \(?[0-9]+\)? [0-9]+[\- ][0-9]+.+:', f)
		isMessageOrUpdate = re.match(r'[A-Z][a-z][a-z] [0-9]+,', f)
	except:
		pass
	if hasNamelikeString and isMessageOrUpdate:
		name = re.match('[A-z]+ *[A-z]*|\+[0-9]+ \(?[0-9]+\)? [0-9]+[\- ][0-9]+', hasNamelikeString.group(0)).group(0)
		if not name in people:
			people[name] = 1
		else:
			people[name] += 1

print "Total messages counted: {}".format(sum(people.values()))
print "{:<30} {:<30}".format('Name','Number of messages')
for k, v in people.iteritems():
    print "{:<30} {:<30}".format(k, v)

# plot number of messages sent by each person
plt.clf()
plt.barh(range(len(people)), people.values(), align='center')
plt.yticks(range(len(people)), people.keys())
plt.title('Messages sent by each person')
plt.xlabel('Number of messages')
plt.tight_layout()
plt.savefig("messagesByPerson.png")