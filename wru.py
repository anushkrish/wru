#!/usr/bin/python
import re
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np

totalMessagesEachDay = []
dailyTotalMessages = np.zeros(7)
dayFrequency = np.zeros(7, dtype=int)
firstDate = None
for f in open("wru_test.txt"):
	a = re.split('[ ,]', f)
	dateString=''
	try:
		if re.match('[A-Z][a-z][a-z]', a[0]) and re.match('[0-9]|[0-9][0-9]', a[1]):
			if re.match('[0-9][0-9][0-9][0-9]', a[3]):
				dateString = a[0] + ' ' + a[1] + ' ' + a[3]
			else:
				dateString = a[0] + ' ' + a[1] + ' ' + datetime.now().year
	except:
		pass
	if dateString:
		dateObject = datetime.strptime(dateString, '%b %d %Y')
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
print "Total days: {}".format(len(totalMessagesEachDay))
print "Days on which at least one message was sent: {}".format(dayFrequency.sum())
np.set_printoptions(2)
print "Average number of messages during each day of the week:\n{}".format(dailyAvgMessages)

days = np.arange(7, dtype=int)
labels = ["Mon", "Tue","Wed","Thur","Fri","Sat","Sun",]
plt.bar(days, dailyAvgMessages)
plt.title('Average number of messages per day on Wru since {}'.format(firstDate))
plt.xlabel('Day of week')
plt.ylabel('Average number of messages')
plt.xticks(days, labels)
#plt.show()
plt.savefig("output.png")