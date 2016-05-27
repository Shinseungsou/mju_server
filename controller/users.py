from flask import Blueprint, current_app

# from config.mjudb import mjudb
from controller import db

users = Blueprint('users', __name__, url_prefix="/users")

@users.route("/")
def users_index():
    return "{\"user\":{\"name\":\"Shin\",\"age\":\"24\"}}"

@users.route("/signup")
def signup():
    # mjudbs = mjudb().setDB(current_app).getDB()
    cursor = db.connect().cursor()
    cursor.execute("select * from users")
    result = []

    for row in cursor:
        result.append(row)

    print result

    return "hello"