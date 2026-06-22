from peewee import MySQLDatabase

from shared.infrastructure.config import AppConfig

if not AppConfig.MYSQL_DB_NAME:
    raise RuntimeError("MYSQL_DB_NAME is not set in the environment")

# Shared MySQL database instance used by all bounded context ORM models
db = MySQLDatabase(
    AppConfig.MYSQL_DB_NAME,
    user=AppConfig.MYSQL_DB_USER,
    password=AppConfig.MYSQL_DB_PASSWORD,
    host=AppConfig.MYSQL_DB_HOST,
    port=AppConfig.MYSQL_DB_PORT,
)


def init_db():
    """Open the database connection and create tables if they don't exist.

    Imports ORM models from the bounded contexts at call time through deferred imports.
    """

    should_close = db.is_closed()
    if should_close:
        db.connect()

    db.create_tables([

    ], safe=True)

    if should_close and not db.is_closed():
        db.close()