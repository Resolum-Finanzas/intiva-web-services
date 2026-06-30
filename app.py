import logging

from flask import Flask

from shared.infrastructure.database import init_db
from iam.interfaces.services import iam_api
from vehicles.interfaces.services import vehicles_api
from vehicles.application.services import on_application_started

app = Flask(__name__)

app.register_blueprint(iam_api, url_prefix="/api/v1")
app.register_blueprint(vehicles_api)  # vehicles_api ya define /api/v1/... en cada ruta

# Logging configuration
logging.basicConfig(
    filename='app.log',
    level=logging.INFO,
    format='%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]',
)


def setup():
    """Set up the database connection, create tables, and seed data."""
    init_db()
    on_application_started()


if __name__ == '__main__':
    import os

    
    if not app.debug or os.environ.get('WERKZEUG_RUN_MAIN') == 'true':
        setup()

    logging.info(app.url_map)
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True
    )