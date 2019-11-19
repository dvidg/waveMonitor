"""
API docu:https://admiraltyapi.portal.azure-api.net/docs/services/uk-tidal-api/operations/Stations_GetStation
API: https://admiraltyapi.azure-api.net/uktidalapi/api/V1/Stations/<URL>/TidalEvents
ID: Porthcawl 0512 | Woolacombe 0535 (Ilfracombe closest)
Visual search site: http://www.ukho.gov.uk/Easytide/easytide/SelectPort.aspx
"""
import http.client
import urllib.request
import urllib.parse
import urllib.error
import base64
import json
import time

duration = 7

def makeRequest(beachID):
	# Request header to include key
	headers = {
			'Ocp-Apim-Subscription-Key': 'c4249a64c1064f4d893dcb19bee78667',
	}

	# Request parameters
	params = urllib.parse.urlencode({
			'duration': duration,
	})

	try:
			conn = http.client.HTTPSConnection('admiraltyapi.azure-api.net')
			conn.request("GET", "/uktidalapi/api/V1/Stations/%s/TidalEvents?%s" % (beachID,params),\
																																					"{body}", headers)
			response = conn.getresponse()
			data = response.read().decode('utf8')
			jsonData = json.loads(data)
			conn.close()
			return jsonData
	except Exception as e:
			print("[Errno {0}] {1}".format(e.errno, e.strerror))
			return -1

def addEpoch(data):
	for x in range(len(data)):
		var = data[x]["DateTime"].split(".")[0]
		p = '%Y-%m-%dT%H:%M:%S'
		epoch = int(time.mktime(time.strptime(var, p)))
		data[x].update({"epoch": epoch})
	return data	

def getData(beachID):
	tideData = addEpoch(makeRequest(beachID))
	return tideData

if __name__ == '__main__':
	getData("0512")
	
