from selenium import webdriver
import time

url = 'https://maoyan.com/board/4'

#设置无界面模式
options=webdriver.ChromeOptions()
options.add_argument('--headless')

browser = webdriver.Chrome(options=options)
browser.get(url)

def get_data():
    # 基准xpath: [<selenium xxx li at xxx>,<selenium xxx li at>]
    li_list = browser.find_elements_by_xpath('//*[@id="app"]/div/div/div[1]/dl/dd')
    for li in li_list:
        item = {}
        # info_list: ['1', '霸王别姬', '主演：张国荣', '上映时间：1993-01-01', '9.5']
        info_list = li.text.split('\n')
        item['number'] = info_list[0]
        item['name'] = info_list[1]
        item['star'] = info_list[2]
        item['time'] = info_list[3]
        item['score'] = info_list[4]

        print(item)

while True:
    get_data()
    try:
        browser.find_element_by_link_text('下一页').click()
        time.sleep(2)
    except Exception as e:
        print('恭喜你!抓取结束')
        browser.quit()
        break