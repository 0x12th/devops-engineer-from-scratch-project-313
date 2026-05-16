import os

from flask import Flask, Response, jsonify
from flask_cors import CORS

from app.db import get_engine, init_db
from app.routes import create_routes


def create_app() -> Flask:
    flask_app = Flask(__name__)
    flask_app.config["JSON_SORT_KEYS"] = False

    CORS(
        flask_app,
        resources={
            r"/api/*": {"origins": ["http://localhost:5173"]},
            r"/r/*": {"origins": "*"},
        },
        methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        allow_headers=["Content-Type", "Authorization"],
    )

    engine = get_engine()
    init_db(engine)
    flask_app.register_blueprint(create_routes(engine))

    @flask_app.errorhandler(404)
    def not_found(_: Exception) -> tuple[Response, int]:
        return jsonify({"error": "not found"}), 404

    @flask_app.errorhandler(500)
    def internal_error(_: Exception) -> tuple[Response, int]:
        return jsonify({"error": "internal server error"}), 500

    return flask_app


app = create_app()


if __name__ == "__main__":
    port = int(os.getenv("BACKEND_PORT", "8080"))
    app.run(host="0.0.0.0", port=port)
