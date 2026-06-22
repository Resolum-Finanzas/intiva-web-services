from peewee import Model

from shared.infrastructure.database import db


class BaseModel(Model):
    """ A base model class that all other models inherit from """

    class Meta:
        database = db