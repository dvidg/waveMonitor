import requests
import json
import time
import datetime

# Woolacombe 1352 | Porthcawl 1449
def getJSON(ID,bounds):

	url  = "http://magicseaweed.com/api/082f1c64c83ce0ed8ba3f08b805fb6fa/forecast/?spot_id="
	full = url+str(ID)+"&start="+str(bounds[0])+"&end="+str(bounds[1])+"&units=eu"
	return requests.get(full).json()

def getTime():
	today    = datetime.date.today()
	tomorrow = today + datetime.timedelta(days=1)

	today_utc    = time.mktime(today.timetuple()) # 0000
	tomorrow_utc = time.mktime(tomorrow.timetuple())+1 # 0001 second day

	threeHours = 3*60*60
	onePointFiveHours = 1.5*60*60

	mid_list = []
	for x in range(8):
		mid_list.append(today_utc+onePointFiveHours+x*threeHours)

	now = time.time()
	closestTime = min(mid_list, key=lambda x:abs(x-now))

	return [closestTime - onePointFiveHours, closestTime + onePointFiveHours + 1]

def getData(b):
	swell = [b[0]["swell"]["components"]["combined"],
			 b[1]["swell"]["components"]["combined"]]

	wind  = [b[0]["wind"],
			 b[1]["wind"]]

	time_interval = 10801

	# gradients
	swell_hgt_gdt = (swell[1]["height"]-swell[0]["height"])/time_interval 
	swell_per_gdt = (swell[1]["period"]-swell[0]["period"])/time_interval
	swell_dir_gdt = (swell[1]["direction"]-swell[0]["direction"])/time_interval
	wind_spd_gdt  = (wind[1]["speed"]-wind[0]["speed"])/time_interval
	wind_dir_gdt  = (wind[1]["direction"]-wind[0]["direction"])/time_interval

	# time
	time_elapsed = int(time.time())-boundTime[0]
	swell_data = {
		"height" : swell[0]["height"]+swell_hgt_gdt*time_elapsed,
		"period" : swell[0]["period"]+swell_per_gdt*time_elapsed,
		"direction" : swell[0]["direction"]+swell_dir_gdt*time_elapsed
	}

	wind_data = {
		"speed": wind[0]["speed"]+wind_spd_gdt*time_elapsed,
		"direction": wind[0]["direction"]+wind_dir_gdt*time_elapsed
	}

	print(wind_data.values())

boundTime = getTime()
p = getJSON(1449,boundTime)
w = getJSON(1352,boundTime)
getData(w)






"""


Time blocks
0000 - 0301 (mid: 01:30)
0300 - 0601 (mid: 04:30)
0600 - 0901 (mid: 07:30)
0900 - 1201 (mid: 10:30)
1200 - 1501 (mid: 13:30)
1500 - 1801 (mid: 16:30)
1800 - 2101 (mid: 19:30)
2100 - 0001 (mid: 22:30)

"""
