from flask import Blueprint, render_template
from controller import db

index = Blueprint('index', __name__, url_prefix="/")

@index.route("/")
def index_index():
    conn = db.connect()
    cursor = conn.cursor()
    cursor.execute("select * from user")
    users = []
    for user in cursor:
        users.append(user[1])
    print users
    return render_template("index.xhtml", title='hello')