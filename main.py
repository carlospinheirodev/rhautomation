import os
from flask import Flask

app = Flask(__name__)

from routes import *

if __name__ == '__main__':
    app.run(
        host='0.0.0.0',  # IMPORTANTE: não use 'localhost' ou '127.0.0.1'
        port=int(os.environ.get('PORT', 5000)),
        debug=os.environ.get('FLASK_ENV') == 'development'
    )
