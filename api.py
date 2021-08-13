#!/usr/bin/env python3
import configparser
import argparse
import aiocron
import asyncio
import logging
import sys
import os
import datetime

from pyit600.exceptions import IT600AuthenticationError, IT600ConnectionError
from pyit600.gateway_singleton import IT600GatewaySingleton
from ExelLib_TT import *
from sendToThingSpeak import ThingSpeakSender

config = configparser.ConfigParser()
config.read('config.ini')


gateway_ip = config['DEFAULT']['gateway_ip']
UID = config['DEFAULT']['UID']
nameLogFile = config["DEFAULT"]["nameLogFile"]
XLSLogger = False
if config["DEFAULT"]["XLSLogger"] == "True":
	XLSLogger = True
ThingSpeakLogger = False
if config["DEFAULT"]["ThingSpeakLogger"] == "True":
	ThingSpeakLogger = True

API_KEY_TEMPERATURE = config["ThingSpeak"]["API_KEY_TEMPERATURE"]
API_KEY_HUMIDITY = config["ThingSpeak"]["API_KEY_HUMIDITY"]
API_KEY_SETTED_TEMPERATURE = config["ThingSpeak"]["API_KEY_SETTED_TEMPERATURE"]

# počet sensorů, nutné číslovat od 1 a nevynechávat čísla
max_climate_devices = config["ThingSpeakFields"]["max_climate_devices"]
# oranžová klubovna
Field_1_unique_id = config["ThingSpeakFields"]["Field_1_unique_id"]
# zelená klubovna
Field_2_unique_id = config["ThingSpeakFields"]["Field_2_unique_id"]
# modrá klubovna
Field_3_unique_id = config["ThingSpeakFields"]["Field_3_unique_id"]
# žlutá klubovna
Field_4_unique_id = config["ThingSpeakFields"]["Field_4_unique_id"]
# velká klubovna
Field_5_unique_id = config["ThingSpeakFields"]["Field_5_unique_id"]
# sklad
Field_6_unique_id = config["ThingSpeakFields"]["Field_6_unique_id"]

Field__unique_id = {}
Field__unique_id["Field_1_unique_id"] = Field_1_unique_id
Field__unique_id["Field_2_unique_id"] = Field_2_unique_id
Field__unique_id["Field_3_unique_id"] = Field_3_unique_id
Field__unique_id["Field_4_unique_id"] = Field_4_unique_id
Field__unique_id["Field_5_unique_id"] = Field_5_unique_id
Field__unique_id["Field_6_unique_id"] = Field_6_unique_id




def printTXTfile(fileName):
	with open(fileName,"r") as f:
		data = f.read()
		print(data)

async def my_climate_callback(device_id):
    print("Got callback for climate device id: " + device_id)


async def my_sensor_callback(device_id):
    print("Got callback for sensor device id: " + device_id)


async def my_switch_callback(device_id):
    print("Got callback for switch device id: " + device_id)


async def my_cover_callback(device_id):
    print("Got callback for cover device id: " + device_id)

#@aiocron.crontab('*/5 * * * *')
async def main():
	dictUID = {}
	dictUID_ = {}
	#logging.basicConfig(filename='../../home/pi/PySalusSkaut/example.log', encoding='utf-8', level=logging.DEBUG)


	# print Header
	for i in range(79):
		print("-", end="")
	print("-")
	printTXTfile("banner.txt")
	now = datetime.datetime.now()
	current_time = now.strftime("%d.%m.%Y %H:%M:%S")
	print("Current TIME: " + current_time)

	print("GATEWAY IP  : " + gateway_ip)

	print("GATEWAY UID : " + UID)

	if ThingSpeakLogger == True:
		print("ThingSpeak  : True")

	else:
		print("ThingSpeak  : False")

	if XLSLogger == True:
		print("XLS logger  : True")

	else:
		print("XLS logger  : False")

	for i in range(79):
		print("-", end="")

	print("-")


	# read data from SALUS GATEWAY
	for i in range(int(max_climate_devices)):
		oneUID = Field__unique_id['Field_' + str(i+1) + '_unique_id']
		dictUID_[oneUID] = 'Field_' + str(i+1) + '_unique_id'
		dictUID[oneUID] = i+1
	async with IT600GatewaySingleton.get_instance(host=gateway_ip, euid=UID, debug=False) as gateway:
		try:
			await gateway.connect()
		except IT600ConnectionError:
			print("Connection error: check if you have specified gateway's IP address correctly.", file=sys.stderr)

			#sys.exit(1)
			sys.exit(0)
		except IT600AuthenticationError:
			print("Authentication error: check if you have specified gateway's EUID correctly.", file=sys.stderr)

			sys.exit(2)
		except ConnectionAbortedError:
			print("Software v hostitelském počítači ukončil vytvořené připojení.", file=sys.stderr)

			sys.exit(3)

		await gateway.add_climate_update_callback(my_climate_callback)
		await gateway.add_binary_sensor_update_callback(my_sensor_callback)
		await gateway.add_switch_update_callback(my_switch_callback)
		await gateway.add_cover_update_callback(my_cover_callback)

		await gateway.poll_status(send_callback=True)

		climate_devices = gateway.get_climate_devices()

		if not climate_devices:
			print("""Warning: no climate devices found. Ensure that you have paired your thermostat(s) with gateway and you can see it in the official Salus app. If it works there, your thermostat might not be supported. If you want to help to get it supported, open GitHub issue and add your thermostat model number and output of this program. Be sure to run this program with --debug option.\n""")
		else:
			print("All climate devices:")
			print(repr(climate_devices))


			ThingSpeakTemperature = ThingSpeakSender(API_KEY_TEMPERATURE)
			ThingSpeakSetedTemperature = ThingSpeakSender(API_KEY_SETTED_TEMPERATURE)
			ThingSpeakHumidity = ThingSpeakSender(API_KEY_HUMIDITY)

			temperature = {}
			humidity = {}
			temperatureSetted = {}

			for climate_device_id in climate_devices:
				print(f"Climate device {climate_device_id} status:")
				#print(repr(climate_devices.get(climate_device_id)))
				print(climate_devices.get(climate_device_id).name, end=": \t\t")
				print(climate_devices.get(climate_device_id).current_temperature, end=" °C, ")
				print(climate_devices.get(climate_device_id).current_humidity, end=" %\r\n")
				print("add UID_ " + dictUID_[climate_device_id] + " = " + climate_device_id)
				temperature[dictUID_[climate_device_id]] = climate_devices.get(climate_device_id).current_temperature
				temperatureSetted[dictUID_[climate_device_id]] = climate_devices.get(climate_device_id).target_temperature
				humidity[dictUID_[climate_device_id]] = climate_devices.get(climate_device_id).current_humidity
				ThingSpeakTemperature.addField(dictUID[climate_device_id],climate_devices.get(climate_device_id).current_temperature)
				ThingSpeakHumidity.addField(dictUID[climate_device_id],climate_devices.get(climate_device_id).current_humidity)
				ThingSpeakSetedTemperature.addField(dictUID[climate_device_id],climate_devices.get(climate_device_id).target_temperature)
				#print(f"Setting heating device {climate_device_id} temperature to 21 degrees celsius")
				#await gateway.set_climate_device_temperature(climate_device_id, 21)

			if ThingSpeakLogger == True:
				print("ThingSpeakLogger >> data have been send")
				ThingSpeakTemperature.send()
				ThingSpeakHumidity.send()
				ThingSpeakSetedTemperature.send()
			if XLSLogger == True:
				XLSaddData(temperature, humidity, temperatureSetted)




if __name__ == "__main__":
	asyncio.run(main(), debug=True)

	#asyncio.get_event_loop().run_forever()
