from Mysqlhelper import MySQLHelper
from werkzeug.security import generate_password_hash, check_password_hash

db = MySQLHelper(
    host="localhost",
    user="root",
    password="CAS!2345",
    database="DoubanMovie"
)


def create_user_table():
    sql = """
    CREATE TABLE IF NOT EXISTS users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(50) NOT NULL UNIQUE,
        email VARCHAR(100),
        password_hash VARCHAR(255) NOT NULL,
        create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """

    db.execute(sql)


def add_user(username, email, password):
    # 检查用户名是否为空
    if username is None or username.strip() == "":
        return {
            "success": False,
            "message": "用户名不能为空"
        }

    # 检查密码是否为空
    if password is None or password.strip() == "":
        return {
            "success": False,
            "message": "密码不能为空"
        }

    username = username.strip()

    if email is not None:
        email = email.strip()

    # 检查用户名是否已经存在
    check_sql = """
    SELECT id
    FROM users
    WHERE username = %s
    """

    result = db.query(check_sql, (username,))

    if len(result) > 0:
        return {
            "success": False,
            "message": "用户名已经存在"
        }

    # 密码加密
    password_hash = generate_password_hash(password)

    # 插入新用户
    insert_sql = """
    INSERT INTO users (username, email, password_hash)
    VALUES (%s, %s, %s)
    """

    db.execute(insert_sql, (username, email, password_hash))

    return {
        "success": True,
        "message": "注册成功"
    }


def login_user(username, password):
    # 检查用户名是否为空
    if username is None or username.strip() == "":
        return {
            "success": False,
            "message": "用户名不能为空"
        }

    # 检查密码是否为空
    if password is None or password.strip() == "":
        return {
            "success": False,
            "message": "密码不能为空"
        }

    username = username.strip()

    # 根据用户名查找用户
    sql = """
    SELECT id, username, password_hash
    FROM users
    WHERE username = %s
    """

    result = db.query(sql, (username,))

    # 如果没有查到用户
    if len(result) == 0:
        return {
            "success": False,
            "message": "用户不存在"
        }

    user = result[0]

    user_id = user[0]
    username = user[1]
    password_hash = user[2]

    # 检查密码是否正确
    if not check_password_hash(password_hash, password):
        return {
            "success": False,
            "message": "密码错误"
        }

    return {
        "success": True,
        "message": "登录成功",
        "user": {
            "id": user_id,
            "username": username
        }
    }