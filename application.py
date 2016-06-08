from controller import app
import logging
from logging.handlers import RotatingFileHandler
#from webzeug.debug import DebuggedApplication


if __name__ == "__main__":
    handler = RotatingFileHandler('foo.log', maxBytes=10000, backupCount=1)
    handler.setLevel(logging.ERROR)
    app.logger.addHandler(handler)
#    app.wsgi_app = DebuggedApplication(app.wsgi_app, True)
    app.run(debug=True, host='0.0.0.0', port=3000)
