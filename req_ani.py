import requests
import re
import csv
import random
from lxml import etree

class BHSpider():
    def __init__(self):
        self.ua_pools = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:73.0) Gecko/20100101 Firefox/73.0",
            "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.94 Safari/537.36",
            "Mozilla/5.0 (compatible; WOW64; MSIE 10.0; Windows NT 6.2)",
            "Opera/9.80 (Windows NT 6.1; WOW64; U; en) Presto/2.10.229 Version/11.62"
        ]
        self.url='https://ani.gamer.com.tw/animeList.php'
        self.header={
           "User-Agent":random.choice(self.ua_pools)
        }
        self.temp_datetime=[]
        self.temp_type = []
        self.temp_director = []
        self.temp_company = []
        self.csv_f = open("new_anime.csv", "a+", encoding="utf-8", newline='')
        self.file = csv.writer(self.csv_f)
        self.file.writerow(['title', 'views', 'datetime', 'type', 'director', 'company'])
    def send_req(self,url):
        response=requests.get(url=url,headers=self.header)
        if response.status_code==200:
           print(url)
        return response

    def parse(self,response):
        html=etree.HTML(response.text)
        class_href=html.xpath('//section[@class="class_list"]//a/@href')
        for href in class_href[1:]:
           class_link='https://ani.gamer.com.tw/'+href
           class_source=self.send_req(class_link)
           self.parse_class(class_source)

    def parse_class(self,response):
        cur_url=response.url
        html = etree.HTML(response.text)
        title=html.xpath('//div[@class="info"]/b/text()')
        views=html.xpath('//span[@class="newanime-count"]/text()')
        pages=html.xpath('//div[@class="page_number"]//text()')[-1]
        content_href=html.xpath('//li/a[@class="animelook"]/@href')
        for href in content_href:
           content_url='https://ani.gamer.com.tw/'+href
           response=self.send_req(content_url)
           datetime,type,director,company=self.parse_content(response)
           self.temp_datetime.append(datetime[0])
           self.temp_type.append(type[0])
           self.temp_director.append(director[0])
           self.temp_company.append(company[0])

        self.wright_csv(title,views,self.temp_datetime, self.temp_type, self.temp_director, self.temp_company)
        self.temp_datetime, self.temp_type, self.temp_director, self.temp_company=[],[],[],[]
        if int(pages)!=1:
           for page in range(2,int(pages)):
               page_url=cur_url + "&page=" + str(page + 1)
               print(page_url)
               response=self.send_req(page_url)
               self.parse_pages(response)

    def parse_pages(self,response):
        html = etree.HTML(response.text)
        title = html.xpath('//div[@class="info"]/b/text()')
        views = html.xpath('//span[@class="newanime-count"]/text()')
        content_href = html.xpath('//li/a[@class="animelook"]/@href')
        for href in content_href:
           content_url = 'https://ani.gamer.com.tw/' + href
           response = self.send_req(content_url)
           datetime, type, director, company = self.parse_content(response)
           self.temp_datetime.append(datetime[0])
           self.temp_type.append(type[0])
           self.temp_director.append(director[0])
           self.temp_company.append(company[0])
        self.wright_csv(title, views, self.temp_datetime, self.temp_type, self.temp_director, self.temp_company)
        self.temp_datetime, self.temp_type, self.temp_director, self.temp_company = [], [], [], []
    def wright_csv(self,title,views,datetime, type, director, company):
        for i in range(len(title)):
            self.file.writerow([title[i],views[i],datetime[i],type[i],director[i],company[i]])

    def parse_content(self,response):
        pattern='上架時間：(.*?) '
        datetime = re.compile(pattern).findall(response.text)
        pattern = '<span>作品.*?>(.*?)</li>'
        type = re.compile(pattern).findall(response.text)
        pattern = '<li><span>導演.*?>(.*?)</li>'
        director = re.compile(pattern).findall(response.text)
        pattern = '<li><span>製作.*?>(.*?)</li>'
        company = re.compile(pattern).findall(response.text)
        return datetime,type,director,company

    def start(self):
        response=self.send_req(self.url)
        self.parse(response)
        self.csv_f.close()

if __name__ == '__main__':
    bhs=BHSpider()
    bhs.start()

