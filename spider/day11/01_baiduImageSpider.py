"""
程序运行效果如下:
    请输入关键字: 赵丽颖
    把所有赵丽颖的图片保存到 ./赵丽颖/xxx.jpg
"""
import requests
from threading import Thread, Lock
from queue import Queue
import json
import os
from fake_useragent import UserAgent
from urllib import parse


class BaiduImageSpider:
    def __init__(self):
        self.url = 'https://image.baidu.com/search/acjson?tn=resultjson_com&ipn=rj&ct=201326592&is=&fp=result&queryWord={}&cl=2&lm=-1&hd=&latest=&copyright=&ie=utf-8&oe=utf-8&adpicid=&st=-1&z=&ic=0&word={}&s=&se=&tab=&width=&height=&face=0&istype=2&qc=&nc=1&fr=&pn={}&rn=30&gsm=1e&1599728538999='
        # 创建对应目录
        self.word = input('请输入关键字:')
        self.directory = './images/{}/'.format(self.word)
        if not os.path.exists(self.directory):
            os.makedirs(self.directory)
        # 队列 锁
        self.q = Queue()
        self.lock = Lock()
        # 编码
        self.params = parse.quote(self.word)

    def get_html(self, url):
        """功能函数:获取响应内容html"""
        headers = {'User-Agent': UserAgent().random}
        html = requests.get(url=url, headers=headers).content

        return html

    def get_total(self):
        """获取图片总数"""
        url = self.url.format(self.params, self.params, 30)
        html = self.get_html(url=url)
        html = json.loads(html.decode('utf-8', 'ignore'))
        return html['displayNum']

    def url_in(self):
        """生成所有要抓取的URL地址,入队列"""
        total = self.get_total()
        for pn in range(0, total, 30):
            page_url = self.url.format(self.params, self.params, pn)
            # URL地址入队列
            self.q.put(page_url)

    def parse_html(self):
        """线程事件函数:获取地址+请求+解析..."""
        while True:
            self.lock.acquire()
            if not self.q.empty():
                url = self.q.get()
                self.lock.release()
                # 请求提取图片链接
                html = self.get_html(url=url)
                # json.loads():把json格式的字符串转为python数据类型
                html = json.loads(html.decode('utf-8', 'ignore'))
                # [:-1]:把列表中的最后一个空字典给切掉
                for one_img_dict in html['data'][:-1]:
                    try:
                        image_url = one_img_dict['hoverURL']
                        # save_image():保存一张图片到本地
                        self.save_image(image_url)
                    except Exception as e:
                        continue
            else:
                self.lock.release()
                break

    def save_image(self, image_url):
        """保存1张图片到本地"""
        html = self.get_html(image_url)
        # filename: ./images/赵丽颖/232323.jpg
        filename = self.directory + image_url[-30:]
        with open(filename, 'wb') as f:
            f.write(html)
        print(filename, '下载成功')

    def run(self):
        # 1.先让URL地址入队列
        self.url_in()
        # 2.创建多线程并启动线程
        t_list = []
        for i in range(3):
            t = Thread(target=self.parse_html)
            t_list.append(t)
            t.start()

        for t in t_list:
            t.join()


if __name__ == '__main__':
    spider = BaiduImageSpider()
    spider.run()
