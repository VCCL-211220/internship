from flask import Flask, jsonify
from flask_cors import CORS
from Mysqlhelper import MySQLHelper


app = Flask(__name__)
CORS(app)
#转成中文
app.json.ensure_ascii = False


db = MySQLHelper(
    host="localhost",
    user="root",
    password="CAS!2345",
    database="DoubanMovie"
)


def count_text_items(result):
    item_count = {}

    for row in result:
        text = row[0]

        if text is not None and text != "":
            items = text.split(" ")

            for item in items:
                item = item.strip()

                if item != "":
                    if item not in item_count:
                        item_count[item] = 1
                    else:
                        item_count[item] += 1

    return item_count


@app.route("/")
def home():
    return "Flask backend is running"


@app.route("/api/movies/top-rating")
def get_top_rating_movies():
    sql = """
    SELECT ranking, title, rating, movie_url
    FROM douban_movie_top100
    ORDER BY rating DESC
    LIMIT 10
    """

    result = db.query(sql)

    data = []

    for row in result:
        data.append({
            "ranking": row[0],
            "title": row[1],
            "rating": float(row[2]),
            "movie_url": row[3]
        })

    return jsonify(data)


@app.route("/api/movies/year-count")
def get_year_count():
    sql = """
    SELECT year, COUNT(*)
    FROM douban_movie_top100
    WHERE year IS NOT NULL
    GROUP BY year
    ORDER BY year
    """

    result = db.query(sql)

    data = []

    for row in result:
        data.append({
            "year": row[0],
            "count": row[1]
        })

    return jsonify(data)


@app.route("/api/movies/country-count")
def get_country_count():
    sql = """
    SELECT country
    FROM douban_movie_top100
    """

    result = db.query(sql)

    country_count = count_text_items(result)

    sorted_countries = sorted(
        country_count.items(),
        key=lambda item: item[1],
        reverse=True
    )

    data = []

    for item in sorted_countries:
        data.append({
            "country": item[0],
            "count": item[1]
        })

    return jsonify(data)


@app.route("/api/movies/top-directors")
def get_top_directors():
    sql = """
    SELECT director, COUNT(*)
    FROM douban_movie_top100
    WHERE director != ''
    GROUP BY director
    ORDER BY COUNT(*) DESC
    LIMIT 10
    """

    result = db.query(sql)

    data = []

    for row in result:
        data.append({
            "director": row[0],
            "count": row[1]
        })

    return jsonify(data)


@app.route("/api/movies/genre-count")
def get_genre_count():
    sql = """
    SELECT genres
    FROM douban_movie_top100
    """

    result = db.query(sql)

    valid_genres = {
        "剧情", "喜剧", "爱情", "动作", "科幻", "动画", "悬疑", "惊悚",
        "恐怖", "犯罪", "同性", "音乐", "歌舞", "传记", "历史", "战争",
        "西部", "奇幻", "冒险", "灾难", "武侠", "古装", "家庭", "儿童",
        "运动", "纪录片"
    }

    genre_count = {}

    for row in result:
        genres_text = row[0]

        if genres_text is not None and genres_text != "":
            genres = genres_text.replace("/", " ").split(" ")

            for genre in genres:
                genre = genre.strip()

                if genre in valid_genres:
                    if genre not in genre_count:
                        genre_count[genre] = 1
                    else:
                        genre_count[genre] += 1

    sorted_genres = sorted(
        genre_count.items(),
        key=lambda item: item[1],
        reverse=True
    )

    data = []

    for item in sorted_genres:
        data.append({
            "genre": item[0],
            "count": item[1]
        })

    return jsonify(data)


@app.route("/api/movies/top-actors")
def get_top_actors():
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

                if "..." in actor or "…" in actor:
                    continue

                if actor != "":
                    if actor not in actor_count:
                        actor_count[actor] = 1
                    else:
                        actor_count[actor] += 1

    sorted_actors = sorted(
        actor_count.items(),
        key=lambda item: item[1],
        reverse=True
    )

    top_actors = sorted_actors[:10]

    data = []

    for item in top_actors:
        data.append({
            "actor": item[0],
            "count": item[1]
        })

    return jsonify(data)


if __name__ == "__main__":
    app.run(debug=True)