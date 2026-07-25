from __future__ import annotations

import json
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Any
from urllib.parse import urlparse

from app.config import Config
from app.logger import get_logger
from app.models import Environment, Namespace


logger = get_logger()


class APIHandler(BaseHTTPRequestHandler):
    server_version = "K8sSelfServiceAPI/1.0"

    def do_GET(self) -> None:
        if self.path_without_query == "/environment":
            environment = Environment(name="dev", cluster="minikube")
            self.write_json(HTTPStatus.OK, environment.to_dict())
            return

        self.write_error(HTTPStatus.NOT_FOUND, "route not found")

    def do_POST(self) -> None:
        if self.path_without_query == "/namespace":
            self.create_namespace()
            return

        self.write_error(HTTPStatus.NOT_FOUND, "route not found")

    def create_namespace(self) -> None:
        payload = self.read_json_body()
        if payload is None:
            return

        name = str(payload.get("name", "")).strip()
        if not name:
            self.write_error(HTTPStatus.BAD_REQUEST, "namespace name is required")
            return

        namespace = Namespace(name=name)
        self.write_json(HTTPStatus.CREATED, namespace.to_dict())

    def read_json_body(self) -> dict[str, Any] | None:
        content_length = int(self.headers.get("Content-Length", "0"))
        if content_length == 0:
            self.write_error(HTTPStatus.BAD_REQUEST, "request body is required")
            return None

        raw_body = self.rfile.read(content_length)
        try:
            payload = json.loads(raw_body)
        except json.JSONDecodeError:
            self.write_error(HTTPStatus.BAD_REQUEST, "invalid request body")
            return None

        if not isinstance(payload, dict):
            self.write_error(HTTPStatus.BAD_REQUEST, "invalid request body")
            return None

        return payload

    @property
    def path_without_query(self) -> str:
        return urlparse(self.path).path

    def write_json(self, status_code: HTTPStatus, data: dict[str, Any]) -> None:
        response = json.dumps(data).encode("utf-8")
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(response)))
        self.end_headers()
        self.wfile.write(response)

    def write_error(self, status_code: HTTPStatus, message: str) -> None:
        self.write_json(status_code, {"error": message})

    def log_message(self, format: str, *args: Any) -> None:
        logger.info("%s - %s", self.address_string(), format % args)


def create_server(host: str, port: int) -> ThreadingHTTPServer:
    return ThreadingHTTPServer((host, port), APIHandler)


def run_server(config: Config) -> None:
    server = create_server(config.host, config.port)
    logger.info("API server starting on %s:%s", config.host, config.port)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        logger.info("API server stopping")
    finally:
        server.server_close()

