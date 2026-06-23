import logging

from flask import Flask

from shared.infrastructure.database import init_db
from iam.interfaces.services import iam_api

app = Flask(__name__)

app.register_blueprint(iam_api, url_prefix="/api/v1")

# Logging configuration
logging.basicConfig(
    filename='app.log',
    level=logging.INFO,
    format='%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]',
)

first_request = True


@app.before_request
def setup():
    """ Set up the database connection and other resources. """
    global first_request
    if first_request:
        first_request = False
        init_db()


if __name__ == '__main__':
    setup()
    logging.info(app.url_map)
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True
    )