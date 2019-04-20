import os
from time import sleep
import multiprocessing
import requests
import smtplib
from email.mime.text import MIMEText
from email.header import Header

def send_change(url,filename):
    changed_list = []
    data = ''
    for line in open('./teemo/output/%s-change.txt'%(url),'rt'):
        changeurl = line.replace('\n','')
        changed_list.append(changeurl)
    for changed_suburl in changed_list:
        data = data + '''<li class="list-group-item">%s</li>'''%(changed_suburl)
    mail_add = open('./mail/%s.mail'%(filename),'rt')
    mail = mail_add.read()
    mail_add.close()
    # 第三方 SMTP 服务
    mail_host="smtp.mxhichina.com"  #设置服务器
    mail_user="mo@k.net"    #用户名
    mail_pass="Ay2"   #口令
    sender = 'm@k.net'
    receivers = [mail]  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱
    mail_msg = """
    <p>你的项目有新的变化（网站监控平台）</p>
    <ul class="list-group">
    %s
    </ul>
    """%(data)
    message = MIMEText(mail_msg, 'html', 'utf-8')
    message['From'] = Header("监控平台", 'utf-8')
    subject = '你的项目有新的变化（网站监控平台）'
    message['Subject'] = Header(subject, 'utf-8')
    try:
        smtpObj = smtplib.SMTP()
        smtpObj.connect(mail_host,25)    # 25 为 SMTP 端口号
        smtpObj.login(mail_user,mail_pass)
        smtpObj.sendmail(sender, receivers, message.as_string())
        print('邮件发送成功:'+ mail)
    except smtplib.SMTPException:
        print('Error: 无法发送邮件')



def run_teemo(url,filename):
    os.system("python ./teemo/teemo.py -d %s -o %s.txt"%(url,url))
    test_survive(url,filename)

def test_survive(url,filename):
    suburl_list = []
    survive_url = []
    compare_dic = {}
    for line in open('./teemo/output/%s.txt'%(url),'rt'):
        suburl = line.replace('\n','')
        suburl_list.append(suburl)
    for i in suburl_list:
        try:
            code = requests.get('http://'+i, timeout=5)
            status = code.status_code
        except:
            try:
                code = requests.get('https://'+i, timeout=5)
                status = code.status_code
            except:
                status = 0

        if status == 200:
            survive_url.append(i)
            print('[*]添加存活 %s'%(i))
            compare_dic[i] = len(code.text)
        else:
            pass
    data = "\n".join(survive_url)
    savefile=open('./teemo/output/%s-survive.txt'%(url),'wb+')
    savefile.write(data.encode('gbk','ignore'))
    savefile.close()
    test_change_url(url,compare_dic,filename)


def test_change_url(url,compare_dic,filename): #新的字节字典
    changed_suburl= []
    try:
        readfile=open('./teemo/output/%s-lenth-data.txt'%(url),'rt')
        lenth_list = eval(readfile.read())
        readfile.close() #老的字节字典
        for suburl in compare_dic:
            if suburl in lenth_list:
                if lenth_list[suburl]-15 < compare_dic[suburl] < lenth_list[suburl]+15:
                    pass
                else:
                    changed_suburl.append(suburl)
        newfile=open('./teemo/output/%s-lenth-data.txt'%(url),'wb+')
        data = str(compare_dic)
        newfile.write(data.encode('gbk','ignore'))
        newfile.close()
        if changed_suburl:
            savechange=open('./teemo/output/%s-change.txt'%(url),'wb+')
            data = "\n".join(changed_suburl)
            savechange.write(data.encode('gbk','ignore'))
            savechange.close()
            send_change(url,filename)
        else:
            print(filename + '子程序均在阈值内')


    except:
        newfile=open('./teemo/output/%s-lenth-data.txt'%(url),'wb+')
        data = str(compare_dic)
        newfile.write(data.encode('gbk','ignore'))
        newfile.close()


def suburl():
    while True:
        for filename in os.listdir('./account/user/'):
            openfile=open('./account/user/%s'%(filename),'rt')
            urllist1 = openfile.read()
            openfile.close()
            if urllist1:
                urllist2 = urllist1.replace('https://','')
                urllist3 = urllist2.replace('http://','')
                urllist4 = urllist3.replace('/','')
                url_list = urllist4.split(",")
                for url in url_list:
                    tested_url = []
                    try:
                        for line in open('./tested/%s.txt'%(filename),'rt'):
                            testedurl = line.replace('\n','')
                            tested_url.append(testedurl)
                        sleep(5)
                    except:
                        pass
                    if url not in tested_url:
                        p = multiprocessing.Process(target=run_teemo, args=(url,filename))
                        p.start()
                        tested_url.append(url)
                        tested=open('./tested/%s.txt'%(filename),'wb+')
                        data = "\n".join(tested_url)
                        tested.write(data.encode('gbk','ignore'))
                        tested.close()
                        print('[*]开始扫描 %s'%(url))
                        sleep(120)
def start_web():
    os.system("python3 manage.py runserver 0.0.0.0:80")

def del_tested():
    while True:
        sleep(86000)
        try:
            for filename in os.listdir('./tested/'):
                os.remove('./tested/%s'%(filename))
                sleep(120)
        except:
            pass

if __name__ == '__main__':
    choose = input('[?]是否启动网站及相关程序(y):')
    if choose == 'y':
        p1 = multiprocessing.Process(target=start_web, args=()) #开启网站
        p1.start()
        p2 = multiprocessing.Process(target=del_tested, args=()) #定时
        p2.start()
        suburl()
    else:
        exit()
