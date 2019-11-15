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


def makeRequest():
	# Request header to include key
	headers = {
			'Ocp-Apim-Subscription-Key': 'c4249a64c1064f4d893dcb19bee78667',
	}

	# Request parameters
	params = urllib.parse.urlencode({
			'duration': '7',
	})

	try:
			conn = http.client.HTTPSConnection('admiraltyapi.azure-api.net')
			conn.request("GET", "/uktidalapi/api/V1/Stations/0512/TidalEvents?%s" % params, "{body}", headers)
			response = conn.getresponse()
			data = response.read()
			print(data)
			conn.close()
	except Exception as e:
			print("[Errno {0}] {1}".format(e.errno, e.strerror))


if __name__ == '__main__':
  makeRequest()
