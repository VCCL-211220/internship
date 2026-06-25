import pymysql
class MySQLHelper:
    def __init__(self,host,user,password,database):
        self.host=host
        self.user=user
        self.password=password
        self.database=database
    def get_connection(self):
        conn=pymysql.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database,
            charset="utf8"
        )
        return conn
    def query(self,select_sql,params=None):
        conn=self.get_connection()
        cursor=conn.cursor()
        cursor.execute(select_sql,params)
        result=cursor.fetchall()
        cursor.close()
        conn.close()
        return result
    def execute(self,modify_sql,params=None):
        conn=self.get_connection()
        cursor=conn.cursor()
        modification=cursor.execute(modify_sql, params)
        conn.commit()
        cursor.close()
        conn.close()
        return modification