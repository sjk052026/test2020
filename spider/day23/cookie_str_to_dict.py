cook_str='OUTFOX_SEARCH_USER_ID=697437109@10.108.160.105; OUTFOX_SEARCH_USER_ID_NCOO=1284502988.9058187; JSESSIONID=aaadiY4jrpsFRdQ-8lqvx; ___rl__test__cookies=1603368128857'
cookies={}
for kv in cook_str.split('; '):
    key = kv.split('=')[0]
    value=kv.split('=')[1]
    cookies[key]=value