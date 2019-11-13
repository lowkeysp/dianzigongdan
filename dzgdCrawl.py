# -*- coding:utf-8 -*-



import requests
from bs4 import BeautifulSoup
import telnetlib
import time
import re

class dzgd_Crawl:

    def __init__(self, dzgdID):
        self.password = 'gyn649@ERT'
        self.username = '13301169107'
        self.session = requests.session()
        self.login_url = 'http://202.97.1.50:8082/dologin'
        self.redirectUrl = 'http://42.99.2.28:2003/login/login_oauth.do'
        self.request_url = 'http://202.97.1.50:8082/oauth/authorize?response_type=code&client_id=QIE479IlXusBDvontwk1Xw==&redirect_uri=' + self.redirectUrl + '&scope=read+write&state=xyz'
        self.authorize_url = 'http://202.97.1.50:8082/oauth/authorize'
        self.dzgdID = dzgdID

        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
            'Accept-Encoding': 'gzip, deflate'
        }

    def login(self):

        #登陆到login页面
        r_login_page = self.session.get(url= self.request_url,headers = self.headers)
        htm = r_login_page.content
        soup = BeautifulSoup(htm, 'lxml')
        #解析获得ts和clientID这两个hidden类的值
        hidden_list = soup.find_all(type="hidden")
        ts = hidden_list[0]['value']
        clientId = hidden_list[1]['value']
        #构建post的参数
        data = {
            'userName': self.username,
            'password': self.password,
            'ts': ts,
            'clientId': clientId
        }
        # 填写账号密码，登陆
        self.session.post(url=self.login_url, data=data)
        data ={
            'user_oauth_approval':True
        }
        self.session.post(url=self.authorize_url, data=data)
        #经过上述的登陆，已经登陆成功了，下面是获得工单对应的IP地址和端口
        dzgd_Url = 'http://42.99.2.28:2003/wstrans/getwstransdetailurl.do?wsid='+ self.dzgdID +'&_=1572934950933'
        request_detail = self.session.get(url= dzgd_Url)
        return request_detail.text


    # 用来解析得到A端和Z端的IP地址和端口
    def parser(self,request_detail_text):

        soup = BeautifulSoup(request_detail_text, 'lxml')
        tr_tag = soup.find_all(name='tr', class_="formtext")
        #分别得到A，Z的tr tag
        A_end_tag = tr_tag[3]
        Z_end_tag = tr_tag[6]
        #获得A端信息
        A_end_port = A_end_tag.find_all('td')[5].string
        A_end_IP = A_end_tag.find_all('td')[7].string
        #获得Z端信息
        Z_end_port = Z_end_tag.find_all('td')[5].string
        Z_end_IP = Z_end_tag.find_all('td')[7].string
        return str(A_end_IP), str(A_end_port), str(Z_end_IP), str(Z_end_port)

    #用来使用telnet登陆设备，获取每个设备的状态
    #注意，IP和port必须是二进制的
    def status(self, IP, port):
        if(IP == b'None'):
            return
        #登陆到了设备

        tel_user = b'jt_sunpeng2019'
        tel_pwd = b'Sunpeng,./123'
        tn = telnetlib.Telnet(IP, port=23, timeout=20)
        tn.read_until(b'Username:')
        time.sleep(1)
        tn.write(tel_user + b'\n')
        time.sleep(1)
        tn.read_until(b'Password:')
        time.sleep(1)
        tn.write(tel_pwd + b'\n')
        time.sleep(1)
        #判断使用什么命令
        bytesTemp = tn.read_very_eager()
        strContext = bytesTemp.decode('utf-8')
        command_line = b''
        finish = b''
        #使用display interface的
        display_pattern = '>$'
        if(re.search(display_pattern,strContext)  != None):
            command_line = b'display interface ' + port + b'\n'
            finish = b'>'
        else:
            command_line = b'show interface ' + port + b'\n'
            finish = b'#'

        tn.write(command_line)
        time.sleep(3)
        for i in range(10):
            tn.write(b' ')
            time.sleep(0.2)
        bytesResult = tn.read_very_eager()
        strResult = bytesResult.decode('utf-8')
        print(strResult)
        #关闭telnet
        tn.write(b'\n')
        tn.read_until(finish)
        tn.close()
        time.sleep(3)


if __name__ == '__main__':
    ID = input("请输入电子工单号:  ")
    dzgd = dzgd_Crawl(ID)
    request_detail = dzgd.login()
    A_end_IP,A_end_port,Z_end_IP,Z_end_port = dzgd.parser(request_detail)
    print('A端：'+ A_end_IP)
    dzgd.status(bytes(A_end_IP,encoding='utf-8'), bytes(A_end_port,encoding='utf-8'))
    time.sleep(1)
    print("******************************************************************************************************")
    print('Z端：' + Z_end_IP)
    dzgd.status(bytes(Z_end_IP,encoding='utf-8'), bytes(Z_end_port,encoding='utf-8'))



