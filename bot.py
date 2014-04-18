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
parser.add_argument('sensor_type', help='type of Sensor. 11|22|2302')
parser.add_argument('GPIO_pin', help='Sensor connected to pin of GPIO')
parser.add_argument('--verbose', '-v', action='count', help='verbosity')

args = parser.parse_args()

dev_type = int(args.sensor_type);
gpio_pin = int(args.GPIO_pin)

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
for cnt in xrange(20):
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

temp = round(t, 0)
humidity = round(h, 0)

comfortable = ''
if temp >= 20 and temp <= 25 and humidity >= 40 and humidity <= 60:
    comfortable = '很舒适哦，喵～～'

now = datetime.now()

greeting = ''
if now.hour >= 5 and now.hour < 10:
    greeting = '喵～早上好。'
elif now.hour >=18 and now.hour < 20:
    greeting = '喵～晚上好。'

print '%s室内温度: %d°C, 相对湿度: %d%% %s' % (greeting, temp, humidity, comfortable)

