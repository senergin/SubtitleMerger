# Quick Python script to solve a very specific problem:
# We couldn't find a single file subtitle for a movie, so insted we merge two part files into one.
# SRT subtitle files are text files, that enumarate each subtitle in order, sepeated by a newline.
# Each subtitle is a 3+ line of text, in following format:
#    {SUBTITLE_INDEX}
#    {START_TIMESTAMP} -->  {END_TIMESTAMP}
#    {LINE_1}
#    ...
#    {LINE_N}
# Written by a Python noob

import sys
import re

hourMilliseconds = 60 * 60 * 1000
minuteMilliseconds = 60 * 1000
secondMilliseconds = 1000

file1Path = sys.argv[1] #'Neredesin Firuze_1.srt'
file2Path = sys.argv[2] #'firuze_2.srt'
file3Path = sys.argv[3] #'firuze_final.srt'

print("SRT file 1: " + file1Path)
print("SRT file 2: " + file2Path)
print("Merged file: " + file3Path)

timestampOffset = -30889

indexDiff = 0
timestampDiff = 0

def textToMilliseconds(text):
	vals = re.split('[:,]+', text)
	number = int(vals[0]) * hourMilliseconds
	number += int(vals[1]) * minuteMilliseconds
	number += int(vals[2]) * secondMilliseconds
	number += int(vals[3])
	return number
	
def millisecondsToText(num):
	hour = int(num / hourMilliseconds)
	minute = int((num % hourMilliseconds) / minuteMilliseconds)
	second = int((num % minuteMilliseconds) / secondMilliseconds)
	millisecond = num % secondMilliseconds
	
	hourStr = str(hour).zfill(2)
	minuteStr = str(minute).zfill(2)
	secondStr = str(second).zfill(2)
	millisecondStr = str(millisecond).zfill(3)
	
	text = hourStr + ':' + minuteStr + ':' + secondStr + ',' + millisecondStr
	return text
	
def parseStartEndText(line):
	vals = str.split(line, ' --> ')
	return [vals[0], vals[1]]
	
def applyTimeOffsetToText(text):
	number = textToMilliseconds(text)
	number += timestampDiff
	return millisecondsToText(number)

file1 = open(file1Path, 'r')
file2 = open(file2Path, 'r')
file3 = open(file3Path, 'w')

# Print first file and calculate offset
case = 0 # 0: index, 1: timestamps, 2: text
exit = False
for line in file1:
	if case == 0:
		if line == '\n':
			exit = True
		else:
			indexDiff = int(line)
			case = 1
	elif case == 1:
		vals = parseStartEndText(line)
		timestamp = textToMilliseconds(vals[1])
		timestampDiff = timestamp + timestampOffset
		case = 2
	elif case == 2:
		if line == '\n':
			case = 0
	
	print(line, end='', file=file3)
	
	if exit:
		break

# Print second file while changing values
case = 0 # 0: index, 1: timestamps, 2: text
exit = False
for line in file2:
	if case == 0:
		if line == '\n':
			exit = True
		else:
			index = int(line) + indexDiff
			line = str(index) + '\n'
			case = 1
	elif case == 1:
		vals = parseStartEndText(line)
		vals = list(map(applyTimeOffsetToText, vals))
		line = vals[0] + ' --> ' + vals[1] + '\n'
		case = 2
	elif case == 2:
		if line == '\n':
			case = 0
	
	print(line, end='', file=file3)
	
	if exit:
		break

file1.close()
file2.close()
file3.close()
