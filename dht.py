#!/usr/bin/env python
# -*- coding:utf-8 -*-

import argparse
import dhtreader
import time
from datetime import datetime


DHT11 = 11
DHT22 = 22
AM2302 = 2302

# parse args
parser = argparse.ArgumentParser()
parser.add_argument('sensor_type', type=int,   help='type of Sensor. 11|22|2302')
parser.add_argument('GPIO_pin',    type=int,   help='Sensor connected to pin of GPIO')
parser.add_argument('-t', '--try-times',    type=int, default=1, help='Try times')
parser.add_argument('-f', '--format', help='output format. -f log will output "YYYY-MM-DD hh:mm:ss temp,humidity')
parser.add_argument('-v', '--verbose', action='count',  help='verbosity')

args = parser.parse_args()

dev_type = args.sensor_type
gpio_pin = args.GPIO_pin
try_times = args.try_times

if dev_type not in [DHT11, DHT22, AM2302]:
    print 'Invalid sensor type, only 11, 22 and 2302 are supported for now!'
    exit(2)
if dev_type == AM2302:
    dev_type = DHT22

if gpio_pin <= 0:
    print 'Invalid GPIO pin#'
    exit(3)

dhtreader.init()

sensor_values = None
for cnt in xrange(try_times):
    sensor_values = dhtreader.read(dev_type, gpio_pin)
    if sensor_values:
        break

    if args.verbose:
        print "cnt", cnt
    time.sleep(3)

if not sensor_values:
    print "sensor read timeout."
    exit(1)

t, h = sensor_values

temp = t
humidity = h

now = datetime.now()

data = {'datetime': now, 'temp': temp, 'humidity': humidity}

if args.format == 'log':
    output_format = '{datetime:%Y-%m-%d %H:%M:%S} {temp:.1f},{humidity:.1f}'
elif args.format == 'simple':
    output_format = '{temp:.1f},{humidity:.1f}'
elif args.format:
    output_format = args.format
else:
    output_format = '温度: {temp:.1f}°C, 相对湿度: {humidity:.1f}%'

print output_format.format(**data)
