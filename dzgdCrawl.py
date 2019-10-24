# -*- coding:utf-8 -*-



import requests
from bs4 import BeautifulSoup
"""
class dzgd_Crawl:

    def __init__(self, username, password):
        self.password = password
        self.username = username
        self.session = requests.session()

        self.startUrl = '42.99.2.28:2003/jsp/login.jsp'


"""


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



#在login中，使用的是post方法







