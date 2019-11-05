# -*- coding:utf-8 -*-



import requests
from bs4 import BeautifulSoup

class dzgd_Crawl:

    def __init__(self, username, password):
        self.password = password
        self.username = username
        self.session = requests.session()
        self.startUrl = '42.99.2.28:2003/jsp/login.jsp'

        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
            'Accept-Encoding': 'gzip, deflate'

        }





headers = {
    'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36',
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    'Accept-Encoding': 'gzip, deflate'

}

s = requests.session()
redirectUrl = 'http://42.99.2.28:2003/login/login_oauth.do'
request_url ='http://202.97.1.50:8082/oauth/authorize?response_type=code&client_id=QIE479IlXusBDvontwk1Xw==&redirect_uri='+redirectUrl+'&scope=read+write&state=xyz'
headers = {
    'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36',
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    'Accept-Encoding': 'gzip, deflate',
}
r = s.get(url=request_url,headers=headers)
htm = r.content
#这时候到了login界面了

soup = BeautifulSoup(htm, 'lxml')

hidden_list = soup.find_all(type="hidden")

ts = hidden_list[0]['value']

clientId = hidden_list[1]['value']
#在login中，使用的是post方法

userName = '13301169107'
password = 'gyn649@ERT'

login_url = 'http://202.97.1.50:8082/dologin'

data = {
    'userName': userName,
    'password': password,
    'ts': ts,
    'clientId': clientId
}


req = s.post(url=login_url,data=data)

data1 ={
    'user_oauth_approval':True
}


r2 = s.post(url= 'http://202.97.1.50:8082/oauth/authorize',data = data1)


r3 = s.get(url='http://42.99.2.28:2003/wstrans/getwstransdetailurl.do?wsid=2019101000141&_=1572934950933')

print(r3.text)


