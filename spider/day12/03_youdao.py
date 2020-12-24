from selenium import webdriver
driver=webdriver.Chrome()
driver.get(url='http://fanyi.youdao.com/')
driver.find_element_by_xpath('//*[@id="inputOriginal"]').send_keys('魔法')
driver.find_element_by_xpath('//*[@id="transMachine"]').click()