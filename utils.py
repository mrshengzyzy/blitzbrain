import codecs
import re

import requests


def get_province_city():
    """
    获取省名称以及城市名称
    """
    response_text = requests.get("http://ip.lockview.cn/ShowIP.aspx").text
    res = re.findall(r"(&nbsp;&nbsp;)(.*?)省(.*?)市", response_text)
    return res[0][1], res[0][2]


def update_svg(template_file, output_file, output_dict):
    output = codecs.open(template_file, 'r', encoding='utf-8').read()
    for key in output_dict:
        output = output.replace(key, output_dict[key])
    codecs.open(output_file, 'w', encoding='utf-8').write(output)
