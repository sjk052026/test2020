import requests
from lxml import etree
from fake_useragent import UserAgent
import random

url='https://tieba.baidu.com/p/6966169466'
headers={'User_Agent':UserAgent().random}

html=requests.get(url=url,headers=headers).content.decode('utf-8','ignore')
p=etree.HTML(html)
src=p.xpath('//div[@class="video_src_wrapper"]/embed/@data-video')[0].strip()

html=requests.get(url=src,headers=headers).content

with open('海贼王01.mp4','wb') as f:
    f.write(html)