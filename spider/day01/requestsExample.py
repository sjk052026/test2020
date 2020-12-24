"""
向京东官网发请求,拿到响应内容
"""
import requests

# get():发请求,得到响应对象
resp = requests.get(url='https://www.jd.com/')
# 1.text属性:获取响应内容-字符串
html = resp.text
# 2.content属性:获取响应内容-bytes 爬取图片 文件 视频....
html = resp.content
# 3.status_code属性:获取HTTP响应码
code = resp.status_code
# 4.url:获取返回实际数据的URL地址
url = resp.url
print(code,url)
