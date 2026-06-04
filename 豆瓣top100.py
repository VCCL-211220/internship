import requests
from bs4 import BeautifulSoup
import pymysql
import matplotlib.pyplot as plt

#确保中文显示正确
plt.rcParams["font.sans-serif"] = ["SimHei"]

class MySQLHelper:
    def __init__(self,host,user,password,database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
    def get_connection(self):
        conn = pymysql.connect(
            host = self.host,
            user = self.user,
            password = self.password,
            database = self.database,
            charset = "utf8mb4"
        )
        return conn
    def query(self,select_sql,params=None):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(select_sql,params)
        result = cursor.fetchall()
        cursor.close()
        conn.close()
        return result
    def execute(self,modify_sql,params=None):
        conn = self.get_connection()
        cursor = conn.cursor()
        modification = cursor.execute(modify_sql, params)
        conn.commit()
        cursor.close()
        conn.close()
        return modification

#create database
def create_database():
    conn = pymysql.connect(
        host = "localhost",
        user = "root",
        password = "CAS!2345",
        charset = "utf8mb4"
    )
    cursor = conn.cursor()
    sql = "CREATE DATABASE IF NOT EXISTS DoubanMovie DEFAULT CHARSET utf8mb4"
    cursor.execute(sql)
    conn.commit()
    cursor.close()
    conn.close()

#create table
def create_douban_movie_table(db):
    sql = """
    CREATE TABLE IF NOT EXISTS douban_movie_top100 (
        ranking INT,
        title VARCHAR(300),
        director VARCHAR(300),
        actors TEXT,
        year INT,
        country VARCHAR(300),
        genres VARCHAR(300),
        rating FLOAT,
        movie_url TEXT,
        PRIMARY KEY (ranking)
    );
    """
    db.execute(sql)

#insert values
def save_douban_movies_to_database(db, movies):
    db.execute("DELETE FROM douban_movie_top100")
    sql = """
    INSERT INTO douban_movie_top100
    (
        ranking,
        title,
        director,
        actors,
        year,
        country,
        genres,
        rating,
        movie_url
    )
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    for movie in movies:
        params = (
            movie["ranking"],
            movie["title"],
            movie["director"],
            movie["actors"],
            movie["year"],
            movie["country"],
            movie["genres"],
            movie["rating"],
            movie["movie_url"]
        )
        db.execute(sql, params)

#找column
def parse_movie_item(item):
    # 排名
    ranking_text = item.find("em").text
    ranking = int(ranking_text)

    # 电影链接
    movie_url = item.find("a")["href"]

    # 电影标题和原始标题
    title_tags = item.find_all("span", class_="title")
    title = title_tags[0].text
    
    # 评分
    rating_text = item.find("span", class_="rating_num").text
    rating = float(rating_text)
    bd = item.find("div", class_="bd")
    p_text = bd.find("p").text.strip()
    
    lines = p_text.split("\n")
    first_line = lines[0].strip()
    second_line = lines[1].strip()
    #导演+演员
    director = ""
    actors = ""

    if "导演:" in first_line:
        director_part = first_line.split("主演:")[0]
        director = director_part.replace("导演:", "").strip()

    if "主演:" in first_line:
        actors = first_line.split("主演:")[1].strip()

    #年份，国家，类型
    info_parts = second_line.split("/")

    year = None
    country = ""
    genres = ""

    if len(info_parts) >= 1:
        year_text = info_parts[0].strip()
        if year_text.isdigit():
            year = int(year_text)

    if len(info_parts) >= 2:
        country = info_parts[1].strip()

    if len(info_parts) >= 3:
        genres = info_parts[2].strip()

    movie = {
        "ranking": ranking,
        "title": title,
        "director": director,
        "actors": actors,
        "year": year,
        "country": country,
        "genres": genres,
        "rating": rating,
        "movie_url": movie_url
    }
    return movie

#把前100分成4页，每页25个电影
def douban_top100():
    starts = [0, 25, 50, 75]

    movies = []

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    for start in starts:
        url = "https://movie.douban.com/top250?start=" + str(start)

        response = requests.get(url, headers=headers)
        response.encoding = "utf-8"

        html = response.text
        content = BeautifulSoup(html, "html.parser")

        movie_items = content.find_all("div", class_="item")

        for item in movie_items:
            movie = parse_movie_item(item)
            movies.append(movie)

    return movies

create_database()

db = MySQLHelper(
    host="localhost",
    user="root",
    password="CAS!2345",
    database="DoubanMovie"
)

create_douban_movie_table(db)
movies = douban_top100()
save_douban_movies_to_database(db, movies)

def show_year_distribution(db):
    sql = """
    SELECT year, COUNT(*)
    FROM douban_movie_top100
    WHERE year IS NOT NULL
    GROUP BY year
    ORDER BY year
    """

    result = db.query(sql)

    years = []
    counts = []

    for row in result:
        years.append(row[0])
        counts.append(row[1])

    plt.figure(figsize=(12, 5))
    plt.plot(years, counts, marker="o")
    plt.xlabel("年份")
    plt.ylabel("电影数量")
    plt.title("豆瓣电影 Top100 年份分布")
    plt.show()
show_year_distribution(db)

#测试年份分布
def test_year_distribution(db):
    sql = """
    SELECT year, COUNT(*)
    FROM douban_movie_top100
    WHERE year IS NOT NULL
    GROUP BY year
    ORDER BY year
    """

    result = db.query(sql)

    print("年份分布测试结果：")
    for row in result:
        print(row)
test_year_distribution(db)

#拿到出现次数，方便后面排序
def get_count(item):
    return item[1]

#统计出现国家
def count_text_items(result):
    item_count = {}

    for row in result:
        text = row[0]

        if text is not None:
            items = text.split(" ")

            for item in items:
                item = item.strip()

                if item != "":
                    if item not in item_count:
                        item_count[item] = 1
                    else:
                        item_count[item] = item_count[item] + 1

    return item_count

def show_country_distribution(db):
    sql = """
    SELECT country
    FROM douban_movie_top100
    """
    result = db.query(sql)

    country_count = count_text_items(result)

    sorted_countries = sorted(country_count.items(), key=get_count, reverse=True)

    names = []
    counts = []

    for item in sorted_countries:
        names.append(item[0])
        counts.append(item[1])

    plt.figure(figsize=(14, 6))
    plt.bar(names, counts)
    plt.xlabel("国家/地区")
    plt.ylabel("电影数量")
    plt.title("豆瓣电影 Top100 国家/地区分布")
    plt.xticks(rotation=45)
    plt.show()

show_country_distribution(db)

def test_country_distribution(db):
    sql = """
    SELECT country
    FROM douban_movie_top100
    """

    result = db.query(sql)

    country_count = count_text_items(result)
    sorted_countries = sorted(country_count.items(), key=get_count, reverse=True)

    print("国家/地区分布测试结果：")
    for row in sorted_countries:
        print(row)
test_country_distribution(db)
     
def show_director_bar_chart(db):
    sql = """
    SELECT director, COUNT(*)
    FROM douban_movie_top100
    WHERE director != ''
    GROUP BY director
    ORDER BY COUNT(*) DESC
    LIMIT 10
    """

    result = db.query(sql)

    directors = []
    counts = []

    for row in result:
        directors.append(row[0])
        counts.append(row[1])

    plt.figure(figsize=(20, 6))
    plt.barh(directors, counts)
    plt.xlabel("电影数量")
    plt.ylabel("导演")
    plt.title("豆瓣电影 Top100 导演作品数量 Top10")
    plt.gca().invert_yaxis()
    plt.subplots_adjust(left=0.25)
    plt.show()

show_director_bar_chart(db)

#测试导演分布
def test_director_top10(db):
    sql = """
    SELECT director, COUNT(*)
    FROM douban_movie_top100
    WHERE director != ''
    GROUP BY director
    ORDER BY COUNT(*) DESC
    LIMIT 10
    """

    result = db.query(sql)

    print("导演 Top10 测试结果：")
    for row in result:
        print(row)

test_director_top10(db)

def show_genres_pie_chart(db):
    sql = """
    SELECT genres
    FROM douban_movie_top100
    """

    result = db.query(sql)

    genre_count = count_text_items(result)

    names = []
    counts = []

    for genre in genre_count:
        names.append(genre)
        counts.append(genre_count[genre])

    plt.figure(figsize=(8, 8))
    plt.pie(counts, labels=names, autopct="%1.1f%%")
    plt.title("豆瓣电影 Top100 类型分布")
    plt.show()

show_genres_pie_chart(db)

def show_actor_bar_chart(db):
    sql = """
    SELECT actors
    FROM douban_movie_top100
    """
    
    result = db.query(sql)

    actor_count = {}

    for row in result:
        actors_text = row[0]

        if actors_text is not None and actors_text != "":
            actors = actors_text.split("/")

            for actor in actors:
                actor = actor.strip()

                  # 跳过带省略号的演员名
                if "..." in actor or "…" in actor:
                    continue

                # 统计演员出现次数
                if actor != "":
                    if actor not in actor_count:
                        actor_count[actor] = 1
                    else:
                        actor_count[actor] = actor_count[actor] + 1

    sorted_actors = sorted(actor_count.items(), key=get_count, reverse=True)

    top_actors = sorted_actors[:10]

    names = []
    counts = []

    for item in top_actors:
        names.append(item[0])
        counts.append(item[1])

    plt.figure(figsize=(16, 6))
    plt.barh(names, counts)
    plt.xlabel("参演电影数量")
    plt.ylabel("演员")
    plt.title("豆瓣电影 Top100 演员参演次数 Top10")
    plt.gca().invert_yaxis()
    plt.show()
show_actor_bar_chart(db)
#测试演员分布
def test_actor_top10(db):
    sql = """
    SELECT actors
    FROM douban_movie_top100
    """
    
    result = db.query(sql)

    actor_count = {}

    for row in result:
        actors_text = row[0]

        if actors_text is not None and actors_text != "":
            actors = actors_text.split("/")

            for actor in actors:
                actor = actor.strip()

                # 跳过带省略号的演员名
                if "..." in actor or "…" in actor:
                    continue

                # 统计演员出现次数
                if actor != "":
                    if actor not in actor_count:
                        actor_count[actor] = 1
                    else:
                        actor_count[actor] = actor_count[actor] + 1

    sorted_actors = sorted(actor_count.items(), key=get_count, reverse=True)

    top_actors = sorted_actors[:10]

    print("演员 Top10 测试结果：")
    for item in top_actors:
        print(item)
test_actor_top10(db)
