from controller import app
import logging
from logging.handlers import RotatingFileHandler

if __name__ == "__main__":
    handler = RotatingFileHandler('foo.log', maxBytes=10000, backupCount=1)
    handler.setLevel(logging.ERROR)
    app.logger.addHandler(handler)
    app.run(debug=True, host='0.0.0.0', port=3000)
