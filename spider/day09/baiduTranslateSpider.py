"""
js逆向破解百度翻译接口(execjs)
"""
import requests
import execjs

class BaiduTranslateSpider:
    def __init__(self):
        self.post_url = 'https://fanyi.baidu.com/v2transapi?from=en&to=zh'
        self.post_headers = {
            "accept": "*/*",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "zh-CN,zh;q=0.9",
            "content-length": "136",
            "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
            "cookie": "BIDUPSID=DB32AF549B2BC699B21EE639FE10F5C9; PSTM=1600692505; BAIDUID=8048D405258DCAF62CA8CBA66FEC43FB:FG=1; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; REALTIME_TRANS_SWITCH=1; FANYI_WORD_SWITCH=1; HISTORY_SWITCH=1; SOUND_SPD_SWITCH=1; SOUND_PREFER_SWITCH=1; delPer=0; PSINO=2; Hm_lvt_64ecd82404c51e03dc91cb9e8c025574=1601037875,1601127236; Hm_lpvt_64ecd82404c51e03dc91cb9e8c025574=1601127248; __yjsv5_shitong=1.0_7_f03d7d370bbdccb9e8fec2b0430b6451dc4b_300_1601127246315_103.102.194.226_af2c339d; yjs_js_security_passport=413026a3d3342315dde4cadb1c40587d1151cab4_1601127247_js; H_PS_PSSID=32617_1456_32736_7542_31660_32723_32231_7516_32115_32718",
            "origin": "https://fanyi.baidu.com",
            "referer": "https://fanyi.baidu.com/",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36",
            "x-requested-with": "XMLHttpRequest",
        }

    def get_sign(self, word):
        """获取sign"""
        with open('translate.js', 'r') as f:
            js_code = f.read()
        # 利用execjs模块获取sign
        js_obj = execjs.compile(js_code)
        sign = js_obj.eval('e("{}")'.format(word))

        return sign

    def attack_bd(self, word):
        """爬虫逻辑函数"""
        sign = self.get_sign(word)
        data = {
            "from": "en",
            "to": "zh",
            "query": word,
            "transtype": "realtime",
            "simple_means_flag": "3",
            "sign": sign,
            "token": "3e7d09995ce56f82e32837ab8047d7fe",
            "domain": "common",
        }
        html = requests.post(url=self.post_url, data=data, headers=self.post_headers).json()

        return html['trans_result']['data'][0]['dst']

    def run(self):
        word = input('请输入要翻译的单词:')
        result = self.attack_bd(word)
        print(result)

if __name__ == '__main__':
    spider = BaiduTranslateSpider()
    spider.run()

































