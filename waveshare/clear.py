#!/usr/bin/python
# -*- coding:utf-8 -*-

import logging
import os
import time
import datetime

import waveshare

logging.basicConfig(level=logging.DEBUG)

try:
    raspberrypi = waveshare.RaspberryPi()
    epd = waveshare.EPD(raspberrypi)
    epd.init()
    epd.clear()
    epd.sleep()

except Exception as e:
    logging.error(e)
