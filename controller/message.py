from flask import Blueprint, request, Response
import json
from datetime import datetime
from pytz import timezone

# from config.mjudb import mjudb

from controller import db

message = Blueprint('message', __name__, url_prefix="/message")

@message.route("/register", methods=["POST"])
def register():
    # if(request.method == 'POST'):
    from_id = request.args.get('from_id')
    to_id = request.args.get('to_id')
    contents = request.args.get('contents')
    from_type = request.args.get('from_type')
    messagetype = request.args.get('mesagetype')
    date = datetime.now(tz=timezone('Asia/Tokyo')).strftime("%Y-%m-%d %H:%M:%S")

    connection = db.connect()
    cursor = connection.cursor()
    query = "insert into " \
            "messages(from_id,to_id,contents,from_type,mesagetype,date) " \
            "values('"+from_id+"','"+to_id+"','"+contents+"','"+from_type+"','"+messagetype+"','"+date+"');"

    cursor.execute(query)
    connection.commit()

    return '{"result":"true"}'
    # else:
    #     return '"result":"fail"'

@message.route("/list", methods=["GET"])
def getmessage():
    user_id = request.args.get('id')
    print "hello"

    connection = db.connect()
    cursor = connection.cursor()
    query = "select * from messages where to_id = "+user_id
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
