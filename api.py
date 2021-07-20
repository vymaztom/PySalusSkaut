#!/usr/bin/env python3
import configparser
import argparse
import asyncio
import logging
import sys

from pyit600.exceptions import IT600AuthenticationError, IT600ConnectionError
from pyit600.gateway_singleton import IT600GatewaySingleton
from ExelLib_TT import *


async def my_climate_callback(device_id):
    print("Got callback for climate device id: " + device_id)


async def my_sensor_callback(device_id):
    print("Got callback for sensor device id: " + device_id)


async def my_switch_callback(device_id):
    print("Got callback for switch device id: " + device_id)


async def my_cover_callback(device_id):
    print("Got callback for cover device id: " + device_id)


async def main():
	dictUID = {}
	logging.basicConfig(level=logging.DEBUG)
	config = configparser.ConfigParser()
	config.read('config.ini')
	argData = config['DEFAULT']
	listUID = config['ThingSpeakFields']
	for i in range(int(listUID['max_climate_devices'])):
		oneUID = listUID['Field_' + str(i+1) + '_unique_id']
		dictUID[oneUID] = i+1
	async with IT600GatewaySingleton.get_instance(host=argData["gateway_ip"], euid=argData["UID"], debug=False) as gateway:
		try:
			await gateway.connect()
			print(argData["gateway_ip"])
			print(argData["UID"])
		except IT600ConnectionError:
			print("Connection error: check if you have specified gateway's IP address correctly.", file=sys.stderr)
			sys.exit(1)
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

			#ThingSpeakTemperature = ThingSpeakSender(config['ThingSpeak']['API_KEY_TEMPERATURE'])
			#ThingSpeakHumidity = ThingSpeakSender(config['ThingSpeak']['API_KEY_HUMIDITY'])

			temperature = {}
			humidity = {}

			for climate_device_id in climate_devices:
				print(f"Climate device {climate_device_id} status:")
				#print(repr(climate_devices.get(climate_device_id)))
				print(climate_devices.get(climate_device_id).name, end=": \t\t")
				print(climate_devices.get(climate_device_id).current_temperature, end=" °C, ")
				print(climate_devices.get(climate_device_id).current_humidity, end=" %\r\n")

				temperature[dictUID[climate_device_id]] = climate_devices.get(climate_device_id).current_temperature
				humidity[dictUID[climate_device_id]] = climate_devices.get(climate_device_id).current_humidity
				#ThingSpeakTemperature.addField(dictUID[climate_device_id],climate_devices.get(climate_device_id).current_temperature)
				#ThingSpeakHumidity.addField(dictUID[climate_device_id],climate_devices.get(climate_device_id).current_humidity)

				#print(f"Setting heating device {climate_device_id} temperature to 21 degrees celsius")
				#await gateway.set_climate_device_temperature(climate_device_id, 21)

			#ThingSpeakTemperature.send()
			#ThingSpeakHumidity.send()
			XLSaddData(temperature, humidity)


if __name__ == "__main__":
	asyncio.run(main(), debug=True)
