import os
from lxml import etree

all_files = [x for x in os.listdir('.') if x.endswith('.xml')]

durations = []

for i in all_files:
	with open(i) as f:
		tree = etree.parse(f)
		asset = tree.getroot()
		duration = asset.xpath("/MediaAsset/PreservationMaster/MediaKeeper/RunningTime/text()")
		for x in duration:
			durations.append(x)

print(durations)
print(len(durations))

hours = []
minutes = []
seconds = []

for face in durations:
	# '00:29:41
	parsed = face.split(":")
	hours.append(parsed[0])
	minutes.append(parsed[1])
	seconds.append(parsed[2])

hours_seconds = sum([int(hour) for hour in hours])*3600
minutes_seconds = sum([int(minute) for minute in minutes])*60
seconds_tally = sum([int(second) for second in seconds])

print("Hours: "+str(hours_seconds))
print("Minutes: "+str(minutes_seconds))
print("Seconds: "+str(seconds_tally))

seconds_total = sum([hours_seconds,minutes_seconds,seconds_tally])

print("Total: "+str(seconds_total))