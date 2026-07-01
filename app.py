import logging
import os

from flask import Flask
from flask_smorest import Api

from analytics.interfaces.services import analytics_api
from iam.infrastructure.middleware.jwt_middleware import JwtMiddleware
from iam.interfaces.services import iam_api
from shared.infrastructure.database import init_db
from vehicles.application.services import on_application_started
from vehicles.interfaces.services import vehicles_api

app = Flask(__name__)

JwtMiddleware(
    exempt_paths=(
        "/api/v1/auth",
        "/openapi.json",
        "/swagger-ui",
        "/static",
    )
).register(app)


app.config["API_TITLE"] = "Intiva Web Services"
app.config["API_VERSION"] = "v1"
app.config["OPENAPI_VERSION"] = "3.0.3"
app.config["OPENAPI_URL_PREFIX"] = "/"
app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist@5.17.14/"
app.config["API_SPEC_OPTIONS"] = {
    "components": {
        "securitySchemes": {
            "bearerAuth": {
                "type": "http",
                "scheme": "bearer",
                "bearerFormat": "JWT",
                "description": "Paste the JWT returned by /api/v1/auth/sign-in",
            }
        }
    }
}

api = Api(app)

api.register_blueprint(iam_api)

api.register_blueprint(vehicles_api)

api.register_blueprint(analytics_api)

# Logging configuration
logging.basicConfig(
    filename='app.log',
    level=logging.INFO,
    format='%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]',
)


def setup():
    """Set up the database connection, create tables, and seed data."""
    init_db()

    cloudinary_api_key = os.getenv("CLOUDINARY_API_KEY", "")
    if not cloudinary_api_key or cloudinary_api_key == "your_api_key":
        logging.warning("Skipping vehicle seed because Cloudinary is not configured.")
        return

    on_application_started()


if __name__ == '__main__':
    if not app.debug or os.environ.get('WERKZEUG_RUN_MAIN') == 'true':
        setup()

    logging.info(app.url_map)
    app.run(
        host='0.0.0.0',
        port=5001,
        debug=True
    )
