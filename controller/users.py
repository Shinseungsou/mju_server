from flask import Blueprint, request
import json

# from config.mjudb import mjudb
from controller import db

users = Blueprint('users', __name__, url_prefix="/users")

@users.route("/", methods=["GET"])
def users_index():
    return "{\"user\":{\"name\":\"Shin\",\"age\":\"24\"}}"

@users.route("/signin")
def signin():
    # mjudbs = mjudb().setDB(current_app).getDB()
    cursor = db.connect().cursor()
    cursor.execute("select * from users")
    result = []
    columns = tuple([d[0] for d in cursor.description])

    for row in cursor:
        result.append(dict(zip(columns, row)))

    print result

    return json.dumps(result)

@users.route("/signup", methods=["POST"])
def signup():
    # if(request.method == 'POST'):
    username = request.args.get('username')
    pw = request.args.get('pw')
    id = request.args.get('id')
    pn = request.args.get('pn')
    nickname = request.args.get('nick')
    email = request.args.get('email')
    gender = request.args.get('gender')
    print "hello"
    # pw = request.form['pw']
    # id = request.form['id']
    # pn = request.form['pn']
    # nickname = request.form['nick']
    # email = request.form['email']

    connection = db.connect()
    cursor = connection.cursor()
    query = "insert into " \
            "users(id,pw,username,nickname,phonenumber,email) " \
            "values('"+id+"','"+pw+"','"+username+"','"+nickname+"','"+pn+"','"+email+"');"

    cursor.execute(query)
    connection.commit()

    return '{"result":"success"}'
    # else:
    #     return '"result":"fail"'