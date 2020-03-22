# crawl-data-of-anime-and-data-analysis

1.Introduction: 
    Crawling website data to analyze the growth of anime websites,the trends of various types of works, the correlation between ratings and popularity, the popularity of director's works and production companies' works are the main purposes of this project. 
    It includes three main parts within BI analysis : crawling the data and setting up the database with MySQL, performing data preprocessing and data visualization.

2.Implementation: There are further information and operaation below.

(1) MySQL Database establishment:

    -save raw data to database

    -export raw data from database

    -connect by pymysql 

(2)Data pre-proccessing:

    -change type of data

    -modify missing values

    -Deduplication

    -calculate average views

    -count works

    -count days

(3)Data visualization:

    -bar chart

    -pie radius chart

    -bar overlap pie chart

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
