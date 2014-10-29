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

def dayInteger(dateString):
	dateObject = dt.datetime.strptime(dateString, '%b %d %Y')
	return dateObject.weekday()

if __name__=="__main__":
	# command line arguments
	parser = argparse.ArgumentParser(description='Analyse Whatsapp conversations', formatter_class= argparse.ArgumentDefaultsHelpFormatter)
	parser.add_argument('-file', dest='inputFile', default='wru.txt', help='File containing Whatsapp history')
	args = parser.parse_args()

	hourlyMessages = np.zeros((7,24), dtype=int)

	for f in open(args.inputFile):
		timeString=''
		dateString=''
		try:
			timeString = re.search(r'[0-9]*[0-9]:[0-9][0-9] [AP]M', f).group(0)
			dateString = re.search(r'^[JFMAMSOND][aepuco][a-z] [0-9]+, ([0-9][0-9][0-9][0-9])*', f).group(0)
			if not re.match(r'[0-9][0-9][0-9][0-9]', dateString.split()[-1]):
				dateString = "{}{}".format(dateString, dt.date.today().year)
			dateString = ' '.join(re.split(' ,|, |[ ,]', dateString))
		except:
			pass
		if timeString and dateString:
			hour = hourInteger(timeString)
			day  = dayInteger(dateString)
			hourlyMessages[day, hour] += 1
	print "Total messages counted: {}".format(np.sum(hourlyMessages))
	
	# plot the punch card
	x = np.arange(24, dtype=int)
	y = np.arange(7, dtype=int)
	X, Y = np.meshgrid(x, y)
	labels = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
	plt.clf()
	plt.scatter(X, Y, s=hourlyMessages)
	plt.title('Punch card')
	plt.xlabel('Hour of the day')
	plt.yticks(y, labels)
	plt.ylabel('Day of the week')
	fig = plt.gcf()
	fig.set_size_inches(12,5)
	plt.tight_layout()
	plt.savefig("punchCard.png")