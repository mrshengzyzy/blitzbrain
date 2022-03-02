#!/usr/bin/python
# -*- coding:utf-8 -*-
import logging
import os
import time
import datetime
from PIL import Image, ImageDraw, ImageFont
import waveshare

logging.basicConfig(level=logging.DEBUG)

try:
    raspberrypi = waveshare.RaspberryPi()
    epd = waveshare.EPD(raspberrypi)
    epd.init()
    # epd.clear()
    # time.sleep(1)

    lib_dir = os.path.dirname(os.path.realpath(__file__))
    font36 = ImageFont.truetype(os.path.join(lib_dir, 'mkt.ttf'), 36)
    font20 = ImageFont.truetype(os.path.join(lib_dir, 'mkt.ttf'), 20)

    date = datetime.datetime.now().strftime('%Y-%m-%d')
    time = datetime.datetime.now().strftime('%H:%M:%S')

    black_image = Image.new('1', (epd.HEIGHT, epd.WIDTH), 255)
    draw_black = ImageDraw.Draw(black_image)
    draw_black.text((40, 0), date, font=font20, fill=0)

    # draw red image
    red_image = Image.new('1', (epd.HEIGHT, epd.WIDTH), 255)
    draw_red = ImageDraw.Draw(red_image)
    draw_red.text((40, 40), time, font=font36, fill=0)
    epd.display(epd.get_buffer(black_image), epd.get_buffer(red_image))

    # epd.clear()
    # epd.sleep()

except Exception as e:
    logging.error(e)
