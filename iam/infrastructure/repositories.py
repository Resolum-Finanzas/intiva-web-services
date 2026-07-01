from typing import Optional
import peewee
from iam.domain.entities import User
from iam.domain.enums import Role
from iam.infrastructure.models import UserModel

class UserRepository:
    @staticmethod
    def find_by_username(username: str) -> Optional[User]:
        try:
            m = UserModel.get(UserModel.username == username)
            return User(m.username, m.password_hash, Role(m.role), m.created_at, m.id)
        except peewee.DoesNotExist:
            return None

    @staticmethod
    def save(user: User) -> User:
        m = UserModel.create(
            username=user.username,
            password_hash=user.password_hash,
            role=user.role.value,
            created_at=user.created_at
        )
        user.user_id = m.id
        return user