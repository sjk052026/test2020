from selenium import webdriver

driver = webdriver.Chrome()
driver.get(url='https://mail.163.com/')
ifram_node = driver.find_element_by_xpath('//div[@class="loginUrs"]/iframe')
driver.switch_to.frame(ifram_node)
driver.find_element_by_name("email").send_keys('sjk2020')
driver.find_element_by_name("password").send_keys('123456')
driver.find_element_by_link_text('登  录').click()