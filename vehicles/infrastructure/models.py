"""Peewee ORM model for the Vehicles bounded context.

Defines the ``cars`` database table used to persist
:class:`~vehicles.domain.entities.Car` domain entities.  This module belongs
to the infrastructure layer and must not be referenced directly from the
domain or application layers; access is mediated through the repository.
"""

from peewee import AutoField, CharField, FloatField, IntegerField, Model

from shared.infrastructure.database import db


class CarModel(Model):
    """ORM mapping for the ``cars`` table.

    Attributes:
        id (AutoField): Auto-incrementing integer primary key.
        make (CharField): Manufacturer name.
        model (CharField): Model designation.
        year (IntegerField): Production year.
        price (FloatField): Listed sale price.
        photo_url (CharField): Public Cloudinary URL for the cover photo.
            Stored as ``null=True`` because a car may be created before a
            photo is uploaded.
    """

    id = AutoField()
    make = CharField()
    model = CharField()
    year = IntegerField()
    price = FloatField()
    photo_url = CharField(null=True)

    class Meta:
        """Peewee metadata: binds the model to the shared database."""

        database = db
        table_name = "cars"