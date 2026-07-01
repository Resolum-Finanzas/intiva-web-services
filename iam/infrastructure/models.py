from peewee import Model, CharField, DateTimeField, AutoField
from shared.infrastructure.database import db
from iam.domain.enums import Role

class UserModel(Model):
    id = AutoField()
    username = CharField(unique=True)
    password_hash = CharField()
    role = CharField(default=Role.ROLE_ADMIN.value)
    created_at = DateTimeField()

    class Meta:
        database = db
        table_name = "users"