import requests
from urllib import parse
import time
import random


class TiebaSpider:
    def __init__(self):
        """定义常用变量"""
        self.url = 'http://tieba.baidu.com/f?kw={}&pn={}'
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0) Gecko/20100101 Firefox/6.0'}

    def get_html(self, url):
        """请求获取响应内容"""
        html = requests.get(url=url, headers=self.headers).text
        return html

    def parse_html(self):
        """解析提取数据"""
        pass

    def save_html(self, filename, html):
        """数据处理"""
        with open(filename, 'w') as f:
            f.write(html)

    def run(self):
        """程序入口函数"""
        name = input('请输入贴吧名:')
        start = int(input('请输入起始页:'))
        end = int(input('请输入终止页:'))
        params = parse.quote(name)
        for page in range(start, end + 1):
            pn = (page - 1) * 50
            page_url = self.url.format(params, pn)
            # 请求 解析 数据处理
            html = self.get_html(url=page_url)
            filename='{}_第{}页.html'.format(name,page)
            self.save_html(filename,html)
            time.sleep(random.randint(1,2))
            print('第',page,'抓取成功')


if __name__ == '__main__':
    spider = TiebaSpider()
    spider.run()

