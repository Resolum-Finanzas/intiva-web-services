from flask import Blueprint, request, jsonify
from iam.application.services import IamApplicationService, SignUpCommand, SignInCommand

iam_api = Blueprint("iam_api", __name__)
_service = IamApplicationService()

@iam_api.route("/auth/sign-up", methods=["POST"])
def sign_up():
    body = request.get_json()
    if not body or not body.get("username") or not body.get("password"):
        return jsonify({"error": "username and password are required"}), 400

    try:
        user = _service.sign_up(SignUpCommand(body["username"], body["password"]))
        return jsonify({
            "id": user.user_id,
            "username": user.username,
            "roles": [user.role.value]
        }), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


@iam_api.route("/auth/sign-in", methods=["POST"])
def sign_in():
    body = request.get_json()
    if not body or not body.get("username") or not body.get("password"):
        return jsonify({"error": "username and password are required"}), 400

    try:
        result = _service.sign_in(SignInCommand(body["username"], body["password"]))
        user = result["user"]
        return jsonify({
            "id": user.user_id,
            "username": user.username,
            "roles": [user.role.value],
            "token": result["token"]
        }), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 401