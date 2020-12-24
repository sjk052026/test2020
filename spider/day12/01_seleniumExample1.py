"""
打开浏览器,输入百度的URL地址
"""
# 导入selenium的webdriver接口
from selenium import webdriver

# 打开浏览器-创建浏览器对象
driver = webdriver.Chrome()
# 输入url地址
driver.get(url='http://www.baidu.com/')

#1.save_screenshot():保存屏幕截图
driver.save_screenshot('baidu.png')
#2.page_source:获取HTML源代码
html=driver.page_source
#3.
code=driver.page_source.find('su')
#4.
driver.maximize_window()