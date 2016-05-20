from flask import Flask
import users

app = Flask(__name__)
app.register_blueprint(users.apis)

@app.route("/")
def index():
    return "{\"user\":{\"name\":\"Shin\",\"age\":\"26\"}}"

if __name__ == "__main__":
    # app.run(debug=True, host='127.0.0.1', port=3000)
    app.run(debug=False, host='0.0.0.0', port=3000)
