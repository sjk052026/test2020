from selenium import webdriver

options = webdriver.ChromeOptions()
options.add_argument('--headless')
driver = webdriver.Chrome(options=options)
driver.get(url='https://music.163.com/#/discover/toplist')
driver.switch_to.frame("contentFrame")
tr_list = driver.find_elements_by_xpath('//table/tbody/tr')
print(tr_list)
for tr in tr_list:
    item={}
    item['rank']=tr.find_element_by_xpath('.//span[@class="num"]').text.strip()
    item['name']=tr.find_element_by_xpath('.//span[@class="txt"]/a/b').get_attribute('title').replace('\xa0',' ')
    item['time']=tr.find_element_by_xpath('.//span[@class="u-dur "]').text.strip()
    item['star']=tr.find_element_by_xpath('.//div[@class="text"]/span').get_attribute('title')
    print(item)

