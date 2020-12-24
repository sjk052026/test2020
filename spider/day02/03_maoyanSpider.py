import re
import requests
import time
import random



class MaoyanSpider:
    def __init__(self):
        self.url='https://maoyan.com/board/4?offset={}'
        self.headers={
            'Cookie':'__mta=209015469.1600347046424.1600350059264.1600350778307.11; uuid_n_v=v1; uuid=644978B0F8E411EA805853CB23A5B1A2B3D9BB7FCDE94493A899A28858E63A98; _csrf=1c299f3164912e34245229d1af68a0d1cd5f64c5626f341cd9bd212d78530642; Hm_lvt_703e94591e87be68cc8da0da7cbd0be2=1600347046; Hm_lpvt_703e94591e87be68cc8da0da7cbd0be2=1600350777; _lx_utm=utm_source%3DBaidu%26utm_medium%3Dorganic; _lxsdk_cuid=1749c1dff0ec8-0b717be9a38f46-77246753-1cc500-1749c1dff0fc8; _lxsdk=644978B0F8E411EA805853CB23A5B1A2B3D9BB7FCDE94493A899A28858E63A98; __mta=209015469.1600347046424.1600347046424.1600347047237.2; mojo-uuid=4ddb772bd23df9c6f2ddd5a04a683646; mojo-trace-id=6; mojo-session-id={"id":"34869316f928bc033cf04a9b71771307","time":1600349168477}; _lxsdk_s=1749c3e636b-51e-a37-461%7C%7C7',
            'User-Agent':'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:71.0) Gecko/20100101 Firefox/71.0'
        }

    def get_html(self,url):
        html=requests.get(url=url,headers=self.headers).text
        self.parse_html(html)

    def parse_html(self,html):
        """正则解析函数"""
        regex = '<div class="movie-item-info">.*?title="(.*?)".*?<p class="star">(.*?)</p>.*?<p class="releasetime">(.*?)</p>'
        pattern=re.compile(regex,re.S)
        r_list=pattern.findall(html)
        self.save_html(r_list)

    def save_html(self,r_list):
        """数据处理的函数"""
        for r in r_list:
            print(r,'++++++')
            item={}
            item['name']=r[0].strip()
            item['star']=r[1].strip()
            item['time']=r[2].strip()
            print(item)

    def run(self):
        """程序的入口函数"""
        for offset in range(0,91,10):
            page_url=self.url.format(offset)
            #开始进行数据抓取
            self.get_html(url=page_url)
            time.sleep(random.randint(1,2))

if __name__ == '__main__':
    spider=MaoyanSpider()
    spider.run()