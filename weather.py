#!/usr/bin/python
# -*- coding:utf-8 -*-

import datetime

output_dict = {
    'TIME_NOW': datetime.datetime.now().strftime("%M:%S"),
    'DAY_ONE': datetime.datetime.now().strftime("%Y-"),
    'DAY_NAME': datetime.datetime.now().strftime("%A"),
}

print(output_dict['TIME_NOW'])
print(output_dict['DAY_ONE'])
print(output_dict['DAY_NAME'])
