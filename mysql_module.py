import pymysql

class DB():
    # connect to mysql at first
    # create cursor
    def __init__(self,user,passwd,database):
        self.user,self.passwd,self.database=user,passwd,database
        self.db=pymysql.connect('localhost',self.user,self.passwd,self.database)
        self.cursor=self.db.cursor()
    # commit sql statement
    def statement(self,sql):
        self.cursor.execute(sql)
        self.db.commit()
    # export data from mysql
    def export(self,sql):
        self.cursor.execute(sql)
        self.res = self.cursor.fetchall()
        self.db.commit()
    # close connection
    def off(self):
        self.db.close()