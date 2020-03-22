import re
import random
import urllib.request
import pymysql
from lxml import etree
from crawl_module import Crawl_Process
from mysql_module import DB


# create null list for saving data which crawled from web
this_title=[]
this_views=[]
upload=[]
score=[]
director=[]
company=[]
types=[]

# 偽裝瀏覽器(call crawl_module and use user-agent)
cp=Crawl_Process()
cp.user_agnet()
# 爬取首頁資料(crawl the homepage of animes )
url="https://ani.gamer.com.tw/animeList.php"
# decode by utf-8, ignore  unicode error
list_data = urllib.request.urlopen(url).read().decode("utf-8","ignore")

# 分類動漫用xpath抓取網址比較快(use xpath for crawling url of each kind anime)
treedata=etree.HTML(list_data)
for j in range(2,17):
    # 爬取每一類
    # follow xpath rules,each kind anime from 2 to 17
    class_filter=treedata.xpath(
        '//*[@id="BH_background"]/div[2]/section[1]/ul/li['+str(j)+']/a/@href'
    )
    class_link="https://ani.gamer.com.tw/"+class_filter[0]
    class_data=urllib.request.urlopen(class_link).read().decode("utf-8","ignore")
    # 抓取每一類最大頁數(get the last page number for crawling every page)
    pat = '<div class="page_number">.*>(.*?)</a></div>'
    pages = re.compile(pat).findall(class_data)

    # page level
    for l in range(1, int(pages[0])+1):
        # 編寫每頁網址(make every page url)
        page_link=class_link+"&page="+str(l)
        page_data=urllib.request.urlopen(page_link).read().decode("utf-8","ignore")
        tree_page = etree.HTML(page_data)
        # 抓取名稱(crawl the name for each anime)
        pat = "<b>(.*?)</b>"
        title=re.compile(pat).findall(page_data)
        # 抓取觀看量(crawl views for each anime)
        views=tree_page.xpath('//span[@class="newanime-count"]/text()')
        # 抓取頁內動漫內容連結(crawl the url for each anime content)
        ani_link=tree_page.xpath('//a[@class="animelook"]/@href')

        # enter every anime content
        for k in range(len(ani_link)):
            # 儲存每次爬下來的名稱與觀看量(save name and views to list which prepare in advance)
            this_title.append(title[k])
            this_views.append(views[k])
            # crawl the content page
            ani_url="https://ani.gamer.com.tw/"+str(ani_link[k])
            ani_detail=urllib.request.urlopen(ani_url).read().decode("utf-8","ignore")
            # 抓取評分,上架日期,導演監督,製作廠商,作品類型
            # (get points,upload date,director,produce company,and type)
            pat1='"uploadDate":"(.*?)T'
            pat2='<div class="ACG-score">(.*?)<'
            pat3='導演監督</span>(.*?)<'
            pat4='製作廠商</span>(.*?)<'
            pat5='作品類型</span>(.*?)<'
            # save to list, and the list will be 2 dim
            upload.append(re.compile(pat1).findall(ani_detail))
            score.append(re.compile(pat2).findall(ani_detail))
            director.append(re.compile(pat3).findall(ani_detail))
            company.append(re.compile(pat4).findall(ani_detail))
            types.append(re.compile(pat5).findall(ani_detail))

    # change 2 dim form to 1 dim list
    this_upload=cp.turn(upload)
    this_score=cp.turn(score)
    this_director=cp.turn(director)
    this_company=cp.turn(company)
    this_types=cp.turn(types)

# 連接mysql 創建游標(call mysql_module to connect mysql and create cursor)
mysql=DB('root','hsieh1205','project')

# 創建表單(create a table for data)
sql='''create table if not exists anime(
id int auto_increment primary key,
title varchar(200) unique,
types varchar(20),
director varchar(50),
company varchar(50),
views varchar(20),
score varchar(5),
upload_date date
)
'''
# 提交語句(commit sql statement)
mysql.statement(sql)

# 插入數據(insert each data)
for a in range(len(this_title)):
    cur_title=this_title[a]
    cur_type=this_types[a]
    cur_director=this_director[a]
    cur_company=this_company[a]
    cur_views=this_views[a]
    cur_score=this_score[a]
    cur_date=this_upload[a]

    sql="insert into anime(title,types,director,company,views,score,upload_date) values" \
        "('"+cur_title+"','"+cur_type+"','"+cur_director+"','"+cur_company+"','"+cur_views+"','"+cur_score+"','"+cur_date+"')"
    # use try and except to avoid interrupting the loop by duplicate titles
    try:
        mysql.statement(sql)
    except Exception as error:
        print(error)
# close connection
mysql.off()

