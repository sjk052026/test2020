import requests
import time
import random
from hashlib import md5


class YdSpider:
    def __init__(self):
        # url:一定是F12抓包抓到的Request URL
        self.url = 'http://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule'
        self.headers = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'keep-alive',
            'Content-Length': '236',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Cookie': 'OUTFOX_SEARCH_USER_ID=880519449@10.108.160.18; OUTFOX_SEARCH_USER_ID_NCOO=889709608.3119488; JSESSIONID=aaaxRa8Gn7_M1-t10uftx; ___rl__test__cookies=1601038427490',
            'Host': 'fanyi.youdao.com',
            'Origin': 'http://fanyi.youdao.com',
            'Referer': 'http://fanyi.youdao.com/',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest',
        }

    def get_ts_salt_sign(self, word):
        # 获取 ts salt sign
        ts = str(int(time.time() * 1000))
        salt = ts + str(random.randint(0, 9))
        # sign
        string = "fanyideskweb" + word + salt + "]BjuETDhU)zqSxf-=B#7m"
        s = md5()
        s.update(string.encode())
        sign = s.hexdigest()

        return ts, salt, sign

    def attack_yd(self, word):
        # 获取到ts salt sign
        ts, salt, sign = self.get_ts_salt_sign(word)
        data = {
            'i': word,
            'from': 'AUTO',
            'to': 'AUTO',
            'smartresult': 'dict',
            'client': 'fanyideskweb',
            'salt': salt,
            'sign': sign,
            'lts': ts,
            'bv': '94ef9c063d6b2a801fab916722d70203',
            'doctype': 'json',
            'version': '2.1',
            'keyfrom': 'fanyi.web',
            'action': 'FY_BY_REALTlME',
        }
        #.json():把json格式的字符串转为了Python数据类型
        html = requests.post(url=self.url, data=data, headers=self.headers).json()

        return html['translateResult'][0][0]['tgt']

    def run(self):
        word = input('请输入需要翻译的单词:')
        print(self.attack_yd(word))

if __name__ == '__main__':
    spider=YdSpider()
    spider.run()