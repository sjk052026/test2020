import requests
import time
from fake_useragent import UserAgent


class ProxyPool:
    def __init__(self):
        self.api_url = 'http://dps.kdlapi.com/api/getdps/?orderid=910094925849799&num=20&pt=1&sep=1'  # 代理链接地址
        self.test_url='http://httpbin.org/get'
        self.headers = {'User-Agent': UserAgent().random}

    def get_proxy(self):
        html = requests.get(url=self.api_url, headers=self.headers).content.decode('utf-8', 'ignore')
        proxy_list=html.split('\r\n')
        for proxy in proxy_list:
            self.test_proxy(proxy)

    def test_proxy(self,proxy):
        proxies={
            'http':'http://309435365:szayclhp@{}'.format(proxy),
            'https':'https://309435365:szayclhp@{}'.format(proxy),
        }
        try:
            resp=requests.get(url=self.test_url,proxies=proxies,headers=self.headers,timeout=3)
            if resp.status_code == 200:
                print(proxy,'可用')
            else:
                print(proxy,'不可用')
        except Exception as e:
            print(proxy,'不可用')

    def run(self):
        self.get_proxy()

if __name__ == '__main__':
    spider=ProxyPool()
    spider.run()