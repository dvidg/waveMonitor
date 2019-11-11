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

def getWindData(b, gdt, x):
	wind  = [b[0]["wind"],
			 b[1]["wind"]]

	wind_data = {
		"speed": wind[0]["speed"]+gdt[0]*x,
		"direction": wind[0]["direction"]+gdt[1]*x
	}
	return wind_data

def getSwellData(b, gdt, x):
	swell = [b[0]["swell"]["components"]["combined"],
			 b[1]["swell"]["components"]["combined"]]

	swell_data = {
		"height" : swell[0]["height"]+gdt[0]*x,
		"period" : swell[0]["period"]+gdt[1]*x,
		"direction" : swell[0]["direction"]+gdt[2]*x
	}

	return swell_data

def getData(b, boundTime):
	swell = [b[0]["swell"]["components"]["combined"],
			 b[1]["swell"]["components"]["combined"]]

	wind  = [b[0]["wind"],
			 b[1]["wind"]]

	time_interval = 10801

	# gradients
	swell_gdt = [
		(swell[1]["height"]-swell[0]["height"])/time_interval,
		(swell[1]["period"]-swell[0]["period"])/time_interval,
		(swell[1]["direction"]-swell[0]["direction"])/time_interval
	]

	wind_gdt = [
		(wind[1]["speed"]-wind[0]["speed"])/time_interval,
		(wind[1]["direction"]-wind[0]["direction"])/time_interval

	]

	# # time
	# time_elapsed = int(time.time())-boundTime[0]
	# 

	main_dict = {}
	for x in range(10801):
		time = x
		main_dict[time+boundTime[0]] = {
			"swell" : getSwellData(b,swell_gdt,time), 
			"wind" : getWindData(b,wind_gdt,time)
		}
	
	return main_dict

def main(id):
	boundTime = getTime()
	b = getJSON(id,boundTime)
	return getData(b, boundTime)
	

if __name__ == '__main__':
	# execution as script
	main(id)


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
