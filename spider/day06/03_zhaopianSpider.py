import requests
url='https://ss0.bdstatic.com/70cFvHSh_Q1YnxGkpoWK1HF6hhy/it/u=2301075202,1136565854&fm=26&gp=0.jpg'
headers={'User_Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0) Gecko/20100101 Firefox/6.0'}

html=requests.get(url=url,headers=headers).content

with open('照片.jpg','wb') as f:
    f.write(html)