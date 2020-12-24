"""
抓取腾讯招聘指定类别下的所有职位信息
"""
import requests
from threading import Thread, Lock
from queue import Queue
from fake_useragent import UserAgent
from urllib import parse


class TencentSpider:
    def __init__(self):
        self.one_url = 'https://careers.tencent.com/tencentcareer/api/post/Query?timestamp=1563912271089&countryId=&cityId=&bgIds=&productId=&categoryId=&parentCategoryId=&attrId=&keyword={}&pageIndex={}&pageSize=10&language=zh-cn&area=cn'
        self.two_url = 'https://careers.tencent.com/tencentcareer/api/post/ByPostId?timestamp=1563912374645&postId={}&language=zh-cn'
        # 队列
        self.one_q = Queue()
        self.two_q = Queue()
        # 锁
        self.lock1 = Lock()
        self.lock2 = Lock()

    def get_html(self, url):
        headers = {'User_Agent': UserAgent().random}
        html = requests.get(url=url, headers=headers).json()
        return html

    def get_total_page(self, params):
        """获取总页数"""
        url = self.one_url.format(params, 1)
        html = self.get_html(url=url)
        count = html['Data']['Count']
        total_page = count // 10 if count % 10 == 0 else count // 10 + 1
        return total_page

    def url_in(self):
        """生成一级页面URL地址,入队列"""
        keyword = input('请输入关键字:')
        params = parse.quote(keyword)
        # 获取总页数
        total_page = self.get_total_page(params)
        # 生成所有页的URL地址,入队列
        for index in range(1, total_page + 1):
            page_url = self.one_url.format(params, index)
            self.one_q.put(page_url)

    def parse_one_page(self):
        """一级页面线程事件函数"""
        # 提取postid,拼接详情页地址,入二级队列
        while True:
            self.lock1.acquire()
            if not self.one_q.empty():
                one_url = self.one_q.get()
                self.lock1.release()
                one_html = self.get_html(url=one_url)
                # 从one_html中提取10个postid的值
                for one_job_dict in one_html['Data']['Posts']:
                    post_id = one_job_dict['PostId']
                    # 拼接详情页的URL地址,并入二级队列
                    two_url = self.two_url.format(post_id)
                    self.two_q.put(two_url)
            else:
                self.lock1.release()
                break

    def parse_two_page(self):
        """二级页面线程事件函数"""
        # 提取职位的具体信息,打印输出
        while True:
            self.lock2.acquire()
            try:
                two_url = self.two_q.get(timeout=2)
                self.lock2.release()
                # 发请求 提取具体数据
                two_html = self.get_html(url=two_url)
                item = {}
                item['name'] = two_html['Data']['RecruitPostName']
                item['type'] = two_html['Data']['CategoryName']
                item['address'] = two_html['Data']['LocationName']
                item['time'] = two_html['Data']['LastUpdateTime']
                item['require'] = two_html['Data']['Requirement']
                item['resp'] = two_html['Data']['Responsibility']
                print(item)
            except:
                self.lock2.release()
                break

    def run(self):
        self.url_in()
        t1_list = []
        for i in range(2):
            t1 = Thread(target=self.parse_one_page)
            t1_list.append(t1)
            t1.start()

        t2_list = []
        for i in range(2):
            t2 = Thread(target=self.parse_two_page)
            t2_list.append(t2)
            t2.start()

        for t1 in t1_list:
            t1.join()

        for t2 in t2_list:
            t2.join()

if __name__ == '__main__':
    spider=TencentSpider()
    spider.run()
