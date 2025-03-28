import requests,time,datetime,smtplib,schedule
from bs4 import BeautifulSoup
from email.mime.text import MIMEText
from email.header import Header

#爬取新闻（目前有：华尔街、界面）

#华尔街新闻
def news_robo_wallstreet(keyword):
    today=datetime.date.today()#获取实时日期
    yesterday=today-datetime.timedelta(days=1)#昨天
    before_yesterday=today-datetime.timedelta(days=2)#前天
    date_list=[str(today),str(yesterday),str(before_yesterday)]

    url='https://api-one.wallstcn.com/apiv1/search/article?query=%s&cursor=&limit=20&vip_type='%(keyword)
    headers={
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36'
        }

    params={
        '﻿query':keyword, #'恒大',
        'cursor':'',
        'limit':'20',
        'vip_type':''
        }

    res=requests.get(url=url,headers=headers,params=params)
    dict_news=res.json()
    list_fresh_news=[]
        #提取信息
    items=dict_news['data']['items']
    for item in items:
        title=item['title'].replace('<em>%s</em>'%(keyword),keyword)
        date=time.strftime("%Y-%m-%d", time.localtime(item['display_time']))
        abstract=item['content_short'].replace('<em>%s</em>'%(keyword),keyword)
        url=item['uri']
        list_new=[title,date,abstract,url]
        if date in date_list:
            list_fresh_news.append(list_new)

        #写入信息
    #list_news_display=[]#已淘汰 2021-09-30 12:32
    str_=''
    for i in list_fresh_news:
        #str_=''
        for r in range(0,len(i)):
             str_=str_+i[r]+'\n'#新闻元素编制成自然段
        str_=str_+'\n'#每条新闻之间空行
    #list_news_display.append(str_)#写入做好格式的新闻#已淘汰 2021-09-30 12:32


    #for ii in list_news_display:#中途检查专用代码#已淘汰 2021-09-30 12:32
        #print(ii)
    return(str_)

#界面新闻
def news_robo_jiemian(keyword):
    today=datetime.date.today()#获取实时日期
    yesterday=today-datetime.timedelta(days=1)#昨天
    before_yesterday=today-datetime.timedelta(days=2)#前天
    date_list=[str(today),str(yesterday),str(before_yesterday)]

    #keyword='恒大'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:92.0) Gecko/20100101 Firefox/92.0',
               'Connection': 'close'
               }
    demand=3  #默认爬3页

    list_fresh_news=[]
    list_date_news=[]
    for i in range(1,demand+1):
        res=requests.get('https://a.jiemian.com/index.php?m=search&a=index&msg=%s&type=&page=%d'%(keyword,i),headers=headers)
        html=res.text
        soup=BeautifulSoup(html,'html.parser')
        new_blocks=soup.find_all(class_='news-view')
        
        for item in new_blocks:
            title=item.find('h3').find('a')['title']
            raw_date=item.find(class_="date").text[0:10]#只把日期取出来，形式为‘2021/10/12’
            year=raw_date[:4]
            month=raw_date[5:7]
            day=raw_date[8:]
            date=year+'-'+month+'-'+day#拼接成‘2021-10-12’
            abstract=item.find('p').text#第一个P是摘要，后边依次为作者、日期
            url=item.find('h3').find('a')['href']
            list_new=[title,date,abstract,url]
            list_date_news.append(date)
            if date in date_list:
                list_fresh_news.append(list_new)
    str_=''
    for i in list_fresh_news:
        for r in range(0,len(i)):
             str_=str_+i[r]+'\n'#新闻元素编制成自然段
        str_=str_+'\n'#每条新闻之间空行
    return(str_)
        


#发邮件
def mail_send(content):
        #SSL连接
    mail163=smtplib.SMTP_SSL('smtp.163.com','465')
        #登录邮箱
    username=input('请输入发送邮箱')
    password=input('请输入邮箱密码')
    mail163.login(username,password)
        #写邮件
    message=MIMEText(content,'plain','utf-8')
    message['Subject']=Header('近期资讯','utf-8')
        #发送
    try:
        mail163.sendmail(username,username,message.as_string())
        print('发送成功')
    except:
        print('发送失败')
    mail163.quit()

def job():
    keyword_list=['恒大','外汇','汇率']#在此输入新闻关键词
    content=''
    for kw in keyword_list:
        content+=(kw+'\n'+'\n'+news_robo_wallstreet(kw)+'\n'+news_robo_jiemian(kw))
    mail_send(content)

schedule.every().day.at('11:16').do(job)
while True:
    schedule.run_pending()
    time.sleep(60)
    
    
        
    


        
    
    

