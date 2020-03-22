import random
import urllib.request

class Crawl_Process():
    # 轉換爬取下來資料成字串(change 2 dim form to 1 dim list)
    def turn(self,list):
        temp = []
        for i in list:
            for j in i:
                temp.append(j)
        return temp

    # 用戶代理偽裝瀏覽器(user agent and global install )
    def user_agnet(self):
        ua_pool = ["Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:73.0) Gecko/20100101 Firefox/73.0",
                   "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36",
                   "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36 OPR/67.0.3575.5"]
        ua = random.choice(ua_pool)
        headers = ("User-Agent", ua)
        opener = urllib.request.build_opener()
        opener.addheaders = [headers]
        urllib.request.install_opener(opener)