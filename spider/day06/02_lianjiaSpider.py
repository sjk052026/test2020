import requests
from lxml import etree
from fake_useragent import UserAgent

url='https://bj.lianjia.com/ershoufang/'
headers={'User-Agent':UserAgent().random}

html=requests.get(url=url,headers=headers).content.decode('Utf-8','ignore')

p=etree.HTML(html)
li_list=p.xpath('//ul[@class="sellListContent"]/li[@class="clear LOGVIEWDATA LOGCLICKDATA"]')
for li in li_list:
    item={}
    name_list=li.xpath('.//div[@class="positionInfo"]/a[1]/text()')
    item['name']=name_list[0].strip() if name_list else None
    address_list=li.xpath('.//div[@class="positionInfo"]/a[2]/text()')
    item['address']=address_list[0].strip() if address_list else None
    info_list=li.xpath('.//div')
    item['info']=info_list[0].strip() if info_list else None

