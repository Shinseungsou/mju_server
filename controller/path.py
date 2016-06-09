from flask import Blueprint, request, Response
import json

# from config.mjudb import mjudb
from controller import db
from time import strftime
from datetime import datetime
from pytz import timezone

path = Blueprint('path', __name__, url_prefix="/path")

@path.route("/", methods=["GET"])
def get_message():
    return "{\"user\":{\"name\":\"Shin\",\"age\":\"24\"}}"

def userlist():
    # mjudbs = mjudb().setDB(current_app).getDB()
    cursor = db.connect().cursor()
    cursor.execute("select * from message")
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

@path.route("/register", methods=["POST"])
def register():
    # if(request.method == 'POST'):
    user_id = request.args.get('id')
    from_lat = request.args.get('from_lat')
    from_lon = request.args.get('from_lon')
    to_lat = request.args.get('to_lat')
    to_lon = request.args.get('to_lon')
    carpooler_type = request.args.get('carpooler_type')
    # date_time = datetime.now(tz=timezone('Asia/Tokyo')).strftime("%Y-%m-%d %H:%M:%S")
    carpooler_type = request.args.get('date_time')
    duration = request.args.get('duration')
    print "hello"
    # pw = request.form['pw']
    # id = request.form['id']
    # pn = request.form['pn']
    # nickname = request.form['nick']
    # email = request.form['email']
    print user_id, from_lat, from_lon, to_lat,to_lon,carpooler_type,datetime,duration

    connection = db.connect()
    cursor = connection.cursor()
    query = "insert into " \
            "path(user_id,from_lat,from_lon,to_lat,to_lon,carpooler_type,date_time,duration)" \
            "values('"+user_id+"','"+from_lat+"','"+from_lon+"','"+to_lat+"','"+to_lon+"','"+carpooler_type+"','"+date_time+"','"+duration+"');"

    cursor.execute(query)
    connection.commit()

    return '{"result":"true"}'
    # else:
    #     return '"result":"fail"'

@path.route("/list", methods=["GET"])
def getmessage():
    user_id = request.args.get('id')
    print "hello"

    connection = db.connect()
    cursor = connection.cursor()
    query = "select * from messages where from_lat = "+user_id
    cursor.execute(query)
    connection.commit()

    result = dict()
    if cursor.rowcount < 1:
        result['result'] = "false"
    else:
        result['result'] = "true"

    columns = tuple([d[0] for d in cursor.description])
    d = dict()
    result['messages'] = []
    data = cursor.fetchall()

    for rows in data:
        for num in range(len(rows)):
            d[columns[num]] = rows[num]
        result['messages'].append(d)

    return Response(json.dumps(result), mimetype='application/json')
