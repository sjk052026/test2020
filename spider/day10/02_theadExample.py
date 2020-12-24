from threading import Thread


# 线程事件函数
def pares_html():
    print('正在抓取......')


# 创建多线程去执行线程事件函数
t_list = []
for i in range(5):
    t = Thread(target=pares_html)#为什么pares_html不加()
    t_list.append(t)
    t.start()

for t in t_list:
    t.join()