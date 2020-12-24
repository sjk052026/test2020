import requests
from lxml import etree
from hashlib import md5

url = 'http://www.biquge.info/32_32050/'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0) Gecko/20100101 Firefox/6.0'}

html = requests.get(url=url, headers=headers).content.decode('utf-8', 'ignore')

p = etree.HTML(html)
r_list = p.xpath('//div[@id="list"]/dl//dd[1]/a/@href')
print(r_list)
for href in r_list:
    two_url = 'http://www.biquge.info/32_32050/' + href
    print(two_url)
    two_html=requests.get(url=two_url, headers=headers).content.decode('utf-8', 'ignore')
    new_p = etree.HTML(two_html)
    story_info = new_p.xpath('//div[@id="content"]/text()')
    for item in story_info:
        print(item)
