import requests
import time
from lxml import etree
from fake_useragent import UserAgent
import random



class IpSpider:
    def __init__(self):
        self.url = 'https://www.kuaidaili.com/free/inha/{}/'
        self.test_url = 'http://httpbin.org/get'
        self.headers = {'User_Agent': UserAgent().random}
        self.f = open('proxy.txt', 'a')

    def get_html(self, url):
        html = requests.get(url=url, headers=self.headers).content.decode('utf-8', 'ignore')

        return html

    def xpath_func(self, html, x):
        p = etree.HTML(html)
        r_list = p.xpath(x)

        return r_list

    def parse_html(self, url):
        html = self.get_html(url)
        tr_x = '//table/tbody//tr'
        tr_list = self.xpath_func(html, tr_x)
        for table in tr_list:
            ip = table.xpath('.//td[1]/text()')[0]
            port = table.xpath('.//td[2]/text()')[0]
            proxies = {
                'http': 'http://{}:{}'.format(ip, port),
                'https': 'https://{}:{}'.format(ip, port)
            }
            try:
                resp = requests.get(url=self.test_url, proxies=proxies, headers=self.headers, timeout=2)
                if resp.status_code == 200:
                    print(ip + ':' + port, '\033[31m可用\033[0m')
                    self.f.write(ip + ':' + port + '\n')
                else:
                    print(ip + ':' + port, '不可用')

            except Exception as e:
                print(ip + ':' + port, '不可用')

    def run(self):
        for page in range(1, 3650):
            url = self.url.format(page)
            time.sleep(random.randint(1, 2))
            self.parse_html(url)

        self.f.close()


if __name__ == '__main__':
    spider = IpSpider()
    spider.run()
