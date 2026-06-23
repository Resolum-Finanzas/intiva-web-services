import bcrypt
import jwt
from datetime import datetime, timezone, timedelta
from typing import Optional
from iam.domain.entities import User
from shared.infrastructure.config import AppConfig


class HashingService:
    @staticmethod
    def hash_password(plain_password: str) -> str:
        return bcrypt.hashpw(plain_password.encode(), bcrypt.gensalt()).decode()

    @staticmethod
    def verify_password(plain_password: str, hashed: str) -> bool:
        return bcrypt.checkpw(plain_password.encode(), hashed.encode())


class TokenService:
    @staticmethod
    def generate_token(user: User) -> str:
        payload = {
            "sub": user.username,
            "role": user.role.value,
            "exp": datetime.now(timezone.utc) + timedelta(minutes=AppConfig.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
        }
        return jwt.encode(payload, AppConfig.JWT_SECRET_KEY, algorithm=AppConfig.JWT_ALGORITHM)

    @staticmethod
    def decode_token(token: str) -> Optional[dict]:
        try:
            return jwt.decode(token, AppConfig.JWT_SECRET_KEY, algorithms=[AppConfig.JWT_ALGORITHM])
        except jwt.PyJWTError:
            return None