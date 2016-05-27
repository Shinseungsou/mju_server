import mysql
from flaskext.mysql import MySQL

class mjudb:
    def __init__(self):
        self.id='mju'
        self.ps='mjussangcarpool!'
        self.db='ssangcarpool'
        self.host='52.69.144.191'
        self.port=3306
        self.mysql = MySQL()
        self.data = "false"

    def setDB(self, app):
        app.config['MYSQL_DATABASE_USER'] =self.id
        app.config['MYSQL_DATABASE_PASSWORD'] = self.ps
        app.config['MYSQL_DATABASE_DB'] = self.db
        app.config['MYSQL_DATABASE_HOST'] = self.host
        app.config['MYSQL_DATABASE_PORT'] = self.port

        self.mysql.init_app(app)

        return self.mysql

    def getDB(self):
        print "getdb", self.mysql
        return self.mysql