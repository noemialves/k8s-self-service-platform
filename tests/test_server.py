import json
import threading
import unittest
from urllib.error import HTTPError
from urllib.request import Request, urlopen

from app.server import create_server


class APIServerTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.server = create_server("127.0.0.1", 0)
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()
        host, port = cls.server.server_address
        cls.base_url = f"http://{host}:{port}"

    @classmethod
    def tearDownClass(cls) -> None:
        cls.server.shutdown()
        cls.server.server_close()
        cls.thread.join(timeout=2)

    def test_get_environment(self) -> None:
        response = self.request("GET", "/environment")

        self.assertEqual(response["status"], 200)
        self.assertEqual(response["body"], {"name": "dev", "cluster": "minikube"})

    def test_create_namespace(self) -> None:
        response = self.request("POST", "/namespace", {"name": " platform-dev "})

        self.assertEqual(response["status"], 201)
        self.assertEqual(response["body"], {"name": "platform-dev"})

    def test_create_namespace_requires_body(self) -> None:
        response = self.request("POST", "/namespace")

        self.assertEqual(response["status"], 400)
        self.assertEqual(response["body"], {"error": "request body is required"})

    def test_create_namespace_requires_name(self) -> None:
        response = self.request("POST", "/namespace", {"name": "   "})

        self.assertEqual(response["status"], 400)
        self.assertEqual(response["body"], {"error": "namespace name is required"})

    def test_create_namespace_rejects_invalid_json(self) -> None:
        response = self.request("POST", "/namespace", raw_body=b"{invalid")

        self.assertEqual(response["status"], 400)
        self.assertEqual(response["body"], {"error": "invalid request body"})

    def request(
        self,
        method: str,
        path: str,
        payload: dict[str, str] | None = None,
        raw_body: bytes | None = None,
    ) -> dict[str, object]:
        body = raw_body
        if payload is not None:
            body = json.dumps(payload).encode("utf-8")

        request = Request(
            f"{self.base_url}{path}",
            data=body,
            method=method,
            headers={"Content-Type": "application/json"},
        )

        try:
            with urlopen(request, timeout=2) as response:
                return {
                    "status": response.status,
                    "body": json.loads(response.read()),
                }
        except HTTPError as error:
            return {
                "status": error.code,
                "body": json.loads(error.read()),
            }

