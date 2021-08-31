import requests,bs4,smtplib         #导入包
from email.mime.text import MIMEText
from email.header import Header
res=requests.get('http://jwc.njtech.edu.cn/index/tzgg.htm')         #发送请求，获得网页数据
res.encoding = 'utf-8'                                              #改变编码格式
# res.raise_for_status()  
web_content=res.text                                                #获得网页内容
soup = bs4.BeautifulSoup(web_content,'html.parser')                 #造汤
# type(soup)

filename='./update.txt'                                             #用于记录已更新的通知号
f = open(filename,"r")                                              #设置文件对象
str = f.read()                                                      #将txt文件的所有内容读入到字符串str中
f.close()                                                           #将文件关闭
latest_flag=str                                                     #上次发送的最新通知号
# print(latest_flag)

href_flag=[]                                                        #标志号数组
tosend_content=[]                                                   #待发送内容
href_group=[]
def delFlag(temp_content):                                          #工具函数（处理链接标志）
    # print(content)
    # print(content[0])
    href_link=temp_content.find('a')['href']
    href_link=href_link.split('/')
    # print(href_link)
    temp='http://jwc.njtech.edu.cn'+'/'+href_link[1]+'/'+href_link[2]+'/'+href_link[3]
    href_group.append(temp)
    href_num=href_link[3].split('.')[0]
    return href_num

def sendEmail(i,main_content):                                      #发送邮件
        # 第三方 SMTP 服务
    mail_host="smtp.qq.com"                                         #设置服务器
    mail_user="youremail@qq.com"                                    #用户名
    mail_pass="授权码"                                               #口令,QQ邮箱是输入授权码，在qq邮箱设置 里用验证过的手机发送短信获得，不含空格
    
    
    sender = '教务处邮件提醒服务<youremail@qq.com>'
    receivers = ['收件人邮箱']                                       # 接收邮件，可设置为你的QQ邮箱或者其他邮箱（可填写多个收件人）
    
    message = MIMEText(href_group[i], 'plain', 'utf-8')
    message['From'] = '"=?gb18030?B?vczO8bSm08q8/szh0NG3/s7x?="<youremail@qq.com>'
    message['To'] =  Header("帅气的你", 'utf-8')                     #邮件头中的收件人文字显示
    
    subject = main_content.getText()
    message['Subject'] = Header(subject, 'utf-8')
    
    try:
        smtpObj = smtplib.SMTP_SSL(mail_host, 465) 
        smtpObj.login(mail_user,mail_pass)  
        smtpObj.sendmail(sender, receivers, message.as_string())
        smtpObj.quit()
        print("邮件发送成功")
    except :
        print("邮件发送失败")

a=0                                                                 #获取所需元素，加入数组
for i in soup.find('div',class_='txt').children:
    if a == 2:
        content=i.select('li')
    a=a+1


for item in content:                                                #获取标志数组
    href_flag.append(delFlag(item))

for i, j in enumerate(href_flag):
    if int(j)>int(latest_flag):
        tosend_content.append(content[i])

# print(href_group)
if(tosend_content !=''):
    for i,j in enumerate(tosend_content):
        sendEmail(i,j)

file=open(filename, 'w')
if tosend_content !='':
    latest_flag=href_flag[0]
    file.write(latest_flag)
    file.close()
