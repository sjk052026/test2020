import requests

from urllib import parse

word = input("请输入搜索关键字:")

params = parse.urlencode({'wd': word})

url = 'https://www.baidu.com/s?{}'.format(params)

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0) Gecko/20100101 Firefox/6.0'}

html = requests.get(url=url, headers=headers).text

filename = '{}.html'.format(word)

with open(filename, 'w', encoding='utf-8') as f:
    f.write(html)
