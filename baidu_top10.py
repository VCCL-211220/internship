import requests
import pymysql


class MySQLHelper:
    def __init__(self, host, user, password, database):
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

    def query(self, select_sql, params=None):
        conn=self.get_connection()
        cursor=conn.cursor()
        cursor.execute(select_sql, params)
        result=cursor.fetchall()
        cursor.close()
        conn.close()
        return result

    def execute(self, modify_sql, params=None):
        conn=self.get_connection()
        cursor=conn.cursor()
        modification=cursor.execute(modify_sql, params)
        conn.commit()
        cursor.close()
        conn.close()
        return modification
    
def create_database():
    conn=pymysql.connect(
        host="localhost",
        user="root",
        password="CAS!2345",
        charset="utf8"
    )
    cursor=conn.cursor()
    sql="CREATE DATABASE IF NOT EXISTS Baidutop10"
    cursor.execute(sql)
    conn.commit()
    cursor.close()
    conn.close()

def create_baidu_hot_table(db):
    sql = """
    CREATE TABLE IF NOT EXISTS baidu_hot_search (
        ranking INT,
        title VARCHAR(255),
        hot_score INT,
        url TEXT,
        create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        PRIMARY KEY (ranking)
    );
    """
    db.execute(sql)


def get_baidu_hot_top10():
    url="https://top.baidu.com/api/board?platform=pc&tab=realtime"
    response=requests.get(url)
    response.encoding="utf-8"
    data=response.json()
    real_data=data["data"]
    cards=real_data["cards"]
    card=cards[0]
    hot_list=card["content"]
    top10=[]

    for item in hot_list[:10]:
        rank=item["index"] + 1
        title=item["word"]
        hot_score=item["hotScore"]
        url=item["url"]
        top10.append({
            "ranking": rank,
            "title": title,
            "hot_score": hot_score,
            "url": url
        })

    return top10


def save_baidu_hot_to_database(db,top10):
    db.execute("DELETE FROM baidu_hot_search")
    sql = """
    INSERT INTO baidu_hot_search (ranking, title, hot_score, url)
    VALUES (%s, %s, %s, %s)
    """

    for item in top10:
        params=(
            item["ranking"],
            item["title"],
            item["hot_score"],
            item["url"]
        )

        db.execute(sql, params)

create_database()
db = MySQLHelper(
    host="localhost",
    user="root",
    password="CAS!2345",
    database="Baidutop10"
)

create_baidu_hot_table(db)
top10=get_baidu_hot_top10()
save_baidu_hot_to_database(db, top10)

result=db.query("SELECT * FROM baidu_hot_search")
for row in result:
    print(row)
result=db.query("SELECT * FROM baidu_hot_search WHERE ranking = %s", (1,))
for row in result:
    print(row)
result=db.query("SELECT ranking, title, hot_score FROM baidu_hot_search WHERE hot_score > %s", (7000000,))
for row in result:
    print(row)
result=db.query("SELECT ranking, title, hot_score FROM baidu_hot_search LIMIT 3")
for row in result:
    print(row)
result=db.query("SELECT ranking, title, hot_score FROM baidu_hot_search WHERE title LIKE %s", ("%习近平%",))
if result:
        for row in result:
            print(row)
else:
    print("no")
