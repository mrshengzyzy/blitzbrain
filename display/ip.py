#!/usr/bin/python
# -*- coding:utf-8 -*-

import re

import requests

IP_URL = "http://ip.lockview.cn/ShowIP.aspx"


def province_city():
    """
    获取省名称以及城市名称
    """
    response_text = requests.get(IP_URL).text
    res = re.findall(r"(&nbsp;&nbsp;)(.*?)省(.*?)市", response_text)
    return res[0][1], res[0][2]
