#!/usr/bin/python
import re
import datetime as dt
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import argparse

def hourInteger(timeString):
	h = int(timeString.split(':')[0])
	afterNoon = (timeString.split()[-1]=='PM')
	if afterNoon and h<12:
		h+=12
	if h==12 and not afterNoon:
		h=0
	return h

if __name__=="__main__":
	# command line arguments
	parser = argparse.ArgumentParser(description='Analyse Whatsapp conversations', formatter_class= argparse.ArgumentDefaultsHelpFormatter)
	parser.add_argument('-file', dest='inputFile', default='wru.txt', help='File containing Whatsapp history')
	args = parser.parse_args()

	hourlyMessages = np.zeros(24, dtype=int)

	for f in open(args.inputFile):
		timeString=''
		try:
			timeString = re.search(r'[0-9]*[0-9]:[0-9][0-9] [AP]M', f).group(0)
			if not re.search(r'[A-z]+ *[A-z]*:|\+[0-9]+ \(?[0-9]+\)? [0-9]+[\- ][0-9]+.+:', f):
				timeString=''
		except:
			pass
		if timeString:
			hour = hourInteger(timeString)
			hourlyMessages[hour]+=1
	print "Total messages counted: {}".format(hourlyMessages.sum())

	# plot number of messages sent each hour
	hours = np.arange(24, dtype=int)
	plt.clf()
	plt.bar(hours, hourlyMessages, align='center')
	plt.title('Messages sent during each hour of the day')
	plt.xlabel('Hour of the day')
	plt.ylabel('Number of messages')
	plt.tight_layout()
	plt.savefig("hourlyMessages.png")
