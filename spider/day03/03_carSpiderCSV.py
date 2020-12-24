import requests
import re
import time
import random
import csv


class CarSpider:
    def __init__(self):
        self.url = 'https://www.che168.com/shanghai/a0_0msdgscncgpi1lto1csp{}exx0/'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.3; .NET4.0C; .NET4.0E)'}
        self.f = open('car.csv', 'w')
        self.writer = csv.writer(self.f)

    def get_html(self, url):
        html = requests.get(url=url, headers=self.headers).text
        self.parse_html(html)

    def parse_html(self, html):
        regex = '<div class="cards-bottom">.*?<h4 class="card-name">(.*?)</h4>.*?<p class="cards-unit">(.*?)</p>.*?<span class="pirce"><em>(.*?)</em>'
        pattern = re.compile(regex, re.S)
        car_list=pattern.findall(html)
        self.save_html(car_list)

    def save_html(self,car_list):
        for car in car_list:
            li=[
                car[0].strip(),
                car[1].strip(),
                car[2].strip()
            ]
            self.writer.writerow(li)
            print(li)

    def run(self):
        for page in range(1,6):
            page_url=self.url.format(page)
            self.get_html(url=page_url)
            time.sleep(random.randint(1,2))
        self.f.close()

if __name__ == '__main__':
    spider=CarSpider()
    spider.run()
