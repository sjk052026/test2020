from selenium import webdriver


class MzbSpider:
    def __init__(self):
        self.options=webdriver.ChromeOptions()
        self.options.add_argument('--headless')

        self.driver = webdriver.Chrome(options=self.options)
        self.driver.get(url='http://www.mca.gov.cn/article/sj/xzqh/2020/')

    def parse_html(self):
        self.driver.find_element_by_partial_link_text('县以上行政区划代码').click()
        all_handles = self.driver.window_handles
        self.driver.switch_to.window(all_handles[1])
        tr_list = self.driver.find_elements_by_xpath('//tr[@height="19"]')
        for tr in tr_list:
            item = {}
            item['code'] = tr.find_element_by_xpath('./td[2]').text.strip()
            item['name'] = tr.find_element_by_xpath('./td[3]').text.strip()
            print(item)

    def run(self):
        self.parse_html()


if __name__ == '__main__':
    spider = MzbSpider()
    spider.run()
