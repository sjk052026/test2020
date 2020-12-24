"""
使用多线程爬取小米应用商店应用信息
"""
import requests
from threading import Thread, Lock
from queue import Queue
import time
from fake_useragent import UserAgent


class XiaomiSpider:
    def __init__(self):
        self.url = 'http://app.mi.com/categotyAllListApi?page={}&categoryId=2&pageSize=30'
        # 队列 锁
        self.url_queue = Queue()
        self.lock = Lock()

    def get_html(self, url):
        """请求功能函数"""
        headers = {'User-Agent': UserAgent().random}
        html = requests.get(url=url, headers=headers).json()
        return html

    def get_total_page(self):
        """获取总页数"""
        html = self.get_html(url=self.url.format(0))
        count = html['count']
        total_page = count // 30 if count % 30 == 0 else count // 30 + 1
        return total_page

    def url_in(self):
        """生成所有要抓取的URL地址,入队列"""
        total_page = self.get_total_page()
        for page in range(0, total_page):
            page_url = self.url.format(page)
            # 入队列
            self.url_queue.put(page_url)

    def parse_html(self):
        """线程事件函数:获取地址+请求+解析+数据处理"""
        while True:
            # 加锁
            self.lock.acquire()
            if not self.url_queue.empty():
                url = self.url_queue.get()
                # 释放锁
                self.lock.release()
                html = self.get_html(url=url)
                for one_app_dict in html['data']:
                    item = {}
                    item['name'] = one_app_dict['displayName']
                    item['type'] = one_app_dict['level1CategoryName']
                    item['link'] = one_app_dict['packageName']
                    print(item)
            else:
                # 释放锁
                self.lock.release()
                break

    def run(self):
        # 先让URL地址入队列
        self.url_in()
        # 创建多线程并执行
        t_list = []
        for i in range(5):
            t = Thread(target=self.parse_html)
            t_list.append(t)
            t.start()

        for t in t_list:
            t.join()


if __name__ == '__main__':
    start_time = time.time()
    spider = XiaomiSpider()
    spider.run()
    end_time = time.time()
    print('time:%.2f' % (end_time - start_time))
