from flask import Blueprint, request, Response
import json

# from config.mjudb import mjudb
from controller import db

users = Blueprint('users', __name__, url_prefix="/users")

@users.route("/", methods=["GET"])
def users_index():
    return "{\"user\":{\"name\":\"Shin\",\"age\":\"24\"}}"

def userlist():
    # mjudbs = mjudb().setDB(current_app).getDB()
    cursor = db.connect().cursor()
    cursor.execute("select * from users")
    result = []
    columns = tuple([d[0] for d in cursor.description])

    for row in cursor:
        result.append(dict(zip(columns, row)))

    print result

    return json.dumps(result)

def simplereturn(result):
    if result :
        return '"result":true'
    else :
        return "'result':false"

@users.route("/signin", methods=["POST"])
def signin():
    # mjudbs = mjudb().setDB(current_app).getDB()
    cursor = db.connect().cursor()
    pw = request.args.get('pw')
    id = request.args.get('id')
    if len(pw) < 1 or len(id) < 1:
        return Response('{"result":false}', status=400, mimetype='application/json')
    cursor.execute("select username, uid, id, gender, nickname from users where id="+id+" and pw="+pw)
    if cursor.rowcount < 1 :
        return '{"result":"false"}'

    result = dict()
    columns = tuple([d[0] for d in cursor.description])
#    result.append(d)
    #d["result"] = 'true'
    #result.append(d)

    data = cursor.fetchone()
    print columns
    print type(data[0]), type(columns[0])

    d = dict()
    # for rows in data:
    #     for num in range(len(rows)):
    #         print rows[num], columns[num]
    #         d[columns[num]] \
    #             = rows[num]
    for num in range(len(data)):
        print columns[num], data[num]
        d[columns[num]] = data[num]

    result["result"] = 'true'
    result["user"] = d

    return Response(json.dumps(result), mimetype='application/json')

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

    return '{"result":"true"}'
    # else:
    #     return '"result":"fail"'

@users.route("/profile", methods=["GET"])
def profile():
    # if(request.method == 'POST'):
    username = request.args.get('id')
    print "hello"
    # pw = request.form['pw']
    # id = request.form['id']
    # pn = request.form['pn']
    # nickname = request.form['nick']
    # email = request.form['email']

    connection = db.connect()
    cursor = connection.cursor()
    query = "select * from users where id = "+id

    cursor.execute(query)
    connection.commit()

    return '{"result":"true"}'

