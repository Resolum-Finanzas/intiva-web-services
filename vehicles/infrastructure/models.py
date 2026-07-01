"""Peewee ORM model for the Vehicles bounded context."""

from peewee import AutoField, CharField, FloatField, IntegerField, Model

from shared.infrastructure.database import db


class CarModel(Model):
    """ORM mapping for the cars table."""

    id = AutoField()
    make = CharField()
    model = CharField()
    year = IntegerField()
    price = FloatField()
    version = CharField(null=True)
    vehicle_type = CharField(null=True)
    risk_category = CharField(null=True)
    reference_price = FloatField(null=True)
    residual_value = FloatField(null=True)
    condition = CharField(null=True)
    fuel_type = CharField(null=True)
    transmission = CharField(null=True)
    mileage = IntegerField(null=True)
    interest_rate = CharField(null=True)
    drivetrain = CharField(null=True)
    color_aesthetics = CharField(null=True)
    engine_power = CharField(null=True)
    combined_consumption = CharField(null=True)
    safety = CharField(null=True)
    comfort = CharField(null=True)
    photo_url = CharField(null=True)
    vehicle_insurance = CharField(null=True)

    class Meta:
        database = db
        table_name = "cars"