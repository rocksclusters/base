#!/opt/rocks/bin/python

import string

places = []
file = open('/usr/share/zoneinfo/zone.tab', 'r')

localTimezone=""
for line in file.readlines():
	l = string.split(line)

	if len(l) < 2 or l[0][0] == '#':
		continue

	if l[2].find("Los_Angeles") >= 0 :
		localTimezone=l[2]
	else:
		places.append(l[2])

file.close()

places.sort()
places.insert(0, localTimezone)
for p in places:
	print '<option>' + p + '</option>'
