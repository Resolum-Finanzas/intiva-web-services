from flask.views import MethodView
from flask_smorest import Blueprint
from marshmallow import Schema, fields

from iam.application.services import IamApplicationService, SignUpCommand, SignInCommand

iam_api = Blueprint(
    "iam",
    __name__,
    url_prefix="/api/v1/auth",
    description="Authentication operations"

)

_service = IamApplicationService()

class AuthRequestSchema(Schema):
    username = fields.Str(required=True, metadata={"example": "user"})
    password = fields.Str(required=True, load_only=True, metadata={"example": "P@ssw0rd"})


class AuthResponseSchema(Schema):
    id = fields.Int()
    username = fields.Str()
    roles = fields.List(fields.Str())
    token = fields.Str()


class ErrorResponseSchema(Schema):
    error = fields.Str()

@iam_api.route("/sign-up")
class SignUpResource(MethodView):

    @iam_api.doc(
        summary="Register user",
        description="Creates a user account and returns the registered user data.",
    )
    @iam_api.arguments(AuthRequestSchema)
    @iam_api.response(201, AuthResponseSchema)
    @iam_api.alt_response(400, schema=ErrorResponseSchema, description="Invalid input")
    def post(self, body):
        try:
            user = _service.sign_up(SignUpCommand(body["username"], body["password"]))
            return {
                "id": user.user_id,
                "username": user.username,
                "roles": [user.role.value],
            }
        except ValueError as e:
            return {"error": str(e)}, 400


@iam_api.route("/sign-in")
class SignInResource(MethodView):

    @iam_api.doc(
        summary="Sign in",
        description="Authenticates a user and returns a JWT token. Use it in Swagger Authorize as: Bearer <token>.",
    )
    @iam_api.arguments(AuthRequestSchema)
    @iam_api.response(200, AuthResponseSchema)
    @iam_api.alt_response(401, schema=ErrorResponseSchema, description="Invalid credentials")
    def post(self, body):
        try:
            result = _service.sign_in(SignInCommand(body["username"], body["password"]))
            user = result["user"]
            return {
                "id": user.user_id,
                "username": user.username,
                "roles": [user.role.value],
                "token": result["token"],
            }
        except ValueError as e:
            return {"error": str(e)}, 401
