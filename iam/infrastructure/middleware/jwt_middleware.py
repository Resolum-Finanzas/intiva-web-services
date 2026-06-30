from __future__ import annotations

from collections.abc import Iterable

from flask import Flask, g, jsonify, request

from iam.domain.services import TokenService


class JwtMiddleware:
    """Global JWT middleware for protected API endpoints."""

    def __init__(self, exempt_paths: Iterable[str] | None = None):
        self.exempt_paths = tuple(exempt_paths or ())

    def register(self, app: Flask) -> None:
        """Attach the middleware to a Flask application."""

        @app.before_request
        def verify_jwt():
            if self._is_exempt_request():
                return None

            auth_header = request.headers.get("Authorization", "")
            if not auth_header.startswith("Bearer "):
                return jsonify({"error": "Missing or invalid Authorization header"}), 401

            token = auth_header.removeprefix("Bearer ").strip()
            payload = TokenService.decode_token(token)
            if payload is None:
                return jsonify({"error": "Invalid or expired token"}), 401

            g.current_user = payload
            return None

    def _is_exempt_request(self) -> bool:
        if request.method == "OPTIONS":
            return True

        return any(
            request.path == path or request.path.startswith(f"{path}/")
            for path in self.exempt_paths
        )
