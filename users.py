from flask import Flask, Blueprint

apis = Blueprint('users', __name__, url_prefix="/users")

@apis.route("/")
def users():
    return "{\"user\":{\"name\":\"Shin\",\"age\":\"24\"}}"
