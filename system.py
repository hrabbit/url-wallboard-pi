import os
import netifaces

class system :
	def getMacAddress(self) :	
		"This returns the mac address of the Pi"
		"As a side note, I just presume we want eth0. Of course if we were on wireless, this might fail miserably"
		return netifaces.ifaddresses('eth0')[netifaces.AF_LINK][0]['addr']
