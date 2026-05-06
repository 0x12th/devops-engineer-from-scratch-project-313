from flask import Blueprint, Response, jsonify, request
from sqlalchemy.engine import Engine
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, func, select

from app.models import Link
from app.serializers import link_to_dict
from app.validators import parse_range_header, validate_short_name


def create_routes(engine: Engine) -> Blueprint:
    routes = Blueprint("routes", __name__)

    @routes.get("/ping")
    def ping() -> str:
        return "pong"

    @routes.get("/api/links")
    def list_links() -> tuple[Response, int, dict[str, str]] | tuple[Response, int]:
        try:
            start, end = parse_range_header(request.args.get("range"))
        except ValueError as error:
            return jsonify({"error": str(error)}), 400

        limit = end - start + 1
        with Session(engine) as session:
            total = session.exec(select(func.count()).select_from(Link)).one()
            links = session.exec(select(Link).order_by(Link.id).offset(start).limit(limit)).all()

        headers = {
            "Accept-Ranges": "links",
            "Content-Range": f"links {start}-{end}/{total}",
        }
        return jsonify([link_to_dict(link) for link in links]), 200, headers

    @routes.post("/api/links")
    def create_link() -> tuple[Response, int]:
        data = request.get_json(silent=True) or {}
        original_url = data.get("original_url")
        short_name = data.get("short_name")

        if not original_url or not short_name:
            return jsonify({"error": "original_url and short_name are required"}), 400

        short_name_error = validate_short_name(short_name)
        if short_name_error:
            return jsonify({"error": short_name_error}), 400

        link = Link(original_url=original_url, short_name=short_name)
        with Session(engine) as session:
            session.add(link)
            try:
                session.commit()
            except IntegrityError:
                session.rollback()
                return jsonify({"error": "short_name already exists"}), 409
            session.refresh(link)
            return jsonify(link_to_dict(link)), 201

    @routes.get("/api/links/<int:link_id>")
    def get_link(link_id: int) -> tuple[Response, int]:
        with Session(engine) as session:
            link = session.get(Link, link_id)
            if link is None:
                return jsonify({"error": "link not found"}), 404
            return jsonify(link_to_dict(link)), 200

    @routes.put("/api/links/<int:link_id>")
    def update_link(link_id: int) -> tuple[Response, int]:
        data = request.get_json(silent=True) or {}
        original_url = data.get("original_url")
        short_name = data.get("short_name")

        if not original_url or not short_name:
            return jsonify({"error": "original_url and short_name are required"}), 400

        short_name_error = validate_short_name(short_name)
        if short_name_error:
            return jsonify({"error": short_name_error}), 400

        with Session(engine) as session:
            link = session.get(Link, link_id)
            if link is None:
                return jsonify({"error": "link not found"}), 404

            link.original_url = original_url
            link.short_name = short_name
            session.add(link)
            try:
                session.commit()
            except IntegrityError:
                session.rollback()
                return jsonify({"error": "short_name already exists"}), 409
            session.refresh(link)
            return jsonify(link_to_dict(link)), 200

    @routes.delete("/api/links/<int:link_id>")
    def delete_link(link_id: int) -> tuple[str, int] | tuple[Response, int]:
        with Session(engine) as session:
            link = session.get(Link, link_id)
            if link is None:
                return jsonify({"error": "link not found"}), 404

            session.delete(link)
            session.commit()
            return "", 204

    @routes.get("/r/<short_name>")
    def redirect_short_link(short_name: str) -> tuple[Response, int]:
        with Session(engine) as session:
            link = session.exec(select(Link).where(Link.short_name == short_name)).first()
            if link is None:
                return jsonify({"error": "link not found"}), 404
            return Response(status=302, headers={"Location": link.original_url})

    return routes
