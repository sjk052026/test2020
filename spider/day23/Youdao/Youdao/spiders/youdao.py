# -*- coding: utf-8 -*-
import scrapy
import time
from hashlib import md5
import json
import random
from ..items import YoudaoItem


class YoudaoSpider(scrapy.Spider):
    name = 'youdao'
    allowed_domains = ['fanyi.youdao.com']
    post_url = 'http://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule'
    word = input('请输入要翻译的单词:')

    def start_requests(self):
        formdata = self.get_formdata()
        yield scrapy.FormRequest(url=self.post_url, formdata=formdata, callback=self.parse)

    def get_formdata(self):
        # 获取ts salt sign
        ts = str(int(time.time() * 1000))
        salt = ts + str(random.randint(0, 9))
        string = "fanyideskweb" + self.word + salt + "]BjuETDhU)zqSxf-=B#7m"
        s = md5()
        s.update(string.encode())
        sign = s.hexdigest()
        # 处理form表单数据
        formdata = {
            "i": self.word,
            "from": "AUTO",
            "to": "AUTO",
            "smartresult": "dict",
            "client": "fanyideskweb",
            "salt": salt,
            "sign": sign,
            "lts": ts,
            "bv": "de08f04bd24b4655cf8f1a0a45286dfa",
            "doctype": "json",
            "version": "2.1",
            "keyfrom": "fanyi.web",
            "action": "FY_BY_REALTlME",
        }

        return formdata


    def parse(self, response):
        html = json.loads(response.text)
        item = YoudaoItem()
        item['result'] = html['translateResult'][0][0]['tgt']
        yield item
