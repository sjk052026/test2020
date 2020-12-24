import requests
from lxml import etree

word=input('请输入要翻译的单词:')
url='http://m.youdao.com/translate'
data={
    'inputtext': word,
    'type': 'AUTO'
}
html=requests.post(url=url,data=data).text
print(html)
p=etree.HTML(html)
result=p.xpath('//ul[@id="translateResult"]/li/text()')[0].strip()
print(result)