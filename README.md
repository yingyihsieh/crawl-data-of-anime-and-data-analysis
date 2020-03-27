# crawl-data-of-anime-and-data-analysis

1.Introduction: 

    Crawling website data to analyze the growth of anime websites,the trends of various types of works, the correlation between ratings and popularity, the popularity of director's works and production companies' works are the main purposes of this project. 
    It includes three main parts within BI analysis : crawling the data and setting up the database with MySQL, performing data preprocessing and data visualization.

2.Implementation: There are further information and operaation below.

(1) MySQL Database establishment:

    -mysql_module.py
    -animal.py
    
    In database phase, mysql_module.py provides basic sql operations, and the sql applications are implemented in animal.py for crawler     work. To be more specific, We have three steps below,
    
    -Save raw data to database,
    
    -Export raw data from database,
    
    -Connection by pymysql

(2)Data pre-proccessing:
    
    -analysis_module.py
    
    In data preprocessing stage, data clean is essential with the following steps,
    
    -Change data type,
    
    -Modify missing values,
    
    -Deduplication,
    
    -Calculate average views,
    
    -Count works,
    
    -Count days

(3)Data visualization:

    -ani_analysis.py

    Because of the pyecharts input request is a list, use the transfer_form function in ani_analysis.py to convert the format of the         data. Other chart functions in ani_analysis.py implement visualization of pyecharts.The following are the results of visual.
    
    -show the proportion of each type in pie chart
    ![image](https://github.com/yingyihsieh/crawl-data-of-anime-and-data-   
    analysis/blob/master/%E5%90%84%E9%A1%9E%E5%88%A5%E5%8D%A0%E6%AF%94.png)
    
    -show counts of each type in bar chart overlap avg views in line chart
    ![image](https://github.com/yingyihsieh/crawl-data-of-anime-and-data-               
                analysis/blob/master/%E5%90%84%E9%A1%9E%E5%88%A5%E4%BD%9C%E5%93%81%E6%95%B8%E8%88%87%E5%B9%B3%E5%9D%87%E8%A7%80%E7%9C%8B%E9%87%8F.png)
    
    -show counts of each company in bar chart overlap avg views in line chart
    ![image](https://github.com/yingyihsieh/crawl-data-of-anime-and-data-   analysis/blob/master/%E5%90%84%E5%BB%A0%E5%95%86%E4%BD%9C%E5%93%81%E6%95%B8%E8%88%87%E5%B9%B3%E5%9D%87%E8%A7%80%E7%9C%8B%E9%87%8F.png)
    -show counts of each director in bar chart overlap avg views in line chart
    ![image](https://github.com/yingyihsieh/crawl-data-of-anime-and-data-analysis/blob/master/%E5%90%84%E5%B0%8E%E6%BC%94%E4%BD%9C%E5%93%81%E6%95%B8%E8%88%87%E5%B9%B3%E5%9D%87%E8%A7%80%E7%9C%8B%E9%87%8F.png)
    -show every year and every month counts of anime in bar chart
    ![image](https://github.com/yingyihsieh/crawl-data-of-anime-and-data-analysis/blob/master/%E7%B6%B2%E7%AB%99%E4%BD%9C%E5%93%81%E6%95%B8%E6%88%90%E9%95%B7%E8%B6%A8%E5%8B%A2.png)
    ![image](https://github.com/yingyihsieh/crawl-data-of-anime-and-data-analysis/blob/master/%E4%BD%9C%E5%93%81%E6%9C%88%E4%BB%BD%E5%88%86%E5%B8%83.png)

    -show points-views relation in scatter
    ![image](https://github.com/yingyihsieh/crawl-data-of-anime-and-data-analysis/blob/master/%E8%A9%95%E5%88%86%E8%88%87%E8%A7%80%E7%9C%8B%E9%87%8F%E9%97%9C%E4%BF%82%E5%9C%96.png)
    -show avg views per day in bar chart
    ![image](https://github.com/yingyihsieh/crawl-data-of-anime-and-data-analysis/blob/master/%E4%BD%9C%E5%93%81%E6%97%A5%E5%B9%B3%E5%9D%87%E8%A7%80%E7%9C%8B%E9%87%8F.png)

3.Environment setting up  

    -Python 3.6

    -Numpy
  
    -Pandas
  
    -Pymysql 0.9.3
  
    -Mysql 8.0.18
  
    -Pyecharts 1.2.1
  
    -lxml 4.5.0

4.Further work
  
    -add other website data to compare
  
    -dynamic chart
