import numpy as np
import pandas as pd
import pymysql
import time,datetime
from mysql_module import DB
from datetime import datetime
from analysis_module import Data_Process
from pyecharts.charts import Bar,Line,Pie,Scatter
from pyecharts import options as opts


# 將numpy格式轉python通用格式(chage ndarray to list)
def transfer_form(x):
    x = x.tolist()
    return x
# 繪製柱狀圖(show bar chart)
# input data of x,data of y,x axis name,y axis name
def bar(x, y, x_name, y_name):
    bar = Bar(init_opts=opts.InitOpts(height="600px", width="1200px"))
    bar.add_xaxis(xaxis_data=x)
    bar.add_yaxis(series_name='每年上架數量', yaxis_data=y)
    bar.set_global_opts(title_opts=opts.TitleOpts(title='數量'),
                        xaxis_opts=opts.AxisOpts(name=x_name),
                        yaxis_opts=opts.AxisOpts(name=y_name))
    bar.set_series_opts(label_opts=opts.LabelOpts(position='right'))
    bar.reversal_axis()
    return bar

# 同時繪製柱狀+折線圖(bar chart overlap line chart)
# input data of x,data of y for bar chart,data of y for line chart
def bar_chart(x,y1,y2)->Bar():
    c = Bar(init_opts=opts.InitOpts(width='1200px',height='800px'))
    c.add_xaxis(xaxis_data=x,)
    # label_opts = opts.LabelOpts(is_show=False) 是否顯示數值
    c.add_yaxis(series_name='',yaxis_data=y1,label_opts=opts.LabelOpts(is_show=True))

    c.set_global_opts(
        title_opts=opts.TitleOpts(title=''),
        yaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=45)),
        datazoom_opts=opts.DataZoomOpts(type_='slider')
    )
    c.extend_axis(yaxis=opts.AxisOpts(name='觀看次數',
                                      type_='value',
                                      min_=min(y2),
                                      max_=max(y2),
                                      interval=500000,
                                      axislabel_opts=opts.LabelOpts(formatter='{value}次')))
    return c
def line(x,y)->Line():
    c=Line()
    c.add_xaxis(xaxis_data=x)
    c.add_yaxis(series_name='平均觀看量',yaxis_index=1,y_axis=y,label_opts=opts.LabelOpts(is_show=True))
    return c

# 將資料轉成pie圖輸入格式(use zip to make the input data form which pie chart needs)
# input x data,y data
def data_pie_form(x,y):
    data_pie = [list(z) for z in list(zip(x, y))]
    return data_pie

# 輪餅圖(draw a pie chart)
# input data which zipped by data_pie_form
def pie_radius_chart(data_pie):
    c = Pie()
    c.add(series_name='類別', data_pair=data_pie, radius=['40%','75%'])
    c.set_global_opts(title_opts=opts.TitleOpts(title='各種類占比'),
                      legend_opts=opts.LegendOpts(orient='vertical',
                                                  pos_top='15%',
                                                  pos_left='2%'))
    c.set_series_opts(tooltip_opts=opts.TooltipOpts(trigger='item',
                                                    formatter='{a} <br/> {b}:{c} ({d}%)'),
                      label_opts=opts.LabelOpts(formatter="{b}:{c}%"))

    return c

# 從數據庫導出資料(call mysql_module to connect mysql and create cursor)
mysql=DB('root','hsieh1205','project')
# export data
sql="select * from anime"
mysql.res=mysql.export(sql)
column_name=['id','title','types','director','company','views','score','upload_date']
df=pd.DataFrame(list(mysql.res),columns=column_name)

# 關閉數據庫連接(close mysql connection)
mysql.off()

# 處理未知導演與未知公司(use 'unknown' instead of NAN in column director and company )
for i in range(len(df)):
    if df['director'][i]=='':
        df['director'][i]='unknown'
    if df['company'][i]=='':
        df['company'][i]='unknown'

# 轉換 觀看量 成 浮點型態(turn views type from str to float,unit=10 thousand )
for i in range(len(df['views'])):
    # print(df['views'][i])
    if '萬' in df['views'][i]:
        df['views'][i]=float(df['views'][i].replace('萬',''))
    else:
        df['views'][i] = float(df['views'][i])/10000

# 轉換評分的型態,未評分給0(turn points type from str to float, value add 0 if none)
for j in range(len(df)):
    # print(type(df['score'][j]))
    if df['score'][j] == '--':
        df['score'][j]=0.0
    else:
        df['score'][j] = float(df['score'][j])

# call analysis_module
dp=Data_Process()
# 提取累計天數(calculate days from upload date)
days_differ=[]
for i in range(len(df)):
    days_differ.append(dp.Caltime(str(df['upload_date'][i])))
df['days_differ']=days_differ

# 計算每部動漫每天平均觀看量(calculate average vies per day for each anime)
views_oneday=[]
for i in range(len(df)):
    views_oneday.append(round(df['views'][i]/df['days_differ'][i],2))

# 計算每種類占比(Calculate the proportion of each type)
# group by type,grand total of every type
group_type,group_type_count=dp.group(df['types'])
type_percent=[]
for i in range(len(group_type_count)):
    type_percent.append(round((group_type_count[i]/sum(group_type_count))*100,2))

# 計算每種類平均觀看(calculate average vies per type)
avg_view_type=dp.avg(group_type,group_type_count,df['types'],df['views'])

# 分類製作廠商與廠商製作次數
# group by company,grand total of every company
group_company,group_company_count=dp.group(df['company'])
# 計算廠商作品平均觀看量(calculate average vies per company)
avg_view_company=dp.avg(group_company,group_company_count,df['company'],df['views'])

# 提取年份做年份分布(pick up year and month)
year=[]
month=[]
for i in range(len(df['upload_date'])):
    year.append(df['upload_date'][i].year)
    month.append(df['upload_date'][i].month)
df['year']=year
df['month']=month

# group by year and month
group_year,group_year_count=dp.group(df['year'])
group_month,group_month_count=dp.group(df['month'])

# group by director
group_director,group_director_count=dp.group(df['director'])
# 計算導演作品平均觀看量(calculate average vies per director)
avg_view_director=dp.avg(group_director,group_director_count,df['director'],df['views'])

# 計算每種類近年增減趨勢(count each type every year)
total=[]
temp_df=df.groupby(['year','types'])
for i in range(len(group_year)):
    static = []
    for j in range(len(group_type)):
        try:
            print(temp_df.get_group((group_year[i],group_type[j])))
            static.append(len(temp_df.get_group((group_year[i], group_type[j]))))
        except Exception as e:
            static.append(0)
            print(e)
    total.append(static)
print(total)

# 繪製各類別逐年作品數(show each type animes for every year bar chart)
x=transfer_form(group_type)
ba = Bar(init_opts=opts.InitOpts(height="600px", width="1200px"))
ba.add_xaxis(xaxis_data=x)
for i in range(len(total)):
    ba.add_yaxis(series_name=str(group_year[i]), yaxis_data=total[i])
ba.set_global_opts(title_opts=opts.TitleOpts(title='各類別逐年作品數'),
                    xaxis_opts=opts.AxisOpts(name="類別"),
                    yaxis_opts=opts.AxisOpts(name="作品數"))
ba.set_series_opts(label_opts=opts.LabelOpts(position='top'))
ba.render()

# 繪製站內所有類別動漫占比(show the proportion of each type pie chart)
x=transfer_form(group_type)
y=type_percent
data=data_pie_form(x,y)
print(data)
pie=pie_radius_chart(data)
pie.render()

# 繪製柱狀圖-每類別動漫數量,折線圖-平均觀看數
# show counts of each type bar chart overlap avg views per type line chart
x,y1=transfer_form(group_type),transfer_form(group_type_count)
y2=avg_view_type
bar=bar_chart(x,y1,y2)
line=line(x,y2)
bar.overlap(line).render()

# 繪製(製作廠商,數量,觀看量)柱狀圖與折線圖
# show counts of each company bar chart overlap avg views per company line chart
x,y1=transfer_form(group_company),transfer_form(group_company_count)
y2=avg_view_company
bar=bar_chart(x,y1,y2)
line=line(x,y2)
bar.overlap(line).render()

# 繪製(導演,作品數量,平均觀看量)柱狀圖與折線圖
# show counts of each director bar chart overlap avg views per director line chart
x,y1=transfer_form(group_director),transfer_form(group_director_count)
y2=avg_view_director
bar=bar_chart(x,y1,y2)
line=line(x,y2)
bar.overlap(line).render()

# 繪製每年與每月作品數量柱狀圖
# show every year and every month counts of anime bar chart
x,y=transfer_form(group_year),transfer_form(group_year_count)
bar=bar(x,y,'數量(單位:部)','年份(單位:年)')
bar.render()
x,y=transfer_form(group_month),transfer_form(group_month_count)
bar=bar(x,y,'數量(單位:部)','月份(單位:月)')
bar.render()

# 觀察評分與觀看數的關係
# show points-views relation in scatter
print(max(df['views']),min(df['views']))
fig = opts.InitOpts(width='1200px',height='600px')
scatter = Scatter(init_opts=fig)
scatter.add_xaxis(xaxis_data=df['views'])
scatter.add_yaxis(series_name='', y_axis=df['score'],
                  # 設計數據值是否展示
                  label_opts=opts.LabelOpts(is_show=False))
scatter.set_global_opts(title_opts=opts.TitleOpts(title='觀看量-評分關係圖',
                                                  pos_left='center',
                                                  pos_top='20'),
                        xaxis_opts=opts.AxisOpts(split_number=25,name='觀看量(單位:萬)'),
                        yaxis_opts=opts.AxisOpts(split_number=20,name='分'))
scatter.render()

# 動漫每天平均觀看量
# show avg views per day bar char
title=[]
for i in range(len(df['title'])):
    title.append(df['title'][i])
ba = Bar(init_opts=opts.InitOpts(height="500px", width="1200px"))
ba.add_xaxis(xaxis_data=title)
ba.add_yaxis(series_name='平均觀看量/天', yaxis_data=views_oneday)
ba.set_global_opts(title_opts=opts.TitleOpts(title='各類別逐日平均觀看數'),
                   xaxis_opts=opts.AxisOpts(name="類別",axislabel_opts=opts.LabelOpts(rotate=75)),
                   yaxis_opts=opts.AxisOpts(name="觀看數(單位:萬)"),
                   datazoom_opts = opts.DataZoomOpts(type_='slider'))
ba.set_series_opts(label_opts=opts.LabelOpts(position='top'))
ba.render()
