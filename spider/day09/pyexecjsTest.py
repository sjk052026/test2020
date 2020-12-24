"""
功能:执行translate.js中的js代码
"""
import execjs

with open('translate.js', 'r') as f:
    js_code = f.read()

# 1.创建编译对象
js_obj = execjs.compile(js_code)
# 2.执行js代码,eval:把一个字符串当做表达式来执行
sign = js_obj.eval('e("hello")')

print(sign)
