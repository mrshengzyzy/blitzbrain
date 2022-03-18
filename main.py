#!/usr/bin/python
# -*- coding:utf-8 -*-

import codecs

from display.weather import *


def update_svg(template_file, output_file, output_dict):
    output = codecs.open(template_file, 'r', encoding='utf-8').read()
    for key in output_dict:
        output = output.replace(key, output_dict[key])
    codecs.open(output_file, 'w', encoding='utf-8').write(output)


def main():
    # 天气
    w = QWeather()
    print(w.FILL)
    # template = 'weather-template.svg'
    # out = 'weather-out.svg'
    # utils.update_svg(template, out, w.FILL)


if __name__ == "__main__":
    main()
