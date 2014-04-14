import urllib2
import os
import json

class ua :

	def getConfig(self, mac_address) :
		"This needs to download the configuratin from URL networks"

		# Request the configuration from the webserver using the returned mac address
		configuration = {
			'refresh_interval': 15, # in seconds
			'queues':[
				'https://u.alltel.com.au/index.php/json/public_dashboard/get_portlets/172/2400/105?auth=712def47d98232cee74bac50f6392277acae456305f4fb18a75beda44da2fad2',
				'https://u.alltel.com.au/index.php/json/public_dashboard/get_portlets/172/2400/107?auth=712def47d98232cee74bac50f6392277acae456305f4fb18a75beda44da2fad2',
				'https://u.alltel.com.au/index.php/json/public_dashboard/get_portlets/172/2400/109?auth=712def47d98232cee74bac50f6392277acae456305f4fb18a75beda44da2fad2',
			]
		}

		return configuration

	def getQueue(self, queue):
		"Return the information about a single queue from the API server"
		result = urllib2.urlopen(url=queue, timeout=10)
		return json.loads(result.read())
