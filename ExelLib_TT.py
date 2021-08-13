#!/usr/bin/env python3
import sys
import os
import datetime
import xlwt
import xlrd
from xlutils.copy import copy as XLScopy

PATHPREFIX = ""

def getXLSNameByDate():
	now = datetime.datetime.now()
	current_time = now.strftime("%m-%Y")
	return PATHPREFIX + current_time + ".xls"

def XLSaddData(temperature = {}, humidity = {}, temperatureSetted = {}):
	fileName = getXLSNameByDate()
	now = datetime.datetime.now()
	if os.path.exists(fileName):
		rb = xlrd.open_workbook(fileName, formatting_info=True)

		r_sheet1 = rb.sheet_by_index(0)
		r1 = r_sheet1.nrows
		wb = XLScopy(rb)
		sheet1 = wb.get_sheet(0)
		sheet1.write(r1, 0, now.strftime("%d.%m %H:%M:%S"))
		sheet1.write(r1, 1, temperature["Field_1_unique_id"])
		sheet1.write(r1, 2, temperature["Field_2_unique_id"])
		sheet1.write(r1, 3, temperature["Field_3_unique_id"])
		sheet1.write(r1, 4, temperature["Field_4_unique_id"])
		sheet1.write(r1, 5, temperature["Field_5_unique_id"])
		sheet1.write(r1, 6, temperature["Field_6_unique_id"])

		r_sheet2 = rb.sheet_by_index(1)
		r2 = r_sheet2.nrows
		sheet2 = wb.get_sheet(1)
		sheet2.write(r2, 0, now.strftime("%d.%m %H:%M:%S"))
		sheet2.write(r2, 1, humidity["Field_1_unique_id"])
		sheet2.write(r2, 2, humidity["Field_2_unique_id"])
		sheet2.write(r2, 3, humidity["Field_3_unique_id"])
		sheet2.write(r2, 4, humidity["Field_4_unique_id"])
		sheet2.write(r2, 5, humidity["Field_5_unique_id"])
		sheet2.write(r2, 6, humidity["Field_6_unique_id"])

		r_sheet3 = rb.sheet_by_index(2)
		r3 = r_sheet3.nrows
		sheet3 = wb.get_sheet(2)
		sheet3.write(r3, 0, now.strftime("%d.%m %H:%M:%S"))
		sheet3.write(r3, 1, temperatureSetted["Field_1_unique_id"])
		sheet3.write(r3, 2, temperatureSetted["Field_2_unique_id"])
		sheet3.write(r3, 3, temperatureSetted["Field_3_unique_id"])
		sheet3.write(r3, 4, temperatureSetted["Field_4_unique_id"])
		sheet3.write(r3, 5, temperatureSetted["Field_5_unique_id"])
		sheet3.write(r3, 6, temperatureSetted["Field_6_unique_id"])


		wb.save(fileName)
	else:
		wb = xlwt.Workbook()
		sheet1 = wb.add_sheet('temperature')
		sheet1.write(0, 0, 'Date - Time')
		sheet1.write(0, 1, 'oranžová klubovna [°C]')
		sheet1.write(0, 2, 'zelená klubovna [°C]')
		sheet1.write(0, 3, 'modrá klubovna [°C]')
		sheet1.write(0, 4, 'žlutá klubovna [°C]')
		sheet1.write(0, 5, 'velká klubovna [°C]')
		sheet1.write(0, 6, 'sklad [°C]')

		sheet1.write(1, 0, now.strftime("%d.%m %H:%M:%S"))
		sheet1.write(1, 1, temperature["Field_1_unique_id"])
		sheet1.write(1, 2, temperature["Field_2_unique_id"])
		sheet1.write(1, 3, temperature["Field_3_unique_id"])
		sheet1.write(1, 4, temperature["Field_4_unique_id"])
		sheet1.write(1, 5, temperature["Field_5_unique_id"])
		sheet1.write(1, 6, temperature["Field_6_unique_id"])


		sheet2 = wb.add_sheet('humidity')
		sheet2.write(0, 0, 'Date - Time')
		sheet2.write(0, 1, 'oranžová klubovna [%]')
		sheet2.write(0, 2, 'zelená klubovna [%]')
		sheet2.write(0, 3, 'modrá klubovna [%]')
		sheet2.write(0, 4, 'žlutá klubovna [%]')
		sheet2.write(0, 5, 'velká klubovna [%]')
		sheet2.write(0, 6, 'sklad [%]')

		sheet2.write(1, 0, now.strftime("%d.%m %H:%M:%S"))
		sheet2.write(1, 1, humidity["Field_1_unique_id"])
		sheet2.write(1, 2, humidity["Field_2_unique_id"])
		sheet2.write(1, 3, humidity["Field_3_unique_id"])
		sheet2.write(1, 4, humidity["Field_4_unique_id"])
		sheet2.write(1, 5, humidity["Field_5_unique_id"])
		sheet2.write(1, 6, humidity["Field_6_unique_id"])


		sheet3 = wb.add_sheet('temperatureSetted')
		sheet3.write(0, 0, 'Date - Time')
		sheet3.write(0, 1, 'oranžová klubovna [°C]')
		sheet3.write(0, 2, 'zelená klubovna [°C]')
		sheet3.write(0, 3, 'modrá klubovna [°C]')
		sheet3.write(0, 4, 'žlutá klubovna [°C]')
		sheet3.write(0, 5, 'velká klubovna [°C]')
		sheet3.write(0, 6, 'sklad [°C]')

		sheet3.write(1, 0, now.strftime("%d.%m %H:%M:%S"))
		sheet3.write(1, 1, temperatureSetted["Field_1_unique_id"])
		sheet3.write(1, 2, temperatureSetted["Field_2_unique_id"])
		sheet3.write(1, 3, temperatureSetted["Field_3_unique_id"])
		sheet3.write(1, 4, temperatureSetted["Field_4_unique_id"])
		sheet3.write(1, 5, temperatureSetted["Field_5_unique_id"])
		sheet3.write(1, 6, temperatureSetted["Field_6_unique_id"])


		wb.save(fileName)




if __name__ == "__main__":
	humidity = {}
	humidity["Field_1_unique_id"] = 50
	humidity["Field_2_unique_id"] = 25.4
	humidity["Field_3_unique_id"] = 50
	humidity["Field_4_unique_id"] = 25.4
	humidity["Field_5_unique_id"] = 50
	humidity["Field_6_unique_id"] = 50

	temperature = {}
	temperature["Field_1_unique_id"] = 25.4
	temperature["Field_2_unique_id"] = 25.4
	temperature["Field_3_unique_id"] = 25.4
	temperature["Field_4_unique_id"] = 25.4
	temperature["Field_5_unique_id"] = 25.4
	temperature["Field_6_unique_id"] = 25.4
	XLSaddData(temperature, humidity)
