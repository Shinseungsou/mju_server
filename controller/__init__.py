from flask import Flask

from config.mjudb import mjudb

app = Flask(__name__)
db = mjudb().setDB(app)

from controller import users, index, message, path

app.register_blueprint(users.users)
app.register_blueprint(index.index)
app.register_blueprint(message.message)
app.register_blueprint(path.path)

