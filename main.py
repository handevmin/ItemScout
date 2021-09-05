
# Initializing
import json

import requests
import pprint

import scrapy


# Setting URL
url = 'https://domeggook.com/ssl/api/'

# Setting Request Parameters
param = dict()
param['ver'] = '4.0'
param['mode'] = 'getItemList'
param['aid'] = '92c50b182ecd3d3ca86d14d87b554e62'
param['market'] = 'dome'
param['om'] = 'json'
param['kw'] = '마스크' # 검색어


# Getting API Response
res = requests.get(url, params=param)

# Parsing
data = json.loads(res.content)

print(data['domeggook']['list']['item'])
pprint.pprint(data['domeggook']['list']['item'])