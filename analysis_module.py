import numpy as np
import pandas as pd
import time,datetime
from datetime import datetime

class Data_Process():
    # 累計至今天數(counts days)
    def Caltime(self,date1, date2=datetime.now().strftime(("%Y-%m-%d"))):

        start = time.mktime(time.strptime(date1, "%Y-%m-%d"))
        end = time.mktime(time.strptime(date2, "%Y-%m-%d"))

        return abs((end - start)/(24*60*60))

    # 將丟入資料進行group by
    # use np.unique to classify data
    # return data after classify and counts
    def group(self,data):
        types=np.asarray(data)
        type,count=np.unique(types,return_counts=True)
        return type,count

    # 求平均觀看數(calculate avg views)
    # input data after np.unique, counts after np.unique, views data
    def avg(self,type,count,data,view_data):
        avg_view=[]
        for i in range(len(type)):
            view_count = 0
            for j in range(len(data)):
                if data[j]==type[i]:
                    view_count+=view_data[j]
            avg_view.append(round(view_count/count[i],2))
        return avg_view
