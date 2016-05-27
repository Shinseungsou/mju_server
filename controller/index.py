from flask import Blueprint

index = Blueprint('index', __name__, url_prefix="/")

@index.route("/")
def index_index():
    return "{\"user\":{\"name\":\"Shin\",\"age\":\"26\"}}"