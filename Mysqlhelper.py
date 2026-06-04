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
db=MySQLHelper("localhost","root","CAS!2345","students")
modify=db.execute("UPDATE student SET height=%s WHERE name=%s",(180,"Tom"))
modify_1=db.execute("INSERT INTO student(name,height) VALUES(%s,%s)",("Vincent",183))
modify_2=db.execute("DELETE FROM student WHERE name=%s",("Vincent",))
result=db.query("SELECT*FROM student")
for row in result:
    print("id:", row[0], "name:", row[1], "height:", row[2])
result_1=db.query("SELECT*FROM student WHERE height > %s",(175,))
for row in result_1:
    print("id:", row[0], "name:", row[1], "height:", row[2])
