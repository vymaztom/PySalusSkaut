import sys
from time import sleep
import urllib.request as urllib2


API_KEY_TEMPERATURE = "M9KG1Q4VUPKGNTL4"
baseURL = 'http://api.thingspeak.com/update?api_key=' + str(API_KEY_TEMPERATURE) + '&field1='

class ThingSpeakSender:

	def __init__(self, _API_KEY):
		self.API_KEY = str(_API_KEY)
		self.URL = "http://api.thingspeak.com/update?api_key=" + str(self.API_KEY)
		self.URL_add = ""

	def addField(self, numberOfField, data):
		self.URL_add = self.URL_add + "&field" + str(int(numberOfField)) + "=" + str(round(float(data),2))

	def send(self):
		print(self.URL + self.URL_add)
		with urllib2.urlopen(self.URL + self.URL_add) as f:
			f.read()
			f.close()
		self.URL_add = ""

	def clear(self):
		self.URL_add = ""


if __name__ == '__main__':
	ThingSpeakTemperature = ThingSpeakSender(API_KEY_TEMPERATURE)
	ThingSpeakTemperature.addField(1,"-1.42")
	ThingSpeakTemperature.addField(2,"-1.42")
	ThingSpeakTemperature.addField(3,"-1.42")
	ThingSpeakTemperature.addField(4,"-1.42")
	ThingSpeakTemperature.addField(5,"-1.42")
	ThingSpeakTemperature.addField(6,"-1.42")
	ThingSpeakTemperature.send()
