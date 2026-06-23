from datetime import datetime, timezone
from typing import Optional
from iam.domain.enums import Role

class User:
    def __init__(
        self,
        username: str,
        password_hash: str,
        role: Role,
        created_at: Optional[datetime] = None,
        user_id: Optional[int] = None
    ):
        self.user_id = user_id
        self.username = username
        self.password_hash = password_hash
        self.role = role
        self.created_at = created_at or datetime.now(timezone.utc)