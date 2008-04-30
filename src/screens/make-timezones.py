#!/opt/rocks/bin/python

import string

places = []
file = open('/usr/share/zoneinfo/zone.tab', 'r')

for line in file.readlines():
	l = string.split(line)

	if len(l) < 2 or l[0][0] == '#':
		continue

	places.append(l[2])

file.close()

places.sort()
for p in places:
	print '<option>' + p + '</option>'
