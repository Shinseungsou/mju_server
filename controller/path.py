from flask import Blueprint, request, Response
import json

# from config.mjudb import mjudb
from controller import db
from datetime import datetime
from pytz import timezone
import math

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

class cpath:
    def __init__(self,from_lat, from_lon, to_lat, to_lon):
        self.from_lat = from_lat
        self.from_lon = from_lon
        self.to_lat = to_lat
        self.to_lon = to_lon

def simplereturn(result):
    if result :
        return '"result":true'
    else :
        return "'result':false"

def getdirection(cpath_car):
    lat = cpath_car.to_lat - cpath_car.from_lat
    lon = cpath_car.to_lon - cpath_car.from_lon
    if lat * lon >= 0:
        return True
    else:
        return False

def get_tri_weight(lat, lon, tri_lat, tri_lon, direction):
    weight = 0
    if lat >= 2 * tri_lat:
        if lon <= tri_lon:
            if direction :
                return 2
            else:
                return 5
        elif lon >= tri_lon * 2:
            if direction :
                return 2
            else:
                return 5
    elif lat <= tri_lat:
        if lon <= tri_lon:
            if direction :
                return 5
            else:
                return 2
        elif lon >= tri_lon * 2:
            if direction :
                return 2
            else:
                return 5
    return 3


def getweight(cpath_car, cpath_walker):
    vcar = dict()
    vwalker = dict()
    vcar['lat'] = cpath_car.to_lat - cpath_car.from_lat
    vcar['lon'] = cpath_car.to_lon - cpath_car.from_lon
    vwalker['lat'] = cpath_walker.to_lat - cpath_walker.from_lat
    vwalker['lon'] = cpath_walker.to_lon - cpath_walker.from_lon
    cos = (vcar['lat']*vwalker['lat']+vcar['lon']*vwalker['lon'])/(math.sqrt(vcar['lat']**2 + vcar['lon']**2)*math.sqrt(vwalker['lat']**2 + vwalker['lon']**2))
    tri_lat = (max(cpath_car.from_lat, cpath_car.to_lat) - min(cpath_car.from_lat, cpath_car.to_lat))/3
    tri_lon = (max(cpath_car.from_lon, cpath_car.to_lon) - min(cpath_car.from_lon, cpath_car.to_lon))/3
    weight = 0
    weight += get_tri_weight(cpath_walker.from_lat - min(cpath_car.from_lat, cpath_car.to_lat), cpath_walker.from_lon - min(cpath_car.from_lon, cpath_car.to_lon), tri_lat, tri_lon, getdirection(cpath_car))
    weight += get_tri_weight(cpath_walker.to_lat - min(cpath_car.from_lat, cpath_car.to_lat), cpath_walker.to_lon - min(cpath_car.from_lon, cpath_car.to_lon), tri_lat, tri_lon, getdirection(cpath_car))
    return weight * cos + weight

def getSquare(from_lat, from_lon, to_lat, to_lon):
    path1 = cpath(from_lat, from_lon, to_lat, to_lon)
    connection = db.connect()
    cursor = connection.cursor()
    query = "select * from path where carpooler_type=2 and from_lat <= %s and from_lat >= %s " \
            "and from_lon <= %s and from_lon >= %s " \
            "and to_lat <= %s and to_lat >= %s " \
            "and to_lon <= %s and to_lon >= %s" \
            % (max(path1.from_lat, path1.to_lat), min(path1.from_lat, path1.to_lat),
               max(path1.from_lon, path1.to_lon), min(path1.from_lon, path1.to_lon),
               max(path1.from_lat, path1.to_lat), min(path1.from_lat, path1.to_lat),
               max(path1.from_lon, path1.to_lon), min(path1.from_lon, path1.to_lon))
    cursor.execute(query)
    connection.commit()

    columns = tuple([d[0] for d in cursor.description])
    d = dict()
    result = []
    data = cursor.fetchall()

    cpath_car = cpath(from_lat, from_lon, to_lat, to_lon)
    for rows in data:
        for num in range(len(rows)):
            if type(rows[num]) == datetime:
                d[columns[num]] = rows[num].strftime("%Y-%m-%d %H:%M:%S")
            else:
                d[columns[num]] = rows[num]
        cpath_walker = cpath(d['from_lat'], d['from_lon'], d['to_lat'], d['to_lon'])
        d['weight'] = getweight(cpath_car, cpath_walker)
        result.append(d)
        d = dict()

    return result

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
    route = request.args.get('route')
    date_time = request.args.get('date_time')
    duration = request.args.get('duration')
    print "hello"
    print user_id, from_lat, from_lon, to_lat,to_lon,carpooler_type,datetime,duration

    connection = db.connect()
    cursor = connection.cursor()
    query = "insert into " \
            "path(user_id,route,from_lat,from_lon,to_lat,to_lon,carpooler_type,date_time,duration)" \
            "values('"+user_id+"','"+route+"','"+from_lat+"','"+from_lon+"','"+to_lat+"','"+to_lon+"','"+carpooler_type+"','"+date_time+"','"+duration+"');"

    cursor.execute(query)
    connection.commit()

    return '{"result":"true"}'

    # else:
    #     return '"result":"fail"'

@path.route("/list", methods=["GET"])
def getlist():
    user_id = request.args.get('id')
    path_id = request.args.get('path')

    connection = db.connect()
    cursor = connection.cursor()

    query = "select * from path where user_id=%s and uid=%s" % (user_id, path_id)

    cursor.execute(query)
    connection.commit()

    columns = tuple([d[0] for d in cursor.description])
    d = dict()
    data = cursor.fetchone()

    for num in range(len(data)):
        d[columns[num]] = data[num]

    result = getSquare(d['from_lat'], d['from_lon'], d['to_lat'], d['to_lon'])

    return Response(json.dumps(result), mimetype='application/json')
