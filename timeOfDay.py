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

hourlyMessages = np.zeros(24, dtype=int)

for f in open(args.inputFile):
	a=''
	try:
		a = re.search(r'[0-9]*[0-9]:[0-9][0-9] [AP]M', f).group(0)
	except:
		pass
	if a:
		hour = int(a.split(':')[0])
		afterNoon = (a.split()[-1]=='PM')
		if afterNoon and hour<12:
			hour+=12
		hourlyMessages[hour]+=1	

# plot number of messages sent each hour
hours = np.arange(24, dtype=int)
plt.clf()
plt.bar(hours, hourlyMessages, align='center')
plt.title('Messages sent during each hour of the day')
plt.xlabel('Hour of the day')
plt.ylabel('Number of messages')
plt.tight_layout()
plt.savefig("hourlyMessages.png")
