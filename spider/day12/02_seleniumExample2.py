from selenium import webdriver
driver=webdriver.Chrome()
driver.get(url='http://www.baidu.com/')
driver.find_element_by_xpath('//*[@id="kw"]').send_keys('赵丽颖')
driver.find_element_by_xpath('//*[@id="su"]').click()
driver.quit()