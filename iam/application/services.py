from iam.domain.entities import User
from iam.domain.enums import Role
from iam.domain.services import HashingService, TokenService
from iam.infrastructure.repositories import UserRepository

class SignUpCommand:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password


class SignInCommand:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password


class IamApplicationService:
    def __init__(self):
        self.user_repository = UserRepository()
        self.hashing_service = HashingService()
        self.token_service = TokenService()

    def sign_up(self, command: SignUpCommand) -> User:
        if self.user_repository.find_by_username(command.username):
            raise ValueError("Username already exists")

        user = User(
            username=command.username,
            password_hash=self.hashing_service.hash_password(command.password),
            role=Role.ROLE_ADMIN
        )
        return self.user_repository.save(user)

    def sign_in(self, command: SignInCommand) -> dict:
        user = self.user_repository.find_by_username(command.username)

        if not user or not self.hashing_service.verify_password(command.password, user.password_hash):
            raise ValueError("Invalid username or password")

        token = self.token_service.generate_token(user)

        return {
            "user": user,
            "token": token
        }