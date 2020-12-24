import requests
from lxml import etree

url='https://tieba.baidu.com/p/6865801940'
headers={'User_Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0) Gecko/20100101 Firefox/6.0'}

html=requests.get(url=url,headers=headers).content.decode('utf-8','ignore')
p=etree.HTML(html)
src=p.xpath('//div[@class="video_src_wrapper"]/embed/@data-video')[0].strip()

html=requests.get(url=src,headers=headers).content

with open('shipin.mp4','wb') as f:
    f.write(html)