"""
示例代码:豆瓣图书top250,只抓取第1页
"""
import requests
from lxml import etree

# 1.定义常用变量
url = 'https://book.douban.com/top250?icn=index-book250-all'
headers = {'User-Agent':'Mozilla/5.0'}

# 2.发请求获取响应内容
html = requests.get(url=url, headers=headers).content.decode('utf-8', 'ignore')

# 3.xpath解析
p = etree.HTML(html)
# 基准xpath,匹配所有书的table节点对象列表
# table_list:[<>,<>,<>,...<>]
table_list = p.xpath('//div[@class="indent"]/table')
for table in table_list:
    item = {}
    item['name'] = table.xpath('.//div[@class="pl2"]/a/@title')[0].strip()
    item['info'] = table.xpath('.//p[@class="pl"]/text()')[0].strip()
    item['score'] = table.xpath('.//span[@class="rating_nums"]/text()')[0].strip()
    item['commit'] = table.xpath('.//span[@class="pl"]/text()')[0].strip()
    item['comment'] = table.xpath('.//span[@class="inq"]/text()')[0].strip()

    print(item)
