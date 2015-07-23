# ARTCategorizer.py
# Usage: python ARTCategorizer.py arg1
# reads from stdin, writes to stdout
# arg1 is rho, the vigilance parameter

import argparse
from ARTNetwork import *
import sys
import numpy as np
import random

categories = 1
rho = 0.5
words = True #TODO Make this an argument
NWORDS = 7
# handle arguments
parser = argparse.ArgumentParser(description='Sort a body of data into categories')
parser.add_argument('rho', type=float, help='the vigilance parameter, how resistant the network is to change', default=0.5)
args = parser.parse_args()

rho = args.rho

# process the data
tempData = []
firstLine = True
for line in sys.stdin:
	
	vals = line.split(',')
	# the revised vector with binary values
	if not firstLine:
		vals2 = [vals[0]]
		for s in vals[1:]:
			vals2.append(1 if float(s) > .05 else 0)
		tempData.append(vals2)
	if firstLine:
		tempData.append(vals)
		firstLine = False
# swap the axes
data = [[] for i in range(len(tempData[0]))]
for i in range(len(tempData)):
	for j in range(len(tempData[i])):
		data[j].append(tempData[i][j])
network = ART1(len(data[1])-1, categories, rho)
random.shuffle(data[1:])
# Train the network with a silent pass through
for point in data[1:-1]:
	network.ART1(point[1:], True)
# Print the results of the second pass
#network.print_results()

if words:
	results = [[] for i in range(network.mNumClusters+1)]
	for point in data[1:-1]:
		# find the cluster for this word and add in the word's data
		result = network.ART1(point[1:], False)
		results[result].append(point)
	# print out the clusters
	for i in range(NWORDS):
	# TODO: This is super inefficient
		for cluster in results:
			if len(cluster) == 0:
				sys.stdout.write('EMPTY')
				continue
			for j in range(len(cluster)):
				for k in range(1, len(cluster[j])):
					cluster[j][k] = float(cluster[j][k])
			tempCluster = sorted(cluster, key=lambda point: -sum(point[1:]))
			sys.stdout.write(str(tempCluster[i%len(cluster)][0]) + ',')
		sys.stdout.write('\n')
else:
	for point in data:
		category = network.ART1(point[1:], False)
		print(point[0] + ", " + str(category))


