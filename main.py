#!/usr/bin/python
# -*- coding:utf-8 -*-
import logging
import os
import time
import datetime
from PIL import Image, ImageDraw, ImageFont, ImageChops
import waveshare
import weather

logging.basicConfig(level=logging.DEBUG)


def edp_init():
    try:
        raspberrypi = waveshare.RaspberryPi()
        epd = waveshare.EPD(raspberrypi)
        epd.init()
        logging.info("edp init done")
        return epd
    except Exception as e:
        logging.error(e)


def message_printer(epd):
    lib_dir = os.path.dirname(os.path.realpath(__file__))
    font36 = ImageFont.truetype(os.path.join(lib_dir, 'mkt.ttf'), 36)
    font24 = ImageFont.truetype(os.path.join(lib_dir, 'mkt.ttf'), 24)

    date_str = datetime.datetime.now().strftime('%Y-%m-%d')
    time_str = datetime.datetime.now().strftime('%H:%M:%S')

    # black image
    black_image = Image.new('1', (epd.HEIGHT, epd.WIDTH), 255)
    draw = ImageDraw.Draw(black_image)
    draw.text((20, 2), date_str, font=font24, fill=0)
    draw.text((20, 36), time_str, font=font36, fill=0)

    image = ImageChops.invert(weather.ICON[weather.SUN])
    draw.bitmap((10, 66), image)
    red_image = Image.new('1', (epd.HEIGHT, epd.WIDTH), 255)
    epd.display(epd.get_buffer(black_image), epd.get_buffer(red_image))


def loop_monitor():
    epd = edp_init()
    while True:
        message_printer(epd)
        time.sleep(60)


if __name__ == "__main__":
    loop_monitor()
