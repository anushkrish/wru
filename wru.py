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

totalMessagesEachDay = []
dailyTotalMessages = np.zeros(7)
dayFrequency = np.zeros(7, dtype=int)
firstDate = None
for f in open(args.inputFile):
	a = re.split(r'[ ,]', f)
	dateString=''
	# get the date in a format that python can understand
	try:
		lastTwoWords = "{} {}".format(a[-2], a[-1])
		if re.match(r'[A-Z][a-z][a-z]', a[0]) and re.match(r'[0-9]|[0-9][0-9]', a[1]) and a[-1]!='joined\n' and lastTwoWords!='was removed\n':
			if re.match(r'[0-9][0-9][0-9][0-9]', a[3]):
				dateString = "{} {} {}".format(a[0], a[1], a[3])
			else:
				dateString = "{} {} {}".format(a[0], a[1], dt.datetime.now().year)
	except:
		pass

	if dateString:
		dateObject = dt.datetime.strptime(dateString, '%b %d %Y')
		if not firstDate:
			firstDate = dateObject
			currentDate = dateObject
			curNumber=1
		elif dateObject==currentDate:
			curNumber+=1
		else:
			dayOfWeek = currentDate.weekday()
			dailyTotalMessages[dayOfWeek]+=curNumber
			dayFrequency[dayOfWeek]+=1
			totalMessagesEachDay.append(curNumber)
			diffDays = (dateObject-currentDate).days
			for i in range(diffDays-1):
				totalMessagesEachDay.append(0)
			currentDate = dateObject
			curNumber = 1
dayOfWeek = currentDate.weekday()
dailyTotalMessages[dayOfWeek]+=curNumber
dayFrequency[dayOfWeek]+=1
totalMessagesEachDay.append(curNumber)

dailyAvgMessages = dailyTotalMessages/dayFrequency
totalDays = len(totalMessagesEachDay)
dates = [firstDate+dt.timedelta(days=x) for x in range(totalDays)]
labels = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

# command line output
print "Total days: {}".format(totalDays)
print "Number of days when at least one message was sent: {}".format(dayFrequency.sum())
dayOfMaxMessages = np.argmax(totalMessagesEachDay)
print "Maximum messages: {} on {} ({})".format(totalMessagesEachDay[dayOfMaxMessages], dt.datetime.strftime(dates[dayOfMaxMessages], "%b %d, %Y"), labels[dates[dayOfMaxMessages].weekday()])

# plot average daily messages
days = np.arange(7, dtype=int)
plt.clf()
plt.bar(days, dailyAvgMessages, align='center')
plt.title('For the period from {} to {}\n(counting only days when messages were sent)'.format(dt.datetime.strftime(firstDate, "%b %d, %Y"), dt.datetime.strftime(currentDate, "%b %d, %Y")))
plt.xlabel('Day of week')
plt.ylabel('Average number of messages')
plt.xticks(days, labels)
plt.tight_layout()
plt.savefig("dailyAvgMessages.png")

# plot total messages each day
plt.clf()
plt.bar(dates, totalMessagesEachDay, align='center')
plt.ylabel('Number of messages')
plt.xticks(rotation=70)
plt.tight_layout()
plt.savefig("totalMessagesEachDay.png")