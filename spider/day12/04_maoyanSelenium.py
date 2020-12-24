"""
使用selenium抓取猫眼电影top100
"""
from selenium import webdriver

# 1.打开浏览器,进入猫眼电影页面
driver = webdriver.Chrome()
driver.get(url='https://maoyan.com/board/4')
# 2.提取10个电影信息的dd节点对象列表
# dd_list:[<>,<>,<>,...,<>]

def parse_html():
    dd_list = driver.find_elements_by_xpath('//*[@id="app"]/div/div/div[1]/dl/dd')
    for dd in dd_list:
        # text属性:获取当前节点以及子节点和后代节点文本内容
        film_info_list = dd.text.split('\n')
        item = {}
        item['rank'] = film_info_list[0]
        item['name'] = film_info_list[1]
        item['star'] = film_info_list[2]
        item['time'] = film_info_list[3]
        item['score'] = film_info_list[4]
        print(item)

while True:
    parse_html()
    try:
        # 当找不到文本内容为"下一页"的a节点时,会抛出异常
        driver.find_element_by_link_text('下一页').click()
    except:
        driver.quit()
        break
