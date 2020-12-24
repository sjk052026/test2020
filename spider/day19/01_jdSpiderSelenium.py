"""
selenium抓取京东指定商品的数据
抓取数据：
    商品名称
    商品价格
    商品评价
    商品价格
"""
from selenium import webdriver
import time
import pymongo

class JdSpider:
    def __init__(self):
        # 设置无界面模式
        self.options = webdriver.ChromeOptions()
        self.options.add_argument('--headless')
        self.driver = webdriver.Chrome(options=self.options)
        self.driver.get(url='https://www.jd.com/')
        # 连接mongodb数据库
        self.conn = pymongo.MongoClient('localhost', 27017)
        self.db = self.conn['jdshopdb']
        self.myset = self.db['jdshopset']
        # 找到 搜索框 + 按钮 做对应操作
        self.driver.find_element_by_xpath('//*[@id="key"]').send_keys('爬虫书')
        self.driver.find_element_by_xpath('//*[@id="search"]/div/div[2]/button').click()
        # 最好休眠一下
        time.sleep(1)

    def parse_html(self):
        """解析提取数据"""
        # 先执行JS脚本,让所有数据都加载
        self.driver.execute_script(
            'window.scrollTo(0,document.body.scrollHeight)'
        )
        time.sleep(2)
        # 提取具体数据
        li_list = self.driver.find_elements_by_xpath('//*[@id="J_goodsList"]/ul/li')
        for li in li_list:
            item = {}
            try:
                item['price'] = li.find_element_by_xpath('.//div[@class="p-price"]/strong').text.strip()
                item['name'] = li.find_element_by_xpath('.//div[@class="p-name"]/a').text.strip()
                item['commit'] = li.find_element_by_xpath('.//div[@class="p-commit"]/strong').text.strip()
                item['shop'] = li.find_element_by_xpath('.//div[@class="p-shopnum"]/a | .//div[@class="p-shopnum"]/span').text.strip()
                print(item)
                # 存入mongodb数据库
                self.myset.insert_one(item)
            except Exception as e:
                print(e)

    def run(self):
        while True:
            self.parse_html()
            # 返回值-1：说明未找到,不是最后一页
            if self.driver.page_source.find('pn-next disabled') == -1:
                self.driver.find_element_by_xpath('//*[@id="J_bottomPage"]/span[1]/a[9]').click()
                # 最好也要休眠一下
                time.sleep(0.5)
            else:
                self.driver.quit()
                break

if __name__ == '__main__':
    spider = JdSpider()
    spider.run()
