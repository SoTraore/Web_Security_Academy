import requests
import sys
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies =  {'http':'http://127.0.0.1:8087', 'https':'http://127.0.0.1:8087'}

def sqli_exploit(url) :
    
    # password = ""
    
    # payload = ""
    # cookies = {"session": "HJ1KpuNxLiPhF9CZOsbW72yC6tyEIb9A", "TrackingId":"Q4gMYceQNFk5eAXe"+payload}
    
    # r = requests.get(url, cookies=cookies, proxies=proxies, verify=False)
    
    # return password
    pass


def main() :
    try :
        url = sys.argv[1].strip()
        uri = sys.argv[2].strip()
        payload = sys.argv[3].strip()
    except IndexError :
        print('[+] Usage: %s <url>' % sys.argv[0])
        print('[+] Example: %s www.example.com' % sys.argv[0])
        
    # password = sqli_exploit(url)

if __name__ == '__main__' :
    main()