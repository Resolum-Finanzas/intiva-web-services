from peewee import PostgresqlDatabase

from shared.infrastructure.config import AppConfig

if not AppConfig.POSTGRES_DB_NAME:
    raise RuntimeError("POSTGRES_DB_NAME is not set in the environment")

db = PostgresqlDatabase(
    AppConfig.POSTGRES_DB_NAME,
    user=AppConfig.POSTGRES_DB_USER,
    password=AppConfig.POSTGRES_DB_PASSWORD,
    host=AppConfig.POSTGRES_DB_HOST,
    port=int(AppConfig.POSTGRES_DB_PORT),
)


def init_db():
    """Open the database connection and create tables if they don't exist.

    Imports ORM models from the bounded contexts at call time through deferred imports.
    """
    from iam.infrastructure.models import UserModel
    from analytics.infrastructure.models import LoanParametersModel, LoanFinancialIndicatorsModel, PaymentScheduleModel, PaymentPeriodModel
    from vehicles.infrastructure.models import CarModel

    should_close = db.is_closed()
    if should_close:
        db.connect()

    db.create_tables([
        UserModel,
        LoanParametersModel,
        LoanFinancialIndicatorsModel,
        PaymentScheduleModel,
        PaymentPeriodModel,
        CarModel,
    ], safe=True)

    if should_close and not db.is_closed():
        db.close()