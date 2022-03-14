#!/usr/bin/python
# -*- coding:utf-8 -*-

from PIL import Image

SUN = "big sun"
SUN2 = "sun"
SUN_CLOUD = "big sun with cloud"
SUN2_CLOUD = "sun with cloud"
MORNING = "good morning"
CLOUD_RAIN = "cloud with rain"
FOG = "fog"

weather = Image.open("weather.jpg")

ICON = {
    SUN: weather.crop((10, 10, 150, 150)).resize((32,32)).convert("1"),
    SUN2: weather.crop((160, 10, 310, 150)),
    SUN_CLOUD: weather.crop((320, 15, 470, 150)),
    SUN2_CLOUD: weather.crop((480, 15, 620, 150)),
    MORNING: weather.crop((640, 15, 780, 150)),
    CLOUD_RAIN: weather.crop((800, 15, 930, 150)),
}
