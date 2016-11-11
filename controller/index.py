from flask import Blueprint, render_template

index = Blueprint('index', __name__, url_prefix="/")

@index.route("/")
def index_index():
    return render_template("index.html")