"""
selenium操作鼠标
打开百度,鼠标移动到设置节点,点击高级搜索
"""
from selenium import webdriver
# 导入鼠标事件类
from selenium.webdriver import ActionChains

# 1.打开浏览器输入百度地址
driver = webdriver.Chrome()
driver.maximize_window()
driver.get(url='http://www.baidu.com/')
# 2.找到 设置 节点
set_node = driver.find_element_by_xpath('//*[@id="s-usersetting-top"]')
# 3.移动鼠标到设置节点
ActionChains(driver).move_to_element(to_element=set_node).perform()

# 4.找到 高级搜索 节点,并点击
driver.find_element_by_link_text('高级搜索').click()
