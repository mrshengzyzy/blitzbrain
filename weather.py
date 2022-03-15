#!/usr/bin/python
# -*- coding:utf-8 -*-
import json

import requests

import utils

# 运动指数
LIFE_RUN_LEVEL = "1"
LIFE_RUN_LABEL = "运动"

# 洗车指数
LIFE_CAR_LEVEL = "2"
LIFE_CAR_LABEL = "洗车"

# 钓鱼指数
LIFE_FISH_LEVEL = "4"
LIFE_FISH_LABEL = "钓鱼"

# 紫外线指数
LIFE_PURPLE_LEVEL = "5"
LIFE_PURPLE_LABEL = "紫外线"

# 空气污染指数
LIFE_AIR_LEVEL = "10"
LIFE_AIR_LABEL = "空气状况"

# 图片替换值
LIFE_RUN = "RUN"
LIFE_CAR = "CAR"
LIFE_FISH = "FISH"
LIFE_PURPLE = "PURPLE"
LIFE_AIR = "AIR"
ICON = "TEMP_ICON"
TEMP = "TEMP_REAL"
FEEL_LIKE = "TEMP_FEELS_LIKE"
TEXT = "TEMP_TEXT"


class QWeather:
    PROVINCE = ""
    CITY = ""
    LOCATION_ID = ""
    KEY = ""
    GEO_API = "https://geoapi.qweather.com/v2/city/lookup?"
    WEATHER_API = "https://devapi.qweather.com/v7/weather/now?"
    LIFE_API = "https://devapi.qweather.com/v7/indices/1d?"

    INFO = {
        "PROVINCE": "",
        "CITY": "",
        "LOCATION_ID": "",
        ICON: "",
        TEMP: "",
        FEEL_LIKE: "",
        TEXT: "",
        LIFE_RUN: "",
        LIFE_CAR: "",
        LIFE_FISH: "",
        LIFE_PURPLE: "",
        LIFE_AIR: "",
    }

    def __init__(self):
        self.get_location_id()
        self.get_life()
        self.get_weather()

    def get_location_id(self):
        # 如果已经配置 locationId 则什么都不做
        if self.LOCATION_ID != "":
            return

        # 如果没有配置省份和城市,查询IP地址接口返回的属地信息
        if self.PROVINCE == "" or self.CITY == "":
            arr = utils.get_province_city()
            self.PROVINCE = arr[0]
            self.CITY = arr[1]

        # 否则根据配置的省份城市查询 locationId
        r = requests.get(self.GEO_API + "amd=" + self.PROVINCE + "&location=" + self.CITY + "&key=" + self.KEY)
        r.raise_for_status()
        res = json.loads(r.text)

        # 返回的是一个列表,优先精确匹配城市
        for c in res["location"]:
            if c["name"] == self.CITY:
                self.LOCATION_ID = c["id"]

        # 无法匹配时返回第一个值
        if self.LOCATION_ID == "":
            self.LOCATION_ID = res["location"][0]["id"]

        # 设置省份和城市
        self.INFO["PROVINCE"] = self.PROVINCE
        self.INFO["CITY"] = self.CITY
        self.INFO["LOCATION_ID"] = self.LOCATION_ID

    def get_life(self):
        r = requests.get(self.LIFE_API + "type=0&location=" + self.LOCATION_ID + "&key=" + self.KEY)
        r.raise_for_status()
        res = json.loads(r.text)
        for c in res["daily"]:
            desc = c["category"]
            t = c["type"]
            if t == LIFE_RUN_LEVEL:
                self.INFO[LIFE_RUN] = desc + LIFE_RUN_LABEL
            elif t == LIFE_CAR_LEVEL:
                self.INFO[LIFE_CAR] = desc + LIFE_CAR_LABEL
            elif t == LIFE_FISH_LEVEL:
                self.INFO[LIFE_FISH] = desc + LIFE_FISH_LABEL
            elif t == LIFE_PURPLE_LEVEL:
                self.INFO[LIFE_PURPLE] = LIFE_PURPLE_LABEL + ": " + desc
            elif t == LIFE_AIR_LEVEL:
                self.INFO[LIFE_AIR] = LIFE_AIR_LABEL + ": " + desc

    def get_weather(self):
        r = requests.get(self.WEATHER_API + "location=" + self.LOCATION_ID + "&key=" + self.KEY)
        r.raise_for_status()
        res = json.loads(r.text)
        weather_now = res["now"]
        self.INFO[ICON] = weather_now["icon"]
        self.INFO[TEMP] = weather_now["temp"]
        self.INFO[FEEL_LIKE] = weather_now["feelsLike"]
        self.INFO[TEXT] = weather_now["text"]
