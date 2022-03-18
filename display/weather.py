#!/usr/bin/python
# -*- coding:utf-8 -*-
import json
from datetime import datetime

from .consts import *
from .ip import *


class QWeather:
    PROVINCE = "山东"
    CITY = "济南"
    LOCATION_ID = "101120101"
    KEY = "4d3906ed14ee49408d7b16b4bc94c802"
    GEO_API = "https://geoapi.qweather.com/v2/city/lookup?"
    WEATHER_API = "https://devapi.qweather.com/v7/weather/3d?"
    LIFE_API = "https://devapi.qweather.com/v7/indices/1d?"

    # 待填充值
    FILL = {
        W_DATE: "",
        W_WEEKDAY: "",
        W_PROVINCE: "",
        W_CITY: "",
        W_ICON: "",
        W_TEMP_MAX: "",
        W_FEEL_MIN: "",
        W_TEXT: "",
        LIFE_RUN_TEMPLATE: "",
        LIFE_FISH_TEMPLATE: "",
        LIFE_PURPLE_TEMPLATE: "",
        LIFE_AIR_TEMPLATE: "",
    }

    def __init__(self):
        self.get_date()
        self.get_location_id()
        self.get_life()
        self.get_weather()

    def get_date(self):
        now = datetime.now()
        date = now.strftime("%Y-%m-%d")
        today = now.weekday()
        self.FILL[W_DATE] = date
        self.FILL[W_WEEKDAY] = weekday.get(str(today), "未知")

    def get_location_id(self):

        # 如果没有配置省份和城市,查询IP地址接口返回的属地信息
        if self.PROVINCE == "" or self.CITY == "":
            arr = province_city()
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
        self.FILL[W_PROVINCE] = self.PROVINCE
        self.FILL[W_CITY] = self.CITY

    def get_life(self):
        """
        生活指标
        """
        r = requests.get(self.LIFE_API + "type=0&location=" + self.LOCATION_ID + "&key=" + self.KEY)
        r.raise_for_status()
        res = json.loads(r.text)
        for c in res["daily"]:
            desc = c["category"]
            t = c["type"]
            if t == LIFE_RUN_LEVEL:
                self.FILL[LIFE_RUN_TEMPLATE] = desc + LIFE_RUN_TEXT
            elif t == LIFE_FISH_LEVEL:
                self.FILL[LIFE_FISH_TEMPLATE] = desc + LIFE_FISH_TEXT
            elif t == LIFE_PURPLE_LEVEL:
                self.FILL[LIFE_PURPLE_TEMPLATE] = LIFE_PURPLE_TEXT + ": " + desc
            elif t == LIFE_AIR_LEVEL:
                self.FILL[LIFE_AIR_TEMPLATE] = LIFE_AIR_TEXT + ": " + desc

    def get_weather(self):
        """
        天气指标
        """
        r = requests.get(self.WEATHER_API + "location=" + self.LOCATION_ID + "&key=" + self.KEY)
        r.raise_for_status()
        res = json.loads(r.text)
        for w in res["daily"]:
            if w["fxDate"] != self.FILL[W_DATE]:
                continue
            # TODO 区分白天夜间图标
            self.FILL[W_ICON] = w["iconDay"]
            self.FILL[W_TEMP_MAX] = w["tempMax"]
            self.FILL[W_FEEL_MIN] = w["tempMin"]
            self.FILL[W_TEXT] = w["textDay"]
