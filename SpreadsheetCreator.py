# SpreadsheetCreator.py
# Creates a spreadsheet of any number of files based on a threshold of wordcount
# argv[1] is -t (--top) or -b (--bottom)
# argv[2] is a number (top N or threshold of N)
# argv[3] is the total frequency file
# argv[4] is the directory to use


import sys
import os.path

# freqChart is a 2d list that contains a word, then a series of frequencies for each word in each file
# all frequencies are in percentages
# [[word,1,2,3,4,5],[word2,1,2,3,4,5],...]
freqChart = []

# handle arguments
top = False
if sys.argv[1] == '-t' or sys.argv[1] == '--top':
	top = True
n = int(sys.argv[2])

# put all of the words in the chart
for line in open((sys.argv[3])).read().split('\n'):
	if len(line.split(',')) > 1:
		word = line.split(',')[0]
		number = int(line.split(',')[1])
		# if we're using the threshold method, make sure it meets the threshold
		if number > n or top:
			freqChart.append([word,number])
# sort on the frequencies across the whole corpus
freqChart = sorted(freqChart, key=lambda list: -list[1])



if top:
	for i in range(n + 1, len(freqChart)):
		freqChart.remove(freqChart[n+1])
# remove the frequencies before going onto the next step
for i in range(len(freqChart)):
	freqChart[i].remove(freqChart[i][1])

freqChart.insert(0, [''])

i = 0
# loop through lines in files
for filename in os.listdir(sys.argv[4]):
	i += 1
	
	total = 0
	# calculate the total number of words in the file
	for line in open(sys.argv[4] + '/' + filename).read().split('\n'):
		if len(line.split(',')) > 1:
			total+= int(line.split(',')[1])
	if total == 0:
		continue
	freqChart[0].append(str(filename))
	# insert numbers into the chart
	for line in open(sys.argv[4] + '/' + filename).read().split('\n'):
		if len(line.split(',')) > 1:
			word = line.split(',')[0]
			number = int(line.split(',')[1])
			# search for the word in the chart
			for k in range(1, len(freqChart)):
				if freqChart[k][0] == word:
					freqChart[k].append(float(number)/total * 100)
					break
	# fill in the other words with 0's
	for k in range(1, len(freqChart)):
		if len(freqChart[k]) < i+1:
			freqChart[k].append(0)
				
# print the resulting chart
for k in range(0, len(freqChart)):
	if k != 0:
		sys.stdout.write(',')
	sys.stdout.write(freqChart[k][0]);
sys.stdout.write('\n');
for i in range(1, len(freqChart[0])):
	sys.stdout.write(freqChart[0][i]);
	for k in range(1, len(freqChart)):
		sys.stdout.write(',')
		sys.stdout.write(str(freqChart[k][i]))
	sys.stdout.write('\n')



