#!/usr/bin/python

import serial
import time
import re
import json
import requests

SERIALPORT = "/dev/ttyUSB0"
BAUDRATE = 9600
URL = "http://localhost/panel"

ser = serial.Serial(SERIALPORT,BAUDRATE,serial.SEVENBITS,serial.PARITY_EVEN,timeout=10)

ser.write("\x2F\x3F\x21\x0D\x0A")

time.sleep(0.5)
numberOfLine = 0
data = {}

while True:
    response = ser.readline()
    if(response.startswith("1-0:2.8")):
        val = response.split('(',1)[1].split(')')[0]
        val_rem = val.replace("*kWh","")
        val_int = int(float(val_rem))
        print(val_int)
        numberOfLine = numberOfLine + 1
        data[numberOfLine] = val_int

    if(numberOfLine == 3):
        json_data = json.dumps(data)
        headers = {'Content-Tpe': 'application/json', 'Accept': 'application/json'}
        print(json_data)
        response = requests.post(URL, headers=headers, json=json.loads(json_data))
        print(response.content)
        break

ser.close()
